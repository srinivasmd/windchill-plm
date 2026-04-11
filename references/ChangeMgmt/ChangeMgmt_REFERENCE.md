---
Domain: ChangeMgmt
Client: `from domains.ChangeMgmt import ChangeMgmtClient`
---

> **Use the ChangeMgmtClient**: `from domains.ChangeMgmt import ChangeMgmtClient`
>
> This reference documents the entity types and properties. For programmatic access, use the domain client.

# Change Management (ChangeMgmt) Domain Reference

Complete reference documentation for the Windchill Change Management OData domain.

## Base URL

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/ChangeMgmt/
```

## Metadata URL

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/ChangeMgmt/$metadata
```

## Domain Overview

The Change Management domain provides access to Windchill's change control objects including:
- **Change Notices** - Formal change orders that implement changes
- **Change Requests** - Requests for engineering changes
- **Change Tasks** - Individual tasks within a change notice
- **Problem Reports** - Documentation of issues or defects
- **Variances** - Requests for deviation from specifications

---

## Entity Types

### ChangeNotice

A Change Notice (CN) is a formal document that authorizes and tracks the implementation of changes to product data. It contains one or more Change Tasks that define the specific work to be done.

**Endpoint:** `/ChangeMgmt/ChangeNotices`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Change notice name |
| **Number** | String | Change notice number (unique) |
| **Description** | String | Description of the change |
| **State** | EnumType | Lifecycle state (e.g., OPEN, INWORK, ISSUED, CLOSED) |
| **FolderName** | String | Folder location name |
| **ChangeNoticeComplexity** | EnumType | Complexity level |
| **ActualFinishDate** | DateTimeOffset | Actual completion date |
| **CreatedBy** | String | Creator username (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **ModifiedBy** | String | Last modifier username (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |
| **MasterID** | String | Master object ID (ReadOnly) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **Context** | PTC.DataAdmin.Container | Container context |
| **Folder** | PTC.DataAdmin.Folder | Folder location |
| **ChangeAdministratorI** | Collection(PTC.PrincipalMgmt.Principal) | Primary change administrators |
| **ChangeAdministratorII** | Collection(PTC.PrincipalMgmt.Principal) | Secondary change administrators |
| **ImplementationPlan** | Collection(PTC.ChangeMgmt.ChangeTask) | Change tasks for implementation |
| **Attachments** | Collection(PTC.ContentItem) | Attached documents |

**CRUD Operations:**

```bash
# Get all change notices
GET /ChangeMgmt/ChangeNotices

# Get change notice by ID
GET /ChangeMgmt/ChangeNotices('{id}')

# Get change notice by number
GET /ChangeMgmt/ChangeNotices?$filter=Number eq 'CN0001'

# Get change notice with expanded navigation
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=ImplementationPlan,Context,Folder

# Filter by state
GET /ChangeMgmt/ChangeNotices?$filter=State/Value eq 'ISSUED'

# Search by name
GET /ChangeMgmt/ChangeNotices?$filter=contains(Name, 'Assembly')

# Create change notice
POST /ChangeMgmt/ChangeNotices
Content-Type: application/json
CSRF_NONCE: {token}

{
  "Name": "Engineering Change Notice",
  "Number": "CN-2024-001",
  "Description": "Description of the change",
  "FolderName": "/Default/Change/Change Notices"
}

# Update change notice
PATCH /ChangeMgmt/ChangeNotices('{id}')
Content-Type: application/json
CSRF_NONCE: {token}

{
  "Description": "Updated description"
}
```

---

### ChangeRequest

A Change Request (CR) is a formal proposal for a change to product data. It documents the need for change and provides justification.

**Endpoint:** `/ChangeMgmt/ChangeRequests`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Change request name |
| **Number** | String | Change request number (unique) |
| **Description** | String | Description of the requested change |
| **State** | EnumType | Lifecycle state |
| **Complexity** | EnumType | Complexity level |
| **ProposedSolution** | String | Proposed solution for the change |
| **NonRecurringCost** | String | Estimated non-recurring cost |
| **FolderName** | String | Folder location name |
| **CabinetName** | String | Cabinet name |
| **CreatedBy** | String | Creator username (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **ModifiedBy** | String | Last modifier username (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **Context** | PTC.DataAdmin.Container | Container context |
| **Folder** | PTC.DataAdmin.Folder | Folder location |
| **ChangeAdministratorI** | Collection(PTC.PrincipalMgmt.Principal) | Change administrators |
| **CRAffectLinks** | Collection(PTC.ChangeMgmt.RelevantRequestDataLinkItem) | Affected items links |
| **Attachments** | Collection(PTC.ContentItem) | Attached documents |

**CRUD Operations:**

```bash
# Get all change requests
GET /ChangeMgmt/ChangeRequests

# Get change request by number
GET /ChangeMgmt/ChangeRequests?$filter=Number eq 'CR0001'

# Filter by state
GET /ChangeMgmt/ChangeRequests?$filter=State/Value eq 'OPEN'

# Get with affected items
GET /ChangeMgmt/ChangeRequests('{id}')?$expand=CRAffectLinks,Context

# Create change request
POST /ChangeMgmt/ChangeRequests
Content-Type: application/json
CSRF_NONCE: {token}

{
  "Name": "Engineering Change Request",
  "Number": "CR-2024-001",
  "Description": "Request for engineering change",
  "ProposedSolution": "Replace component with updated version",
  "FolderName": "/Default/Change/Change Requests"
}
```

---

### ChangeTask

A Change Task (CT) is a unit of work within a Change Notice. It defines specific actions to implement a change.

**Endpoint:** `/ChangeMgmt/ChangeTasks`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Change task name |
| **Number** | String | Change task number |
| **Description** | String | Task description |
| **State** | EnumType | Lifecycle state |
| **Sequence** | String | Task sequence number |
| **Stage** | String | Current stage |
| **ActualFinishDate** | DateTimeOffset | Actual completion date |
| **CreatedBy** | String | Creator username (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **ModifiedBy** | String | Last modifier username (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |
| **MasterID** | String | Master object ID (ReadOnly) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **ChangeNotice** | PTC.ChangeMgmt.ChangeNotice | Parent change notice |
| **Context** | PTC.DataAdmin.Container | Container context |
| **Assignee** | Collection(PTC.PrincipalMgmt.User) | Assigned users |
| **Reviewer** | Collection(PTC.PrincipalMgmt.User) | Reviewer users |
| **ResultingObjects** | Collection(PTC.ChangeMgmt.Changeable) | Objects created by this task |
| **ResultingLinks** | Collection(PTC.ChangeMgmt.ResultingLinkItem) | Links to resulting objects |
| **UnincorporatedLinks** | Collection(PTC.ChangeMgmt.UnincorporatedLinkItem) | Unincorporated item links |
| **CNAffectLinks** | Collection(PTC.ChangeMgmt.AffectedActivityDataLinkItem) | Affected items |
| **Attachments** | Collection(PTC.ContentItem) | Attached documents |

**CRUD Operations:**

```bash
# Get all change tasks
GET /ChangeMgmt/ChangeTasks

# Get change task by number
GET /ChangeMgmt/ChangeTasks?$filter=Number eq 'CT0001'

# Get task with resulting objects
GET /ChangeMgmt/ChangeTasks('{id}')?$expand=ResultingObjects,Assignee,ChangeNotice

# Get tasks for a specific change notice
GET /ChangeMgmt/ChangeTasks?$filter=ChangeNotice/Number eq 'CN0001'

# Get resulting objects (parts/documents modified by this task)
GET /ChangeMgmt/ChangeTasks('{id}')/ResultingObjects

# Get affected objects
GET /ChangeMgmt/ChangeTasks('{id}')?$expand=CNAffectLinks($expand=Changeable)
```

---

### ProblemReport

A Problem Report documents an issue, defect, or problem discovered in a product.

**Endpoint:** `/ChangeMgmt/ProblemReports`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Problem report name |
| **Number** | String | Problem report number |
| **Description** | String | Description of the problem |
| **State** | EnumType | Lifecycle state |
| **Severity** | EnumType | Problem severity |
| **Priority** | EnumType | Problem priority |
| **Category** | EnumType | Problem category |
| **ReportedDate** | DateTimeOffset | Date problem was reported |
| **CreatedBy** | String | Creator username (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **Context** | PTC.DataAdmin.Container | Container context |
| **Attachments** | Collection(PTC.ContentItem) | Attached documents |
| **ReportedAgainstLinkItem** | Collection | Items affected by the problem |

---

### Variance

A Variance is a formal request for deviation from specifications or requirements.

**Endpoint:** `/ChangeMgmt/Variances`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Variance name |
| **Number** | String | Variance number |
| **Description** | String | Description of the variance |
| **State** | EnumType | Lifecycle state |
| **StartDate** | DateTimeOffset | Variance start date |
| **EndDate** | DateTimeOffset | Variance end date |
| **CreatedBy** | String | Creator username (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **Context** | PTC.DataAdmin.Container | Container context |
| **VarianceOwners** | Collection(PTC.PrincipalMgmt.User) | Variance owners |
| **VarianceSubstituteLinks** | Collection | Substitute item links |

---

## Common Query Examples

### Get All Open Change Notices

```bash
GET /ChangeMgmt/ChangeNotices?$filter=State/Value eq 'OPEN'&$expand=ImplementationPlan
```

### Get Change Notice with All Tasks

```bash
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=ImplementationPlan($expand=Assignee,ResultingObjects)
```

### Get Resulting Objects from Change Task

```bash
GET /ChangeMgmt/ChangeTasks('{task_id}')/ResultingObjects
```

### Get Affected Objects for Change Notice

```bash
GET /ChangeMgmt/ChangeNotices('{id}')/ImplementationPlan?$expand=CNAffectLinks($expand=Changeable)
```

### Search Change Requests by Name

```bash
GET /ChangeMgmt/ChangeRequests?$filter=contains(Name, 'Engine')
```

### Get Change Tasks Assigned to User

```bash
GET /ChangeMgmt/ChangeTasks?$filter=Assignee/any(a: a/Name eq 'jsmith')
```

### Get Change Notices in Date Range

```bash
GET /ChangeMgmt/ChangeNotices?$filter=CreatedOn ge 2024-01-01T00:00:00Z and CreatedOn le 2024-12-31T23:59:59Z
```

---

## Lifecycle States

Common lifecycle states for Change Management objects:

| State | Description |
|-------|-------------|
| **OPEN** | Created, not yet being processed |
| **INWORK** | Being actively worked on |
| **ISSUED** | Approved and released for implementation |
| **CLOSED** | Implementation complete |
| **CANCELLED** | Cancelled without implementation |
| **HELD** | Temporarily suspended |

---

## Relationships Between Change Objects

```
ChangeRequest (CR)
    └── Documents need for change
         └── May lead to → ChangeNotice (CN)
                            └── Contains → ChangeTask (CT)
                                            └── Modifies → ResultingObjects
                                            └── Affects → AffectedObjects
```

---

## Notes

1. **CSRF Token Required**: All write operations (POST, PATCH, DELETE) require the `CSRF_NONCE` header.

2. **Lifecycle Management**: Change objects follow Windchill lifecycle templates. Use SetState actions to transition states.

3. **Navigation Performance**: Expanding multiple navigation properties can impact performance. Only expand what you need.

4. **Object Identifiers**: IDs are OIDs in the format `OR:<ObjectType>:<NumericID>`.

---

## Schema Version

Schema Version: Various (check metadata for version details)
