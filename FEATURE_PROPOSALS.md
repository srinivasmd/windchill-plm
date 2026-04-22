# Zephyr Skill Enhancement Proposals

## Current State Analysis

- **Domain Clients:** 28 domains implemented
- **Query Methods:** 363 get_* methods across domain clients
- **Total Lines:** ~12,102 lines in domain client code
- **Actions Extracted:** 100+ actions in actions.json
- **Test Coverage:** None (deprecated test_csrf.py only)
- **Async Support:** None
- **Logging:** None
- **Caching:** None (server-side only)

---

## 1. TEST SUITE

**Gap:** No automated tests found (only deprecated test_csrf.py in scripts/old/)

**Proposed:**
- Unit tests for each domain client
- Integration tests with mock Windchill responses
- CSRF token flow tests
- Property resolution tests
- Error handling tests

**Files to Create:**
```
tests/
├── __init__.py
├── conftest.py
├── test_windchill_base.py
├── test_property_resolver.py
├── test_domains/
│   ├── test_prodmgmt.py
│   ├── test_changemgmt.py
│   └── ...
└── fixtures/
    ├── parts_response.json
    ├── change_notices_response.json
    └── ...
```

---

## 2. ASYNC SUPPORT

**Gap:** All operations are synchronous - no async/await patterns

**Proposed:**
- Async client variant for parallel queries
- Batch operations with asyncio.gather()
- Connection pooling with aiohttp
- Rate limiting with semaphores

**Example Use Case:**
```python
# Fetch 50 parts' BOMs concurrently instead of 50 sequential calls
async with AsyncProdMgmtClient() as client:
    parts = await client.get_parts(top=50)
    boms = await asyncio.gather(*[
        client.get_bom(part['ID']) for part in parts
    ])
```

**Files to Create:**
```
scripts/
├── windchill_async_base.py
└── domains/
    └── ProdMgmt/
        └── async_client.py
```

---

## 3. SMART CACHING LAYER

**Gap:** Only "CachedNavigationCriteria" entity exists - no client-side caching

**Proposed:**
- Metadata caching (entities.json, actions.json) with TTL
- CSRF token caching with auto-refresh
- Query result caching with configurable TTL
- Invalidation strategies by domain/entity type

**Example:**
```python
client = ProdMgmtClient(
    config_path="config.json",
    cache_enabled=True,
    cache_ttl=300,  # 5 minutes
    cache_invalid_on_write=True
)
```

**Files to Create:**
```
scripts/
├── cache_manager.py
└── cache_backends/
    ├── memory_cache.py
    ├── redis_cache.py
    └── file_cache.py
```

---

## 4. LOGGING & DEBUGGING

**Gap:** No logging module integration found

**Proposed:**
- Structured logging (JSON format)
- Request/response logging with redacted credentials
- Performance metrics (latency per domain)
- Debug mode with full HTTP traces

**Example:**
```python
import logging
from windchill_base import WindchillBaseClient

logging.basicConfig(level=logging.INFO)
client = ProdMgmtClient(config_path="config.json", log_level="DEBUG")

# Logs:
# {"timestamp": "2024-04-12T10:30:00Z", "level": "INFO", "domain": "ProdMgmt", "action": "query", "entity": "Parts", "duration_ms": 7234}
```

**Configuration:**
```json
{
  "logging": {
    "level": "INFO",
    "format": "json",
    "file": "/var/log/zephyr/client.log",
    "redact_credentials": true,
    "include_request_body": false
  }
}
```

---

## 5. CLI TOOL

**Gap:** No command-line interface for ad-hoc queries

**Proposed:**
```bash
# Part operations
zephyr parts list --top 50 --state RELEASED
zephyr parts get V0056726 --bom --expand Creator
zephyr parts create --number PART-001 --name "Widget" --type COMPONENT

# Change management
zephyr changes list --state OPEN
zephyr changes get CN-001 --tasks

# CAPA operations
zephyr capa list --priority HIGH
zephyr capa create --description "Issue found" --priority HIGH

# BOM operations
zephyr bom get PART-001 --levels 5
zephyr bom compare PART-001 PART-002 --output diff.html

# Export
zephyr parts list --format csv --output parts.csv
zephyr bom get PART-001 --format xlsx --output bom.xlsx
```

**Files to Create:**
```
scripts/
└── cli.py

# Or as standalone package:
cli/
├── __init__.py
├── main.py
├── commands/
│   ├── parts.py
│   ├── changes.py
│   ├── capa.py
│   ├── bom.py
│   └── export.py
└── formatters/
    ├── table.py
    ├── json.py
    ├── csv.py
    └── xlsx.py
```

---

## 6. ACTION WRAPPER METHODS

**Gap:** actions.json lists 100+ actions, but only ~10% have friendly wrappers

**Current Coverage:**
- ProdMgmt: CheckOut, CheckIn, Revise, SetState, GetMultiLevelBOMRollup
- ChangeMgmt: Limited action wrappers
- Other domains: Minimal action coverage

**Proposed:**

### Auto-generate wrappers from actions.json:
```python
# In windchill_base.py
def invoke_action(self, action_name: str, entity_id: str = None, 
                  parameters: dict = None) -> dict:
    """Generic action invocation with parameter validation."""
    action_meta = self._get_action_metadata(action_name)
    validated_params = self._validate_action_params(action_meta, parameters)
    return self._execute_action(action_name, entity_id, validated_params)
```

### Priority Actions to Wrap (ProdMgmt):
| Action | Purpose | Parameters |
|--------|---------|------------|
| CreateAssociations | Link parts to documents | PartDocAssociation[] |
| GetEquivalenceNetworkForParts | Find equivalent parts | Parts[] |
| AssignPlant | Assign manufacturing plant | Parts[], Plants[], ChangeOid |
| DetectAndResolveDiscrepancies | BOM reconciliation | DiscrepancyContext |
| GetManufacturingBOM | Manufacturing view of BOM | NavigationCriteria |

### Domain-specific wrappers:
```python
# domains/ProdMgmt/client.py additions
def create_part_document_association(self, part_id: str, document_id: str, 
                                      association_type: str = "Reference") -> dict:
    """Create Part-Document association."""
    return self.invoke_unbound_action('CreateAssociations', {
        'PartDocAssociations': [{
            'Part': {'ID': part_id},
            'Document': {'ID': document_id},
            'Type': association_type
        }]
    })

def get_equivalent_parts(self, part_ids: List[str]) -> List[dict]:
    """Find all equivalent parts across plants."""
    return self.invoke_unbound_action('GetEquivalenceNetworkForParts', {
        'parts': [{'ID': pid} for pid in part_ids]
    })
```

---

## 7. BOM COMPARISON & DIFF

**Gap:** Only GetMultiLevelBOMRollup exists, no comparison tools

**Proposed:**

### BOM Diff API:
```python
from domains.ProdMgmt import ProdMgmtClient

client = ProdMgmtClient(config_path="config.json")

# Compare two BOMs
diff = client.compare_boms(
    part_number_a="PART-001",
    part_number_b="PART-002",
    levels=5
)

# Result structure:
{
    "added": [
        {"number": "NEW-PART", "level": 2, "quantity": 5}
    ],
    "removed": [
        {"number": "OLD-PART", "level": 3, "quantity": 2}
    ],
    "changed": [
        {
            "number": "MODIFIED-PART",
            "level": 2,
            "changes": {
                "quantity": {"old": 3, "new": 5},
                "material": {"old": "Steel", "new": "Aluminum"}
            }
        }
    ]
}
```

### Version Comparison:
```python
# Compare Part A.1 vs Part A.2
diff = client.compare_part_versions(
    part_number="PART-001",
    version_a="A.1",
    version_b="A.2"
)
```

### Export Formats:
```python
# Export diff to HTML
diff.to_html("bom_diff.html")

# Export to CSV
diff.to_csv("bom_diff.csv")

# Visual tree diff
diff.visualize(mode="side-by-side")
```

**Files to Create:**
```
scripts/
└── bom_diff.py

references/
└── ProdMgmt/
    └── ProdMgmt_BOM_DIFF.md
```

---

## 8. BATCH OPERATIONS FRAMEWORK

**Gap:** Some domains have bulk ops (check_out_parts_bulk), inconsistent coverage

**Proposed:**

### Unified Batch Interface:
```python
from domains.ProdMgmt import ProdMgmtClient
from batch import BatchOperation

client = ProdMgmtClient(config_path="config.json")

# Create batch operation
batch = BatchOperation(
    client=client,
    operation="set_state",
    items=["PART-001", "PART-002", "PART-003"],
    params={"state": "RELEASED"},
    batch_size=10,
    concurrency=3,
    retry_count=3,
    retry_delay=2.0
)

# Execute with progress callback
result = batch.execute(
    progress_callback=lambda completed, total: print(f"{completed}/{total}")
)

# Result
{
    "total": 3,
    "successful": 3,
    "failed": 0,
    "errors": [],
    "duration_seconds": 12.5
}
```

### Retry with Exponential Backoff:
```python
batch = BatchOperation(
    client=client,
    operation="revise_parts",
    items=part_ids,
    retry_count=3,
    retry_delay=1.0,
    retry_backoff=2.0,  # 1s, 2s, 4s
    retry_on=[500, 502, 503, 504]  # Retry on server errors
)
```

### Resume Interrupted Batches:
```python
# Save batch state
batch.save_state("/tmp/batch_state.json")

# Resume later
batch = BatchOperation.restore_state("/tmp/batch_state.json")
batch.resume()
```

**Files to Create:**
```
scripts/
├── batch.py
└── batch_state_manager.py
```

---

## 9. CROSS-DOMAIN RELATIONSHIPS

**Gap:** CrossDomain_Navigations.md exists but no helpers

**Proposed:**

### Relationship Traversal Helpers:
```python
# Part -> ChangeNotice -> Tasks -> AffectedObjects
part_changes = client.get_part_change_history("PART-001")
# Returns all change notices affecting this part

# Part -> Documents -> Attachments
attachments = client.get_part_document_attachments("PART-001")
# Returns all document attachments for a part

# CAPA -> Plan -> Actions -> Resources
capa_details = capa_client.get_capa_full_details(capa_id)
# Returns CAPA with expanded Plan, Actions, Resources
```

### Pre-defined Traversal Paths:
```python
TRAVERSAL_PATHS = {
    "part_to_changes": [
        ("ProdMgmt", "Parts", "AffectedBy"),
        ("ChangeMgmt", "ChangeNotices", "Tasks")
    ],
    "part_to_documents": [
        ("ProdMgmt", "Parts", "DescribedBy"),
        ("DocMgmt", "Documents", "Attachments")
    ],
    "capa_to_resources": [
        ("CAPA", "CAPAs", "Plan"),
        ("CAPA", "ActionPlans", "Actions"),
        ("Factory", "Actions", "Resources")
    ]
}

# Usage
result = client.traverse_path(
    start_entity="Parts",
    start_id=part_id,
    path_name="part_to_changes"
)
```

**Files to Create:**
```
scripts/
└── cross_domain.py

references/
└── CrossDomain_Relationships.md
```

---

## 10. EXPORT FORMATS

**Gap:** Only JSON output, output_formatter.py exists but underutilized

**Proposed:**

### CSV Export:
```python
from exporters import CSVExporter

parts = client.get_parts(top=100)
exporter = CSVExporter(parts)
exporter.save("parts.csv", columns=["Number", "Name", "State", "Creator"])

# With custom formatting
exporter.save("parts.csv", 
    columns=["Number", "Name", "State"],
    headers={"Number": "Part Number", "State": "Lifecycle State"},
    include_header=True
)
```

### Excel Export:
```python
from exporters import ExcelExporter

bom = client.get_bom(part_id)
exporter = ExcelExporter(bom)
exporter.save("bom.xlsx", 
    sheet_name="BOM",
    formatting={
        "header": {"bold": True, "bg_color": "#4472C4"},
        "alternating_rows": True
    }
)
```

### BOM Tree Visualization:
```python
from exporters import BOMTreeExporter

bom = client.get_multi_level_bom(part_id, levels=5)
exporter = BOMTreeExporter(bom)
exporter.save("bom_tree.txt", format="ascii")  # ASCII tree
exporter.save("bom_tree.html", format="html")  # Collapsible HTML
```

### PDF Reports:
```python
from exporters import PDFExporter

change_notice = client.get_change_notice_by_number("CN-001")
exporter = PDFExporter(change_notice, template="change_notice")
exporter.save("CN-001.pdf")
```

**Files to Create:**
```
scripts/
└── exporters/
    ├── __init__.py
    ├── base.py
    ├── csv_exporter.py
    ├── excel_exporter.py
    ├── pdf_exporter.py
    └── tree_exporter.py
```

---

## 11. WEBHOOK SUBSCRIPTIONS

**Gap:** Windchill supports event notifications, no integration

**Proposed:**

### Event Subscription:
```python
from zephyr.webhooks import WebhookManager

webhooks = WebhookManager(config_path="config.json")

# Subscribe to entity changes
webhooks.subscribe(
    entity_type="Parts",
    events=["created", "modified", "state_changed"],
    callback_url="https://myapp.com/webhooks/parts"
)

# Subscribe to workflow events
webhooks.subscribe(
    entity_type="ChangeNotices",
    events=["workflow_started", "task_assigned", "workflow_completed"],
    callback_url="https://myapp.com/webhooks/changes"
)
```

### Polling-based Detection:
```python
# For servers without webhook support
from zephyr.polling import PollingManager

poller = PollingManager(config_path="config.json", poll_interval=60)
poller.watch("Parts", filter_expr="State eq 'RELEASED'", 
             on_change=lambda event: process_event(event))
poller.start()
```

### Callback Handlers:
```python
# Flask example
from flask import Flask, request
from zephyr.webhooks import WebhookHandler

app = Flask(__name__)
handler = WebhookHandler(secret="my-webhook-secret")

@app.route("/webhooks/parts", methods=["POST"])
def handle_part_webhook():
    event = handler.parse(request.json)
    if event.type == "created":
        sync_new_part(event.data)
    return {"status": "ok"}, 200
```

**Files to Create:**
```
scripts/
├── webhooks.py
└── polling.py
```

---

## 12. CONFIGURATION PROFILES

**Gap:** Single config.json, no environment support

**Proposed:**

### Multi-profile Configuration:
```json
{
  "profiles": {
    "dev": {
      "server_url": "https://windchill-dev.example.com",
      "verify_ssl": false,
      "timeout": 60
    },
    "staging": {
      "server_url": "https://windchill-staging.example.com",
      "verify_ssl": true,
      "timeout": 30
    },
    "prod": {
      "server_url": "https://windchill.example.com",
      "verify_ssl": true,
      "timeout": 30
    }
  },
  "default_profile": "dev"
}
```

### Environment Variable Overrides:
```bash
export WINDCHILL_PROFILE=prod
export WINDCHILL_SERVER_URL=https://windchill.example.com
export WINDCHILL_USERNAME=admin
export WINDCHILL_TIMEOUT=60
```

### Usage:
```python
# Auto-detect from environment
client = ProdMgmtClient()  # Uses WINDCHILL_PROFILE

# Explicit profile
client = ProdMgmtClient(profile="staging")

# Direct credentials (for testing)
client = ProdMgmtClient(
    base_url="https://test.example.com",
    username="test_user",
    password="test_pass"
)
```

**Files to Create:**
```
scripts/
└── config_manager.py
```

---

## 13. VALIDATION LAYER

**Gap:** No pre-flight validation for create/update operations

**Proposed:**

### Schema-based Validation:
```python
from zephyr.validation import validate_part_create, ValidationError

part_data = {
    "Number": "PART-001",
    "Name": "Widget",
    "Type": "COMPONENT"
}

try:
    validated = validate_part_create(part_data)
    client.create_part(**validated)
except ValidationError as e:
    print(f"Validation failed: {e.errors}")
```

### Metadata-driven Validation:
```python
# Auto-generated from entities.json
def validate_entity(entity_type: str, data: dict, operation: str) -> dict:
    """Validate entity against OData metadata."""
    schema = get_entity_schema(entity_type)
    errors = []
    
    # Required fields
    for field in schema.required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Type checking
    for field, value in data.items():
        expected_type = schema.get_field_type(field)
        if not isinstance(value, expected_type):
            errors.append(f"Field '{field}' must be {expected_type}")
    
    if errors:
        raise ValidationError(errors)
    
    return data
```

### Custom Validation Rules:
```python
from zephyr.validation import validators

# Part number format
@validators.register("part_number")
def validate_part_number(value: str) -> bool:
    return re.match(r"^[A-Z]{2,4}-\d{4,6}$", value) is not None

# Use in schema
validators.add_rule("Part", "Number", "part_number")
```

**Files to Create:**
```
scripts/
└── validation/
    ├── __init__.py
    ├── validators.py
    ├── schemas/
    │   ├── part_schema.py
    │   ├── change_notice_schema.py
    │   └── ...
    └── rules/
        └── custom_rules.py
```

---

## 14. GRAPHQL TRANSLATOR

**Gap:** OData can be complex for frontend consumers

**Proposed:**

### GraphQL Schema Generation:
```python
from zephyr.graphql import generate_schema

# Generate GraphQL schema from OData metadata
schema = generate_schema(
    metadata_path="references/entities.json",
    output_path="graphql/schema.graphql"
)
```

### Query Translation:
```graphql
# GraphQL query
query {
  parts(filter: {state: {eq: "RELEASED"}}, top: 10) {
    Number
    Name
    State
    Creator {
      Name
    }
    Uses {
      child_part {
        Number
        quantity
      }
    }
  }
}
```

Translates to OData:
```
GET /ProdMgmt/Parts?$filter=State eq 'RELEASED'&$top=10&$expand=Creator,Uses($expand=child_part)
```

### Implementation:
```python
from zephyr.graphql import GraphQLTranslator

translator = GraphQLTranslator()
odata_query = translator.translate("""
  query {
    parts(filter: {state: {eq: "RELEASED"}}) {
      Number
      Name
    }
  }
""")
# Returns: "Parts?$filter=State eq 'RELEASED'&$select=Number,Name"
```

**Files to Create:**
```
scripts/
└── graphql/
    ├── __init__.py
    ├── schema_generator.py
    ├── translator.py
    └── resolvers.py
```

---

## 15. MOCK SERVER FOR TESTING

**Gap:** Testing requires live Windchill server

**Proposed:**

### Mock Server Implementation:
```python
from zephyr.mock import MockWindchillServer

# Start mock server
server = MockWindchillServer(port=8080)
server.start()

# Configure responses
server.add_response(
    path="/ProdMgmt/Parts",
    response={"value": [{"ID": "123", "Number": "PART-001"}]},
    status_code=200
)

# Use in tests
client = ProdMgmtClient(base_url="http://localhost:8080")
parts = client.get_parts()  # Returns mock data

server.stop()
```

### Response Fixtures:
```python
# Load from real API responses
server.load_fixtures("tests/fixtures/")

# Record real responses for later playback
server.record_mode = True
# Make real API calls...
server.save_fixtures("tests/fixtures/")
```

### CI/CD Integration:
```yaml
# GitHub Actions
- name: Run Tests
  run: |
    python -m zephyr.mock --port 8080 &
    pytest tests/
```

**Files to Create:**
```
scripts/
└── mock/
    ├── __init__.py
    ├── server.py
    ├── fixtures.py
    └── recorder.py

tests/
└── fixtures/
    ├── parts_list.json
    ├── part_detail.json
    ├── bom.json
    └── change_notices.json
```

---

## Prioritization Matrix

| Priority | Feature | Impact | Effort | Dependencies |
|----------|---------|--------|--------|--------------|
| **P0** | Test Suite | High | Medium | None |
| **P0** | Logging | High | Low | None |
| **P1** | CLI Tool | High | Medium | None |
| **P1** | Configuration Profiles | Medium | Low | None |
| **P2** | Async Support | High | Medium | None |
| **P2** | Caching | Medium | Medium | Logging |
| **P2** | Action Wrappers | High | Medium | None |
| **P3** | Validation Layer | Medium | Medium | None |
| **P3** | Batch Operations | Medium | Medium | Logging |
| **P3** | Export Formats | Medium | Low | None |
| **P4** | BOM Diff | Medium | Medium | None |
| **P4** | Cross-Domain Relationships | Medium | Medium | None |
| **P5** | Webhook Subscriptions | Low | High | Logging |
| **P5** | GraphQL Translator | Low | High | None |
| **P5** | Mock Server | Low | Medium | Test Suite |

---

## Implementation Roadmap

### Phase 1: Foundation (1-2 weeks)
- Test Suite (P0)
- Logging (P0)
- Configuration Profiles (P1)

### Phase 2: UX Improvements (2-3 weeks)
- CLI Tool (P1)
- Export Formats (P3)
- Action Wrappers (P2)

### Phase 3: Performance (2-3 weeks)
- Async Support (P2)
- Caching (P2)
- Batch Operations (P3)

### Phase 4: Advanced Features (3-4 weeks)
- Validation Layer (P3)
- BOM Diff (P4)
- Cross-Domain Relationships (P4)

### Phase 5: Enterprise Features (4-6 weeks)
- Webhook Subscriptions (P5)
- GraphQL Translator (P5)
- Mock Server (P5)

---

## Notes

- Each feature should be implemented as a separate branch
- All new features require tests before merge
- Documentation updates required for each feature
- Breaking changes require version bump and migration guide
