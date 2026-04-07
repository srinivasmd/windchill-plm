# Windchill PLM REST API Client

A comprehensive Python client for interacting with PTC Windchill PLM REST APIs. Supports OAuth 2.0 and Basic authentication.

## Features

- **Complete CRUD Operations**: Create, Read, Update, Delete for all Windchill entities
- **Generic Scripts**: Unified scripts that work with ANY entity type
- **Domain Coverage**: DocMgmt, ProdMgmt, ChangeMgmt, QMS, DataAdmin, PrincipalMgmt, CEM, and more
- **BOM Management**: Query and explore Bill of Materials
- **Supplier Management**: Query suppliers, contacts, and sites
- **Quality Management**: Quality actions, CAPA, non-conformances
- **Change Management**: Change notices, requests, and tasks

## Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/windchill-plm.git
cd windchill-plm
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
    "password": "your-password"
  },
  "verify_ssl": true,
  "timeout": 30
}
```

## Quick Start

### Query Parts
```bash
python scripts/query_parts.py --number "PART-001"
python scripts/query_parts.py --state RELEASED --top 10
```

### Query Documents
```bash
python scripts/query_documents.py --number "DOC-001"
python scripts/query_documents.py --name "Specification"
```

### Query BOM
```bash
python scripts/query_bom.py "PART-001"
```

### Generic Query (Any Entity)
```bash
python scripts/generic_query.py --entity ChangeNotice --top 10
python scripts/generic_query.py --entity QualityAction --number "QA-001"
python scripts/generic_query.py --entity User --name "john"
```

### Create Entities
```bash
# Using generic create
python scripts/generic_create.py --entity Document --name "My Doc" --number "DOC-001"

# Entity-specific create
python scripts/create_part.py --name "New Part" --number "PART-001"
python scripts/create_supplier.py --name "Supplier Inc" --number "SUP-001"
```

### Update Entities
```bash
python scripts/generic_update.py --entity Part --number "PART-001" --description "Updated"
python scripts/update_document.py --number "DOC-001" --name "New Name"
```

### Delete Entities
```bash
python scripts/generic_delete.py --entity Document --number "DOC-001" --force
```

## Supported Entity Types

| Domain | Entities |
|--------|----------|
| DocMgmt | Document, ControlledDocument, Quality, Record, TestDocument, ReferenceDocument, SoftwareDocument |
| ProdMgmt | Part, PartUse, PartSubstituteLink |
| DataAdmin | Folder, Container, ProductContainer, LibraryContainer |
| ChangeMgmt | ChangeNotice, ChangeRequest, ChangeTask, ChangeOrder |
| QMS | QualityAction, QualityObject, NonConformance, CAPA, Place, QualityContact, Subject |
| CEM | CustomerExperience, RelatedProduct |
| PrincipalMgmt | User, Group, Organization |
| CADDocumentMgmt | CADDocument, EPMDocument |
| MfgProcMgmt | ProcessPlan, Operation |
| ServiceInfoMgmt | SIMDocument, InformationStructure |

## Scripts Reference

### Query Scripts (GET)
- `query_parts.py` - Query parts with filters
- `query_documents.py` - Query documents
- `query_suppliers.py` - Query suppliers
- `query_bom.py` - Query Bill of Materials
- `query_change_mgmt.py` - Query change notices, requests, tasks
- `query_workflow.py` - Query workflow items
- `query_cem.py` - Query customer experiences
- `query_udi.py` - Query UDI records
- `generic_query.py` - Query ANY entity type

### Create Scripts (POST)
- `create_part.py` - Create parts
- `create_document.py` - Create documents
- `create_supplier.py` - Create suppliers
- `create_folder.py` - Create folders
- `generic_create.py` - Create ANY entity type

### Update Scripts (PATCH)
- `update_part.py` - Update parts
- `update_document.py` - Update documents
- `update_supplier.py` - Update suppliers
- `generic_update.py` - Update ANY entity type

### Delete Scripts (DELETE)
- `delete_folder.py` - Delete folders
- `generic_delete.py` - Delete ANY entity type

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
    "password": "your-password"
  }
}
```

## Reference Documentation

See the `references/` directory for detailed documentation:
- Entity definitions and properties
- Navigation properties and relationships
- API metadata (XML/JSON schemas)
- Domain-specific references

## License

MIT License

## Contributing

Contributions welcome! Please read the contributing guidelines first.
