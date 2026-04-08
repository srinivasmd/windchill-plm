---
name: windchill-plm
description: Connect to Windchill PLM REST APIs with OAuth or Basic authentication. Query parts, documents, change requests, suppliers, BOMs, CAD documents, workflows, and more.
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
---

# Windchill PLM REST API Client

This skill provides a Python client for interacting with PTC Windchill PLM REST APIs. Supports both OAuth 2.0 and Basic authentication.

## Quick Start

1. Copy `config.example.json` to `config.json` in the skill directory
2. Configure your Windchill server URL and authentication method
3. Use the `windchill_client.py` script for API interactions

## Configuration

### OAuth 2.0 (Recommended for Production)

```json
{
  "server_url": "https://windchill.example.com/Windchill",
  "odata_base_url": "https://windchill.example.com/Windchill/servlet/odata/",
  "auth_type": "oauth",
  "oauth": {
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "token_url": "https://windchill.example.com/Windchill/oauth2/token",
    "scope": "windchill"
  },
  "verify_ssl": true,
  "timeout": 30
}
```

### Basic Authentication (For Testing/Dev)

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

## Using the Client Script

The main client script provides methods for common Windchill operations:

```bash
python scripts/windchill_client.py <operation> [options]
```

## Query Scripts

### query_parts.py

Query Windchill Parts with filtering options.

```bash
# Get part by number
python scripts/query_parts.py --number TOPLVL

# Get all released parts
python scripts/query_parts.py --state RELEASED --top 10

# Search parts by name
python scripts/query_parts.py --name "Bolt" --output parts.json
```

### query_bom.py

Query Bill of Materials (BOM) for a part.

```bash
# Get BOM for part TOPLVL
python scripts/query_bom.py --url https://windchill.example.com/Windchill/servlet/odata/ --username user --password pass TOPLVL

# Save to file
python scripts/query_bom.py --output bom.json TOPLVL
```

### query_document_attachments.py

Query a Windchill document and its attachments.

```bash
# Get document and attachments
python scripts/query_document_attachments.py --url https://windchill.example.com/Windchill/servlet/odata/ --username user --password pass 0000003822
```

### query_cad_documents.py

Query CAD Documents from Windchill CADDocumentMgmt domain.

```bash
# Get CAD document by number
python scripts/query_cad_documents.py get --number 0000001234

# Get CAD structure
python scripts/query_cad_documents.py structure --id OR:wt.epm.EPMDocument:12345
```

### query_change_mgmt.py

Query Change Management objects from Windchill ChangeMgmt domain.

```bash
# Get Change Notice by number
python scripts/query_change_mgmt.py notice --number CN0001

# Query Change Requests by state
python scripts/query_change_mgmt.py query-requests --filter "State/Value eq 'OPEN'"
```

### query_process_plan.py

Query Process Plan from Windchill MfgProcMgmt domain.

```bash
# Get process plan by number
python scripts/query_process_plan.py --number 0000000041

# Get process plan with operations expanded
python scripts/query_process_plan.py --number 0000000041 --expand "Operations"
```

### query_workflow.py

Query Workflow items from Windchill Workflow domain.

```bash
# Get all work items (top 10)
python scripts/query_workflow.py --top 10

# Get pending work items for a specific user
python scripts/query_workflow.py --filter "Status/Value eq 'PENDING' and Owner/Name eq 'Pat'" --expand Owner,Subject
```

### query_suppliers.py

Query Windchill Suppliers with filtering and expansion options.

```bash
# Get all suppliers (default top 20)
python scripts/query_suppliers.py

# Get top 50 suppliers
python scripts/query_suppliers.py --top 50

# Filter suppliers by name
python scripts/query_suppliers.py --name "Texas"

# Filter using OData expression
python scripts/query_suppliers.py --filter "contains(Name, 'Murata')"

# Expand Organization with pagination
python scripts/query_suppliers.py --expand Organization --top 100

# Filter by supplier type
python scripts/query_suppliers.py --type manufacturer
python scripts/query_suppliers.py --type vendor

# Get all suppliers with pagination
python scripts/query_suppliers.py --all --expand Organization

# Output to JSON file
python scripts/query_suppliers.py --output suppliers.json

# Raw JSON output
python scripts/query_suppliers.py --raw --top 10
```

### query_supplier_detail.py

Get detailed information for a specific supplier by ID or name.

```bash
# Get supplier by ID
python scripts/query_supplier_detail.py --id "OR:com.ptc.windchill.suma.supplier.Manufacturer:3678342"

# Get supplier by name
python scripts/query_supplier_detail.py --name "Texas Instruments"
python scripts/query_supplier_detail.py --name "Murata"

# Expand navigation properties
python scripts/query_supplier_detail.py --name "Panasonic" --expand Organization

# Output to JSON file
python scripts/query_supplier_detail.py --name "Murata" --output supplier.json

# Raw JSON output
python scripts/query_supplier_detail.py --name "Texas" --raw
```

### query_supplier_by_name.py

Query supplier(s) by name with full details (reusable script).

```bash
# Basic search by name
python scripts/query_supplier_by_name.py "Texas Instruments"

# Using --name flag
python scripts/query_supplier_by_name.py --name "Murata" --expand Organization

# Get all matches (not just first)
python scripts/query_supplier_by_name.py --name "Texas" --all-matches

# Query by supplier ID
python scripts/query_supplier_by_name.py --id "OR:com.ptc.windchill.suma.supplier.Manufacturer:3678248"

# Output to JSON file
python scripts/query_supplier_by_name.py --name "Panasonic" --output supplier.json

# Raw JSON output
python scripts/query_supplier_by_name.py --name "Murata" --raw
```

### query_service_info_mgmt.py

Query Service Information Management records.

```bash
# Get all SIMDocuments
python3 scripts/query_service_info_mgmt.py --top 10

# Get Information Structures (Service view)
python3 scripts/query_service_info_mgmt.py --collection InformationStructures --top 20
```

## Write Operations (POST, PATCH, DELETE)

### create_supplier.py

Create a new Supplier in Windchill.

```bash
# Create a new supplier
python scripts/create_supplier.py --name "Texas Instruments" --number "SUP-001"

# Create with description
python scripts/create_supplier.py --name "New Vendor" --number "SUP-002" --description "Electronics vendor"

# Create supplier and save to file
python scripts/create_supplier.py --name "Test Supplier" --number "SUP-003" --output supplier.json

# Create manufacturer or vendor type
python scripts/create_supplier.py --name "Supplier Name" --number "SUP-004" --type manufacturer
python scripts/create_supplier.py --name "Vendor Name" --number "SUP-005" --type vendor
```

### update_supplier.py

Update an existing Supplier in Windchill.

```bash
# Update supplier by ID
python scripts/update_supplier.py --id "OR:com.ptc.windchill.suma.supplier.Manufacturer:3678342" --name "New Name"

# Update supplier by number (auto-lookup)
python scripts/update_supplier.py --number "SUP-001" --description "Updated description"

# Update multiple fields
python scripts/update_supplier.py --id "OR:..." --name "Updated Name" --description "New description"

# Save updated result to file
python scripts/update_supplier.py --number "SUP-001" --name "New Name" --output updated.json
```

### create_part.py

Create a new Part in Windchill.

```bash
# Create a new part
python scripts/create_part.py --name "Resistor 10K" --number "PART-001"

# Create with description
python scripts/create_part.py --name "Capacitor 100uF" --number "PART-002" --description "Electrolytic capacitor"

# Create part and save to file
python scripts/create_part.py --name "PCB Board" --number "PART-003" --output part.json
```

### update_part.py

Update an existing Part in Windchill.

```bash
# Update part by ID
python scripts/update_part.py --id "OR:com.ptc.windchill.suma.part.ManufacturerPart:12345" --name "New Name"

# Update part by number (auto-lookup)
python scripts/update_part.py --number "PART-001" --description "Updated description"

# Update multiple fields
python scripts/update_part.py --id "OR:..." --name "Updated Name" --description "New description"
```

### create_document.py

Create a new Document in Windchill.

```bash
# Create a new document
python scripts/create_document.py --name "Design Specification" --number "DOC-001"

# Create with description
python scripts/create_document.py --name "Test Report" --number "DOC-002" --description "Final test results"

# Create document and save to file
python scripts/create_document.py --name "Drawing" --number "DOC-003" --output document.json
```

### update_document.py

Update an existing Document in Windchill.

```bash
# Update document by ID
python scripts/update_document.py --id "OR:com.ptc.windchill.suma.document.ManufacturerDocument:12345" --name "New Name"

# Update document by number (auto-lookup)
python scripts/update_document.py --number "DOC-001" --description "Updated description"

# Update multiple fields
python scripts/update_document.py --id "OR:..." --name "Updated Name" --description "New description"
```

### create_folder.py

Create a new Folder in Windchill DataAdmin domain.

```bash
# Create a new folder
python scripts/create_folder.py --name "Design Documents" --description "Product design documentation"

# Create subfolder under parent
python scripts/create_folder.py --name "Test Folder" --parent "OR:com.ptc.windchill.suma.folder.Folder:12345"

# Create folder and save to file
python scripts/create_folder.py --name "New Folder" --output folder.json
```

### delete_folder.py

Delete a Folder from Windchill DataAdmin domain.

```bash
# Delete a folder (prompts for confirmation if not empty)
python scripts/delete_folder.py --id "OR:com.ptc.windchill.suma.folder.Folder:12345"

# Force delete without confirmation
python scripts/delete_folder.py --id "OR:..." --force
```

### query_udi.py

Query UDI (Unique Device Identification) records.

```bash
# Get all UDI supersets (top 10)
python3 scripts/query_udi.py --top 10

# Find UDI by device identifier
python3 scripts/query_udi.py --filter "DeviceIdentifier eq '12345678901234'" --expand Subjects,Details
```

### explore_windchill.py

Explore Windchill OData domains and available endpoints.

```bash
# Explore all domains
python scripts/explore_windchill.py explore

# Get metadata for a domain
python scripts/explore_windchill.py metadata --domain ProdMgmt
```

## Generic CRUD Scripts

These unified scripts handle any entity type across all Windchill domains.

### generic_query.py

Query any entity type from any Windchill domain.

```bash
# Query documents
python scripts/generic_query.py --entity Document --top 10

# Query change notices with filter
python scripts/generic_query.py --entity ChangeNotice --filter "State/Display eq 'OPEN'"

# Query by number
python scripts/generic_query.py --entity QualityAction --number "QA-001"

# Query users by name
python scripts/generic_query.py --entity User --name "john"

# Query with expand and select
python scripts/generic_query.py --entity Part --expand Uses --select ID,Name,Number --top 20
```

Supported entities: Document, Part, ChangeNotice, ChangeRequest, ChangeTask, QualityAction, NonConformance, CAPA, User, Group, Organization, Folder, Container, CustomerExperience, and more.

### generic_create.py

Create any entity type that supports CREATE operations.

```bash
# Create a document
python scripts/generic_create.py --entity Document --name "My Document" --number "DOC-001"

# Create a part
python scripts/generic_create.py --entity Part --name "My Part" --number "PART-001"

# Create with container
python scripts/generic_create.py --entity Quality --name "Quality Doc" --number "Q-001" --container "OR:wt.inf.container.WTContainer:12345"

# Create with additional properties (JSON)
python scripts/generic_create.py --entity ChangeNotice --name "CN-001" --number "CN-001" --props '{"ChangeType": "Minor"}'
```

Supported entities for CREATE: Document, ControlledDocument, Quality, Part, Folder, ChangeNotice, ChangeRequest, QualityAction, CAPA, CustomerExperience, and more.

### generic_update.py

Update any entity type that supports UPDATE operations.

```bash
# Update by ID
python scripts/generic_update.py --entity Document --id "OR:com.ptc.DocMgmt.Document:12345" --name "New Name"

# Update by number (auto-lookup)
python scripts/generic_update.py --entity Part --number "PART-001" --description "Updated description"

# Update with additional properties
python scripts/generic_update.py --entity ChangeNotice --id "OR:..." --props '{"Priority": "High"}'
```

### generic_delete.py

Delete any entity type that supports DELETE operations.

```bash
# Delete by ID (prompts for confirmation)
python scripts/generic_delete.py --entity Document --id "OR:com.ptc.DocMgmt.Document:12345"

# Delete by number
python scripts/generic_delete.py --entity Part --number "PART-001"

# Force delete without confirmation
python scripts/generic_delete.py --entity Folder --id "OR:..." --force

# Dry run (show what would be deleted)
python scripts/generic_delete.py --entity Document --number "DOC-001" --dry-run
```

## Entity Types Reference

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

## Telegram Formatted Output

The scripts now support rich Markdown formatting for Telegram gateway responses:

### Output Features
- **Markdown Tables**: Properly aligned columns with headers
- **Entity Emojis**: Document, Part, Supplier, ChangeNotice, etc.
- **State Indicators**: RELEASED, INWORK, REVIEW, REJECTED, CANCELLED
- **Bold Headers**: `*Entity Type*` for clear section separation
- **Code Blocks**: IDs displayed as `inline code`
- **Success/Error Messages**: Visual indicators with emojis

### Usage Example

```bash
# Table view (default)
python scripts/generic_query.py --entity Part --top 5

# Detailed view for single entity
python scripts/generic_query.py --entity Part --number "PART-001" --detail

# Raw JSON output
python scripts/generic_query.py --entity Part --raw
```

### Formatted Output Example

```
*🔧 Part* `3 found`

| Number | Name | State |
|--------|------|-------|
| ENG-001 | Engine Assembly | 🟢 RELEASED |
| PIS-001 | Piston Component | 🔵 INWORK |
| CYL-001 | Cylinder Head | 🟡 REVIEW |

✅ *Created* 🔧 *Part*: `ENG-001`
```

### Using output_formatter.py

```python
from output_formatter import OutputFormatter

formatter = OutputFormatter()

# Print entity table
formatter.print_entity_table(entities, "Part", ["Number", "Name", "State"])

# Print entity detail
formatter.print_entity_detail(entity, "Part")

# Print operation result
formatter.print_operation_result("Created", "Part", "PART-001", True)
```

## Available Operations

**Object Operations:**
- get-object: Retrieve an object by OID or number
- search: Search for objects using query criteria
- create: Create a new Windchill object
- update: Update an existing object's attributes
- delete: Delete a Windchill object

**Part Management:**
- get-bom: Get Bill of Materials for a part
- get-part: Retrieve part details

**Document Management (DocMgmt):**
- get-documents: Query documents with filters
- get-document: Get a specific document by ID
- create-document: Create a new document
- update-document: Update document attributes

**Supplier Management (SupplierMgmt):**
- get-suppliers: Query suppliers with filters
- get-supplier: Get a specific supplier by ID
- create-supplier: Create a new supplier record
- update-supplier: Update supplier attributes
- get-supplier-sites: Get all sites for a supplier
- get-supplier-contacts: Get all contacts for a supplier

**Product Management (ProdMgmt):**
- get-parts: Query parts with filters
- get-part: Get a specific part by ID or number
- create-part: Create a new part
- update-part: Update part attributes

## Reference Documentation

See the `references/` directory for detailed documentation on each domain:

- **ProdMgmt**: Parts, BOMs, product structures
- **DocMgmt**: Documents, attachments
- **CADDocumentMgmt**: CAD documents, structures
- **ChangeMgmt**: Change notices, requests, tasks
- **SupplierMgmt**: Suppliers, sites, contacts
- **MfgProcMgmt**: Process plans, operations
- **Workflow**: Work items, activities
- **QMS**: Quality actions, non-conformances, CAPA
- **RegMstr**: Regulations, requirements, compliance
- **DataAdmin**: Containers, folders
- **PrincipalMgmt**: Users, groups, organizations
