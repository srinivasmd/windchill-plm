# Changelog

All notable changes to the Zephyr skill are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.3.0] - 2026-04-23

A feature and bugfix release adding CLI terminal interface, async query manager,
and critical OData compatibility fixes for Windchill PLM. 2,254 lines added across 22 files.

### Added

#### CLI Terminal Interface
- `zephyr_cli.py`: Full-featured terminal CLI with 30+ subcommands (736 lines)
- Commands: parts, documents, bom, search, count, domains, cache, etc.
- Tabular and JSON output formats
- Auto-corrects common OData filter mistakes (enum /Value suffix, PascalCase properties)
- Search registry: maps CLI resource names to domain client search_* methods
- Run: `python scripts/zephyr_cli.py <command> [options]`

#### Async Query Manager
- `async_query_manager.py`: Parallel HTTP via aiohttp with semaphore concurrency control (1,217 lines)
- Retry with exponential backoff for transient failures
- Parallel BOM traversal and batch entity fetching
- Falls back to synchronous when aiohttp is unavailable
- Integrated into domain clients via `query_all()`, `query_iter()`, `count_entities()`

#### New Domain Client Search Methods
- SupplierMgmt: `search_suppliers()` — full-text supplier search
- CADDocumentMgmt: `search_cad_documents()` — full-text CAD document search
- ChangeMgmt: `search_change_notices()`, `search_change_requests()` — full-text search
- MfgProcMgmt: `search_process_plans()` — full-text process plan search
- Every domain now has both `search_*()` ($search) and `query_*()` ($filter) methods

### Changed

- SKILL.md: +74 lines — CLI docs, async query manager, search_* method examples for 5 domains
- CAPABILITIES.md: Entity set names corrected to match actual Windchill API endpoints
- DOMAIN_CLIENT_GUIDE.md: +79 lines — entity set verification pattern, search method pattern, domain testing procedure
- AGENT_NOTES.md: +27 lines — 3 new pitfalls (search_* vs query_*, enum /Value, BOM $expand=Uses)
- Removed: `FEATURE_PROPOSALS.md` (stale planning doc), `pyproject.toml` (not needed for agent skill)

### Fixed

#### OData Compatibility (Critical Fixes)
- **8 wrong entity set names** in CLI DOMAIN_REGISTRY causing 404 errors:
  - Baselines → BACReceivedDeliveries (BACMgmt)
  - ControlDocuments → TrainingRecords (DocumentControl)
  - Folders → ProjectContainers (DataAdmin)
  - WorkflowProcesses → WorkItems (Workflow)
  - LifecycleTemplates → WorkItems (Workflow)
  - CAPAs → Quality (QMS)
  - Registrations → RegulatorySubmissions (RegMstr)
  - UDIRecords → UDISuperSets (UDI)
  - ServiceDocuments → SIMDocuments (ServiceInfoMgmt)
- **OData filter property names must be PascalCase** — `Number` not `number`, `Name` not `name` (17 property name fixes)
- **Enum properties require /Value suffix** — `State/Value eq 'RELEASED'` not `State eq 'RELEASED'` (400 error without /Value)
- **BOM child part details** — `get_bom()` now defaults `expand_uses=True` and auto-expands `$expand=Uses` to include child Number/Name
- **Navigation URL order** — `/{nav}` segment must come BEFORE `?$expand=` query params (400 error if reversed)
- **PTC client** — fixed `_get_csrf_token()` → `get_csrf_token()` method call
- **windchill_base.py** — fixed missing CacheManager import

---

## [1.2.0] - 2026-04-22

A major feature release adding OData filter expressions, dual-backend response caching,
and agent portability documentation. 4,701 lines added across 94 files.

### Added

#### OData Filter Builder
- Full OData `$filter` expression support via `odata_filter_builder.py` (964 lines)
- Comparison operators: `eq`, `ne`, `gt`, `lt`, `ge`, `le`
- Logical operators: `and`, `or`, `not`
- String functions: `contains`, `startswith`, `endswith`, `indexof`, `substring`, `tolower`, `toupper`, `trim`, `length`, `concat`
- Date functions: `year`, `month`, `day`, `hour`, `minute`, `second`
- Math functions: `round`, `floor`, `ceiling`
- Type casting and `null` comparisons
- ODataFilter integrates directly into `query_entities()` — pass ODataFilter objects as `filter_expr`
- Test suite: `test_odata_expressions.py` (339 lines, full coverage)

#### Response Caching
- `cache_manager.py`: Dual-backend cache with in-memory LRU + file persistence (750 lines)
- TTL-based expiration with per-entity-set custom TTLs
- LRU eviction for memory cache (default 256 entries)
- File-based persistence — cache survives across process restarts
- SHA256-based cache keys from URL + query params
- Pattern-based invalidation (`invalidate_on_write(domain, entity_set)`)
- Thread-safe operations with locking
- Stats tracking: hits, misses, hit rate, entry counts
- Integrated into `windchill_base.py` `_request()` pipeline:
  - GET requests: check cache first, store on miss
  - Write ops (POST/PATCH/DELETE): auto-invalidate affected entity sets
- Cache control methods: `cache_status()`, `cache_clear()`, `cache_invalidate()`, `cache_cleanup()`, `cache_stats()`
- Graceful degradation if cache_manager is unavailable
- Configurable via `config.json` cache section
- Test suite: `test_cache_manager.py` (427 lines, 29 unit tests)

#### Agent Portability Documentation
- `AGENT_NOTES.md`: Critical implementation details and learnings for AI agents (274 lines)
  - API quirks (CSRF header name, URL double-slash bug, case-sensitive properties)
  - Missing/alternative endpoints (GetBOM → Uses navigation)
  - Domain client usage patterns
- `references/CAPABILITIES.md`: Comprehensive capability reference (364 lines)
  - OData filter expression support (data types, operators, functions)
  - Domain client listing with available methods
  - Navigation property reference
  - Quick-start examples

#### Domain Client Module Refactor
- All 28 domain clients now have proper `__init__.py` with exports
- Consistent `client.py` structure across all domains
- `DOMAIN_CLIENT_GUIDE.md`: Step-by-step guide for creating new domain clients
- Updated reference documentation with Apache 2.0 license headers for all domains

### Changed

- License updated from MIT to Apache 2.0 (with NOTICE file)
- `config.example.json`: Added cache configuration section
- SKILL.md: +367 lines — caching docs, OData filter docs, updated capability summary
- `windchill_base.py`: +219 lines — cache integration, ODataFilter support in `query_entities()`
- Server URLs replaced: hardcoded PTC demo server URL → generic `windchill.example.com` placeholder
  - No real server URLs in reference files; actual server from user's `config.json`

### Fixed

- `odata_base_url` double-slash bug: `.rstrip('/')` applied to avoid `//` in URLs
- Documentation for search methods corrected in SKILL.md

### Removed

- Hardcoded PTC demo server URL from all reference files

---

## [1.1.0] - 2026-04-11

### Added
- 28 domain clients organized with dedicated reference documentation
- Reference docs for ChangeMgmt, PrincipalMgmt, QMS, RegMstr, PTC Common entities
- Feature roadmap for skill enhancements
- Domain client helper methods for DocMgmt and ProdMgmt

### Changed
- Major refactor: domain clients reorganized from flat structure to `scripts/domains/{Domain}/`
- README renamed to "Agentic Skill" with comprehensive documentation
- Telegram formatting documentation in SKILL.md

### Removed
- Metadata XML files removed from git tracking (`.gitignore`)

---

## [1.0.0] - 2026-04-07

### Added
- Initial release of Zephyr Windchill PLM REST API client
- OAuth 2.0 and Basic authentication
- OData query support for Parts, Documents, Change objects, Suppliers, BOMs
- Base client (`windchill_base.py`) with CSRF_NONCE header handling
- Domain-specific clients for ProdMgmt, DocMgmt, ChangeMgmt, and more
- Navigation property traversal (Uses, Documents, etc.)
- SKILL.md with capability summary and usage patterns

---

[1.3.0]: https://github.com/srinivasmd/windchill-plm/releases/tag/v1.3.0
[1.2.0]: https://github.com/srinivasmd/windchill-plm/releases/tag/v1.2.0
[1.1.0]: https://github.com/srinivasmd/windchill-plm/releases/tag/v1.1.0
[1.0.0]: https://github.com/srinivasmd/windchill-plm/releases/tag/v1.0.0
