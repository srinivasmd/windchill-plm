# Supplier Management Domain (SupplierMgmt) Reference

Complete reference for the Windchill PLM Supplier Management OData domain.

## Base URL

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/SupplierMgmt/
```

## Entity Overview

| Entity Set | Entity Type | Description | Primary Key |
|------------|-------------|-------------|-------------|
| Suppliers | Supplier | Supplier records with company information | ID |
| Organizations | Organization | Organization entities | ID |
| SupplierSites | SupplierSite | Physical locations/facilities for suppliers | ID |
| SupplierContacts | SupplierContact | Contact persons associated with suppliers | ID |
| SupplierProducts | SupplierProduct | Products/parts supplied by suppliers | ID |
| SupplierContracts | SupplierContract | Contracts and agreements with suppliers | ID |
| SupplierQualifications | SupplierQualification | Supplier qualification and certification records | ID |
| SupplierEvaluations | SupplierEvaluation | Supplier performance evaluations | ID |

---

## Suppliers Entity

### Properties

| Property | Type | Description | Read-Only |
|----------|------|-------------|-----------|
| ID | String | Unique identifier (OID) | Yes |
| Number | String | Supplier number/code | No |
| Name | String | Supplier/company name | No |
| OrganizationName | String | Organization name | No |
| Description | String | Description of the supplier | No |
| State | Object | Lifecycle state (Value/Display) | No |
| Address | String | Street address | No |
| Address2 | String | Additional address line | No |
| City | String | City | No |
| StateProvince | String | State or province | No |
| Country | String | Country | No |
| PostalCode | String | Postal/ZIP code | No |
| Phone | String | Phone number | No |
| Phone2 | String | Alternate phone number | No |
| Email | String | Email address | No |
| Website | String | Company website | No |
| TaxID | String | Tax identification number | No |
| DUNSNumber | String | D-U-N-S number | No |
| Rating | String | Supplier rating | No |
| Classification | Object | Supplier classification attributes | No |
| CabinetName | String | Cabinet name | Yes |
| FolderLocation | String | Folder path | Yes |
| CreatedBy | String | User who created the record | Yes |
| CreatedOn | DateTime | Creation timestamp | Yes |
| ModifiedBy | String | User who last modified | Yes |
| LastModified | DateTime | Last modification timestamp | Yes |
| Identity | String | Display identity string | Yes |
| Latest | Boolean | Is this the latest version | Yes |
| Version | String | Version identifier | Yes |
| VersionID | String | Version ID (VR:...) | Yes |

### Navigation Properties

| Property | Target Type | Description |
|----------|-------------|-------------|
| SupplierSites | SupplierSite | Collection of supplier sites |
| SupplierContacts | SupplierContact | Collection of supplier contacts |
| SupplierProducts | SupplierProduct | Products supplied by this supplier |
| SupplierContracts | SupplierContract | Contracts with this supplier |

### CRUD Operations

#### GET /Suppliers
Retrieve all suppliers or with filters.

```http
GET /SupplierMgmt/Suppliers
GET /SupplierMgmt/Suppliers?$filter=Name eq 'Acme Corp'
GET /SupplierMgmt/Suppliers?$select=Number,Name,State,Country
GET /SupplierMgmt/Suppliers?$orderby=Name asc
GET /SupplierMgmt/Suppliers?$top=50&$skip=0
```

#### GET /Suppliers('{id}')
Retrieve a specific supplier by ID.

```http
GET /SupplierMgmt/Suppliers('OR:wt.supplier.WTSupplier:12345')
```

#### POST /Suppliers
Create a new supplier.

```http
POST /SupplierMgmt/Suppliers
Content-Type: application/json

{
  "Name": "New Supplier Inc.",
  "OrganizationName": "New Supplier Inc.",
  "Number": "SUP-001",
  "Address": "123 Supplier St",
  "City": "Supplier City",
  "StateProvince": "CA",
  "Country": "United States",
  "PostalCode": "12345",
  "Phone": "+1-555-123-4567",
  "Email": "contact@newsupplier.com",
  "Website": "https://www.newsupplier.com"
}
```

#### PATCH /Suppliers('{id}')
Update an existing supplier.

```http
PATCH /SupplierMgmt/Suppliers('OR:wt.supplier.WTSupplier:12345')
Content-Type: application/json

{
  "Address": "456 New Address Ave",
  "Phone": "+1-555-987-6543",
  "Email": "newemail@supplier.com"
}
```

#### DELETE /Suppliers('{id}')
Delete a supplier.

```http
DELETE /SupplierMgmt/Suppliers('OR:wt.supplier.WTSupplier:12345')
```

---

## SupplierSites Entity

### Properties

| Property | Type | Description | Read-Only |
|----------|------|-------------|-----------|
| ID | String | Unique identifier (OID) | Yes |
| Name | String | Site name | No |
| Number | String | Site number/code | No |
| SupplierID | String | Parent supplier ID (OID) | No |
| SupplierName | String | Parent supplier name | Yes |
| Address | String | Street address | No |
| Address2 | String | Additional address line | No |
| City | String | City | No |
| StateProvince | String | State or province | No |
| Country | String | Country | No |
| PostalCode | String | Postal/ZIP code | No |
| Phone | String | Phone number | No |
| Email | String | Email address | No |
| SiteType | String | Type of site (e.g., Manufacturing, Warehouse) | No |
| IsPrimary | Boolean | Is this the primary site | No |
| IsActive | Boolean | Is the site active | No |
| CreatedBy | String | User who created the record | Yes |
| CreatedOn | DateTime | Creation timestamp | Yes |
| ModifiedBy | String | User who last modified | Yes |
| LastModified | DateTime | Last modification timestamp | Yes |

### CRUD Operations

#### GET /SupplierSites
Retrieve all supplier sites.

```http
GET /SupplierMgmt/SupplierSites
GET /SupplierMgmt/SupplierSites?$filter=SupplierID eq 'OR:wt.supplier.WTSupplier:12345'
GET /SupplierMgmt/SupplierSites?$filter=Country eq 'United States'
```

#### POST /SupplierSites
Create a new supplier site.

```http
POST /SupplierMgmt/SupplierSites
Content-Type: application/json

{
  "Name": "Main Distribution Center",
  "SupplierID": "OR:wt.supplier.WTSupplier:12345",
  "Address": "789 Site Road",
  "City": "Site City",
  "StateProvince": "TX",
  "Country": "United States",
  "PostalCode": "54321",
  "Phone": "+1-555-555-5555",
  "SiteType": "Warehouse",
  "IsPrimary": true,
  "IsActive": true
}
```

---

## SupplierContacts Entity

### Properties

| Property | Type | Description | Read-Only |
|----------|------|-------------|-----------|
| ID | String | Unique identifier (OID) | Yes |
| FirstName | String | First name | No |
| LastName | String | Last name | No |
| FullName | String | Full name (computed) | Yes |
| SupplierID | String | Parent supplier ID (OID) | No |
| SupplierName | String | Parent supplier name | Yes |
| Email | String | Email address | No |
| Phone | String | Phone number | No |
| Mobile | String | Mobile phone number | No |
| Title | String | Job title | No |
| Role | String | Role/position (e.g., Purchasing Manager) | No |
| Department | String | Department | No |
| IsPrimary | Boolean | Is this the primary contact | No |
| IsActive | Boolean | Is the contact active | No |
| Address | String | Contact address | No |
| City | String | City | No |
| StateProvince | String | State or province | No |
| Country | String | Country | No |
| PostalCode | String | Postal/ZIP code | No |
| CreatedBy | String | User who created the record | Yes |
| CreatedOn | DateTime | Creation timestamp | Yes |
| ModifiedBy | String | User who last modified | Yes |
| LastModified | DateTime | Last modification timestamp | Yes |

### CRUD Operations

#### GET /SupplierContacts
Retrieve all supplier contacts.

```http
GET /SupplierMgmt/SupplierContacts
GET /SupplierMgmt/SupplierContacts?$filter=SupplierID eq 'OR:wt.supplier.WTSupplier:12345'
GET /SupplierMgmt/SupplierContacts?$filter=Role eq 'Purchasing Manager'
```

#### POST /SupplierContacts
Create a new supplier contact.

```http
POST /SupplierMgmt/SupplierContacts
Content-Type: application/json

{
  "FirstName": "John",
  "LastName": "Doe",
  "SupplierID": "OR:wt.supplier.WTSupplier:12345",
  "Email": "john.doe@supplier.com",
  "Phone": "+1-555-111-2222",
  "Mobile": "+1-555-333-4444",
  "Title": "Mr.",
  "Role": "Purchasing Manager",
  "Department": "Procurement",
  "IsPrimary": true,
  "IsActive": true
}
```

---

## Organizations Entity

### Properties

| Property | Type | Description | Read-Only |
|----------|------|-------------|-----------|
| ID | String | Unique identifier (OID) | Yes |
| Name | String | Organization name | No |
| Number | String | Organization number/code | No |
| Type | String | Organization type (e.g., Supplier, Customer, Partner) | No |
| Description | String | Description | No |
| Address | String | Street address | No |
| City | String | City | No |
| StateProvince | String | State or province | No |
| Country | String | Country | No |
| PostalCode | String | Postal/ZIP code | No |
| Phone | String | Phone number | No |
| Email | String | Email address | No |
| Website | String | Company website | No |
| TaxID | String | Tax identification number | No |
| DUNSNumber | String | D-U-N-S number | No |
| CreatedBy | String | User who created the record | Yes |
| CreatedOn | DateTime | Creation timestamp | Yes |
| ModifiedBy | String | User who last modified | Yes |
| LastModified | DateTime | Last modification timestamp | Yes |

### CRUD Operations

#### GET /Organizations
Retrieve all organizations or filter by type.

```http
GET /SupplierMgmt/Organizations
GET /SupplierMgmt/Organizations?$filter=Type eq 'Supplier'
GET /SupplierMgmt/Organizations?$filter=contains(Name, 'Acme')
```

---

## Common Query Options

### $filter
Filter results based on property values.

```http
?filter=Name eq 'Acme Corp'
?filter=contains(Name, 'Acme')
?filter=Country eq 'United States' and State eq 'Active'
?filter=CreatedOn ge '2024-01-01'
```

### $select
Select specific properties to return.

```http
?$select=Number,Name,State,Country,Email
```

### $expand
Expand related entities.

```http
?$expand=SupplierSites
?$expand=SupplierContacts
?$expand=SupplierSites,SupplierContacts
```

### $orderby
Sort results.

```http
?$orderby=Name asc
?$orderby=CreatedOn desc
```

### $top and $skip
Pagination.

```http
?$top=50&$skip=0
```

---

## Error Responses

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (authentication failed) |
| 403 | Forbidden (permission denied) |
| 404 | Not Found |
| 500 | Internal Server Error |

### Error Response Format

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": [
      {
        "code": "string",
        "message": "string"
      }
    ]
  }
}
```

---

## Lifecycle States

Common supplier lifecycle states:

| State | Description |
|-------|-------------|
| InWork | In progress/under review |
| Released | Active and approved |
| Obsolete | No longer in use |
| Canceled | Cancelled |

---

## Quick Reference Examples

### Get All Active Suppliers
```http
GET /SupplierMgmt/Suppliers?$filter=State/Value eq 'RELEASED'
```

### Get Suppliers by Country
```http
GET /SupplierMgmt/Suppliers?$filter=Country eq 'United States'&$orderby=Name
```

### Get Supplier with Sites and Contacts
```http
GET /SupplierMgmt/Suppliers('OR:wt.supplier.WTSupplier:12345')?$expand=SupplierSites,SupplierContacts
```

### Search Suppliers by Name
```http
GET /SupplierMgmt/Suppliers?$filter=contains(Name, 'Acme')
```

### Get Primary Contacts for All Suppliers
```http
GET /SupplierMgmt/SupplierContacts?$filter=IsPrimary eq true
```

### Get Manufacturing Sites
```http
GET /SupplierMgmt/SupplierSites?$filter=SiteType eq 'Manufacturing'
```