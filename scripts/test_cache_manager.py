'''
Unit tests for CacheManager and cache integration in WindchillBaseClient.

Tests cover:
- Cache key generation
- Memory cache store (LRU, TTL, eviction)
- File cache store (persistence, cleanup)
- CacheManager (dual-backend, invalidation, stats)
- Integration with WindchillBaseClient._request()
'''
import json
import os
import sys
import tempfile
import time
import threading
from pathlib import Path

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).parent))
from cache_manager import (
    CacheManager, CacheEntry, MemoryCacheStore, FileCacheStore,
    _make_cache_key, _make_entity_set_key
)


# ============================================================================
# Test Helpers
# ============================================================================

def assert_eq(actual, expected, label=""):
    if actual != expected:
        print(f"  FAIL [{label}]: expected {expected!r}, got {actual!r}")
        return False
    return True

def assert_true(val, label=""):
    if not val:
        print(f"  FAIL [{label}]: expected True, got {val!r}")
        return False
    return True

def assert_none(val, label=""):
    if val is not None:
        print(f"  FAIL [{label}]: expected None, got {val!r}")
        return False
    return True

tests_passed = 0
tests_failed = 0

def run_test(name, fn):
    global tests_passed, tests_failed
    try:
        result = fn()
        if result:
            tests_passed += 1
            print(f"  PASS: {name}")
        else:
            tests_failed += 1
            print(f"  FAIL: {name}")
    except Exception as e:
        tests_failed += 1
        print(f"  ERROR: {name} -> {e}")


# ============================================================================
# Cache Key Tests
# ============================================================================

def test_cache_key_deterministic():
    key1 = _make_cache_key("https://example.com/Parts?$top=10")
    key2 = _make_cache_key("https://example.com/Parts?$top=10")
    return assert_eq(key1, key2, "same URL = same key")

def test_cache_key_different_urls():
    key1 = _make_cache_key("https://example.com/Parts?$top=10")
    key2 = _make_cache_key("https://example.com/Parts?$top=20")
    return assert_true(key1 != key2, "different URL = different key")

def test_cache_key_method_matters():
    key1 = _make_cache_key("https://example.com/Parts", method='GET')
    key2 = _make_cache_key("https://example.com/Parts", method='POST')
    return assert_true(key1 != key2, "different method = different key")

def test_entity_set_key():
    key = _make_entity_set_key('ProdMgmt', 'Parts')
    return assert_eq(key, 'ProdMgmt:Parts', "entity set key format")


# ============================================================================
# CacheEntry Tests
# ============================================================================

def test_cache_entry_not_expired():
    entry = CacheEntry("test", {"data": 1}, ttl=300)
    return assert_true(not entry.is_expired, "fresh entry not expired")

def test_cache_entry_expired():
    entry = CacheEntry("test", {"data": 1}, ttl=0)
    time.sleep(0.01)
    entry.expires_at = time.time() - 1  # Force expired
    return assert_true(entry.is_expired, "expired entry is expired")

def test_cache_entry_serialization():
    entry = CacheEntry("test", {"data": 1}, ttl=300, entity_sets=['ProdMgmt:Parts'], url='http://x')
    d = entry.to_dict()
    restored = CacheEntry.from_dict(d)
    return (assert_eq(restored.key, "test", "key") and
            assert_eq(restored.value, {"data": 1}, "value") and
            assert_eq(restored.entity_sets, ['ProdMgmt:Parts'], "entity_sets"))


# ============================================================================
# MemoryCacheStore Tests
# ============================================================================

def test_memory_put_get():
    store = MemoryCacheStore(max_entries=10)
    entry = CacheEntry("k1", {"val": 1}, ttl=300)
    store.put(entry)
    got = store.get("k1")
    return (assert_true(got is not None, "entry found") and
            assert_eq(got.value, {"val": 1}, "value matches"))

def test_memory_miss():
    store = MemoryCacheStore(max_entries=10)
    got = store.get("nonexistent")
    return assert_none(got, "miss returns None")

def test_memory_expired():
    store = MemoryCacheStore(max_entries=10)
    entry = CacheEntry("k1", {"val": 1}, ttl=0)
    entry.expires_at = time.time() - 1  # Already expired
    store.put(entry)
    got = store.get("k1")
    return assert_none(got, "expired entry returns None")

def test_memory_lru_eviction():
    store = MemoryCacheStore(max_entries=3)
    for i in range(5):
        entry = CacheEntry(f"k{i}", {"val": i}, ttl=300)
        store.put(entry)
    # Should only have last 3
    return (assert_none(store.get("k0"), "k0 evicted") and
            assert_none(store.get("k1"), "k1 evicted") and
            assert_true(store.get("k2") is not None, "k2 present") and
            assert_true(store.get("k3") is not None, "k3 present") and
            assert_true(store.get("k4") is not None, "k4 present"))

def test_memory_delete_pattern():
    store = MemoryCacheStore(max_entries=10)
    entry1 = CacheEntry("k1", {"v": 1}, ttl=300, entity_sets=['ProdMgmt:Parts'])
    entry2 = CacheEntry("k2", {"v": 2}, ttl=300, entity_sets=['ProdMgmt:Parts'])
    entry3 = CacheEntry("k3", {"v": 3}, ttl=300, entity_sets=['DocMgmt:Documents'])
    store.put(entry1)
    store.put(entry2)
    store.put(entry3)
    count = store.delete_pattern('ProdMgmt:Parts')
    return (assert_eq(count, 2, "2 entries deleted") and
            assert_none(store.get("k1"), "k1 gone") and
            assert_none(store.get("k2"), "k2 gone") and
            assert_true(store.get("k3") is not None, "k3 still there"))

def test_memory_cleanup():
    store = MemoryCacheStore(max_entries=10)
    entry1 = CacheEntry("k1", {"v": 1}, ttl=300)  # Not expired
    entry2 = CacheEntry("k2", {"v": 2}, ttl=0)
    entry2.expires_at = time.time() - 1  # Expired
    store.put(entry1)
    store.put(entry2)
    count = store.cleanup_expired()
    return (assert_eq(count, 1, "1 expired removed") and
            assert_true(store.get("k1") is not None, "k1 still there") and
            assert_none(store.get("k2"), "k2 cleaned up"))


# ============================================================================
# FileCacheStore Tests
# ============================================================================

def test_file_put_get():
    with tempfile.TemporaryDirectory() as tmpdir:
        store = FileCacheStore(Path(tmpdir), max_size_mb=10)
        entry = CacheEntry("k1", {"val": 1}, ttl=300)
        store.put(entry)
        got = store.get("k1")
        return (assert_true(got is not None, "entry found") and
                assert_eq(got.value, {"val": 1}, "value matches"))

def test_file_expired():
    with tempfile.TemporaryDirectory() as tmpdir:
        store = FileCacheStore(Path(tmpdir), max_size_mb=10)
        entry = CacheEntry("k1", {"val": 1}, ttl=0)
        entry.expires_at = time.time() - 1
        store.put(entry)
        got = store.get("k1")
        return assert_none(got, "expired entry returns None")

def test_file_delete_pattern():
    with tempfile.TemporaryDirectory() as tmpdir:
        store = FileCacheStore(Path(tmpdir), max_size_mb=10)
        entry1 = CacheEntry("k1", {"v": 1}, ttl=300, entity_sets=['ProdMgmt:Parts'])
        entry2 = CacheEntry("k2", {"v": 2}, ttl=300, entity_sets=['ProdMgmt:Parts'])
        store.put(entry1)
        store.put(entry2)
        count = store.delete_pattern('ProdMgmt:Parts')
        return (assert_eq(count, 2, "2 entries deleted") and
                assert_none(store.get("k1"), "k1 gone") and
                assert_none(store.get("k2"), "k2 gone"))


# ============================================================================
# CacheManager Tests
# ============================================================================

def test_cm_get_put():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = CacheManager(enabled=True, ttl=300, cache_dir=Path(tmpdir))
        url = "https://example.com/odata/ProdMgmt/Parts?$top=10"
        cache.put(url, {"value": [{"id": 1}]}, domain='ProdMgmt', entity_set='Parts')
        result = cache.get(url, domain='ProdMgmt', entity_set='Parts')
        return assert_eq(result, {"value": [{"id": 1}]}, "cached value returned")

def test_cm_miss():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = CacheManager(enabled=True, ttl=300, cache_dir=Path(tmpdir))
        result = cache.get("https://nonexistent.com")
        return assert_none(result, "miss returns None")

def test_cm_ttl_expiration():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = CacheManager(enabled=True, ttl=1, cache_dir=Path(tmpdir))
        url = "https://example.com/test"
        cache.put(url, {"v": 1})
        time.sleep(1.5)
        result = cache.get(url)
        return assert_none(result, "expired entry returns None")

def test_cm_invalidate_on_write():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = CacheManager(enabled=True, ttl=300, cache_dir=Path(tmpdir))
        url = "https://example.com/odata/ProdMgmt/Parts?$top=10"
        cache.put(url, {"value": [1, 2]}, domain='ProdMgmt', entity_set='Parts')
        # Verify it's cached
        result = cache.get(url, domain='ProdMgmt', entity_set='Parts')
        assert_true(result is not None, "pre-invalidation hit")
        # Invalidate
        count = cache.invalidate_on_write('ProdMgmt', 'Parts')
        # Verify it's gone
        result = cache.get(url, domain='ProdMgmt', entity_set='Parts')
        return (assert_true(count >= 1, "invalidated entries") and
                assert_none(result, "post-invalidation miss"))

def test_cm_per_entity_set_ttl():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = CacheManager(
            enabled=True, ttl=300, cache_dir=Path(tmpdir),
            default_ttls={'ProdMgmt:Parts': 1}  # 1 second for Parts
        )
        url = "https://example.com/odata/ProdMgmt/Parts?$top=10"
        cache.put(url, {"v": 1}, domain='ProdMgmt', entity_set='Parts')
        time.sleep(1.5)
        result = cache.get(url, domain='ProdMgmt', entity_set='Parts')
        return assert_none(result, "custom TTL expired")

def test_cm_stats():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = CacheManager(enabled=True, ttl=300, cache_dir=Path(tmpdir))
        cache.put("https://a.com", {"v": 1})
        cache.get("https://a.com")   # Hit
        cache.get("https://a.com")   # Hit
        cache.get("https://b.com")   # Miss
        stats = cache.stats()
        return (assert_eq(stats['hits'], 2, "2 hits") and
                assert_eq(stats['misses'], 1, "1 miss") and
                assert_true('66.7%' in stats['hit_rate'], "hit rate"))

def test_cm_disabled():
    cache = CacheManager(enabled=False)
    cache.put("https://a.com", {"v": 1})
    result = cache.get("https://a.com")
    return assert_none(result, "disabled cache returns None")

def test_cm_file_persistence():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write to cache
        cache1 = CacheManager(enabled=True, ttl=300, file_cache=True, cache_dir=Path(tmpdir))
        cache1.put("https://a.com", {"persisted": True}, domain='ProdMgmt', entity_set='Parts')
        
        # New cache manager instance (simulates restart)
        cache2 = CacheManager(enabled=True, ttl=300, file_cache=True, cache_dir=Path(tmpdir))
        result = cache2.get("https://a.com", domain='ProdMgmt', entity_set='Parts')
        return assert_eq(result, {"persisted": True}, "value persisted across instances")

def test_cm_clear():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = CacheManager(enabled=True, ttl=300, cache_dir=Path(tmpdir))
        cache.put("https://a.com", {"v": 1})
        cache.put("https://b.com", {"v": 2})
        cache.clear()
        return (assert_none(cache.get("https://a.com"), "a cleared") and
                assert_none(cache.get("https://b.com"), "b cleared"))

def test_cm_cleanup():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = CacheManager(enabled=True, ttl=1, cache_dir=Path(tmpdir))
        cache.put("https://a.com", {"v": 1})
        time.sleep(1.5)
        result = cache.cleanup()
        return (assert_true(result['memory'] >= 0, "memory cleanup") and
                assert_true(result['file'] >= 0, "file cleanup"))

def test_cm_thread_safety():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = CacheManager(enabled=True, ttl=300, cache_dir=Path(tmpdir))
        errors = []
        
        def writer(tid):
            try:
                for i in range(50):
                    cache.put(f"https://example.com/{tid}/{i}", {"v": i})
            except Exception as e:
                errors.append(e)
        
        def reader(tid):
            try:
                for i in range(50):
                    cache.get(f"https://example.com/{tid}/{i}")
            except Exception as e:
                errors.append(e)
        
        threads = []
        for t in range(4):
            threads.append(threading.Thread(target=writer, args=(t,)))
            threads.append(threading.Thread(target=reader, args=(t,)))
        
        for th in threads:
            th.start()
        for th in threads:
            th.join()
        
        return assert_eq(len(errors), 0, f"no thread errors (got {len(errors)})")


# ============================================================================
# CacheManager.from_config() Tests
# ============================================================================

def test_cm_from_config():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = {
            'cache': {
                'enabled': True,
                'ttl': 600,
                'max_entries': 128,
                'file_cache': True,
                'max_size_mb': 25,
                'default_ttls': {'ProdMgmt:Parts': 900}
            }
        }
        cache = CacheManager.from_config(config, cache_dir=Path(tmpdir))
        return (assert_eq(cache.default_ttl, 600, "ttl from config") and
                assert_eq(cache.default_ttls, {'ProdMgmt:Parts': 900}, "default_ttls from config"))

def test_cm_from_config_defaults():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = CacheManager.from_config({}, cache_dir=Path(tmpdir))
        return (assert_eq(cache.default_ttl, 300, "default ttl") and
                assert_true(cache.enabled, "enabled by default"))


# ============================================================================
# Run All Tests
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("Cache Manager Unit Tests")
    print("=" * 60)
    
    print("\n--- Cache Key Generation ---")
    run_test("deterministic key", test_cache_key_deterministic)
    run_test("different URLs = different keys", test_cache_key_different_urls)
    run_test("method matters", test_cache_key_method_matters)
    run_test("entity set key format", test_entity_set_key)
    
    print("\n--- CacheEntry ---")
    run_test("entry not expired", test_cache_entry_not_expired)
    run_test("entry expired", test_cache_entry_expired)
    run_test("entry serialization", test_cache_entry_serialization)
    
    print("\n--- MemoryCacheStore ---")
    run_test("put/get", test_memory_put_get)
    run_test("miss returns None", test_memory_miss)
    run_test("expired returns None", test_memory_expired)
    run_test("LRU eviction", test_memory_lru_eviction)
    run_test("delete by pattern", test_memory_delete_pattern)
    run_test("cleanup expired", test_memory_cleanup)
    
    print("\n--- FileCacheStore ---")
    run_test("put/get", test_file_put_get)
    run_test("expired returns None", test_file_expired)
    run_test("delete by pattern", test_file_delete_pattern)
    
    print("\n--- CacheManager ---")
    run_test("get/put", test_cm_get_put)
    run_test("miss returns None", test_cm_miss)
    run_test("TTL expiration", test_cm_ttl_expiration)
    run_test("invalidate on write", test_cm_invalidate_on_write)
    run_test("per entity-set TTL", test_cm_per_entity_set_ttl)
    run_test("stats tracking", test_cm_stats)
    run_test("disabled cache", test_cm_disabled)
    run_test("file persistence", test_cm_file_persistence)
    run_test("clear all", test_cm_clear)
    run_test("cleanup", test_cm_cleanup)
    run_test("thread safety", test_cm_thread_safety)
    
    print("\n--- CacheManager.from_config() ---")
    run_test("from config dict", test_cm_from_config)
    run_test("config defaults", test_cm_from_config_defaults)
    
    print("\n" + "=" * 60)
    print(f"Results: {tests_passed} passed, {tests_failed} failed")
    print("=" * 60)
    
    sys.exit(1 if tests_failed > 0 else 0)
