# Agent Notes for Zephyr Skill

Critical implementation details and learnings for AI agents using this skill. Read this before working with Windchill APIs.

---

## Critical Implementation Details

### API Quirks

| Issue | Detail |
|-------|--------|
| **CSRF Header Name** | Use `CSRF_NONCE` (NOT `X-PTC-CSRF-Token`) |
| **URL Double-Slash Bug** | `odata_base_url` needs `.rstrip('/')` to avoid double-slash in URLs |
| **Case-Sensitive Properties** | OData filter properties are PascalCase: `Number` not `number`, `Name` not `name`, `ContainerID` not `containerID`. Wrong case = 400 error. Fixed 17 bugs across 11 domain clients in commit 37a93c2. |
| **Enum Properties Need /Value** | PTC.EnumType properties (State, Priority, Severity, Status, etc.) require `/Value` in filters: `State/Value eq 'RELEASED'` (NOT `State eq 'RELEASED'`). Direct comparison = 400 error "types not compatible". CLI auto-corrects common enum names. Fixed in commit 8fbe72a. |
| **Slow Demo Server** | PTC demo server is slow (7-8s per call is normal, not a bug) |
| **No Real Server URLs in Reference Files** | Reference docs use `windchill.example.com` placeholder. Actual server comes from user's `config.json`. |
| **Missing Import Blocks** | Every optional module (cache_manager, odata_filter_builder, property_resolver) MUST have a `try/except ImportError` block defining its `_AVAILABLE` flag. Forgetting this causes `NameError` at runtime. |

### Missing/Alternative Endpoints

| Missing Endpoint | Alternative |
|------------------|-------------|
| `GetBOM` action | Use `Uses` navigation property: `client.get_bom(part_id)` |

---

## Key Patterns

### Always Use Domain Clients

```python
# CORRECT - Use domain client
from domains.ProdMgmt import ProdMgmtClient
client = ProdMgmtClient(config_path="config.json")
parts = client.query_entities('Parts', filter_expr=my_filter)

# WRONG - Don't create ad-hoc scripts
# See scripts/old/ for deprecated examples - DO NOT USE
```

### Use ODataFilter Builder

```python
# CORRECT - Use ODataFilter
from odata_filter_builder import ODataFilter
f = ODataFilter().eq('State', 'RELEASED').and_contains('Name', 'Bracket')
parts = client.query_entities('Parts', filter_expr=f)

# AVOID - Raw strings (works but no type safety)
parts = client.query_entities('Parts', filter_expr="State eq 'RELEASED'")
```

### Module Name

The filter builder module is `odata_filter_builder.py` (NOT `filter_builder.py`):
```python
from odata_filter_builder import ODataFilter, Filter, ODataType
```

---

## Domain Client Reference

### Available Domains (28 total)

| Domain | Client Class | Purpose |
|--------|--------------|---------|
| ProdMgmt | `ProdMgmtClient` | Parts, BOMs, product structures |
| DocMgmt | `DocMgmtClient` | Documents, attachments |
| CADDocumentMgmt | `CADDocumentMgmtClient` | CAD documents, drawings |
| ChangeMgmt | `ChangeMgmtClient` | Change notices, requests, tasks |
| QMS | `QMSClient` | Quality management (CAPA/NCR) |
| CAPA | `CAPAClient` | Corrective and Preventive Actions |
| NC | `NCClient` | Nonconformance tracking |
| SupplierMgmt | `SupplierMgmtClient` | Suppliers, vendor parts |
| MfgProcMgmt | `MfgProcMgmtClient` | Process plans, operations |
| Workflow | `WorkflowClient` | Work items, activities |
| Audit | `AuditClient` | Audit records, compliance |
| PrincipalMgmt | `PrincipalMgmtClient` | Users, groups, roles |
| ProjMgmt | `ProjMgmtClient` | Project plans, activities |
| PartListMgmt | `PartListMgmtClient` | Illustrated parts lists |
| ClfStructure | `ClfStructureClient` | Classification hierarchy |
| DocumentControl | `DocumentControlClient` | Controlled documents |
| DynamicDocMgmt | `DynamicDocMgmtClient` | Dynamic documents |
| EffectivityMgmt | `EffectivityMgmtClient` | Part effectivity |
| Factory | `FactoryClient` | Standard operations, SCCs |
| NavCriteria | `NavCriteriaClient` | Navigation criteria, config specs |
| ProdPlatformMgmt | `ProdPlatformMgmtClient` | Variant specifications |
| ServiceInfoMgmt | `ServiceInfoMgmtClient` | Service documentation |
| RegMstr | `RegMstrClient` | Regulatory Master |
| UDI | `UDIClient` | Unique Device Identification |
| CEM | `CEMClient` | Customer experiences |
| DataAdmin | `DataAdminClient` | Containers, folders |
| PTC | `PTCClient` | Common utilities, content download |

### Base Class

All domain clients inherit from `WindchillBaseClient` in `scripts/windchill_base.py`.

### Helper Methods Pattern

Each domain client has helper methods. Check `scripts/domains/{Domain}/client.py` before writing code:

```python
# Check client for existing helpers first
client = ProdMgmtClient()

# Common helpers available:
client.get_part_by_number("PART-001")      # Get by number
client.search_parts("bracket")             # Full-text search
client.get_bom(part_id)                    # BOM via Uses navigation
client.get_part_versions(part_id)          # Version history
```

---

## OData Filter Capabilities

Fully supported per PTC Windchill REST Services specification:

### Data Types
- `Edm.String`, `Edm.Int16`, `Edm.Int32`, `Edm.Int64`
- `Edm.Boolean`, `Edm.DateTimeOffset`
- `Edm.Single`, `Edm.Double`, `Edm.Decimal`, `Edm.Guid`

### Comparison Operators
`eq`, `ne`, `gt`, `lt`, `ge`, `le`

### Logical Operators
`and`, `or`, `not`

### String Functions
`startswith`, `endswith`, `contains`

### Type Checking
`isof` - both forms: `isof('type')` and `isof(property, 'type')`

### Special Properties
`ID`, `CreatedBy`, `ModifiedBy`, `View`

### Usage Examples

```python
from odata_filter_builder import ODataFilter, Filter

# Simple equality (for string/number properties)
f = ODataFilter().eq('Name', 'Bracket')

# Enum properties - MUST use /Value suffix
f = ODataFilter().eq('State/Value', 'RELEASED')
f = ODataFilter().eq('Priority/Value', 'High')

# Multiple conditions
f = ODataFilter().eq('State/Value', 'RELEASED').and_gt('Quantity', 100)

# String functions
f = ODataFilter().contains('Name', 'Bracket')
f = ODataFilter().startswith('Number', 'ASM')

# Special properties
f = ODataFilter().by_id('OR:wt.part.WTPart:12345')
f = ODataFilter().by_created_by('admin')

# Type checking
f = ODataFilter().isof('WTPart')

# Complex boolean logic
f = Filter.or_(
 Filter.and_(Filter.eq('State/Value', 'RELEASED'), Filter.contains('Name', 'Bracket')),
 Filter.and_(Filter.eq('State/Value', 'APPROVED'), Filter.startswith('Number', 'ASM'))
)

# Use with query_entities
results = client.query_entities('Parts', filter_expr=f)
```

---

## Common Navigation Properties

| Entity | Navigation | Returns |
|--------|------------|---------|
| Part | `Uses` | BOM children (PartUsageLink) |
| Part | `UsedBy` | Parent assemblies |
| Part | `Versions` | Version history |
| Document | `Attachments` | Attached files |
| Document | `PrimaryContent` | Primary file content |
| ChangeNotice | `Tasks` | Change tasks |
| ChangeNotice | `AffectedObjects` | Affected items |
| CAPA | `Plan` | Action Plan |
| CAPA | `AffectedObjects` | Affected items |

---

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid domain request" | Double slash in URL | Check `odata_base_url` - client auto-fixes but verify config |
| "CSRF token missing" | POST without token | Get token from `/PTC/GetCSRFToken()` endpoint |
| "$top not supported" | Single-entity navigation | Remove pagination params for single entity queries |
| 7-8s response time | PTC demo server | Normal behavior, not a bug |
| Property not found | Case mismatch | Use exact case: `Number` not `number` |
| 400 "types not compatible" | Enum compared to string | Use `/Value` suffix: `State/Value eq 'X'` not `State eq 'X'` |
| NameError `CACHE_MANAGER_AVAILABLE` | Missing import block | Add `try/except ImportError` block defining `_AVAILABLE` flag |

---

## File Structure

```
zephyr/
├── SKILL.md              # Main skill file (capabilities first)
├── AGENT_NOTES.md        # This file - critical learnings
├── references/
│   ├── CAPABILITIES.md   # Full capability reference
│   └── {Domain}/         # Per-domain documentation
│       ├── {Domain}_REFERENCE.md
│       ├── {Domain}_Entities.json
│       ├── {Domain}_Navigations.md
│       └── {Domain}_Actions.md
└── scripts/
    ├── windchill_base.py         # Base client class
    ├── windchill_odata_client.py # Comprehensive OData client
    ├── odata_filter_builder.py   # OData filter construction
    ├── property_resolver.py      # Case-insensitive property resolution
    ├── output_formatter.py       # Output formatting
    └── domains/                  # Domain-specific clients (USE THESE)
        ├── ProdMgmt/client.py
        ├── DocMgmt/client.py
        └── ... (28 domains)
```

**DEPRECATED:** `scripts/old/` - Do not use. Use domain clients instead.

---

## Quick Start Checklist for New Agents

1. [ ] Read `references/CAPABILITIES.md` for full feature reference
2. [ ] Import domain client: `from domains.ProdMgmt import ProdMgmtClient`
3. [ ] Import filter builder: `from odata_filter_builder import ODataFilter`
4. [ ] Check `scripts/domains/{Domain}/client.py` for helper methods
5. [ ] Use `query_entities(entity_set, filter_expr=filter)` for queries
6. [ ] Use `get_navigation(entity, id, nav_prop)` for related entities
7. [ ] Remember: CSRF header is `CSRF_NONCE`, properties are case-sensitive

---

## Configuration

Config file location: `/home/ubuntu/.hermes/skills/zephyr/config.json` (gitignored)

```json
{
  "server_url": "https://windchill.example.com/Windchill",
  "odata_base_url": "https://windchill.example.com/Windchill/servlet/odata/",
  "auth_type": "basic",
  "basic": {
    "username": "your_username",
    "password": "your_password"
  },
  "verify_ssl": true,
  "timeout": 30
}
```

Note: Credentials are nested under `basic` or `oauth` object, not at root level.
