# Change Management (ChangeMgmt) Domain Reference

Complete reference documentation for the Windchill Change Management OData domain.

## Base URL

```
https://windchill.example.com/Windchill/servlet/odata/ChangeMgmt/
```

## Metadata URL

```
https://windchill.example.com/Windchill/servlet/odata/ChangeMgmt/$metadata
```

## Domain Overview

The Change Management (ChangeMgmt) domain provides access to Windchill's change management objects including:

### Change Objects
- **ChangeNotices** - Change Notices (ECN - Engineering Change Notices)
- **ChangeRequests** - Change Requests (ECR - Engineering Change Requests)
- **ChangeTasks** - Change Tasks (Activities within a Change Notice)
- **ChangeOrders** - Change Orders

### Related Objects
- **ResultingObjects** - Objects created or modified by a change
- **AffectedObjects** - Objects impacted by a change

---

## Entity Types

### ChangeNotice

Change Notice (ECN) - Formal documentation of approved changes to be implemented.

**Endpoint:** `/ChangeMgmt/ChangeNotices`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Change Notice name |
| **Number** | String | Change Notice number |
| **Description** | String | Description of the change |
| **State** | EnumType | Lifecycle state (e.g., OPEN, IN_WORK, CLOSED) |
| **LifeCycleTemplateName** | String | Lifecycle template name (ReadOnly) |
| **FolderLocation** | String | Folder path location |
| **CreatedBy** | String | User who created (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **ModifiedBy** | String | User who last modified (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **NeedDate** | DateTimeOffset | Need date for implementation |
| **ApprovalDate** | DateTimeOffset | Approval date |
| **CustomerName** | String | Customer name if applicable |
| **ChangeType** | String | Type of change |
| **ChangeReason** | String | Reason for change |
| **MasterID** | String | Master object ID (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` → PTC.DataAdmin.Container (Container context)
- `Creator` → PTC.PrincipalMgmt.User (User who created)
- `Modifier` → PTC.PrincipalMgmt.User (User who last modified)
- `ChangeRequests` → Collection(PTC.ChangeMgmt.ChangeRequest) (Linked change requests)
- `ChangeTasks` → Collection(PTC.ChangeMgmt.ChangeTask) (Child change tasks)
- `ResultingObjects` → Collection(PTC.ChangeMgmt.Changeable) (Objects created/modified)
- `AffectedObjects` → Collection(PTC.ChangeMgmt.Changeable) (Objects impacted)
- `Folder` → PTC.DataAdmin.Folder (Containing folder)

**CRUD Operations:**

```bash
# Get all change notices
GET /ChangeMgmt/ChangeNotices

# Get change notice by ID
GET /ChangeMgmt/ChangeNotices('{id}')

# Get change notice by number
GET /ChangeMgmt/ChangeNotices?$filter=Number eq 'CN-00001'

# Get change notice by name
GET /ChangeMgmt/ChangeNotices?$filter=contains(Name, 'Design Change')

# Filter by state
GET /ChangeMgmt/ChangeNotices?$filter=State/Value eq 'OPEN'

# Expand with change tasks
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=ChangeTasks,ChangeRequests

# Expand with resulting objects
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=ResultingObjects

# Expand with affected objects
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=AffectedObjects

# Get with context and creator
GET /ChangeMgmt/ChangeNotices?$expand=Context,Creator

# Select specific properties
GET /ChangeMgmt/ChangeNotices?$select=ID,Name,Number,State,NeedDate

# Order by creation date
GET /ChangeMgmt/ChangeNotices?$orderby=CreatedOn desc

# Top results
GET /ChangeMgmt/ChangeNotices?$top=50
```

---

### ChangeRequest

Change Request (ECR) - Request for change to be evaluated and approved.

**Endpoint:** `/ChangeMgmt/ChangeRequests`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Change Request name |
| **Number** | String | Change Request number |
| **Description** | String | Description of the requested change |
| **State** | EnumType | Lifecycle state (e.g., OPEN, UNDER_REVIEW, APPROVED, REJECTED) |
| **LifeCycleTemplateName** | String | Lifecycle template name (ReadOnly) |
| **FolderLocation** | String | Folder path location |
| **CreatedBy** | String | User who created (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **ModifiedBy** | String | User who last modified (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **NeedDate** | DateTimeOffset | Need date for implementation |
| **Justification** | String | Business justification |
| **Urgency** | String | Urgency level |
| **ChangeType** | String | Type of change |
| **MasterID** | String | Master object ID (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` → PTC.DataAdmin.Container (Container context)
- `Creator` → PTC.PrincipalMgmt.User (User who created)
- `Modifier` → PTC.PrincipalMgmt.User (User who last modified)
- `ChangeNotices` → Collection(PTC.ChangeMgmt.ChangeNotice) (Linked change notices)
- `AffectedObjects` → Collection(PTC.ChangeMgmt.Changeable) (Objects impacted)
- `Folder` → PTC.DataAdmin.Folder (Containing folder)

**CRUD Operations:**

```bash
# Get all change requests
GET /ChangeMgmt/ChangeRequests

# Get change request by ID
GET /ChangeMgmt/ChangeRequests('{id}')

# Get change request by number
GET /ChangeMgmt/ChangeRequests?$filter=Number eq 'CR-00001'

# Filter by state
GET /ChangeMgmt/ChangeRequests?$filter=State/Value eq 'OPEN'

# Get open or under review requests
GET /ChangeMgmt/ChangeRequests?$filter=State/Value eq 'OPEN' or State/Value eq 'UNDER_REVIEW'

# Expand with change notices
GET /ChangeMgmt/ChangeRequests('{id}')?$expand=ChangeNotices

# Get with affected objects
GET /ChangeMgmt/ChangeRequests?$expand=AffectedObjects

# Order by need date
GET /ChangeMgmt/ChangeRequests?$orderby=NeedDate asc
```

---

### ChangeTask

Change Task - Individual task within a Change Notice for implementation.

**Endpoint:** `/ChangeMgmt/ChangeTasks`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Change Task name |
| **Number** | String | Change Task number |
| **Description** | String | Task description |
| **State** | EnumType | Lifecycle state (e.g., NOT_STARTED, IN_PROGRESS, COMPLETED) |
| **LifeCycleTemplateName** | String | Lifecycle template name (ReadOnly) |
| **FolderLocation** | String | Folder path location |
| **CreatedBy** | String | User who created (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **ModifiedBy** | String | User who last modified (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **DueDate** | DateTimeOffset | Due date for completion |
| **CompletionDate** | DateTimeOffset | Actual completion date |
| **Assignee** | String | Assigned user |
| **MasterID** | String | Master object ID (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` → PTC.DataAdmin.Container (Container context)
- `Creator` → PTC.PrincipalMgmt.User (User who created)
- `Modifier` → PTC.PrincipalMgmt.User (User who last modified)
- `ChangeNotice` → PTC.ChangeMgmt.ChangeNotice (Parent change notice)
- `ResultingObjects` → Collection(PTC.ChangeMgmt.Changeable) (Objects created/modified)
- `Folder` → PTC.DataAdmin.Folder (Containing folder)

**CRUD Operations:**

```bash
# Get all change tasks
GET /ChangeMgmt/ChangeTasks

# Get change task by ID
GET /ChangeMgmt/ChangeTasks('{id}')

# Get change task by number
GET /ChangeMgmt/ChangeTasks?$filter=Number eq 'CT-00001'

# Filter by state
GET /ChangeMgmt/ChangeTasks?$filter=State/Value eq 'IN_PROGRESS'

# Get tasks for a specific change notice
GET /ChangeMgmt/ChangeTasks?$filter=ChangeNotice/Number eq 'CN-00001'

# Expand with change notice
GET /ChangeMgmt/ChangeTasks('{id}')?$expand=ChangeNotice

# Get with resulting objects
GET /ChangeMgmt/ChangeTasks?$expand=ResultingObjects

# Order by due date
GET /ChangeMgmt/ChangeTasks?$orderby=DueDate asc
```

---

### Changeable (Affected/Resulting Objects)

Base type for objects that can be affected by or result from a change.

**Navigation Properties:**
- `Context` → PTC.DataAdmin.Container
- `Creator` → PTC.PrincipalMgmt.User
- `Modifier` → PTC.PrincipalMgmt.User

---

## Common Query Examples

### Get Change Notice with Full Details

```bash
GET /ChangeMgmt/ChangeNotices('OR:wt.change2.WTChangeOrder2:12345')?$expand=ChangeTasks,ChangeRequests,AffectedObjects,ResultingObjects,Context,Creator
```

### Find Open Change Requests

```bash
GET /ChangeMgmt/ChangeRequests?$filter=State/Value eq 'OPEN'&$expand=AffectedObjects&$orderby=CreatedOn desc
```

### Get Change Tasks Due This Week

```bash
GET /ChangeMgmt/ChangeTasks?$filter=DueDate ge 2026-01-01T00:00:00Z and DueDate le 2026-01-07T23:59:59Z&$expand=ChangeNotice,Creator
```

### Get Change Notices for a Specific Product/Container

```bash
GET /ChangeMgmt/ChangeNotices?$filter=Context/Name eq 'Product Name'&$expand=ChangeTasks
```

### Search by Description

```bash
GET /ChangeMgmt/ChangeNotices?$filter=contains(Description, 'material')
```

### Get Change Notice with Affected Parts

```bash
GET /ChangeMgmt/ChangeNotices('{id}')/AffectedObjects?$expand=Context
```

### Count Open Change Notices

```bash
GET /ChangeMgmt/ChangeNotices/$count?$filter=State/Value eq 'OPEN'
```

---

## State Values

### Change Notice States
- **OPEN** - Open for editing
- **IN_WORK** - Being processed
- **UNDER_REVIEW** - Under review
- **APPROVED** - Approved for implementation
- **IMPLEMENTING** - Being implemented
- **CLOSED** - Completed and closed
- **CANCELLED** - Cancelled

### Change Request States
- **OPEN** - Open for submission
- **UNDER_REVIEW** - Being reviewed
- **APPROVED** - Approved to proceed
- **REJECTED** - Rejected
- **CLOSED** - Closed

### Change Task States
- **NOT_STARTED** - Not yet started
- **IN_PROGRESS** - In progress
- **COMPLETED** - Completed
- **CANCELLED** - Cancelled

---

## Entity Relationships

```
┌─────────────────────────────────────────────────────────────────────────┐
│ PTC.ChangeMgmt Namespace                                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐      ChangeTasks     ┌──────────────┐                │
│  │ ChangeNotice │──────────────────────►│  ChangeTask  │                │
│  ├──────────────┤                       ├──────────────┤                │
│  │ - ChangeTasks│                       │ - Resulting  │                │
│  │ - ChangeReq. │                       │ - ChangeNote │                │
│  │ - Affected   │                       └──────┬───────┘                │
│  │ - Resulting  │                              │                        │
│  └──────┬───────┘                              │                        │
│         │                                      │                        │
│         │ ChangeRequests                       │ ResultingObjects       │
│         │                                      │                        │
│         ▼                                      ▼                        │
│  ┌──────────────┐                       ┌──────────────┐                │
│  │ChangeRequest │                       │  Changeable  │                │
│  ├──────────────┤                       ├──────────────┤                │
│  │ - ChangeNoti│                       │ - Context    │                │
│  │ - Affected   │                       │ - Creator    │                │
│  └──────┬───────┘                       └──────────────┘                │
│         │                                                                │
│         │ AffectedObjects                                                │
│         │                                                                │
│         ▼                                                                │
│  ┌──────────────┐                                                        │
│  │  Changeable  │                                                        │
│  └──────────────┘                                                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Cross-Domain References

| From Entity | Navigation Property | Target Domain | Target Entity |
|-------------|---------------------|---------------|---------------|
| ChangeNotice | Context | DataAdmin | Container |
| ChangeNotice | Creator | PrincipalMgmt | User |
| ChangeNotice | Modifier | PrincipalMgmt | User |
| ChangeNotice | Folder | DataAdmin | Folder |
| ChangeRequest | Context | DataAdmin | Container |
| ChangeRequest | Creator | PrincipalMgmt | User |
| ChangeTask | ChangeNotice | ChangeMgmt | ChangeNotice |
| ChangeTask | Context | DataAdmin | Container |

---

## Pagination

Use `$top` and `$skip` for pagination:

```bash
GET /ChangeMgmt/ChangeNotices?$top=50&$skip=0
GET /ChangeMgmt/ChangeNotices?$top=50&$skip=50
```

---

## Notes

1. **READ-ONLY Access** - Change objects are typically read through OData. Creation and modification are done through Windchill UI or other API endpoints.

2. **Lifecycle Management** - All change objects follow Windchill lifecycle templates with defined state transitions.

3. **Workflow Integration** - Change objects are closely tied to Windchill workflow processes.

4. **Object Identifiers** - IDs are OIDs in format `OR:wt.change2.WTChangeOrder2:xxxxx` for Change Notices.

5. **Affected vs Resulting**:
   - **Affected Objects**: Items that will be impacted by the change
   - **Resulting Objects**: New versions or items created by the change
