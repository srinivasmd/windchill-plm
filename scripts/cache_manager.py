'''
Windchill PLM Response Cache Manager

Provides dual-backend caching (in-memory + file) for OData query responses:
- In-memory LRU cache for instant repeated lookups
- File-based cache for persistence across sessions
- TTL (time-to-live) expiration per entry
- SHA256-based cache keys from URL + query params
- Cache invalidation (manual, pattern-based, on write ops)
- Cache stats tracking (hits, misses, evictions)
- Zero-dependency (uses only stdlib: hashlib, json, time, pathlib)

Usage:
    from cache_manager import CacheManager

    cache = CacheManager(enabled=True, ttl=300, max_memory_entries=256)

    # Get from cache or return None
    data = cache.get('https://windchill.example.com/servlet/odata/ProdMgmt/Parts?$top=10')

    # Store in cache
    cache.put(url, response_data)

    # Invalidate on write operations
    cache.invalidate_on_write('Parts')

    # Stats
    print(cache.stats())
'''
# Copyright 2025 Windchill PLM Client Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib
import json
import os
import threading
import time
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ============================================================================
# Cache Key Generation
# ============================================================================

def _make_cache_key(url: str, method: str = 'GET', body: str = '') -> str:
    '''
    Generate SHA256 cache key from request URL, method, and body.

    Args:
        url: Request URL
        method: HTTP method (GET, POST, etc.)
        body: Request body string (for POST/PATCH uniqueness)

    Returns:
        Hex digest string (64 chars)
    '''
    raw = f"{method.upper()}|{url}|{body}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


def _make_entity_set_key(domain: str, entity_set: str) -> str:
    '''
    Generate a pattern key for entity set cache invalidation.

    Args:
        domain: OData domain name
        entity_set: Entity set name

    Returns:
        Pattern string like 'ProdMgmt:Parts'
    '''
    return f"{domain}:{entity_set}"


# ============================================================================
# Cache Entry
# ============================================================================

class CacheEntry:
    '''A single cache entry with value, TTL, and metadata.'''

    __slots__ = ('key', 'value', 'expires_at', 'created_at',
                 'hit_count', 'entity_sets', 'url')

    def __init__(self, key: str, value: Any, ttl: int,
                 entity_sets: List[str] = None, url: str = ''):
        self.key = key
        self.value = value
        self.created_at = time.time()
        self.expires_at = self.created_at + ttl if ttl > 0 else float('inf')
        self.hit_count = 0
        self.entity_sets = entity_sets or []
        self.url = url

    @property
    def is_expired(self) -> bool:
        return time.time() > self.expires_at

    @property
    def age_seconds(self) -> float:
        return time.time() - self.created_at

    @property
    def ttl_remaining(self) -> float:
        return max(0, self.expires_at - time.time())

    def to_dict(self) -> dict:
        return {
            'key': self.key,
            'value': self.value,
            'expires_at': self.expires_at,
            'created_at': self.created_at,
            'hit_count': self.hit_count,
            'entity_sets': self.entity_sets,
            'url': self.url,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'CacheEntry':
        entry = cls.__new__(cls)
        entry.key = data['key']
        entry.value = data['value']
        entry.expires_at = data['expires_at']
        entry.created_at = data['created_at']
        entry.hit_count = data.get('hit_count', 0)
        entry.entity_sets = data.get('entity_sets', [])
        entry.url = data.get('url', '')
        return entry


# ============================================================================
# In-Memory Cache Store (LRU)
# ============================================================================

class MemoryCacheStore:
    '''
    Thread-safe in-memory LRU cache store.

    Uses OrderedDict for O(1) LRU eviction.
    Automatically evicts expired entries on access.
    '''

    def __init__(self, max_entries: int = 256):
        self._max_entries = max_entries
        self._store: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[CacheEntry]:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            if entry.is_expired:
                del self._store[key]
                return None
            # Move to end (most recently used)
            self._store.move_to_end(key)
            entry.hit_count += 1
            return entry

    def put(self, entry: CacheEntry):
        with self._lock:
            if entry.key in self._store:
                del self._store[entry.key]
            self._store[entry.key] = entry
            self._store.move_to_end(entry.key)
            # Evict oldest if over capacity
            while len(self._store) > self._max_entries:
                self._store.popitem(last=False)

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._store:
                del self._store[key]
                return True
            return False

    def delete_pattern(self, entity_set_key: str) -> int:
        '''Delete all entries matching an entity set pattern.'''
        with self._lock:
            keys_to_delete = [
                k for k, v in self._store.items()
                if entity_set_key in v.entity_sets
            ]
            for k in keys_to_delete:
                del self._store[k]
            return len(keys_to_delete)

    def clear(self):
        with self._lock:
            self._store.clear()

    def cleanup_expired(self) -> int:
        '''Remove all expired entries. Returns count of removed.'''
        with self._lock:
            keys_to_delete = [
                k for k, v in self._store.items()
                if v.is_expired
            ]
            for k in keys_to_delete:
                del self._store[k]
            return len(keys_to_delete)

    @property
    def size(self) -> int:
        return len(self._store)


# ============================================================================
# File-Based Cache Store
# ============================================================================

class FileCacheStore:
    '''
    File-based cache store for persistence across sessions.

    Stores each entry as a JSON file in a cache directory.
    Keys are hashed and stored as filenames.
    Thread-safe via directory-level locking.
    '''

    def __init__(self, cache_dir: Path, max_size_mb: int = 50):
        self._cache_dir = cache_dir / 'response_cache'
        self._max_size_bytes = max_size_mb * 1024 * 1024
        self._lock = threading.Lock()
        self._ensure_dir()

    def _ensure_dir(self):
        self._cache_dir.mkdir(parents=True, exist_ok=True)

    def _entry_path(self, key: str) -> Path:
        return self._cache_dir / f"{key}.json"

    def get(self, key: str) -> Optional[CacheEntry]:
        path = self._entry_path(key)
        if not path.exists():
            return None
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            entry = CacheEntry.from_dict(data)
            if entry.is_expired:
                path.unlink(missing_ok=True)
                return None
            return entry
        except (json.JSONDecodeError, KeyError, OSError):
            return None

    def put(self, entry: CacheEntry):
        with self._lock:
            path = self._entry_path(entry.key)
            try:
                with open(path, 'w') as f:
                    json.dump(entry.to_dict(), f)
            except OSError:
                pass  # Silently fail on disk errors

    def delete(self, key: str) -> bool:
        path = self._entry_path(key)
        try:
            if path.exists():
                path.unlink()
                return True
        except OSError:
            pass
        return False

    def delete_pattern(self, entity_set_key: str) -> int:
        '''Delete all entries matching an entity set pattern.'''
        count = 0
        for path in self._cache_dir.glob('*.json'):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                if entity_set_key in data.get('entity_sets', []):
                    path.unlink(missing_ok=True)
                    count += 1
            except (json.JSONDecodeError, OSError):
                continue
        return count

    def clear(self):
        with self._lock:
            for path in self._cache_dir.glob('*.json'):
                try:
                    path.unlink()
                except OSError:
                    pass

    def cleanup_expired(self) -> int:
        '''Remove all expired entries. Returns count of removed.'''
        count = 0
        for path in self._cache_dir.glob('*.json'):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                if data.get('expires_at', 0) < time.time():
                    path.unlink(missing_ok=True)
                    count += 1
            except (json.JSONDecodeError, OSError):
                continue
        return count

    @property
    def size(self) -> int:
        return len(list(self._cache_dir.glob('*.json')))

    @property
    def total_bytes(self) -> int:
        total = 0
        for path in self._cache_dir.glob('*.json'):
            try:
                total += path.stat().st_size
            except OSError:
                pass
        return total


# ============================================================================
# Cache Manager (Main Interface)
# ============================================================================

class CacheManager:
    '''
    Dual-backend response cache for Windchill OData queries.

    Features:
    - In-memory LRU cache for instant lookups
    - Optional file-based cache for cross-session persistence
    - TTL-based expiration
    - Entity-set-aware invalidation (invalidate on writes)
    - Cache stats (hits, misses, evictions, hit rate)
    - Thread-safe operations
    - Zero external dependencies

    Config options (passed via config.json or constructor):
        cache.enabled       bool    Enable/disable caching (default: True)
        cache.ttl           int     Time-to-live in seconds (default: 300)
        cache.max_entries   int     Max in-memory entries (default: 256)
        cache.file_cache    bool    Enable file-based persistence (default: True)
        cache.max_size_mb   int     Max file cache size in MB (default: 50)
        cache.default_ttl   dict    Per-entity-set TTL overrides

    Example:
        cache = CacheManager(
            enabled=True,
            ttl=300,
            max_entries=256,
            file_cache=True,
            cache_dir=Path('/home/ubuntu/.hermes/skills/zephyr')
        )

        # Check cache
        data = cache.get(url, domain='ProdMgmt', entity_set='Parts')
        if data is not None:
            return data  # Cache HIT

        # Store result
        cache.put(url, response_data, domain='ProdMgmt', entity_set='Parts')

        # Invalidate on write
        cache.invalidate_on_write(domain='ProdMgmt', entity_set='Parts')

        # Stats
        stats = cache.stats()
    '''

    def __init__(self, enabled: bool = True, ttl: int = 300,
                 max_entries: int = 256, file_cache: bool = True,
                 cache_dir: Path = None, max_size_mb: int = 50,
                 default_ttls: Dict[str, int] = None):
        '''
        Initialize CacheManager.

        Args:
            enabled: Enable/disable caching globally
            ttl: Default TTL in seconds for cache entries
            max_entries: Max in-memory cache entries (LRU eviction)
            file_cache: Enable file-based persistence
            cache_dir: Base directory for file cache (default: skill dir)
            max_size_mb: Max file cache size in MB
            default_ttls: Per entity-set TTL overrides
                           e.g., {'ProdMgmt:Parts': 600, 'ChangeMgmt:ChangeNotices': 60}
        '''
        self.enabled = enabled
        self.default_ttl = ttl
        self.default_ttls = default_ttls or {}
        self._memory = MemoryCacheStore(max_entries)
        self._file: Optional[FileCacheStore] = None
        self._stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'invalidations': 0,
            'file_hits': 0,
        }

        if file_cache and cache_dir:
            self._file = FileCacheStore(cache_dir, max_size_mb)

    @classmethod
    def from_config(cls, config: dict, cache_dir: Path = None) -> 'CacheManager':
        '''
        Create CacheManager from config dict.

        Args:
            config: Full config dict (reads from 'cache' sub-key)
            cache_dir: Base directory for file cache

        Returns:
            CacheManager instance
        '''
        cache_config = config.get('cache', {})

        return cls(
            enabled=cache_config.get('enabled', True),
            ttl=cache_config.get('ttl', 300),
            max_entries=cache_config.get('max_entries', 256),
            file_cache=cache_config.get('file_cache', True),
            cache_dir=cache_dir,
            max_size_mb=cache_config.get('max_size_mb', 50),
            default_ttls=cache_config.get('default_ttls', {}),
        )

    def _get_ttl(self, domain: str, entity_set: str) -> int:
        '''Get TTL for a specific domain:entity_set combination.'''
        key = _make_entity_set_key(domain, entity_set)
        return self.default_ttls.get(key, self.default_ttl)

    def get(self, url: str, method: str = 'GET',
            domain: str = None, entity_set: str = None) -> Optional[Any]:
        '''
        Get cached response for a URL.

        Checks memory first, then file cache.
        Returns None on cache miss or if caching is disabled.

        Args:
            url: Request URL
            method: HTTP method
            domain: OData domain (for TTL lookup)
            entity_set: Entity set name (for TTL lookup)

        Returns:
            Cached response data or None
        '''
        if not self.enabled:
            return None

        cache_key = _make_cache_key(url, method)

        # Check memory cache first
        entry = self._memory.get(cache_key)
        if entry is not None:
            self._stats['hits'] += 1
            return entry.value

        # Check file cache
        if self._file is not None:
            entry = self._file.get(cache_key)
            if entry is not None:
                # Promote to memory cache
                self._memory.put(entry)
                self._stats['file_hits'] += 1
                self._stats['hits'] += 1
                return entry.value

        self._stats['misses'] += 1
        return None

    def put(self, url: str, value: Any, method: str = 'GET',
            domain: str = None, entity_set: str = None,
            ttl: int = None):
        '''
        Store response in cache.

        Args:
            url: Request URL
            value: Response data to cache
            method: HTTP method
            domain: OData domain (for entity-set tracking & TTL)
            entity_set: Entity set name (for invalidation & TTL)
            ttl: Override TTL for this entry
        '''
        if not self.enabled:
            return

        cache_key = _make_cache_key(url, method)
        effective_domain = domain or ''
        effective_entity_set = entity_set or ''
        effective_ttl = ttl or self._get_ttl(effective_domain, effective_entity_set)

        # Build entity set keys for invalidation tracking
        entity_sets = []
        if effective_domain and effective_entity_set:
            entity_sets.append(_make_entity_set_key(effective_domain, effective_entity_set))
        if effective_domain:
            entity_sets.append(f"{effective_domain}:")

        entry = CacheEntry(
            key=cache_key,
            value=value,
            ttl=effective_ttl,
            entity_sets=entity_sets,
            url=url,
        )

        # Store in memory
        self._memory.put(entry)

        # Store in file cache
        if self._file is not None:
            self._file.put(entry)

    def invalidate(self, url: str, method: str = 'GET') -> bool:
        '''
        Invalidate a specific cached URL.

        Args:
            url: Request URL to invalidate
            method: HTTP method

        Returns:
            True if entry was found and removed
        '''
        cache_key = _make_cache_key(url, method)
        found = self._memory.delete(cache_key)
        if self._file:
            self._file.delete(cache_key)
        if found:
            self._stats['invalidations'] += 1
        return found

    def invalidate_on_write(self, domain: str, entity_set: str) -> int:
        '''
        Invalidate all cached entries for an entity set.

        Call this after any write operation (POST, PATCH, DELETE)
        to ensure stale data is not returned on subsequent reads.

        Args:
            domain: OData domain (e.g., 'ProdMgmt')
            entity_set: Entity set name (e.g., 'Parts')

        Returns:
            Number of entries invalidated
        '''
        if not self.enabled:
            return 0

        pattern_key = _make_entity_set_key(domain, entity_set)
        count = self._memory.delete_pattern(pattern_key)
        if self._file:
            count += self._file.delete_pattern(pattern_key)
        self._stats['invalidations'] += count
        return count

    def invalidate_domain(self, domain: str) -> int:
        '''
        Invalidate all cached entries for an entire domain.

        Args:
            domain: OData domain (e.g., 'ProdMgmt')

        Returns:
            Number of entries invalidated
        '''
        if not self.enabled:
            return 0

        domain_pattern = f"{domain}:"
        count = self._memory.delete_pattern(domain_pattern)
        if self._file:
            count += self._file.delete_pattern(domain_pattern)
        self._stats['invalidations'] += count
        return count

    def clear(self):
        '''Clear all cached entries (memory + file).'''
        self._memory.clear()
        if self._file:
            self._file.clear()
        self._stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'invalidations': 0,
            'file_hits': 0,
        }

    def cleanup(self) -> dict:
        '''
        Remove all expired entries from both stores.

        Returns:
            Dict with 'memory' and 'file' cleanup counts
        '''
        mem_count = self._memory.cleanup_expired()
        file_count = 0
        if self._file:
            file_count = self._file.cleanup_expired()
        return {'memory': mem_count, 'file': file_count}

    def stats(self) -> dict:
        '''
        Get cache statistics.

        Returns:
            Dict with hits, misses, hit_rate, size, etc.
        '''
        total_requests = self._stats['hits'] + self._stats['misses']
        hit_rate = (self._stats['hits'] / total_requests * 100) if total_requests > 0 else 0.0

        return {
            'enabled': self.enabled,
            'hits': self._stats['hits'],
            'misses': self._stats['misses'],
            'hit_rate': f"{hit_rate:.1f}%",
            'file_hits': self._stats['file_hits'],
            'invalidations': self._stats['invalidations'],
            'memory_entries': self._memory.size,
            'file_entries': self._file.size if self._file else 0,
            'file_bytes': self._file.total_bytes if self._file else 0,
            'default_ttl': self.default_ttl,
        }

    def warm(self, urls: List[Tuple[str, str, str, str]], fetch_fn) -> int:
        '''
        Pre-warm the cache by fetching a list of URLs.

        Args:
            urls: List of (url, method, domain, entity_set) tuples
            fetch_fn: Async/sync function that takes a URL and returns data

        Returns:
            Number of entries successfully cached
        '''
        if not self.enabled:
            return 0

        count = 0
        for url, method, domain, entity_set in urls:
            try:
                data = fetch_fn(url)
                self.put(url, data, method=method, domain=domain, entity_set=entity_set)
                count += 1
            except Exception:
                continue
        return count


# ============================================================================
# Cache Decorators
# ============================================================================

def cached_method(ttl: int = None):
    '''
    Decorator for caching method results.

    Usage:
        @cached_method(ttl=600)
        def get_parts(self, ...):
            ...

    Note: This is a convenience decorator. For most use cases,
    prefer the integrated cache in WindchillBaseClient which
    automatically handles entity-set-aware invalidation.
    '''
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            cache = getattr(self, '_cache', None)
            if cache is None or not cache.enabled:
                return func(self, *args, **kwargs)

            # Build cache key from function name + args
            key_parts = [func.__name__]
            key_parts.extend(str(a) for a in args)
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = hashlib.sha256('|'.join(key_parts).encode()).hexdigest()

            # Check cache
            entry = cache._memory.get(cache_key)
            if entry is not None:
                return entry.value

            # Execute and cache
            result = func(self, *args, **kwargs)
            effective_ttl = ttl or cache.default_ttl
            entry = CacheEntry(key=cache_key, value=result, ttl=effective_ttl)
            cache._memory.put(entry)
            return result

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    return decorator


# ============================================================================
# CLI Entry Point
# ============================================================================

def main():
    '''CLI for cache management.'''
    import argparse

    parser = argparse.ArgumentParser(description='Windchill Cache Manager')
    parser.add_argument('--stats', action='store_true', help='Show cache stats')
    parser.add_argument('--clear', action='store_true', help='Clear all cache')
    parser.add_argument('--cleanup', action='store_true', help='Remove expired entries')
    parser.add_argument('--cache-dir', default=str(Path(__file__).parent.parent),
                        help='Cache directory path')

    args = parser.parse_args()

    cache = CacheManager(
        enabled=True,
        cache_dir=Path(args.cache_dir),
    )

    if args.stats:
        stats = cache.stats()
        print("Cache Statistics:")
        for k, v in stats.items():
            print(f"  {k}: {v}")

    if args.clear:
        cache.clear()
        print("Cache cleared.")

    if args.cleanup:
        result = cache.cleanup()
        print(f"Cleaned up {result['memory']} memory entries, {result['file']} file entries.")


if __name__ == '__main__':
    main()
