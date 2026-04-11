---
Domain: DataAdmin
Client: `from domains.DataAdmin import DataAdminClient`
---

> **Use the DataAdminClient**: `from domains.DataAdmin import DataAdminClient`
>
> This reference documents the entity types and properties. For programmatic access, use the domain client.

# Data Administration Domain Reference

Complete reference documentation for the Windchill Data Administration OData domain.

## Base URL

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/DataAdmin/
```

## Metadata URL

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/DataAdmin/$metadata
```

## Domain Overview

The Data Administration domain provides access to container and folder management in Windchill including:

### Container Types
- **Containers** - Base container entity
- **ProductContainer** - Product containers
- **LibraryContainer** - Library containers
- **ProjectContainer** - Project containers
- **OrganizationContainer** - Organization containers
- **Site** - Site containers

### Folder Management
- **Folder** - Folder hierarchy and management
- **FolderContent** - Folder contents

### Participants
- **Participant** - Participants in containers

### Constraint & Property Management (Functions)
- **GetDriverProperties** - Get driver attributes for Windchill types
- **GetConstraints** - Get constraints on properties
- **GetPregeneratedValue** - Get pregenerated values (like Number) before entity creation

---

## Entity Types

### Container

Base container entity representing logical containers in Windchill.

**Endpoint:** `/DataAdmin/Containers`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) |
| **Name** | String | Container name |
| **Description** | String | Description |
| **OrganizationID** | String | Organization ID |
| **OrganizationName** | String | Organization name (ReadOnly, NonSortable) |
| **CreatedBy** | String | User who created |
| **PrivateAccess** | Boolean | Private access flag |
| **CreatedOn** | DateTime | Creation timestamp |
| **LastModified** | DateTime | Last modification timestamp |

**Navigation Properties:**
- `Folders` - Folders in this container
- `Creator` - User who created the container
- `Organization` - Associated organization

**CRUD Operations:**

```bash
# Get all containers
GET /DataAdmin/Containers

# Get container by ID
GET /DataAdmin/Containers('{id}')

# Get container by name
GET /DataAdmin/Containers?$filter=Name eq 'MyProduct'

# Expand with folders
GET /DataAdmin/Containers('{id}')?$expand=Folders

# Expand with organization
GET /DataAdmin/Containers('{id}')?$expand=Organization
```

---

### ProductContainer

Product container extending the base Container entity.

**Endpoint:** `/DataAdmin/Containers` (filtered by type)

**Operations:** `READ`

**Properties:** Inherits all properties from `Container`

**Navigation Properties:**
- `AssignedOptionSet` - Assigned option set (ReadOnly)
- `OptionPoolAliases` - Option pool aliases (ReadOnly)
- `OptionPool` - Option pool items (ReadOnly)

**Query Operations:**

```bash
# Get product containers
GET /DataAdmin/Products

# Get product container with option sets
GET /DataAdmin/Containers('{id}')?$expand=AssignedOptionSet,OptionPool

# Get product container with option pool aliases
GET /DataAdmin/Containers('{id}')?$expand=OptionPoolAliases
```

---

### LibraryContainer

Library container extending the base Container entity.

**Endpoint:** `/DataAdmin/Containers` (filtered by type)

**Operations:** `READ`

**Properties:** Inherits all properties from `Container`

**Navigation Properties:**
- `AssignedOptionSet` - Assigned option set (ReadOnly)
- `OptionPoolAliases` - Option pool aliases (ReadOnly)
- `OptionPool` - Option pool items (ReadOnly)

**Query Operations:**

```bash
# Get library containers
GET /DataAdmin/Libraries

# Get library container with option sets
GET /DataAdmin/Containers('{id}')?$expand=AssignedOptionSet,OptionPool
```

---

### ProjectContainer

Project container extending the base Container entity.

**Endpoint:** `/DataAdmin/Containers` (filtered by type)

**Operations:** `READ`

**Properties:** Inherits all properties from `Container`

**Query Operations:**

```bash
# Get project containers
GET /DataAdmin/Projects
```

---

### OrganizationContainer

Organization container extending the base Container entity.

**Endpoint:** `/DataAdmin/Containers` (filtered by type)

**Operations:** `READ`

**Properties:** Inherits all properties from `Container`

**Query Operations:**

```bash
# Get organization containers
GET /DataAdmin/Organizations
```

---

### Site

Site container extending the base Container entity.

**Endpoint:** `/DataAdmin/Containers` (filtered by type)

**Operations:** `READ`

**Properties:** Inherits all properties from `Container`

**Query Operations:**

```bash
# Get site containers
GET /DataAdmin/Sites
```

---

### Folder

Folder hierarchy and management.

**Endpoint:** `/DataAdmin/Folders`

**Operations:** `READ`, `CREATE`, `UPDATE`, `DELETE`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Folder name |
| **Description** | String | Description |
| **Location** | String | Folder location (NonFilterable, NonSortable) |
| **CreatedOn** | DateTime | Creation timestamp (ReadOnly) |
| **LastModified** | DateTime | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- `Folders` - Subfolders (ContainsTarget=true)
- `Contents` - Folder contents (ReadOnly, ContainsTarget=true)
- `FolderContents` - Generic folder contents (ReadOnly, ContainsTarget=true)

**CRUD Operations:**

```bash
# Get all folders
GET /DataAdmin/Folders

# Get folder by ID
GET /DataAdmin/Folders('{id}')

# Get folder with subfolders
GET /DataAdmin/Folders('{id}')?$expand=Folders

# Get folder with contents
GET /DataAdmin/Folders('{id}')?$expand=Contents

# Get folder with generic folder contents
GET /DataAdmin/Folders('{id}')?$expand=FolderContents

# Create folder
POST /DataAdmin/Folders
Content-Type: application/json
X-CSRF-Token: {token}

{
  "Name": "New Folder",
  "Description": "Folder description"
}

# Update folder
PATCH /DataAdmin/Folders('{id}')
Content-Type: application/json
X-CSRF-Token: {token}

{
  "Name": "Updated Folder Name",
  "Description": "Updated description"
}

# Delete folder
DELETE /DataAdmin/Folders('{id}')
X-CSRF-Token: {token}
```

---

### FolderContent

Folder contents representation.

**Endpoint:** `/DataAdmin/FolderContent`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **Name** | String | Content name |
| **Description** | String | Description |

**Query Operations:**

```bash
# Get folder contents via Folder navigation
GET /DataAdmin/Folders('{folder_id}')/Contents
```

---

### Participant

Participants in containers.

**Endpoint:** `/DataAdmin/Participants`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key) |
| **Role** | EnumType | Participant role |

**Navigation Properties:**
- `Principals` - Collection of principals (users, groups)

**Query Operations:**

```bash
# Get all participants
GET /DataAdmin/Participants

# Get participant by ID
GET /DataAdmin/Participants('{id}')

# Expand with principals
GET /DataAdmin/Participants('{id}')?$expand=Principals
```

---

## Functions

### GetDriverProperties

Get the driver attributes for a Windchill type.

**Function Signature:**
```
PTC.DataAdmin.GetDriverProperties(Container, EntityName)
PTC.DataAdmin.GetDriverProperties(Container, EntityName, EntityVersion)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| **Container** | Container | The container context |
| **EntityName** | String | The entity type name |
| **EntityVersion** | String | (Optional) The entity version |

**Returns:** `PropertyList` - A list of PropertyItems

**Usage Example:**

```bash
# Get driver properties for Part entity
GET /DataAdmin/Containers('{container_id}')/PTC.DataAdmin.GetDriverProperties(EntityName='PTC.ProdMgmt.Part')

# Get driver properties with version
GET /DataAdmin/Containers('{container_id}')/PTC.DataAdmin.GetDriverProperties(EntityName='PTC.ProdMgmt.Part', EntityVersion='1.0')
```

**Response Structure (PropertyList):**
```json
{
  "Items": [
    {
      "Name": "PropertyName",
      "Type": "PropertyType",
      "Value": "PropertyValue"
    }
  ]
}
```

---

### GetConstraints

Get all constraints on all properties for a Windchill type.

**Function Signatures:**
```
PTC.DataAdmin.GetConstraints(Container, EntityName, DriverProperties) - Collection(PropertyDetail)
PTC.DataAdmin.GetConstraints(Container, EntityName, EntityVersion, DriverProperties) - Collection(PropertyDetail)
PTC.DataAdmin.GetConstraints(Container, EntityName, EntityVersion, PropertyName, DriverProperties) - PropertyDetail
PTC.DataAdmin.GetConstraints(Container, EntityName, PropertyName, DriverProperties) - PropertyDetail
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| **Container** | Container | The container context |
| **EntityName** | String | The entity type name |
| **EntityVersion** | String | (Optional) The entity version |
| **PropertyName** | String | (Optional) Specific property name |
| **DriverProperties** | PropertyList | Driver properties from GetDriverProperties |

**Returns:** `Collection(PropertyDetail)` or `PropertyDetail`

**Usage Examples:**

```bash
# First get driver properties
GET /DataAdmin/Containers('{container_id}')/PTC.DataAdmin.GetDriverProperties(EntityName='PTC.ProdMgmt.Part')

# Then get all constraints for the entity
POST /DataAdmin/Containers('{container_id}')/PTC.DataAdmin.GetConstraints
Content-Type: application/json

{
  "EntityName": "PTC.ProdMgmt.Part",
  "DriverProperties": {
    "Items": [
      {"Name": "Name", "Type": "string", "Value": ""},
      {"Name": "Number", "Type": "string", "Value": ""}
    ]
  }
}

# Get constraints for a specific property
POST /DataAdmin/Containers('{container_id}')/PTC.DataAdmin.GetConstraints
Content-Type: application/json

{
  "EntityName": "PTC.ProdMgmt.Part",
  "PropertyName": "Name",
  "DriverProperties": {
    "Items": [
      {"Name": "Name", "Type": "string", "Value": ""}
    ]
  }
}
```

**Response Structure (PropertyDetail):**
```json
{
  "Entity": "PTC.ProdMgmt.Part",
  "Property": "Name",
  "DefaultValue": "",
  "LegalValues": ["Value1", "Value2"],
  "Constraints": [
    {
      "Type": "StringLength",
      "Value": "50",
      "ValueTwo": null
    }
  ],
  "Visibility": {
    "Create": "Required",
    "Edit": "Enabled",
    "EPMUpload": "Hidden"
  },
  "DefaultUnits": null
}
```

---

### GetPregeneratedValue

Get a pregenerated value (like Number) before an entity is created.

**Function Signatures:**
```
PTC.DataAdmin.GetPregeneratedValue(Container, EntityName, PropertyName, DriverProperties) - String
PTC.DataAdmin.GetPregeneratedValue(Container, EntityName, EntityVersion, PropertyName, DriverProperties) - String
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| **Container** | Container | The container context |
| **EntityName** | String | The entity type name |
| **EntityVersion** | String | (Optional) The entity version |
| **PropertyName** | String | The property name to pregenerate |
| **DriverProperties** | PropertyList | Driver properties from GetDriverProperties |

**Returns:** `String` - The pregenerated value

**Usage Examples:**

```bash
# Get a pregenerated number for a new Part
POST /DataAdmin/Containers('{container_id}')/PTC.DataAdmin.GetPregeneratedValue
Content-Type: application/json

{
  "EntityName": "PTC.ProdMgmt.Part",
  "PropertyName": "Number",
  "DriverProperties": {
    "Items": [
      {"Name": "Name", "Type": "string", "Value": "MyPart"}
    ]
  }
}

# Response: "0000001234"
```

---

## Complex Types

### PropertyDetail

Property details for constraint list.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **Container** | String | Container name (ReadOnly) |
| **Entity** | String | Entity name (ReadOnly) |
| **Property** | String | Property name (ReadOnly) |
| **DefaultValue** | String | Default value (ReadOnly) |
| **LegalValues** | Collection(EnumType) | Legal values (ReadOnly) |
| **Constraints** | Collection(Constraint) | Constraints (ReadOnly) |
| **Visibility** | VisibilityItem | Visibility settings (ReadOnly) |
| **DefaultUnits** | String | Default units (ReadOnly) |

---

### Constraint

Constraint type applied to a property.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **Type** | String | Constraint type (ReadOnly) |
| **Value** | String | Primary value (ReadOnly) |
| **ValueTwo** | String | Secondary value (ReadOnly) |

**Common Constraint Types:**
- `StringLength` - Maximum string length
- `NumericRange` - Numeric range (min/max)
- `RegularExpression` - Regex pattern
- `Required` - Required field
- `Unique` - Unique value required

---

### VisibilityItem

Describes the visibility for a property.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **Create** | String | Visibility during create (Required/Enabled/Hidden) |
| **Edit** | String | Visibility during edit (Required/Enabled/Hidden) |
| **EPMUpload** | String | Visibility during EPM upload (Required/Enabled/Hidden) |

---

### PropertyItem

Describes a single property for constraints.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **Name** | String | Property name |
| **Type** | String | Property type |
| **Value** | String | Property value |

---

### PropertyList

A list of PropertyItems for constraints.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **Items** | Collection(PropertyItem) | List of property items |

---

## Common Query Examples

### Filter Containers by Type

```bash
# Get only product containers
GET /DataAdmin/Containers?$filter=startswith(ID, 'OR:wt.pdmlink.PDMLinkProduct')

# Get only library containers
GET /DataAdmin/Containers?$filter=startswith(ID, 'OR:wt.inf.library.WTLibrary')

# Search by name
GET /DataAdmin/Containers?$filter=contains(Name, 'MyProduct')
```

### Folder Navigation

```bash
# Get subfolders recursively
GET /DataAdmin/Folders('{id}')?$expand=Folders($expand=Folders)

# Get all contents in folder
GET /DataAdmin/Folders('{id}')/FolderContents

# Get folder with contents and subfolders
GET /DataAdmin/Folders('{id}')?$expand=Folders,Contents,FolderContents
```

### Sorting

```bash
# Sort containers by name
GET /DataAdmin/Containers?$orderby=Name

# Sort folders by creation date
GET /DataAdmin/Folders?$orderby=CreatedOn desc
```

### Pagination

```bash
# Get first 10 containers
GET /DataAdmin/Containers?$top=10

# Get next 10 containers (skip first 10)
GET /DataAdmin/Containers?$skip=10&$top=10
```

### Select Specific Properties

```bash
# Get only name and description for containers
GET /DataAdmin/Containers?$select=ID,Name,Description,OrganizationName

# Get only name and location for folders
GET /DataAdmin/Folders?$select=ID,Name,Location
```

---

## Entity Sets

The DataAdmin domain defines the following entity sets:

| Entity Set | Entity Type | Description |
|------------|-------------|-------------|
| **Containers** | Container | All containers |
| **Folders** | Folder | All folders |
| **Participants** | Participant | All participants |
| **Sites** | Site | Site containers |
| **Products** | ProductContainer | Product containers |
| **Libraries** | LibraryContainer | Library containers |
| **Projects** | ProjectContainer | Project containers |
| **Organizations** | OrganizationContainer | Organization containers |