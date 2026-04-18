# Zephyr Skill Capabilities Reference

This document provides a comprehensive reference of all capabilities supported by the Zephyr Windchill PLM client. Use this to quickly understand what's available without reading through examples.

---

## OData Filter Expression Support

Zephyr's `odata_filter_builder.py` provides full support for Windchill OData REST API filter expressions as documented by PTC.

### Data Types Supported

| OData Type | Python Type | Example |
|------------|-------------|---------|
| `Edm.String` | `str` | `.eq('Name', 'Bracket')` |
| `Edm.Int16` | `int` | `.gt('Quantity', 100)` |
| `Edm.Int32` | `int` | `.eq('Version', 2)` |
| `Edm.Int64` | `int` | `.eq('ID', 1234567890)` |
| `Edm.Boolean` | `bool` | `.eq('IsActive', True)` → `IsActive eq true` |
| `Edm.DateTimeOffset` | `datetime` | `.gt('CreatedOn', datetime(2024,1,1))` |
| `Edm.Single` | `float` | `.gt('Weight', 1.5)` |
| `Edm.Double` | `float` | `.eq('Rate', 3.14159)` |
| `Edm.Decimal` | `Decimal` | `.eq('Price', Decimal('19.99'))` |
| `Edm.Guid` | `str` | `.eq('UUID', '...')` (auto-formatted) |

### Comparison Operators

| Operator | Method | Example | Output |
|----------|--------|---------|--------|
| `eq` | `.eq(prop, val)` | `.eq('State', 'RELEASED')` | `State eq 'RELEASED'` |
| `ne` | `.ne(prop, val)` | `.ne('State', 'CANCELLED')` | `State ne 'CANCELLED'` |
| `gt` | `.gt(prop, val)` | `.gt('Quantity', 100)` | `Quantity gt 100` |
| `lt` | `.lt(prop, val)` | `.lt('Quantity', 500)` | `Quantity lt 500` |
| `ge` | `.ge(prop, val)` | `.ge('CreatedOn', date)` | `CreatedOn ge datetime'...'` |
| `le` | `.le(prop, val)` | `.le('ModifiedOn', date)` | `ModifiedOn le datetime'...'` |

### Logical Operators

| Operator | Method | Example | Output |
|----------|--------|---------|--------|
| `and` | `.and_(filter)` | `.eq('A', 1).and_(.eq('B', 2))` | `(A eq 1 and B eq 2)` |
| `or` | `.or_(filter)` | `.eq('A', 1).or_(.eq('A', 2))` | `(A eq 1 or A eq 2)` |
| `not` | `.not_()` | `.eq('State', 'RELEASED').not_()` | `not(State eq 'RELEASED')` |

**Fluent Chaining:**
- `.and_eq()`, `.or_eq()` - combine existing filter with equality
- `.and_ne()`, `.or_ne()` - combine with inequality
- `.and_gt()`, `.or_gt()`, `.and_lt()`, `.or_lt()` - combine with comparison
- `.and_ge()`, `.or_ge()`, `.and_le()`, `.or_le()` - combine with range bounds

### String Functions

| Function | Method | Example | Output |
|----------|--------|---------|--------|
| `startswith` | `.startswith(prop, val)` | `.startswith('Number', 'ASM')` | `startswith(Number, 'ASM')` |
| `endswith` | `.endswith(prop, val)` | `.endswith('Number', '-001')` | `endswith(Number, '-001')` |
| `contains` | `.contains(prop, val)` | `.contains('Name', 'Bracket')` | `contains(Name, 'Bracket')` |

**Fluent variants:** `.and_startswith()`, `.or_contains()`, `.and_endswith()`, etc.

### Type Checking Function

| Function | Method | Example | Output |
|----------|--------|---------|--------|
| `isof(type)` | `.isof('WTPart')` | `.isof('WTPart')` | `isof('WTPart')` |
| `isof(prop, type)` | `.isof('WTPart', 'Item')` | `.isof('WTPart', 'Item')` | `isof(Item, 'WTPart')` |

### Special Properties

Windchill exposes these special properties for filtering:

| Property | Convenience Method | Example | Output |
|----------|-------------------|---------|--------|
| `ID` | `.by_id()` | `.by_id('OR:wt.part.WTPart:123')` | `ID eq 'OR:wt.part.WTPart:123'` |
| `CreatedBy` | `.by_created_by()` | `.by_created_by('admin')` | `CreatedBy eq 'admin'` |
| `ModifiedBy` | `.by_modified_by()` | `.by_modified_by('user1')` | `ModifiedBy eq 'user1'` |
| `View` | `.by_view()` | `.by_view('Manufacturing')` | `View eq 'Manufacturing'` |

**Fluent variants:** `.and_by_id()`, `.or_by_created_by()`, `.and_by_modified_by()`, `.or_by_view()`

### Additional Utility Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `.in_list(prop, values)` | Property in list of values | `.in_list('State', ['A', 'B'])` → `(State eq 'A' or State eq 'B')` |
| `.between(prop, low, high)` | Range check (inclusive) | `.between('Qty', 10, 100)` → `(Qty ge 10 and Qty le 100)` |
| `.is_null(prop)` | Check for null | `.is_null('Description')` → `Description eq null` |
| `.is_not_null(prop)` | Check for non-null | `.is_not_null('ReviewDate')` → `ReviewDate ne null` |

---

## Domain Clients Available

Zephyr provides 28 domain-specific clients. Each client follows the same pattern:

```python
from domains.<Domain> import <Domain>Client
client = <Domain>Client(config_path="config.json")
```

### Domain Coverage

| Domain | Purpose | Key Entity Sets |
|--------|---------|-----------------|
| **ProdMgmt** | Parts, BOMs, product structures | Parts, PartUsages |
| **DocMgmt** | Documents, attachments | Documents, Folders |
| **CADDocumentMgmt** | CAD models, drawings | CADDocuments |
| **ChangeMgmt** | Change notices, requests | ChangeNotices, ChangeTasks |
| **QMS** | Quality management | CAPAs, NCRs, QualityActions |
| **CAPA** | Corrective/Preventive Actions | CAPAs, CAPAActionPlans |
| **NC** | Nonconformance tracking | Nonconformances, AffectedObjects |
| **SupplierMgmt** | Suppliers, vendor parts | Manufacturers, VendorParts |
| **MfgProcMgmt** | Process plans, operations | ProcessPlans, Operations |
| **Workflow** | Work items, activities | WorkItems, Activities |
| **Audit** | Audit records | AuditRecords |
| **PrincipalMgmt** | Users, groups, roles | Users, Groups, Roles |
| **ProjMgmt** | Project plans, activities | ProjectPlans, Activities |
| **PartListMgmt** | Illustrated parts lists | PartLists, PartListItems |
| **ClfStructure** | Classification hierarchy | ClfNodes, ClassifiedObjects |
| **DocumentControl** | Controlled documents | ControlDocuments, TrainingRecords |
| **DynamicDocMgmt** | Dynamic documents | DynamicDocuments, BurstConfigurations |
| **EffectivityMgmt** | Part effectivity | PartEffectivityContexts, Effectivities |
| **Factory** | Standard operations, SCCs | StandardOperations, StandardProcedures |
| **NavCriteria** | Navigation criteria | NavigationCriteria, CachedNavigationCriteria |
| **ProdPlatformMgmt** | Variant specifications | VariantSpecifications, Options |
| **ServiceInfoMgmt** | Service documentation | ServiceDocuments |
| **RegMstr** | Regulatory master | RegMstrRecords |
| **UDI** | Unique Device Identification | UDIRecords |
| **CEM** | Customer experiences | CustomerExperiences |
| **DataAdmin** | Containers, folders | Containers, Folders |
| **PTC** | Common utilities, content download | (Cross-domain) |

---

## Query Methods

All domain clients inherit these methods from `WindchillBaseClient`:

### Basic Queries

| Method | Purpose | Example |
|--------|---------|---------|
| `query_entities(entity_set, ...)` | Query entity set with optional filters | `client.query_entities('Parts', filter_expr=f)` |
| `get_entity(entity_set, id, ...)` | Get single entity by ID | `client.get_entity('Parts', part_id)` |
| `search(entity_set, term, ...)` | Full-text search ($search) | `client.search('Parts', 'bracket')` |

### Pagination Methods

| Method | Purpose | Memory |
|--------|---------|--------|
| `query_all(entity_set, ...)` | Fetch ALL entities | O(n) - loads all |
| `query_iter(entity_set, ...)` | Generator for large datasets | O(1) - constant |
| `count_entities(entity_set, ...)` | Get count only | O(1) - no data |

### Navigation Properties

| Method | Purpose | Example |
|--------|---------|---------|
| `get_navigation(entity, id, nav_prop)` | Get related entities | `client.get_navigation('Parts', id, 'Uses')` |

### CRUD Operations

| Method | Purpose | Example |
|--------|---------|---------|
| `create_entity(entity_set, data)` | Create new entity | `client.create_entity('Parts', {...})` |
| `update_entity(entity_set, id, data)` | Update entity | `client.update_entity('Parts', id, {...})` |
| `delete_entity(entity_set, id)` | Delete entity | `client.delete_entity('Parts', id)` |

---

## Common Patterns by Task

### Find Parts by Criteria

```python
from domains.ProdMgmt import ProdMgmtClient
from odata_filter_builder import ODataFilter

client = ProdMgmtClient(config_path="config.json")

# By number
part = client.get_part_by_number("PART-001")

# By state and name pattern
f = ODataFilter().eq('State', 'RELEASED').and_contains('Name', 'Bracket')
parts = client.query_entities('Parts', filter_expr=f)

# By date range
from datetime import datetime
f = ODataFilter().between('CreatedOn', datetime(2024,1,1), datetime(2024,12,31))
parts = client.query_entities('Parts', filter_expr=f)
```

### Get BOM Structure

```python
# Method 1: Using domain client
bom = client.get_bom(part_id)  # Returns PartUsageLink objects

# Method 2: With child part details expanded
bom = client.query_entities(f"Parts('{part_id}')/Uses?$expand=Uses")
```

### Query Documents with Attachments

```python
from domains.DocMgmt import DocMgmtClient

client = DocMgmtClient(config_path="config.json")

# Get document by number
doc = client.get_document_by_number("DOC-001")

# Get attachments
attachments = client.get_document_attachments(doc['ID'])

# Get primary content
content = client.get_document_primary_content(doc['ID'])
```

### Filter by Special Properties

```python
from odata_filter_builder import ODataFilter

# Find all items created by specific user
f = ODataFilter().by_created_by('admin')
results = client.query_entities('Parts', filter_expr=f)

# Find items modified by user in specific state
f = ODataFilter().by_modified_by('engineer1').and_eq('State', 'INWORK')
results = client.query_entities('Parts', filter_expr=f)

# Filter by ID
f = ODataFilter().by_id('OR:wt.part.WTPart:12345')
result = client.query_entities('Parts', filter_expr=f)
```

### Complex Boolean Logic

```python
from odata_filter_builder import ODataFilter, Filter

# (State = RELEASED AND contains Name 'Bracket') OR (State = APPROVED AND startsWith Number 'ASM')
f = Filter.or_(
    Filter.and_(
        Filter.eq('State', 'RELEASED'),
        Filter.contains('Name', 'Bracket')
    ),
    Filter.and_(
        Filter.eq('State', 'APPROVED'),
        Filter.startswith('Number', 'ASM')
    )
)
parts = client.query_entities('Parts', filter_expr=f)
```

---

## Integration with Other Agents

When deploying Zephyr skill to another AI agent, ensure the agent:

1. **Loads the skill first** - Use `skill_view(name='zephyr')` to understand capabilities
2. **Checks domain clients** - Look in `scripts/domains/<Domain>/client.py` for helper methods
3. **Uses ODataFilter** - Don't write raw filter strings; use the builder
4. **Avoids scripts/old/** - Deprecated scripts, use domain clients instead
5. **Checks references/** - Entity definitions, navigation properties, actions per domain

### First Query Pattern

```python
# 1. Import client
import sys
sys.path.insert(0, '/path/to/skills/zephyr/scripts')
from domains.ProdMgmt import ProdMgmtClient
from odata_filter_builder import ODataFilter

# 2. Initialize
client = ProdMgmtClient(config_path="config.json")

# 3. Build filter
f = ODataFilter().eq('State', 'RELEASED').and_contains('Name', 'search_term')

# 4. Execute
results = client.query_entities('Parts', filter_expr=f)
```

---

## Quick Reference Tables

### Most Used Filters

| Need | Code |
|------|------|
| Exact match | `.eq('Field', 'value')` |
| Contains | `.contains('Field', 'text')` |
| Starts with | `.startswith('Field', 'prefix')` |
| Greater than | `.gt('Field', number)` |
| Date range | `.between('Date', start, end)` |
| Multiple values | `.in_list('Field', ['a', 'b', 'c'])` |
| Not null | `.is_not_null('Field')` |

### Most Used Entity Sets

| Domain | Entity Sets |
|--------|-------------|
| ProdMgmt | Parts, PartUsages, Manufacturers |
| DocMgmt | Documents, Folders, Attachments |
| ChangeMgmt | ChangeNotices, ChangeTasks, ChangeRequests |
| QMS | CAPAs, NCRs, QualityActions |
| SupplierMgmt | Manufacturers, VendorParts, Suppliers |
| Workflow | WorkItems, Activities |

### Common Navigation Properties

| From | Navigation | Gets |
|------|------------|------|
| Part | Uses | BOM children |
| Part | UsedBy | Parent assemblies |
| Part | Versions | Version history |
| Document | Attachments | Attached files |
| ChangeNotice | Tasks | Change tasks |
| CAPA | Plan | Action plan |
