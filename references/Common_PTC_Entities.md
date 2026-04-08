# Common PTC Entities and Cross-Domain Navigation

## Overview

This document describes common PTC entities that are referenced across multiple Windchill OData domains, including base types, containers, and cross-domain navigation patterns.

---

## PTC Namespace Entities

### Container (PTC.DataAdmin.Container)

The Container entity represents Windchill containers (Products, Libraries, Projects) and is referenced by almost all other entities.

**Namespace:** `PTC.DataAdmin`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly, Key) |
| **Name** | String | Container name |
| **Description** | String | Container description |
| **ContainerType** | EnumType | Type of container |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Container Types:**
- `PRODUCT` - Product container
- `LIBRARY` - Library container
- `PROJECT` - Project container
- `PROGRAM` - Program container

**Navigation from Other Entities:**

```bash
# Get container from a part
GET /ProdMgmt/Parts('{id}')/Context

# Get container from a document
GET /DocMgmt/Documents('{id}')/Context

# Get container from a change notice
GET /ChangeMgmt/ChangeNotices('{id}')/Context

# Get container from a workflow work item
GET /Workflow/WorkItems('{id}')/Context

# Filter by container name
GET /ProdMgmt/Parts?$filter=Context/Name eq 'Product A'
```

---

### User (PTC.PrincipalMgmt.User)

The User entity represents Windchill users and is referenced by all entities that track creators, modifiers, owners, etc.

**Namespace:** `PTC.PrincipalMgmt`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly, Key) |
| **Name** | String | Username (login name) |
| **FullName** | String | User's full display name |
| **Email** | String | User's email address |
| **FirstName** | String | User's first name |
| **LastName** | String | User's last name |
| **Title** | String | Job title |
| **Organization** | String | Organization name |
| **Department** | String | Department name |
| **Disabled** | Boolean | Whether account is disabled |

**Common Navigation Properties:**

| Navigation | Source Entity | Source Domain | Description |
|------------|---------------|---------------|-------------|
| `Creator` | Part | ProdMgmt | User who created the part |
| `Modifier` | Part | ProdMgmt | User who last modified |
| `Creator` | Document | DocMgmt | Document creator |
| `Modifier` | Document | DocMgmt | Document modifier |
| `Creator` | ChangeNotice | ChangeMgmt | Change creator |
| `Modifier` | ChangeNotice | ChangeMgmt | Change modifier |
| `Owner` | WorkItem | Workflow | Work item assignee |
| `CompletedBy` | WorkItem | Workflow | User who completed work item |
| `Creator` | QualityIssue | QMS | Issue reporter |
| `Creator` | RegulatorySpec | RegMstr | Spec creator |

**Navigation Examples:**

```bash
# Get creator of a part
GET /ProdMgmt/Parts('{id}')/Creator

# Get modifier of a document
GET /DocMgmt/Documents('{id}')/Modifier

# Get owner of a work item
GET /Workflow/WorkItems('{id}')/Owner

# Get completed by user
GET /Workflow/WorkItems('{id}')/CompletedBy

# Filter by creator
GET /ProdMgmt/Parts?$filter=Creator/Name eq 'admin'

# Expand with user details
GET /ProdMgmt/Parts?$expand=Creator($select=Name,FullName,Email)
```

---

### Group (PTC.PrincipalMgmt.Group)

The Group entity represents user groups for access control.

**Namespace:** `PTC.PrincipalMgmt`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly, Key) |
| **Name** | String | Group name |
| **Description** | String | Group description |
| **GroupType** | EnumType | Type of group |

**Navigation Examples:**

```bash
# Get user's groups
GET /PrincipalMgmt/Users('{id}')/Groups

# Get group members
GET /PrincipalMgmt/Groups('{id}')/Members

# Get nested groups
GET /PrincipalMgmt/Groups('{id}')?$expand=ParentGroup,ChildGroups
```

---

## Base Entity Types

### LifecycleManaged

Base type for all entities that have lifecycle states.

**Properties (inherited):**

| Property | Type | Description |
|----------|------|-------------|
| **State** | EnumType | Lifecycle state |
| **LifeCycleTemplateName** | String | Lifecycle template name |

**Entities Inheriting:**
- Part (ProdMgmt)
- Document (DocMgmt)
- ChangeNotice (ChangeMgmt)
- ChangeRequest (ChangeMgmt)
- ChangeTask (ChangeMgmt)
- QualityIssue (QMS)
- Nonconformance (QMS)
- RegulatorySpecification (RegMstr)
- RegulatorySubmission (RegMstr)
- RegulatoryApproval (RegMstr)

**State Transitions:**

```bash
# Get valid state transitions
GET /ProdMgmt/Parts('{id}')/PTC.ProdMgmt.GetValidStateTransitions

# Set state
POST /ProdMgmt/Parts('{id}')/PTC.ProdMgmt.SetState
Content-Type: application/json
X-CSRF-Token: {token}

{
  "State": {"Value": "RELEASED"}
}
```

---

### Versioned

Base type for all entities that have version information.

**Properties (inherited):**

| Property | Type | Description |
|----------|------|-------------|
| **Version** | String | Version (A.1, A.2, B.1, etc.) |
| **Iteration** | String | Iteration |
| **MasterID** | String | Master ID |

**Entities Inheriting:**
- Part (ProdMgmt)
- Document (DocMgmt)
- CADDocument (CADDocumentMgmt)
- EPMDocument (CADDocumentMgmt)

**Version Navigation:**

```bash
# Get master ID
GET /ProdMgmt/Parts('{id}')/MasterID

# Get all versions of a part
GET /ProdMgmt/Parts?$filter=MasterID eq '{master_id}'

# Filter by version
GET /ProdMgmt/Parts?$filter=Version eq 'A.1'
```

---

### Foldered

Base type for all entities that have folder locations.

**Properties (inherited):**

| Property | Type | Description |
|----------|------|-------------|
| **FolderLocation** | String | Folder path in Windchill |

**Entities Inheriting:**
- Part (ProdMgmt)
- Document (DocMgmt)
- ChangeNotice (ChangeMgmt)
- QualityIssue (QMS)
- RegulatorySpecification (RegMstr)

**Folder Navigation:**

```bash
# Filter by folder
GET /ProdMgmt/Parts?$filter=FolderLocation eq '/Default/Parts'

# Filter by folder (contains)
GET /ProdMgmt/Parts?$filter=contains(FolderLocation, 'Parts')

# Filter by folder path
GET /DocMgmt/Documents?$filter=startswith(FolderLocation, '/Default')
```

---

### IdentifiableObject

Base type for all entities with Name and Number.

**Properties (inherited):**

| Property | Type | Description |
|----------|------|-------------|
| **Name** | String | Object name |
| **Number** | String | Object number (unique identifier) |

**Entities Inheriting:**
- Part (ProdMgmt)
- Document (DocMgmt)
- ChangeNotice (ChangeMgmt)
- ChangeRequest (ChangeMgmt)
- QualityIssue (QMS)
- RegulatorySpecification (RegMstr)

---

## Cross-Domain Navigation Patterns

### Part to Documents

```bash
# Path: Part -> Describes -> Document
GET /ProdMgmt/Parts('{id}')/Describes

# Path: Part -> References -> Document
GET /ProdMgmt/Parts('{id}')/References

# Path: Part -> Attachments -> Document
GET /ProdMgmt/Parts('{id}')/Attachments
```

### Part to CAD Documents

```bash
# Path: Part -> BuildRules -> EPMDocument
GET /ProdMgmt/Parts('{id}')/BuildRules

# Expand with CAD documents
GET /ProdMgmt/Parts?$expand=BuildRules($expand=EPMDocument)
```

### Part to Change Objects

```bash
# Path: Part -> AffectedBy -> ChangeNotice
GET /ChangeMgmt/ChangeNotices?$expand=AffectedObjects($filter=Changeable/ID eq '{part_id}')

# Path: Part -> ResultingFrom -> ChangeNotice
GET /ChangeMgmt/ChangeNotices?$expand=ResultingObjects($filter=ResultingChangeable/ID eq '{part_id}')
```

### Document to Parts

```bash
# Path: Document -> DescribedBy -> Part
GET /DocMgmt/Documents('{id}')/DescribedBy

# Path: Document -> ReferencedBy -> Part
GET /DocMgmt/Documents('{id}')/ReferencedBy
```

### Work Item to Business Object

```bash
# Path: WorkItem -> Subject -> BusinessObject
GET /Workflow/WorkItems('{id}')/Subject

# Get subject details
GET /Workflow/WorkItems('{id}')?$expand=Subject
```

### Change to Affected Objects

```bash
# Path: ChangeNotice -> AffectedObjects -> Changeable
GET /ChangeMgmt/ChangeNotices('{id}')/AffectedObjects?$expand=Changeable

# Path: ChangeNotice -> ResultingObjects -> ResultingChangeable
GET /ChangeMgmt/ChangeNotices('{id}')/ResultingObjects?$expand=ResultingChangeable
```

### Quality to User

```bash
# Path: QualityIssue -> Reporter -> User
GET /QMS/QualityIssues('{id}')/Reporter

# Path: QualityAction -> Owner -> User
GET /QMS/QualityActions('{id}')/Owner
```

### Customer Experience to QMS

```bash
# Path: CustomerExperience -> EntryLocation -> Place
GET /CEM/CustomerExperiences('{id}')/EntryLocation

# Path: CustomerExperience -> PrimaryRelatedPersonOrLocation -> QualityContact
GET /CEM/CustomerExperiences('{id}')/PrimaryRelatedPersonOrLocation
```

---

## Common OData Patterns

### Filtering on Navigation Properties

```bash
# Filter by container name
GET /ProdMgmt/Parts?$filter=Context/Name eq 'Product A'

# Filter by creator name
GET /ProdMgmt/Parts?$filter=Creator/Name eq 'admin'

# Filter by state
GET /ProdMgmt/Parts?$filter=State/Value eq 'RELEASED'
```

### Expanding Multiple Navigations

```bash
# Expand with multiple navigations
GET /ProdMgmt/Parts?$expand=Context,Creator,Modifier,Describes,References

# Nested expansion
GET /ProdMgmt/Parts?$expand=Creator($expand=Organization),Context
```

### Selecting Navigation Properties

```bash
# Select specific navigation properties
GET /ProdMgmt/Parts?$select=Name,Number&$expand=Creator($select=Name,FullName)

# Select from nested navigation
GET /ProdMgmt/Parts?$expand=Context($select=Name,ContainerType)
```

---

## Type Icon

Many entities have a `TypeIcon` property that provides icon information for UI rendering.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **IconKey** | String | Icon key |
| **IconClass** | String | Icon CSS class |
| **IconPath** | String | Icon file path |

**Usage:**

```bash
# Icons are typically non-filterable and non-sortable
# They are returned with the entity but cannot be filtered on

GET /ProdMgmt/Parts?$select=Name,Number,TypeIcon
```

---

## ObjectType

Many entities have an `ObjectType` property indicating the specific Windchill type.

**Usage:**

```bash
# ObjectType is typically non-filterable and non-sortable
# It indicates the specific Windchill type (e.g., wt.part.WTPart)

GET /ProdMgmt/Parts?$select=Name,Number,ObjectType
```

---

## Entity Inheritance Hierarchy

```
IdentifiableObject
├── Name: String
├── Number: String
│
├── Foldered
│   └── FolderLocation: String
│
├── Versioned
│   ├── Version: String
│   ├── Iteration: String
│   └── MasterID: String
│
└── LifecycleManaged
    ├── State: EnumType
    └── LifeCycleTemplateName: String

Entities:
- Part (ProdMgmt): IdentifiableObject + Versioned + Foldered + LifecycleManaged
- Document (DocMgmt): IdentifiableObject + Versioned + Foldered + LifecycleManaged
- ChangeNotice (ChangeMgmt): IdentifiableObject + Foldered + LifecycleManaged
- QualityIssue (QMS): IdentifiableObject + Foldered + LifecycleManaged
```

---

## Notes

1. **Cross-Domain References**: Most navigation properties that reference User, Container, or other common entities use the PTC namespace.

2. **Navigation Performance**: Expanding navigation properties can impact performance. Only expand what you need.

3. **Filtering Limitations**: Some properties (TypeIcon, ObjectType) are non-filterable and non-sortable.

4. **State Management**: Use domain-specific functions for state transitions (SetState, GetValidStateTransitions).

5. **Version Navigation**: Use MasterID to navigate between versions of the same object.

6. **Folder Navigation**: Use FolderLocation for folder-based filtering and organization.
