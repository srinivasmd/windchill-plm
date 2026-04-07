# Windchill PLM REST API Reference

## Base URL

All API requests are made to the Windchill server base URL configured in `config.json`:
```
https://windchill.example.com/Windchill
```

## OData Domains

### Document Management Domain (DocMgmt)
```
https://windchill.example.com/Windchill/servlet/odata/DocMgmt/
```

### Supplier Management Domain (SupplierMgmt)
```
https://windchill.example.com/Windchill/servlet/odata/SupplierMgmt/
```

### Product Management Domain (ProdMgmt)
```
https://windchill.example.com/Windchill/servlet/odata/ProdMgmt/
```

## Authentication

### OAuth 2.0 Authorization Header
```
Authorization: Bearer <access_token>
```

### Basic Authentication
Uses standard HTTP Basic Auth header (handled automatically by client).

## Common Endpoints

### Objects API

#### Get Object by OID
```
GET /api/v3/objects/{oid}
```

#### Get Object by Type and Number
```
GET /api/v3/objects/{type}/{number}
```

Types:
- `WTPart` - Parts
- `WTDocument` - Documents
- `EPMDocument` - CAD documents
- `ChangeRequest2` - Change requests
- `PromotionNotice` - Promotion notices

#### Search Objects
```
GET /api/v3/objects/{type}/search?type={type}&name={name}
```

#### Create Object
```
POST /api/v3/objects/{type}
Content-Type: application/json

{
  "name": "Object Name",
  "displayIdentifier": "PART-001",
  ...
}
```

#### Update Object
```
PATCH /api/v3/objects/{oid}
Content-Type: application/json

{
  "name": "Updated Name",
  ...
}
```

### Parts API

#### Get Bill of Materials
```
GET /api/v3/parts/{oid}/bom
```

#### Get Part Structure
```
GET /api/v3/parts/{oid}/structure
```

### Documents API

#### Get Document Content
```
GET /api/v3/documents/{oid}/content
```

#### Upload Document
```
POST /api/v3/documents/{oid}/content
Content-Type: multipart/form-data
```

### Supplier Management API (SupplierMgmt)

#### Get All Suppliers
```
GET /odata/SupplierMgmt/Suppliers
```

#### Get Supplier by ID
```
GET /odata/SupplierMgmt/Suppliers('{oid}')
```

#### Create Supplier
```
POST /odata/SupplierMgmt/Suppliers
Content-Type: application/json

{
  "Name": "Supplier Name",
  "Number": "SUP-001",
  "Country": "United States",
  "Email": "contact@supplier.com"
}
```

#### Update Supplier
```
PATCH /odata/SupplierMgmt/Suppliers('{oid}')
Content-Type: application/json

{
  "Address": "New Address",
  "Phone": "+1-555-123-4567"
}
```

#### Delete Supplier
```
DELETE /odata/SupplierMgmt/Suppliers('{oid}')
```

#### Get Supplier Sites
```
GET /odata/SupplierMgmt/SupplierSites
GET /odata/SupplierMgmt/Suppliers('{oid}')/SupplierSites
```

#### Create Supplier Site
```
POST /odata/SupplierMgmt/SupplierSites
Content-Type: application/json

{
  "Name": "Site Name",
  "SupplierID": "OR:wt.supplier.WTSupplier:12345",
  "Address": "123 Site Road",
  "City": "City",
  "Country": "United States"
}
```

#### Get Supplier Contacts
```
GET /odata/SupplierMgmt/SupplierContacts
GET /odata/SupplierMgmt/Suppliers('{oid}')/SupplierContacts
```

#### Create Supplier Contact
```
POST /odata/SupplierMgmt/SupplierContacts
Content-Type: application/json

{
  "FirstName": "John",
  "LastName": "Doe",
  "SupplierID": "OR:wt.supplier.WTSupplier:12345",
  "Email": "john.doe@supplier.com",
  "Role": "Purchasing Manager"
}
```

#### Get Organizations
```
GET /odata/SupplierMgmt/Organizations
GET /odata/SupplierMgmt/Organizations?$filter=Type eq 'Supplier'
```

### Product Management API (ProdMgmt)

#### Get All Parts
```
GET /odata/ProdMgmt/Parts
```

#### Get Part by ID
```
GET /odata/ProdMgmt/Parts('{oid}')
```

#### Get Part by Number
```
GET /odata/ProdMgmt/Parts?$filter=Number eq 'PART-001'
```

#### Create Part
```
POST /odata/ProdMgmt/Parts
Content-Type: application/json

{
  "Name": "Part Name",
  "Number": "PART-001",
  "Description": "Part description",
  "DefaultUnit": "ea",
  "View": "Design",
  "Source": "Buy",
  "ContainerID": "OR:wt.pdmlink.PDMLinkProduct:12345"
}
```

#### Update Part
```
PATCH /odata/ProdMgmt/Parts('{oid}')
Content-Type: application/json

{
  "Description": "Updated description",
  "Source": "Make"
}
```

#### Delete Part
```
DELETE /odata/ProdMgmt/Parts('{oid}')
```

#### Get BOM for Part
```
GET /odata/ProdMgmt/Parts('{oid}')/PartUsages
GET /odata/ProdMgmt/Parts('{oid}')/PartUsages?$expand=Child
```

#### Get All Part Usages
```
GET /odata/ProdMgmt/PartUsages
```

#### Get Part Usage by ID
```
GET /odata/ProdMgmt/PartUsages('{oid}')
```

#### Add to BOM (Create Part Usage)
```
POST /odata/ProdMgmt/PartUsages
Content-Type: application/json

{
  "ParentID": "OR:wt.part.WTPart:12345",
  "ChildID": "OR:wt.part.WTPart:67890",
  "Quantity": 4,
  "Unit": "ea",
  "FindNumber": "10",
  "LineNumber": "1"
}
```

#### Update BOM Item
```
PATCH /odata/ProdMgmt/PartUsages('{oid}')
Content-Type: application/json

{
  "Quantity": 8,
  "FindNumber": "20"
}
```

#### Remove from BOM
```
DELETE /odata/ProdMgmt/PartUsages('{oid}')
```

#### Get Part Master
```
GET /odata/ProdMgmt/PartMasters('{oid}')
```

#### Get All Versions of a Part
```
GET /odata/ProdMgmt/PartMasters('{master_oid}')/Parts
```

#### Get Organizations
```
GET /odata/ProdMgmt/Organizations
GET /odata/ProdMgmt/Organizations?$filter=Type eq 'Supplier'
```

#### Create Organization
```
POST /odata/ProdMgmt/Organizations
Content-Type: application/json

{
  "Name": "Organization Name",
  "Number": "ORG-001",
  "Type": "Supplier",
  "Address": "123 Main St",
  "City": "City",
  "Country": "United States",
  "PostalCode": "12345"
}
```

## Object Identifiers

Windchill objects can be identified by:
- **OID**: Internal object ID (e.g., `OR:wt.part.WTPart:12345`)
- **Number**: User-facing identifier (e.g., `PART-001`)
- **Name**: Display name

## Common Object Types

| Type | Description | Example OID Format |
|------|-------------|-------------------|
| WTPart | Part | OR:wt.part.WTPart:12345 |
| WTDocument | Document | OR:wt.doc.WTDocument:67890 |
| EPMDocument | CAD Document | OR:wt.epm.EPMDocument:54321 |
| WTPartUsageLink | BOM Link | OR:wt.part.WTPartUsageLink:11111 |
| ChangeRequest2 | Change Request | OR:wt.change2.ChangeRequest2:22222 |
| PromotionNotice | Promotion | OR:wt.maturity.PromotionNotice:33333 |
| WTChangeActivity2 | Change Activity | OR:wt.change2.WTChangeActivity2:44444 |
| WTSupplier | Supplier | OR:wt.supplier.WTSupplier:55555 |
| SupplierSite | Supplier Site | OR:wt.supplier.SupplierSite:66666 |
| SupplierContact | Supplier Contact | OR:wt.supplier.SupplierContact:77777 |
| WTPart | Part | OR:wt.part.WTPart:88888 |
| WTPartUsageLink | BOM Link | OR:wt.part.WTPartUsageLink:99999 |
| WTPartMaster | Part Master | OR:wt.part.WTPartMaster:11111 |
| WTProduct | Product | OR:wt.pdmlink.PDMLinkProduct:22222 |
| WTOrganization | Organization | OR:wt.org.WTOrganization:33333 |

## Common Attributes

### WTPart Attributes
- `name` - Part name
- `displayIdentifier` - Part number
- `defaultUnit` - Unit of measure
- `view` - View (e.g., Design, Manufacturing)
- `versionInfo` - Version info
- `iterationInfo` - Iteration info
- `state` - Lifecycle state

### WTDocument Attributes
- `name` - Document name
- `displayIdentifier` - Document number
- `documentType` - Document type
- `description` - Description
- `versionInfo` - Version info
- `iterationInfo` - Iteration info
- `state` - Lifecycle state

### WTSupplier Attributes
- `name` - Supplier name
- `number` - Supplier number
- `organizationName` - Organization name
- `description` - Description
- `address` - Street address
- `city` - City
- `stateProvince` - State or province
- `country` - Country
- `postalCode` - Postal/ZIP code
- `phone` - Phone number
- `email` - Email address
- `website` - Company website
- `taxID` - Tax identification number
- `dunsNumber` - D-U-N-S number
- `rating` - Supplier rating
- `state` - Lifecycle state

### SupplierSite Attributes
- `name` - Site name
- `number` - Site number
- `supplierID` - Parent supplier OID
- `address` - Street address
- `city` - City
- `stateProvince` - State or province
- `country` - Country
- `postalCode` - Postal/ZIP code
- `phone` - Phone number
- `siteType` - Site type (Manufacturing, Warehouse, etc.)
- `isPrimary` - Is primary site
- `isActive` - Is site active

### SupplierContact Attributes
- `firstName` - First name
- `lastName` - Last name
- `fullName` - Full name
- `supplierID` - Parent supplier OID
- `email` - Email address
- `phone` - Phone number
- `mobile` - Mobile phone
- `title` - Job title
- `role` - Role/position
- `department` - Department
- `isPrimary` - Is primary contact
- `isActive` - Is contact active

### WTPart Attributes
- `name` - Part name
- `number` - Part number
- `version` - Version (e.g., "1.2")
- `revision` - Revision (e.g., "A")
- `state` - Lifecycle state
- `defaultUnit` - Unit of measure (ea, kg, m, etc.)
- `view` - View (Design, Manufacturing, Service, etc.)
- `source` - Source (Buy, Make, MakeBuy)
- `containerName` - Container name
- `containerID` - Container ID
- `organizationName` - Organization name
- `description` - Description
- `keywords` - Keywords
- `folderLocation` - Folder location
- `folderName` - Folder name
- `checkoutState` - Check out state
- `checkOutStatus` - Check out status
- `latest` - Is latest version
- `lifeCycleTemplateName` - Lifecycle template name
- `masterID` - Master ID
- `versionID` - Version ID
- `createdBy` - User who created the record
- `createdOn` - Creation timestamp
- `modifiedBy` - User who last modified
- `lastModified` - Last modification timestamp
- `classification` - Classification attributes

### WTPartUsageLink Attributes
- `parentID` - Parent part OID
- `childID` - Child part OID
- `quantity` - Usage quantity
- `unit` - Unit of measure
- `findNumber` - Find number
- `lineNumber` - Line number
- `referenceDesignator` - Reference designator
- `usageType` - Usage type
- `occurrenceType` - Occurrence type
- `isDefault` - Is default usage
- `isLatest` - Is latest version
- `state` - Lifecycle state
- `version` - Version
- `revision` - Revision

### WTPartMaster Attributes
- `number` - Part number
- `name` - Part name
- `type` - Part type
- `defaultUnit` - Default unit of measure
- `view` - Default view
- `versionInfo` - Version info
- `iterationInfo` - Iteration info
- `createdBy` - User who created the record
- `createdOn` - Creation timestamp
- `modifiedBy` - User who last modified
- `lastModified` - Last modification timestamp

### WTOrganization Attributes
- `name` - Organization name
- `number` - Organization number
- `type` - Organization type (Supplier, Customer, etc.)
- `address` - Street address
- `city` - City
- `stateProvince` - State or province
- `country` - Country
- `postalCode` - Postal/ZIP code
- `phone` - Phone number
- `email` - Email address
- `website` - Company website
- `description` - Description
- `state` - Lifecycle state
- `createdBy` - User who created the record
- `createdOn` - Creation timestamp
- `modifiedBy` - User who last modified
- `lastModified` - Last modification timestamp

## Response Format

All responses return JSON:

```json
{
  "oid": "OR:wt.part.WTPart:12345",
  "name": "My Part",
  "displayIdentifier": "PART-001",
  "type": "WTPart",
  "state": "APPROVED",
  ...
}
```

Search responses include a `items` array:

```json
{
  "items": [
    {
      "oid": "OR:wt.part.WTPart:12345",
      "name": "Part 1",
      "displayIdentifier": "PART-001"
    },
    {
      "oid": "OR:wt.part.WTPart:67890",
      "name": "Part 2",
      "displayIdentifier": "PART-002"
    }
  ],
  "total": 2
}
```

## Error Responses

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Authentication failed |
| 403 | Forbidden - No permission |
| 404 | Not Found - Object doesn't exist |
| 500 | Server Error |

## Pagination

Search results support pagination:
```
GET /api/v3/objects/WTPart/search?page=1&size=50
```