---
name: zephyr
description: Zephyr - A Python REST API client for PTC Windchill PLM. Query parts, documents, change requests, suppliers, BOMs, CAD documents, workflows, and more. Supports OAuth 2.0 and Basic authentication.
tags:
  - windchill
  - plm
  - ptc
  - odata
  - rest-api
  - enterprise
  - product-lifecycle-management
  - bom
  - change-management
  - supplier-management
  - cad
  - quality-management
  - regulatory-compliance
  - zephyr
---

# Zephyr - Windchill PLM REST API Client

Zephyr is a Python client for interacting with PTC Windchill PLM REST APIs. Supports OAuth 2.0 and Basic authentication.

## Quick Start

1. Copy `config.example.json` to `config.json` in the skill directory
2. Configure your Windchill server URL and authentication
3. Use domain clients for best practices

```python
import sys
sys.path.insert(0, '/home/ubuntu/.hermes/skills/zephyr/scripts')
from domains.ProdMgmt import ProdMgmtClient

client = ProdMgmtClient(config_path="config.json")

# Query parts (use query_entities for Parts entity set)
parts = client.query_entities('Parts', top=10)

# Search parts by term
results = client.search_parts('bracket', top=10)

# Get part by number
part = client.get_part_by_number("PART-001")
```

---

## CRITICAL WARNINGS

| Issue | Solution |
|-------|----------|
| **scripts/old/ is DEPRECATED** | Use domain clients in `scripts/domains/` instead |
| **DO NOT create ad-hoc scripts** | Use existing domain clients directly - they support all query patterns |
| **URL double-slash bug** | Client auto-fixes trailing slashes. If "Invalid domain request", check URLs. |
| **CSRF token required** | Header: `CSRF_NONCE: <token>` (NOT `X-PTC-CSRF-Token`) |
| **OData properties case-sensitive** | Use `PropertyResolver` or pass dict to `_build_filter_from_dict()` |
| **GetBOM not exposed** | Use `Uses` navigation: `client.get_bom(part_id)` |
| **Slow API (7-8s/call)** | PTC demo servers are slow - this is expected, not a bug |
| **ManufacturerParts in ProdMgmt** | ManufacturerParts/VendorParts are in ProdMgmt domain, NOT SupplierMgmt |
| **search_* uses $search (full-text)** | `search_parts()`, `search_documents()` use full-text search across ALL fields. For field-specific filtering, use `query_entities()` with `filter_expr=\"contains(Name, 'term')\"` |

---

## Domain Clients (28 domains)

| Domain | Client | Purpose |
|--------|--------|---------|
| ProdMgmt | `ProdMgmtClient` | Parts, BOMs, product structures |
| ProdPlatformMgmt | `ProdPlatformMgmtClient` | Variant specifications, options, choices |
| PartListMgmt | `PartListMgmtClient` | Illustrated Parts Lists, illustrations, substitutes |
| ProjMgmt | `ProjMgmtClient` | Project plans, activities, milestones |
| NC | `NCClient` | Nonconformance tracking, quality issues |
| DocMgmt | `DocMgmtClient` | Documents, attachments |
| CADDocumentMgmt | `CADDocumentMgmtClient` | CAD documents, drawings |
| ChangeMgmt | `ChangeMgmtClient` | Change notices, requests, tasks |
| SupplierMgmt | `SupplierMgmtClient` | Suppliers, vendor parts |
| MfgProcMgmt | `MfgProcMgmtClient` | Process plans, operations |
| CEM | `CEMClient` | Customer experiences |
| BACMgmt | `BACMgmtClient` | Baselines, configurations |
| Workflow | `WorkflowClient` | Work items, activities |
| Audit | `AuditClient` | Audit records, compliance |
| DataAdmin | `DataAdminClient` | Containers, folders |
| ServiceInfoMgmt | `ServiceInfoMgmtClient` | Service documentation |
| UDI | `UDIClient` | Unique Device Identification |
| RegMstr | `RegMstrClient` | Regulatory Master |
| QMS | `QMSClient` | Quality Management (CAPA/NCR) |
| PrincipalMgmt | `PrincipalMgmtClient` | Users, groups, roles |
| PTC | `PTCClient` | Common entities, content download |
| CAPA | `CAPAClient` | Corrective and Preventive Actions |
| DocumentControl | `DocumentControlClient` | Controlled documents, training records |
| ClfStructure | `ClfStructureClient` | Classification hierarchy, nodes |
| DynamicDocMgmt | `DynamicDocMgmtClient` | Dynamic documents, burst configurations |
| EffectivityMgmt | `EffectivityMgmtClient` | Part effectivity, serial/lot/date effectivity |
| Factory | `FactoryClient` | Standard operations, procedures, SCC, resources |
| NavCriteria | `NavCriteriaClient` | Navigation criteria, config specs, filters |

---

## Common Patterns

### OData Filter Builder

Zephyr includes a comprehensive OData filter builder (`odata_filter_builder.py`) for constructing complex queries.

**NEW: `query_entities()` now accepts ODataFilter objects directly!**

```python
import sys
sys.path.insert(0, '/home/ubuntu/.hermes/skills/zephyr/scripts')
from odata_filter_builder import ODataFilter
from domains.ProdMgmt import ProdMgmtClient

client = ProdMgmtClient(config_path="config.json")

# Method 1: Pass ODataFilter object directly (RECOMMENDED)
f = ODataFilter().eq('State', 'RELEASED').and_contains('Name', 'Bracket')
parts = client.query_entities('Parts', filter_expr=f)

# Method 2: Raw string filter (works but no type safety)
parts = client.query_entities('Parts', filter_expr="State eq 'RELEASED' and contains(Name, 'Bracket')")

# Simple equality filter
f = ODataFilter().eq('Number', 'V0056726')
# Result: "Number eq 'V0056726'"

# Complex filter with AND/OR
f = (ODataFilter()
    .eq('State', 'RELEASED')
    .and_gt('Quantity', 10))
# Result: "State eq 'RELEASED' and Quantity gt 10"

# String functions
f = ODataFilter().contains('Name', 'Engine')
# Result: "contains(Name, 'Engine')"

# Grouped expressions with OR
f = (ODataFilter()
    .eq('State', 'RELEASED')
    .or_(ODataFilter().eq('State', 'APPROVED')))
# Result: "(State eq 'RELEASED' or State eq 'APPROVED')"

# Type checking with isof
f = ODataFilter().isof('WTPart')
# Result: "isof('WTPart')"

# Special properties (ID, CreatedBy, ModifiedBy, View)
f = ODataFilter().by_id('OR:wt.part.WTPart:12345')
# Result: "ID eq 'OR:wt.part.WTPart:12345'"

f = ODataFilter().by_created_by('admin').and_by_modified_by('user1')
# Result: "CreatedBy eq 'admin' and ModifiedBy eq 'user1'"
```

**Supported OData Expressions:**

| Category | Operators/Methods | Example |
|----------|-------------------|---------|
| Comparison | `eq`, `ne`, `gt`, `lt`, `ge`, `le` | `.eq('State', 'RELEASED')` |
| Logical | `and_()`, `or_()`, `not_()` | `.and_(ODataFilter().eq('State', 'APPROVED'))` |
| String | `startswith`, `endswith`, `contains` | `.contains('Name', 'Bracket')` |
| Type Check | `isof` | `.isof('WTPart')` |
| Special Props | ID, CreatedBy, ModifiedBy, View | `.by_id('OR:wt.part.WTPart:12345')` |
| Data Types | String, Int16/32/64, Boolean, DateTimeOffset, Single, Double | `.gt('Quantity', 100)` |

---

### Pagination for Large Datasets

Zephyr provides automatic pagination for handling large result sets:

```python
import sys
sys.path.insert(0, '/home/ubuntu/.hermes/skills/zephyr/scripts')
from domains.ProdMgmt import ProdMgmtClient

client = ProdMgmtClient(config_path="config.json")

# Get ALL parts (automatic pagination)
all_parts = client.query_all('Parts', filter_expr="State eq 'RELEASED'")

# With progress callback
def progress(page, count, total):
 print(f"Page {page}: {count} entities (total: {total})")
all_parts = client.query_all('Parts', progress_callback=progress)

# Memory-efficient iteration (generator)
for part in client.query_iter('Parts', filter_expr="State eq 'RELEASED'"):
 process_part(part) # Process one at a time

# Count before fetching
count = client.count_entities('Parts', filter_expr="State eq 'RELEASED'")
print(f"Found {count} released parts")

if count > 1000:
 # Use iterator for memory efficiency
 for part in client.query_iter('Parts'):
 export_part(part)
else:
 # Safe to load all at once
 parts = client.query_all('Parts')
```

**Pagination Methods:**

| Method | Purpose | Memory Usage |
|--------|---------|--------------|
| `query_all()` | Fetch all entities as list | O(n) - loads all into memory |
| `query_iter()` | Generator yielding one at a time | O(1) - constant memory |
| `count_entities()` | Get count without fetching data | O(1) - no entity data |

### Query Parts and BOM

```python
from domains.ProdMgmt import ProdMgmtClient
client = ProdMgmtClient(config_path="config.json")

# Query parts using query_entities
parts = client.query_entities('Parts', top=50)

# Search parts by term (full-text search)
results = client.search_parts('bracket')

# Get part by number
part = client.get_part_by_number("V0056726")

# Get BOM
bom = client.get_bom(part_id)
for item in bom:
 print(f"{item['child_part']['number']} | Qty: {item['quantity']}")
```

### Query Change Notices

```python
from domains.ChangeMgmt import ChangeMgmtClient
client = ChangeMgmtClient(config_path="config.json")

# Query change notices using query_entities
cns = client.query_entities('ChangeNotices', top=50)

# Get change notice by number
cn = client.get_change_notice_by_number("CN-2024-001")
```

### Query Quality Records (CAPA/NCR)

```python
from domains.QMS import QMSClient
client = QMSClient(config_path="config.json")

capas = client.get_capas()
open_capas = client.get_open_capas()
ncrs = client.get_ncrs()
```

### Query CAPA Domain (Dedicated Client)

```python
from domains.CAPA import CAPAClient
client = CAPAClient(config_path="config.json")

# Get CAPAs with expanded navigation properties
capa = client.get_capa_by_id(capa_id, expand=['Plan', 'PrimarySite'])
plan_actions = client.get_action_plan_actions(plan_id)

# Set CAPA state
client.set_capa_state(capa_id, 'CLOSED')
```

### Query DocumentControl Domain

```python
from domains.DocumentControl import DocumentControlClient
client = DocumentControlClient(config_path="config.json")

# Get controlled documents
docs = client.get_control_documents()
doc = client.get_control_document_by_number("DOC-001")

# Get training records
records = client.get_training_records_by_user(user_id)
```

### Query ClfStructure (Classification Hierarchy)

```python
from domains.ClfStructure import ClfStructureClient
client = ClfStructureClient(config_path="config.json")

# Navigate classification hierarchy
root_nodes = client.get_root_clf_nodes()
children = client.get_child_clf_nodes(parent_id)
path = client.get_classification_path(node_id)
tree = client.get_classification_tree(max_depth=3)
```

### Query Suppliers

```python
from domains.SupplierMgmt import SupplierMgmtClient
client = SupplierMgmtClient(config_path="config.json")

# Query suppliers (returns Manufacturers and Vendors)
suppliers = client.query_suppliers(top=50)

# Get specific supplier by name
supplier = client.get_supplier_by_name("Amphenol")

# Get supplier by ID
supplier = client.get_supplier_by_id("OR:com.ptc.windchill.suma.supplier.Manufacturer:2167863")

# Query manufacturer parts
mfg_parts = client.query_manufacturer_parts(filter_expr="Name eq 'Connector'")

# Query vendor parts
vendor_parts = client.query_vendor_parts(top=100)
```

### Get Document Attachments

```python
from domains.DocMgmt import DocMgmtClient
client = DocMgmtClient(config_path="config.json")

doc = client.get_document_by_number("DOC-001")
attachments = client.get_document_attachments(doc_id)
```

### DynamicDocMgmt - Dynamic Documents

```python
from domains.DynamicDocMgmt import DynamicDocMgmtClient
client = DynamicDocMgmtClient(config_path="config.json")

# Query dynamic documents
docs = client.get_dynamic_documents(top=50)
doc = client.get_dynamic_document_by_number("DYN-DOC-001")

# Get document with expanded navigation
doc = client.get_dynamic_document_by_id(doc_id, expand=["Creator", "Master", "Attachments"])

# Version control
client.check_out_document(doc_id)
client.check_in_document(doc_id, check_in_note="Updated content")
client.revise_document(doc_id)

# File upload (multi-stage)
client.upload_stage1(doc_id, no_of_files=1)
client.upload_stage3(doc_id, content_info={"FileName": "drawing.pdf"})

# Lifecycle state
client.set_document_state(doc_id, "RELEASED")
```

### EffectivityMgmt - Part Effectivity

```python
from domains.EffectivityMgmt import EffectivityMgmtClient
client = EffectivityMgmtClient(config_path="config.json")

# Query effectivity contexts
contexts = client.get_part_effectivity_contexts(top=50)
by_part = client.get_contexts_by_part(part_id)

# Get effectivity managed entities
entities = client.get_effectivity_managed_entities(top=50)
effectivities = client.get_entity_effectivities(entity_id)

# Query specific effectivity types
date_effs = client.get_date_effectivities_by_range("2024-01-01", "2024-12-31")
unit_effs = client.get_unit_effectivities_by_range(start_unit=100, end_unit=200)
serial_effs = client.get_serial_number_effectivities()
lot_effs = client.get_lot_effectivities()

# Set effectivities
client.set_effectivities_for_entity(entity_id, [
    {"Type": "DateEffectivity", "StartDate": "2024-01-01", "EndDate": "2024-12-31"}
])
```

### Factory - Standard Operations & Procedures

```python
from domains.Factory import FactoryClient
client = FactoryClient(config_path="config.json")

# Query standard operations
operations = client.get_standard_operations(top=50)
op = client.get_standard_operation_by_number("OP-001")

# Get operation with expanded navigation
op = client.get_standard_operation_by_id(op_id, expand=["Creator", "Master", "StandardProcedureUsages"])

# Version control for operations
client.check_out_operation(op_id, check_out_note="Updating operation")
client.check_in_operation(op_id, check_in_note="Changes complete")
client.revise_operation(op_id)

# Lifecycle state management
client.set_operation_state(op_id, "RELEASED")
client.set_operations_state_bulk([op_id1, op_id2], "INWORK")

# Standard Control Characteristics (SCC)
sccs = client.get_standard_control_characteristics(top=50)
scc = client.get_scc_by_number("SCC-001")

# SCC with expanded navigation
scc = client.get_scc_by_id(scc_id, expand=["Master", "ResourceUsages", "StandardProcedureUsages"])

# SCC version control and state
client.check_out_scc(scc_id)
client.check_in_scc(scc_id, check_in_note="Updated")
client.set_scc_state(scc_id, "RELEASED")

# Update SCC related links
client.update_scc_related_links(scc_id, test_run="TR-001", update_requests=[
    {"LinkType": "ResourceUsage", "Action": "Add", "ResourceId": "RES-001"}
])

# Standard Procedures
procedures = client.get_standard_procedures(top=50)
proc = client.get_standard_procedure_by_number("PROC-001")
client.set_procedure_state(proc_id, "RELEASED")

# Resources
resources = client.get_resources(top=50)
resource = client.get_resource_by_number("RES-001")
resource_usages = client.get_resource_usages(resource_id)
```

### NavCriteria - Navigation Criteria & Config Specs

```python
from domains.NavCriteria import NavCriteriaClient
client = NavCriteriaClient(config_path="config.json")

# Query navigation criteria
criteria = client.get_navigation_criteria(top=50)
criteria = client.get_navigation_criteria_by_name("MyConfig")
shared = client.get_shared_criteria()

# Build configuration specifications
standard_spec = client.build_standard_config_spec(view="Manufacturing")
baseline_spec = client.build_baseline_config_spec("OR:wt.proj.Baseline:12345")
effectivity_spec = client.build_effectivity_date_config_spec(
    start_date="2024-01-01T00:00:00Z",
    end_date="2024-12-31T23:59:59Z"
)

# Build filters
attr_filter = client.build_attribute_filter("Material", "Equals", "Steel")
box_filter = client.build_box_spatial_filter(0, 0, 0, 100, 100, 100)
option_filter = client.build_option_filter("Color", ["Red", "Blue"])

# Create navigation criteria
criteria = client.create_navigation_criteria(
    name="ManufacturingView",
    applicable_type="WTPart",
    config_specs=[standard_spec],
    filters=[attr_filter],
    apply_to_top_level=True,
    shared_to_all=True
)

# EPMDocument configuration
epm_spec = client.build_epmdoc_standard_config_spec(view="Design")

# Update criteria
client.update_navigation_criteria(criteria_id, config_specs=[baseline_spec])
```

### NC - Nonconformance Management

```python
from domains.NC import NCClient
client = NCClient(config_path="config.json")

# Query nonconformances
ncs = client.get_nonconformances(top=50)
open_ncs = client.get_open_nonconformances()
nc = client.get_nonconformance_by_number("NC-2024-001")

# Get by state/priority/severity
by_state = client.get_nonconformances_by_state("OPEN")
by_priority = client.get_nonconformances_by_priority("HIGH")
by_severity = client.get_nonconformances_by_severity("CRITICAL")

# Get with expanded navigation
nc = client.get_nonconformance_by_id(nc_id, expand=[
    "AffectedObjects",
    "ImmediateActions",
    "Creator",
    "Owner"
])

# Create nonconformance
nc = client.create_nonconformance(
    description="Material defect in batch A-123",
    identified_date="2024-01-15T10:00:00Z",
    source="Incoming Inspection",
    priority="HIGH",
    severity="MAJOR",
    location="Warehouse A",
    assigned_to="OR:wt.org.WTUser:12345"
)

# Manage affected objects
affected = client.add_affected_object(
    nc_id=nc["ID"],
    name="Part-001",
    number="PART-001",
    quantity=100,
    disposition="Scrap"
)
objects = client.get_affected_objects(nc_id)

# Manage immediate actions
action = client.add_immediate_action(
    nc_id=nc["ID"],
    description="Quarantine affected batch",
    action_type="CONTAINMENT",
    action_date="2024-01-15T12:00:00Z"
)
actions = client.get_immediate_actions(nc_id)

# Lifecycle management
client.set_nonconformance_state(nc_id, "IN_REVIEW")
client.reserve_nonconformance(nc_id, reservation_note="Reviewing NC")
client.undo_reservation_nonconformance(nc_id)

# File attachment
client.upload_attachment(nc_id, file_name="inspection_report.pdf", file_path="/path/to/file.pdf")
```

### ProdPlatformMgmt - Variant Specifications & Options

```python
from domains.ProdPlatformMgmt import ProdPlatformMgmtClient
client = ProdPlatformMgmtClient(config_path="config.json")

# Query variant specifications
specs = client.get_variant_specifications(top=50)
released = client.get_variant_specifications_by_state("RELEASED")
spec = client.get_variant_specification_by_number("VS-2024-001")

# Get with expanded navigation
spec = client.get_variant_specification_by_id(spec_id, expand=[
    "Options",
    "OptionSets",
    "Creator",
    "Owner"
])

# Query options and option sets
options = client.get_options(top=50)
option = client.get_option_by_number("OPT-001")
option_sets = client.get_option_sets(top=50)
option_set = client.get_option_set_by_number("OS-001")

# Get options for variant specification
options = client.get_options_for_variant_spec(spec_id)
option_sets = client.get_option_sets_for_variant_spec(spec_id)

# Manage choices
choices = client.get_choices(top=50)
design_choices = client.get_design_choices_for_option(option_id)
sales_choices = client.get_sales_choices_for_option(option_id)

# Create variant specification
spec = client.create_variant_specification(
    name="Product Family A",
    description="Variant specification for Product Family A",
    effectivity="2024-01-01 to 2024-12-31"
)

# Create option set
option_set = client.create_option_set(
    name="Color Options",
    expression="Color IN ('Red', 'Blue', 'Green')",
    is_active=True
)

# Version control
client.check_out_variant_specification(spec_id, check_out_note="Updating specification")
client.check_in_variant_specification(spec_id, check_in_note="Changes complete")
client.undo_check_out_variant_specification(spec_id)
client.revise_variant_specification(spec_id, description="New revision")

# Lifecycle state management
client.set_variant_specification_state(spec_id, "RELEASED")
client.set_variant_specifications_state_bulk([spec_id1, spec_id2], "INWORK")
client.set_option_set_state(option_set_id, "RELEASED")
client.set_choice_state(choice_id, "RELEASED")
```

### PartListMgmt - Illustrated Parts Lists

```python
from domains.PartListMgmt import PartListMgmtClient
client = PartListMgmtClient(config_path="config.json")

# Query Part Lists
partlists = client.get_partlists(top=50)
released = client.get_partlists_by_state("RELEASED")
partlist = client.get_partlist_by_number("PL-001")

# Get with expanded navigation
partlist = client.get_partlist_by_id(partlist_id, expand=[
    "Uses",
    "Creator",
    "Organization",
    "Versions"
])

# Get Part List Items
items = client.get_partlist_items(top=50)
item = client.get_partlist_item_by_id(item_id)
items = client.get_partlist_items_for_partlist(partlist_id)

# Get Illustrations
illustrations = client.get_illustrations(top=50)
ill = client.get_illustration_by_id(ill_id)
illustrations = client.get_illustrations_for_partlist(partlist_id)

# Get Substitutes and Supplements
substitutes = client.get_substitutes_for_item(item_id)
supplements = client.get_supplements_for_item(item_id)

# Version control
client.check_out_partlist(partlist_id, check_out_note="Updating part list")
client.check_in_partlist(partlist_id, check_in_note="Changes complete")
client.undo_check_out_partlist(partlist_id)
client.revise_partlist(partlist_id)

# Bulk operations
client.check_out_partlists_bulk([pl_id1, pl_id2], check_out_note="Bulk update")
client.check_in_partlists_bulk([pl_id1, pl_id2], check_in_note="Bulk complete")
client.revise_partlists_bulk([pl_id1, pl_id2])

# Lifecycle state management
client.set_partlist_state(partlist_id, "RELEASED")
client.set_partlists_state_bulk([pl_id1, pl_id2], "RELEASED")

# Update properties
client.update_partlist_properties(partlist_id, updates=[
    {"Name": "New Part List Name"}
])
client.update_partlist_item_properties(item_id, updates=[
    {"Quantity": "10"}
])
```

### ProjMgmt - Project Management

```python
from domains.ProjMgmt import ProjMgmtClient
client = ProjMgmtClient(config_path="config.json")

# Query Project Plans
plans = client.get_project_plans(top=50)
plan = client.get_project_plan_by_id(plan_id)
plan = client.get_project_plan_by_name("Product Development 2026")

# Get with expanded navigation
plan = client.get_project_plan_by_id(plan_id, expand=[
    "Activities",
    "ImmediateChildren",
    "Context"
])

# Query Activities
activities = client.get_activities(top=50)
activity = client.get_activity_by_id(activity_id)
activities = client.get_activities_by_name("Design Review")
activities = client.get_activities_by_plan_name("Product Development 2026")

# Get specific types
milestones = client.get_milestones(top=50)
summaries = client.get_summary_activities(top=50)
deliverables = client.get_deliverable_activities(top=50)

# Navigation properties
activities = client.get_activities_for_plan(plan_id)
top_level = client.get_immediate_children(plan_id)
children = client.get_activity_children(activity_id)
owner = client.get_activity_owner(activity_id)
deliverables = client.get_activity_deliverables(activity_id)

# Create Project Plan
plan = client.create_project_plan(
    name="New Product Launch",
    deadline="2026-12-31",
    estimated_start="2026-06-01",
    estimated_finish="2026-12-31"
)

# Create Activity
activity = client.create_activity(
    name="Phase 1: Design",
    start_date="2026-05-01T00:00:00Z",
    finish_date="2026-05-31T00:00:00Z",
    summary=True
)

# Create Milestone
milestone = client.create_activity(
    name="Design Complete",
    start_date="2026-05-31T00:00:00Z",
    finish_date="2026-05-31T00:00:00Z",
    milestone=True
)

# Add Activity to Plan
client.add_activity_to_plan(plan_id, activity_id)

# Create and add in one step
activity = client.create_activity_in_plan(
    plan_id=plan_id,
    name="Testing Phase",
    start_date="2026-06-01T00:00:00Z",
    finish_date="2026-06-30T00:00:00Z"
)

# Update Activity
client.update_activity(activity_id, percent_work_complete=75.0)
client.update_activity(activity_id, status="IN_PROGRESS")

# Update Project Plan
client.update_project_plan(plan_id, percent_work_complete=50.0)
```

---

## BOM Query (Uses Navigation)

Since `GetBOM` may not be exposed, use the `Uses` navigation:

```python
# Method 1: Domain client (returns usage links only - no child part details)
from domains.ProdMgmt import ProdMgmtClient
client = ProdMgmtClient(config_path="config.json")
bom = client.get_bom(part_id)  # Returns PartUsageLink objects

# Method 2: Direct OData call with $expand=Uses to get child part details
from windchill_odata_client import WindchillODataClient
client = WindchillODataClient(config_path="config.json")
bom = client.query_entities(f"Parts('{part_id}')/Uses?$expand=Uses")

for item in bom:
    child = item.get('Uses', {})
    print(f"{child.get('Number')} | {child.get('Name')} | Qty: {item.get('Quantity')}")
```

---

## File Structure

```
zephyr/
├── SKILL.md              # This file (quick reference)
├── config.example.json   # Configuration template
├── scripts/
│   ├── windchill_base.py         # Base client
│   ├── windchill_odata_client.py # Comprehensive OData client
│   ├── property_resolver.py      # Case-insensitive property resolution
│   ├── output_formatter.py       # Output formatting
│ └── domains/ # Domain-specific clients (USE THESE)
│ ├── ProdMgmt/
│ ├── DocMgmt/
│ ├── ChangeMgmt/
│ ├── CAPA/
│ ├── DocumentControl/
│ ├── ClfStructure/
│ ├── DynamicDocMgmt/
│ ├── EffectivityMgmt/
│ ├── Factory/
│ ├── NavCriteria/
│ ├── NC/
│ ├── ProdPlatformMgmt/
│ ├── PartListMgmt/
│ ├── ProjMgmt/
│ └── ... (28 domains)
└── references/ # Detailed documentation by domain
 ├── ProdMgmt/
 │ ├── ProdMgmt_REFERENCE.md
 │ ├── ProdMgmt_Navigations.md
 │ └── ProdMgmt_Entities.json
 ├── ChangeMgmt/
 ├── QMS/
 ├── CAPA/
 ├── DocumentControl/
 ├── ClfStructure/
 ├── DynamicDocMgmt/
 ├── EffectivityMgmt/
 ├── Factory/
 ├── NavCriteria/
 └── ... (24 domains)
```

---

## Reference Documentation

For detailed usage, see `references/<Domain>/<Domain>_REFERENCE.md`:

| Domain | Reference File | Key Entities |
|--------|----------------|--------------|
| ProdMgmt | `references/ProdMgmt/ProdMgmt_REFERENCE.md` | Part, PartUse, BOM |
| ChangeMgmt | `references/ChangeMgmt/ChangeMgmt_REFERENCE.md` | ChangeNotice, ChangeTask |
| QMS | `references/QMS/QMS_REFERENCE.md` | CAPA, NCR, QualityAction |
| DocMgmt | `references/DocMgmt/DocMgmt_REFERENCE.md` | Document, Attachment |
| PTC | `references/PTC/PTC_REFERENCE.md` | Common types, OID format |
| CAPA | `references/CAPA/CAPA_REFERENCE.md` | CAPA, CAPAActionPlan, Action |
| DocumentControl | `references/DocumentControl/DocumentControl_REFERENCE.md` | ControlDocument, TrainingRecord |
| ClfStructure | `references/ClfStructure/ClfStructure_REFERENCE.md` | ClfNode, ClassifiedObject |
| DynamicDocMgmt | `references/DynamicDocMgmt/DynamicDocMgmt_REFERENCE.md` | DynamicDocument, BurstConfiguration |
| EffectivityMgmt | `references/EffectivityMgmt/EffectivityMgmt_REFERENCE.md` | PartEffectivityContext, Effectivity |
| Factory | `references/Factory/Factory_REFERENCE.md` | StandardOperation, StandardProcedure, StandardControlCharacteristic |
| NavCriteria | `references/NavCriteria/NavCriteria_REFERENCE.md` | NavigationCriteria, CachedNavigationCriteria |
| NC | `references/NC/NC_REFERENCE.md` | Nonconformance, AffectedObject, ImmediateAction |
| ProdPlatformMgmt | `references/ProdPlatformMgmt/ProdPlatformMgmt_REFERENCE.md` | VariantSpecification, OptionSet, Option, Choice |
| PartListMgmt | `references/PartListMgmt/PartListMgmt_REFERENCE.md` | PartList, PartListItem, Illustration, Substitute, Supplement |
| ProjMgmt | `references/ProjMgmt/ProjMgmt_REFERENCE.md` | ProjectPlan, Activity |

---

## Configuration

**Basic Auth Format:**
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

**OAuth 2.0 Format:**
```json
{
 "server_url": "https://windchill.example.com/Windchill",
 "odata_base_url": "https://windchill.example.com/Windchill/servlet/odata/",
 "auth_type": "oauth",
 "oauth": {
   "client_id": "your_client_id",
   "client_secret": "your_client_secret",
   "token_url": "https://windchill.example.com/Windchill/oauth2/token",
   "scope": "windchill"
 },
 "verify_ssl": true,
 "timeout": 30
}
```

**Important:** Credentials are nested under `basic` or `oauth` object, not at root level. Config file location: `/home/ubuntu/.hermes/skills/zephyr/config.json` (gitignored).

---

## Key Navigation Properties

| Entity | Navigation | Purpose |
|--------|------------|---------|
| Part | `Uses` | BOM children |
| Part | `UsedBy` | Parent assemblies |
| Part | `Versions` | Version history |
| Document | `Attachments` | File attachments |
| ChangeNotice | `Tasks` | Change tasks |
| ChangeNotice | `AffectedObjects` | Affected items |
| CAPA | `Plan` | Action Plan |
| CAPA | `PrimarySite` | Primary location |
| CAPA | `AffectedObjects` | Affected items |
| ClfNode | `Children` | Child classifications |
| ClfNode | `ClassifiedObjects` | Objects in classification |
| DynamicDocument | `Creator` | Document creator |
| DynamicDocument | `Master` | Document master |
| DynamicDocument | `Versions` | Version history |
| DynamicDocument | `Attachments` | File attachments |
| DynamicDocument | `Members` | Document members |
| PartEffectivityContext | `Part` | Associated part |
| PartEffectivityContext | `Effectivity` | Associated effectivity |
| Effectivity | `PartEffectivity` | Part effectivity reference |
| StandardOperation | `Folder` | Operation folder |
| StandardOperation | `Master` | Operation master |
| StandardOperation | `Versions` | Version history |
| StandardOperation | `StandardProcedureUsages` | Procedure usages |
| StandardControlCharacteristic | `Folder` | SCC folder |
| StandardControlCharacteristic | `Master` | SCC master |
| StandardControlCharacteristic | `ResourceUsages` | Resource usages |
| StandardControlCharacteristic | `StandardProcedureUsages` | Procedure usages |
| StandardProcedure | `Folder` | Procedure folder |
| StandardProcedure | `Master` | Procedure master |
| Resource | `Folder` | Resource folder |
| Resource | `ResourceUsages` | Resource usages |

---

## Actions (39 total)

See `references/PTC/actions.json` for full list. Common actions:

**Unbound**: CreateAssociations, SetStateParts, ReviseParts, CheckOutParts

**Bound**: CheckOut, CheckIn, UndoCheckOut, Revise, GetMultiLevelBOMRollup

---

## Deprecated Scripts

**DO NOT USE** `scripts/old/` - Use domain clients instead:

| Old Script | Use Instead |
|------------|-------------|
| query_parts.py | `ProdMgmtClient.query_entities('Parts')` |
| query_change_notices.py | `ChangeMgmtClient.query_entities('ChangeNotices')` |
| query_qms.py | `QMSClient.query_entities('CAPAs')` or `CAPAClient` |
| generic_query.py | `WindchillODataClient.query_entities()` |

**DO NOT CREATE AD-HOC SCRIPTS** - Domain clients already support all query patterns:

```python
# Instead of creating a new script like search_docs_038.py, use:

from domains.DocMgmt import DocMgmtClient
client = DocMgmtClient(config_path="config.json")

# Field-specific search (recommended)
docs = client.query_entities('Documents', filter_expr="contains(Number, '038')")

# Or use the search method for full-text search
docs = client.search_documents('038')
```

---

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid domain request" | Double slash in URL | Check odata_base_url trailing slash |
| "CSRF token missing" | POST without token | Get token from `/PTC/GetCSRFToken()` |
| "$top not supported" | Single-entity navigation | Remove pagination params |
| 7-8s response time | PTC demo server | Normal behavior, not a bug |

---

## License

Apache License 2.0. See [LICENSE](LICENSE) file for full text.

**Key Points:**
- Free to use, modify, and distribute
- Must include license copy in distributions
- Must retain copyright notices
- Patent license granted by contributors
- See [Apache 2.0 Summary](https://www.apache.org/licenses/LICENSE-2.0)
