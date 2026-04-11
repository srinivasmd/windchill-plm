# Zephyr - Windchill PLM REST API Client

A comprehensive Python client for interacting with PTC Windchill PLM REST APIs. Supports OAuth 2.0 and Basic authentication.

## Features

- **Modular Architecture**: 16 domain-specific clients for clean, maintainable code
- **Complete CRUD Operations**: Create, Read, Update, Delete for all Windchill entities
- **BOM Management**: Query and explore Bill of Materials with multi-level rollup
- **Domain Coverage**: ProdMgmt, DocMgmt, ChangeMgmt, QMS, RegMstr, UDI, and more
- **Type-Safe Methods**: Domain clients provide typed methods for common operations
- **CLI Support**: All domain clients include command-line interfaces

## Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/zephyr.git
cd zephyr
```

2. Install dependencies:
```bash
pip install requests
```

3. Copy `config.example.json` to `config.json` and configure:
```json
{
  "server_url": "https://windchill.example.com/Windchill",
  "odata_base_url": "https://windchill.example.com/Windchill/servlet/odata/",
  "auth_type": "basic",
  "basic": {
    "username": "your-username",
    "password": "***"
  },
  "verify_ssl": true,
  "timeout": 30
}
```

## Quick Start

### Using Domain Clients (Recommended)

```python
from domains.ProdMgmt import ProdMgmtClient
from domains.DocMgmt import DocMgmtClient
from domains.ChangeMgmt import ChangeMgmtClient

# Initialize clients
part_client = ProdMgmtClient(config_path="config.json")

# Query parts
parts = part_client.get_parts(filter_expr="State/Value eq 'RELEASED'", top=10)
part = part_client.get_part_by_number("PART-001")

# Get BOM
bom = part_client.get_bom(part_id)
where_used = part_client.get_where_used(part_id)

# Multi-level BOM
report = part_client.get_multi_level_components_report(part_id)
```

### Domain Clients

| Domain | Client | Key Methods |
|--------|--------|-------------|
| ProdMgmt | `ProdMgmtClient` | Parts, BOM, check-in/out, revise |
| DocMgmt | `DocMgmtClient` | Documents, folders, attachments |
| ChangeMgmt | `ChangeMgmtClient` | Change notices, requests, tasks |
| SupplierMgmt | `SupplierMgmtClient` | Suppliers, manufacturer parts |
| QMS | `QMSClient` | CAPA, NCR, quality actions |
| RegMstr | `RegMstrClient` | Registrations, compliance |
| UDI | `UDIClient` | UDI records, GUDID submission |
| PrincipalMgmt | `PrincipalMgmtClient` | Users, groups, roles |

## Supported Domains (16 total)

| Domain | Description |
|--------|-------------|
| ProdMgmt | Parts, BOMs, product structures |
| DocMgmt | Documents, attachments |
| CADDocumentMgmt | CAD documents, structures |
| ChangeMgmt | Change notices, requests, tasks |
| SupplierMgmt | Suppliers, sites, contacts |
| MfgProcMgmt | Process plans, operations |
| CEM | Customer Experience Management |
| BACMgmt | Baselines, associations |
| Workflow | Lifecycle templates |
| Audit | Audit records, resolution |
| DataAdmin | Containers, products, sites |
| ServiceInfoMgmt | Service documents, bulletins |
| UDI | Unique Device Identification |
| RegMstr | Regulatory Master |
| QMS | Quality Management System |
| PrincipalMgmt | Users, groups, organizations |

## CLI Usage

Each domain client includes a CLI:

```bash
# ProdMgmt
python scripts/domains/ProdMgmt/client.py --parts
python scripts/domains/ProdMgmt/client.py --part-number PART-001
python scripts/domains/ProdMgmt/client.py --bom PART-ID

# DocMgmt
python scripts/domains/DocMgmt/client.py --documents
python scripts/domains/DocMgmt/client.py --document-number DOC-001

# ChangeMgmt
python scripts/domains/ChangeMgmt/client.py --notices
python scripts/domains/ChangeMgmt/client.py --notice-number CN-001

# QMS
python scripts/domains/QMS/client.py --capas
python scripts/domains/QMS/client.py --open-capas
```

## Examples

### Parts and BOM

```python
from domains.ProdMgmt import ProdMgmtClient

client = ProdMgmtClient(config_path="config.json")

# Get released parts
parts = client.get_parts(filter_expr="State/Value eq 'RELEASED'")

# Get BOM
bom = client.get_bom(part_id)

# Multi-level components report
report = client.get_multi_level_components_report(part_id)

# Lifecycle operations
client.check_out_part(part_id)
client.update_part(part_id, {"Name": "Updated Name"})
client.check_in_part(part_id)
```

### Change Management

```python
from domains.ChangeMgmt import ChangeMgmtClient

client = ChangeMgmtClient(config_path="config.json")

# Get open change notices
notices = client.get_change_notices(filter_expr="State/Value eq 'OPEN'")

# Get affected objects
affected = client.get_change_notice_affected_objects(cn_id)

# Get tasks
tasks = client.get_change_notice_tasks(cn_id)
```

### Quality Management

```python
from domains.QMS import QMSClient

client = QMSClient(config_path="config.json")

# Get open CAPAs
capas = client.get_open_capas()

# Get NCRs
ncrs = client.get_open_ncrs()

# Get quality actions
actions = client.get_quality_actions()
```

## Authentication

### OAuth 2.0 (Recommended)
```json
{
  "auth_type": "oauth",
  "oauth": {
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "token_url": "https://windchill.example.com/Windchill/oauth2/token",
    "scope": "windchill"
  }
}
```

### Basic Authentication
```json
{
  "auth_type": "basic",
  "basic": {
    "username": "your-username",
    "password": "***"
  }
}
```

## Project Structure

```
zephyr/
|-- SKILL.md                  # Skill definition
|-- README.md                  # This file
|-- config.example.json        # Configuration template
|-- references/                # Reference documentation
|   |-- *_REFERENCE.md        # Domain references
|   |-- *_Navigations.md      # Navigation properties
|   +-- entities.json         # Entity metadata
+-- scripts/
    |-- windchill_base.py     # Base OData client
    |-- windchill_odata_client.py  # Comprehensive client
    |-- output_formatter.py   # Output formatting
    |-- old/                  # Deprecated scripts
    |   |-- query_*.py
    |   |-- create_*.py
    |   +-- ...
    +-- domains/              # Domain-specific clients
        |-- ProdMgmt/
        |-- DocMgmt/
        |-- ChangeMgmt/
        +-- ... (16 domains)
```

## Reference Documentation

See the `references/` directory for detailed documentation on each domain:
- Entity definitions and properties
- Navigation properties and relationships
- API metadata (XML/JSON schemas)
- Domain-specific references

## License

MIT License

## Contributing

Contributions welcome! Please read the contributing guidelines first.
