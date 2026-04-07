# Product Management Domain - Complete Reference

## Base URL
```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/ProdMgmt/
```

## Entity Sets
- **Parts** - Part objects (WTPart)
- **PartUsages** - Part usage links (BOM relationships)
- **PartMasters** - Part master records
- **BOMs** - Bill of Materials structures
- **Organizations** - Organization entities
- **Products** - Product containers
- **Containers** - Container objects

---

## Part Entity (WTPart)

### Operations
- **READ, CREATE, UPDATE, DELETE** - Full CRUD support
- **Notifiable, Workable** - Supports notifications and workflow

### Part Types

| Entity | Operations | Capabilities |
|--------|------------|--------------|
| WTPart | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| Part | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| ElectricalPart | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| MechanicalPart | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| SoftwarePart | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| DocumentPart | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| Fastener | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| StandardPart | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| PurchasedPart | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| ManufacturedPart | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |

---

## Part Properties (WTPart)

| Property | Type | Description |
|----------|------|-------------|
| ID | String | Unique OID identifier |
| Name | String | Part name |
| Number | String | Part number |
| Version | String | Version (e.g., "1.2") |
| Revision | String | Revision (e.g., "A") |
| State | EnumType | Lifecycle state |
| DisplayValue | String | Display value |
| FolderLocation | String | Folder location |
| FolderName | String | Folder name |
| CabinetName | String | Cabinet name |
| CheckoutState | String | Check out state |
| CheckOutStatus | String | Check out status |
| Latest | Boolean | Is latest version |
| LifeCycleTemplateName | String | Lifecycle template name |
| MasterID | String | Master ID |
| VersionID | String | Version ID |
| DefaultUnit | String | Default unit of measure |
| View | String | View (Design, Manufacturing, etc.) |
| Source | String | Source (Buy, Make, etc.) |
| OrganizationName | String | Organization name |
| ContainerName | String | Container name |
| ContainerID | String | Container ID |
| CreatedBy | String | Created by user |
| CreatedOn | DateTimeOffset | Creation timestamp |
| ModifiedBy | String | Modified by user |
| LastModified | DateTimeOffset | Last modification timestamp |
| Description | String | Description |
| Keywords | String | Keywords |
| Classification | ClassificationInfo | Classification info |
| Identity | String | Identity |
| ObjectType | String | Object type |
| DocTypeName | String | Document type name |
| GeneralStatus | Icon | General status |
| ChangeStatus | Icon | Change status |
| ShareStatus | Icon | Share status |
| WorkInProgressState | WorkInProgressType | Work in progress state |
| TypeIcon | Icon | Type icon |

---

## Part Usage Link (WTPartUsageLink)

### Operations
- **READ, CREATE, UPDATE, DELETE** - Full CRUD support

### Properties

| Property | Type | Description |
|----------|------|-------------|
| ID | String | Unique OID identifier |
| ParentID | String | Parent part ID |
| ChildID | String | Child part ID |
| Quantity | Decimal | Usage quantity |
| Unit | String | Unit of measure |
| FindNumber | String | Find number |
| LineNumber | String | Line number |
| ReferenceDesignator | String | Reference designator |
| Position | String | Position |
| UsageType | String | Usage type |
| OccurrenceType | String | Occurrence type |
| IsDefault | Boolean | Is default usage |
| IsLatest | Boolean | Is latest version |
| State | EnumType | Lifecycle state |
| Version | String | Version |
| Revision | String | Revision |
| CreatedBy | String | Created by user |
| CreatedOn | DateTimeOffset | Creation timestamp |
| ModifiedBy | String | Modified by user |
| LastModified | DateTimeOffset | Last modification timestamp |

---

## Part Master (WTPartMaster)

### Operations
- **READ, UPDATE** - Read and update only

### Properties

| Property | Type | Description |
|----------|------|-------------|
| ID | String | Unique OID identifier |
| Number | String | Part number |
| Name | String | Part name |
| Type | String | Part type |
| DefaultUnit | String | Default unit of measure |
| View | String | Default view |
| VersionInfo | String | Version info |
| IterationInfo | String | Iteration info |
| CreatedBy | String | Created by user |
| CreatedOn | DateTimeOffset | Creation timestamp |
| ModifiedBy | String | Modified by user |
| LastModified | DateTimeOffset | Last modification timestamp |

---

## Bill of Materials (BOM)

### Operations
- **READ** - Read only (BOM is derived from PartUsages)

### BOM Properties

| Property | Type | Description |
|----------|------|-------------|
| RootPartID | String | Root part ID |
| Level | Integer | BOM level |
| Quantity | Decimal | Total quantity |
| Unit | String | Unit of measure |
| FindNumber | String | Find number |
| LineNumber | String | Line number |
| IsPhantom | Boolean | Is phantom part |
| IsOption | Boolean | Is option part |
| EffectiveDate | Date | Effective date |
| ExpirationDate | Date | Expiration date |

---

## Organization Entity

### Operations
- **READ, CREATE, UPDATE, DELETE** - Full CRUD support

### Properties

| Property | Type | Description |
|----------|------|-------------|
| ID | String | Unique OID identifier |
| Name | String | Organization name |
| Number | String | Organization number |
| Type | String | Organization type (Supplier, Customer, etc.) |
| Address | String | Street address |
| City | String | City |
| StateProvince | String | State or province |
| Country | String | Country |
| PostalCode | String | Postal/ZIP code |
| Phone | String | Phone number |
| Email | String | Email address |
| Website | String | Company website |
| Description | String | Description |
| State | EnumType | Lifecycle state |
| CreatedBy | String | Created by user |
| CreatedOn | DateTimeOffset | Creation timestamp |
| ModifiedBy | String | Modified by user |
| LastModified | DateTimeOffset | Last modification timestamp |

---

## Product Entity

### Operations
- **READ, CREATE, UPDATE, DELETE** - Full CRUD support

### Properties

| Property | Type | Description |
|----------|------|-------------|
| ID | String | Unique OID identifier |
| Name | String | Product name |
| Number | String | Product number |
| Type | String | Product type |
| State | EnumType | Lifecycle state |
| Description | String | Description |
| ContainerType | String | Container type |
| RootFolder | String | Root folder |
| CreatedBy | String | Created by user |
| CreatedOn | DateTimeOffset | Creation timestamp |
| ModifiedBy | String | Modified by user |
| LastModified | DateTimeOffset | Last modification timestamp |

---

## API Endpoints

### Parts

#### Query Parts
```
GET /ProdMgmt/Parts
GET /ProdMgmt/Parts?$filter=Name eq 'MyPart'
GET /ProdMgmt/Parts?$filter=contains(Number, 'PART-')
GET /ProdMgmt/Parts?$select=Number,Name,State,Description
GET /ProdMgmt/Parts?$top=10&$orderby=Name
```

#### Get Part by ID
```
GET /ProdMgmt/Parts('{id}')
GET /ProdMgmt/Parts('{id}')?$expand=PartUsages
```

#### Create Part
```
POST /ProdMgmt/Parts
Content-Type: application/json

{
  "Name": "My Part",
  "Number": "PART-001",
  "Description": "Test part",
  "DefaultUnit": "ea",
  "View": "Design",
  "Source": "Make",
  "ContainerID": "OR:wt.pdmlink.PDMLinkProduct:12345"
}
```

#### Update Part
```
PATCH /ProdMgmt/Parts('{id}')
Content-Type: application/json

{
  "Description": "Updated description",
  "Source": "Buy"
}
```

#### Delete Part
```
DELETE /ProdMgmt/Parts('{id}')
```

### Part Usages (BOM)

#### Query Part Usages
```
GET /ProdMgmt/PartUsages
GET /ProdMgmt/PartUsages?$filter=ParentID eq '{parent_id}'
GET /ProdMgmt/PartUsages?$filter=ChildID eq '{child_id}'
```

#### Get BOM for a Part
```
GET /ProdMgmt/Parts('{part_id}')/PartUsages
GET /ProdMgmt/Parts('{part_id}')/PartUsages?$expand=Child
```

#### Create Part Usage (Add to BOM)
```
POST /ProdMgmt/PartUsages
Content-Type: application/json

{
  "ParentID": "OR:wt.part.WTPart:12345",
  "ChildID": "OR:wt.part.WTPart:67890",
  "Quantity": 2,
  "Unit": "ea",
  "FindNumber": "10",
  "LineNumber": "1"
}
```

#### Update Part Usage
```
PATCH /ProdMgmt/PartUsages('{id}')
Content-Type: application/json

{
  "Quantity": 3,
  "FindNumber": "15"
}
```

#### Delete Part Usage
```
DELETE /ProdMgmt/PartUsages('{id}')
```

### Part Masters

#### Query Part Masters
```
GET /ProdMgmt/PartMasters
GET /ProdMgmt/PartMasters?$filter=Number eq 'PART-001'
```

#### Get Part Master by ID
```
GET /ProdMgmt/PartMasters('{id}')
```

#### Get All Versions of a Part
```
GET /ProdMgmt/PartMasters('{master_id}')/Parts
```

### Organizations

#### Query Organizations
```
GET /ProdMgmt/Organizations
GET /ProdMgmt/Organizations?$filter=Type eq 'Supplier'
GET /ProdMgmt/Organizations?$filter=contains(Name, 'Acme')
```

#### Get Organization by ID
```
GET /ProdMgmt/Organizations('{id}')
```

#### Create Organization
```
POST /ProdMgmt/Organizations
Content-Type: application/json

{
  "Name": "New Organization",
  "Number": "ORG-001",
  "Type": "Supplier",
  "Address": "123 Main St",
  "City": "City",
  "Country": "United States",
  "PostalCode": "12345"
}
```

### Products

#### Query Products
```
GET /ProdMgmt/Products
GET /ProdMgmt/Products?$filter=Name eq 'My Product'
```

#### Get Product by ID
```
GET /ProdMgmt/Products('{id}')
```

#### Create Product
```
POST /ProdMgmt/Products
Content-Type: application/json

{
  "Name": "New Product",
  "Number": "PROD-001",
  "Description": "Test product",
  "ContainerType": "PDMLinkProduct"
}
```

---

## OData Query Options

| Option | Description | Example |
|--------|-------------|---------|
| $filter | Filter results | `$filter=Name eq 'Test'` |
| $select | Select properties | `$select=Number,Name,State` |
| $top | Limit results | `$top=10` |
| $skip | Skip results | `$skip=20` |
| $orderby | Sort results | `$orderby=Name asc` |
| $expand | Expand navigation properties | `$expand=PartUsages` |
| $count | Count results | `$count=true` |

---

## Common Filter Operators

| Operator | Description | Example |
|----------|-------------|---------|
| eq | Equal | `Name eq 'Test'` |
| ne | Not equal | `State ne 'CANCELED'` |
| gt | Greater than | `Quantity gt 10` |
| ge | Greater or equal | `Quantity ge 10` |
| lt | Less than | `Quantity lt 100` |
| le | Less or equal | `Quantity le 100` |
| and | Logical AND | `Name eq 'Test' and State eq 'APPROVED'` |
| or | Logical OR | `State eq 'APPROVED' or State eq 'RELEASED'` |
| contains | Contains substring | `contains(Number, 'PART-')` |
| startswith | Starts with | `startswith(Name, 'BOLT-')` |

---

## Expand Options

### Expand Part Usages
```
GET /ProdMgmt/Parts('{id}')?$expand=PartUsages
```

### Expand Child Parts in BOM
```
GET /ProdMgmt/Parts('{id}')/PartUsages?$expand=Child
```

### Expand Parent Part
```
GET /ProdMgmt/PartUsages('{id}')?$expand=Parent
```

### Expand Both Parent and Child
```
GET /ProdMgmt/PartUsages('{id}')?$expand=Parent,Child
```

---

## Authentication
Use Basic Authentication with:
- **Username:** pat
- **Password:** ptc

---

## Common Use Cases

### Search for Parts by Number Pattern
```
GET /ProdMgmt/Parts?$filter=contains(Number, 'BOLT-')&$select=Number,Name,State,DefaultUnit
```

### Get All Parts in a Container
```
GET /ProdMgmt/Parts?$filter=ContainerID eq 'OR:wt.pdmlink.PDMLinkProduct:12345'
```

### Get All Released Parts
```
GET /ProdMgmt/Parts?$filter=State/Value eq 'RELEASED'
```

### Get BOM for a Part (Multi-level)
```
GET /ProdMgmt/Parts('{id}')/PartUsages?$expand=Child($expand=PartUsages)
```

### Find Parts by Classification
```
GET /ProdMgmt/Parts?$filter=Classification/ClfNodeInternalName eq 'Fasteners'
```

### Get All Purchased Parts
```
GET /ProdMgmt/Parts?$filter=Source eq 'Buy'
```

### Get All Manufactured Parts
```
GET /ProdMgmt/Parts?$filter=Source eq 'Make'
```

---

## Quick Reference Examples

### Example 1: Create a Simple Part
```bash
POST /ProdMgmt/Parts
Content-Type: application/json

{
  "Name": "Hex Bolt M6",
  "Number": "BOLT-M6-001",
  "Description": "M6 Hex Bolt, 20mm length",
  "DefaultUnit": "ea",
  "View": "Design",
  "Source": "Buy",
  "ContainerID": "OR:wt.pdmlink.PDMLinkProduct:10082558"
}
```

### Example 2: Query Parts and Get BOM
```bash
# Get part by number
GET /ProdMgmt/Parts?$filter=Number eq 'BOLT-M6-001'

# Get BOM for the part
GET /ProdMgmt/Parts('{part_id}')/PartUsages?$expand=Child
```

### Example 3: Add Child to BOM
```bash
POST /ProdMgmt/PartUsages
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

### Example 4: Search for Parts by Name
```bash
GET /ProdMgmt/Parts?$filter=contains(Name, 'Bolt')&$select=Number,Name,State,Source
```

### Example 5: Get All Parts with Pagination
```bash
GET /ProdMgmt/Parts?$top=50&$skip=0&$orderby=Name asc
```

---

## Lifecycle State Values

Common lifecycle states for parts:
- **INWORK** - In Work
- **PRELIMINARY** - Preliminary
- **RELEASED** - Released
- **UNDERREVIEW** - Under Review
- **APPROVED** - Approved
- **OBSOLETE** - Obsolete
- **CANCELED** - Canceled

---

## Part Source Values

Common source values:
- **Make** - Manufactured internally
- **Buy** - Purchased from supplier
- **MakeBuy** - Both make and buy options

---

## Part View Values

Common view values:
- **Design** - Design view
- **Manufacturing** - Manufacturing view
- **Service** - Service view
- **Simulation** - Simulation view