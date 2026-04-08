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

The Change Management domain provides access to change control objects in Windchill including:

### Change Objects
- **ChangeNotice** - Engineering Change Notices (ECN)
- **ChangeRequest** - Change Requests (ECR)
- **ChangeTask** - Change Tasks
- **ChangeActivity2** - Change Activities
- **ChangeOrder** - Change Orders

### Related Objects
- **AffectedObject** - Objects affected by changes
- **ResultingObject** - Objects resulting from changes
- **Changeable** - Objects that can be changed (parts, documents)

---

## Entity Types

### ChangeNotice

Engineering Change Notice (ECN) - Formal documentation of a proposed change.

**Endpoint:** `/ChangeMgmt/ChangeNotices`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Change Notice name |
| **Number** | String | Change Notice number (unique identifier) |
| **Description** | String | Detailed description of the change |
| **State** | EnumType | Lifecycle state (ReadOnly) |
| **LifeCycleTemplateName** | String | Lifecycle template name (ReadOnly) |
| **FolderLocation** | String | Folder path in Windchill |
| **Version** | String | Version information (A.1, A.2, etc.) |
| **Iteration** | String | Iteration information |
| **MasterID** | String | Master ID (ReadOnly) |
| **CreatedBy** | String | Created by (ReadOnly) |
| **ModifiedBy** | String | Modified by (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` - Container (PTC.DataAdmin.Container)
- `Creator` - Creator user (PTC.PrincipalMgmt.User)
- `Modifier` - Modifier user (PTC.PrincipalMgmt.User)
- `ChangeRequest` - Related Change Request
- `ChangeTasks` - Collection of Change Tasks
- `AffectedObjects` - Objects affected by this change
- `ResultingObjects` - Objects resulting from this change
- `ChangeActivities` - Related Change Activities

**CRUD Operations:**

```bash
# Get all change notices
GET /ChangeMgmt/ChangeNotices

# Get change notice by ID
GET /ChangeMgmt/ChangeNotices('{id}')

# Get change notice by number
GET /ChangeMgmt/ChangeNotices?$filter=Number eq 'CN-000001'

# Get change notice by name
GET /ChangeMgmt/ChangeNotices?$filter=Name eq 'Engine Assembly Change'

# Search by number or name
GET /ChangeMgmt/ChangeNotices?$filter=contains(Number, 'CN') or contains(Name, 'Assembly')

# Filter by state
GET /ChangeMgmt/ChangeNotices?$filter=State/Value eq 'OPEN'

# Expand with context
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=Context

# Expand with change tasks
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=ChangeTasks

# Expand with affected objects
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=AffectedObjects

# Expand with resulting objects
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=ResultingObjects

# Expand all navigation properties
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=Context,Creator,Modifier,ChangeTasks,AffectedObjects,ResultingObjects

# Select specific properties
GET /ChangeMgmt/ChangeNotices?$select=ID,Name,Number,State,Description

# Order by
GET /ChangeMgmt/ChangeNotices?$orderby=CreatedOn desc
GET /ChangeMgmt/ChangeNotices?$orderby=Number asc

# Create change notice
POST /ChangeMgmt/ChangeNotices
Content-Type: application/json
X-CSRF-Token: {token}

{
  "Name": "Engine Assembly Design Change",
  "Number": "CN-000001",
  "Description": "Update engine assembly to incorporate new piston design",
  "FolderLocation": "/Default/Engineering/Changes"
}

# Update change notice
PATCH /ChangeMgmt/ChangeNotices('{id}')
Content-Type: application/json
X-CSRF-Token: {token}

{
  "Description": "Updated description with additional details"
}
```

---

### ChangeRequest

Change Request (ECR) - Request for a change before formal approval.

**Endpoint:** `/ChangeMgmt/ChangeRequests`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Change Request name |
| **Number** | String | Change Request number (unique identifier) |
| **Description** | String | Detailed description of the requested change |
| **State** | EnumType | Lifecycle state (ReadOnly) |
| **LifeCycleTemplateName** | String | Lifecycle template name (ReadOnly) |
| **FolderLocation** | String | Folder path in Windchill |
| **NeedDate** | DateTimeOffset | Date by which change is needed |
| **Justification** | String | Business justification for the change |
| **MasterID** | String | Master ID (ReadOnly) |
| **CreatedBy** | String | Created by (ReadOnly) |
| **ModifiedBy** | String | Modified by (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` - Container (PTC.DataAdmin.Container)
- `Creator` - Creator user (PTC.PrincipalMgmt.User)
- `Modifier` - Modifier user (PTC.PrincipalMgmt.User)
- `ChangeNotices` - Related Change Notices
- `AffectedObjects` - Objects affected by this request
- `ChangeActivities` - Related Change Activities

**CRUD Operations:**

```bash
# Get all change requests
GET /ChangeMgmt/ChangeRequests

# Get change request by number
GET /ChangeMgmt/ChangeRequests?$filter=Number eq 'CR-000001'

# Filter by state
GET /ChangeMgmt/ChangeRequests?$filter=State/Value eq 'SUBMITTED'

# Filter by need date
GET /ChangeMgmt/ChangeRequests?$filter=NeedDate ge 2026-03-01T00:00:00Z

# Expand with change notices
GET /ChangeMgmt/ChangeRequests('{id}')?$expand=ChangeNotices

# Expand with affected objects
GET /ChangeMgmt/ChangeRequests('{id}')?$expand=AffectedObjects

# Create change request
POST /ChangeMgmt/ChangeRequests
Content-Type: application/json
X-CSRF-Token: {token}

{
  "Name": "Piston Material Change Request",
  "Number": "CR-000001",
  "Description": "Request to change piston material from aluminum to titanium",
  "Justification": "Weight reduction and improved durability",
  "NeedDate": "2026-04-01T00:00:00Z",
  "FolderLocation": "/Default/Engineering/Changes"
}
```

---

### ChangeTask

Change Task - Individual task within a Change Notice.

**Endpoint:** `/ChangeMgmt/ChangeTasks`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Change Task name |
| **Number** | String | Change Task number |
| **Description** | String | Task description |
| **State** | EnumType | Lifecycle state (ReadOnly) |
| **LifeCycleTemplateName** | String | Lifecycle template name (ReadOnly) |
| **FolderLocation** | String | Folder path in Windchill |
| **MasterID** | String | Master ID (ReadOnly) |
| **CreatedBy** | String | Created by (ReadOnly) |
| **ModifiedBy** | String | Modified by (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` - Container (PTC.DataAdmin.Container)
- `Creator` - Creator user (PTC.PrincipalMgmt.User)
- `Modifier` - Modifier user (PTC.PrincipalMgmt.User)
- `ChangeNotice` - Parent Change Notice
- `AffectedObjects` - Objects affected by this task
- `ResultingObjects` - Objects resulting from this task

**CRUD Operations:**

```bash
# Get all change tasks
GET /ChangeMgmt/ChangeTasks

# Get change task by number
GET /ChangeMgmt/ChangeTasks?$filter=Number eq 'CT-000001'

# Get tasks for a specific change notice
GET /ChangeMgmt/ChangeNotices('{id}')/ChangeTasks

# Expand with change notice
GET /ChangeMgmt/ChangeTasks('{id}')?$expand=ChangeNotice

# Create change task (via change notice)
POST /ChangeMgmt/ChangeNotices('{id}')/ChangeTasks
Content-Type: application/json
X-CSRF-Token: {token}

{
  "Name": "Update Part Design",
  "Number": "CT-000001",
  "Description": "Modify the part design according to change requirements"
}
```

---

### ChangeActivity2

Change Activity - Detailed activity within a change process.

**Endpoint:** `/ChangeMgmt/ChangeActivities`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Activity name |
| **Number** | String | Activity number |
| **Description** | String | Activity description |
| **State** | EnumType | Lifecycle state (ReadOnly) |
| **LifeCycleTemplateName** | String | Lifecycle template name (ReadOnly) |
| **MasterID** | String | Master ID (ReadOnly) |
| **CreatedBy** | String | Created by (ReadOnly) |
| **ModifiedBy** | String | Modified by (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- `Context` - Container (PTC.DataAdmin.Container)
- `Creator` - Creator user (PTC.PrincipalMgmt.User)
- `Modifier` - Modifier user (PTC.PrincipalMgmt.User)
- `ChangeNotice` - Related Change Notice
- `ChangeRequest` - Related Change Request
- `AffectedObjects` - Objects affected by this activity
- `ResultingObjects` - Objects resulting from this activity

**CRUD Operations:**

```bash
# Get all change activities
GET /ChangeMgmt/ChangeActivities

# Get change activity by ID
GET /ChangeMgmt/ChangeActivities('{id}')

# Filter by state
GET /ChangeMgmt/ChangeActivities?$filter=State/Value eq 'COMPLETED'

# Expand with affected objects
GET /ChangeMgmt/ChangeActivities('{id}')?$expand=AffectedObjects,ResultingObjects
```

---

### AffectedObject

Objects affected by a change (parts, documents, etc.).

**Endpoint:** Navigation property from Change entities

**Operations:** `READ`, `CREATE`, `DELETE`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **ObjectType** | String | Type of affected object |
| **Name** | String | Object name |
| **Number** | String | Object number |
| **Version** | String | Version information |
| **State** | EnumType | Object state |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- `Changeable` - The actual object being affected
- `ChangeActivity2` - Related Change Activity
- `ChangeNotice` - Related Change Notice

**CRUD Operations:**

```bash
# Get affected objects for a change notice
GET /ChangeMgmt/ChangeNotices('{id}')/AffectedObjects

# Get affected objects for a change activity
GET /ChangeMgmt/ChangeActivities('{id}')/AffectedObjects

# Expand with the actual object
GET /ChangeMgmt/ChangeNotices('{id}')/AffectedObjects?$expand=Changeable
```

---

### ResultingObject

Objects created or modified as a result of a change.

**Endpoint:** Navigation property from Change entities

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **ObjectType** | String | Type of resulting object |
| **Name** | String | Object name |
| **Number** | String | Object number |
| **Version** | String | Version information |
| **State** | EnumType | Object state |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- `ResultingChangeable` - The actual resulting object
- `ChangeActivity2` - Related Change Activity
- `ChangeNotice` - Related Change Notice

**CRUD Operations:**

```bash
# Get resulting objects for a change notice
GET /ChangeMgmt/ChangeNotices('{id}')/ResultingObjects

# Get resulting objects for a change activity
GET /ChangeMgmt/ChangeActivities('{id}')/ResultingObjects

# Expand with the actual object
GET /ChangeMgmt/ChangeNotices('{id}')/ResultingObjects?$expand=ResultingChangeable
```

---

## Actions

### SetState

Set the lifecycle state for a change object.

**Action Signature:**
```
PTC.ChangeMgmt.SetState(lifecycleManaged, State) -> ChangeObject
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| **lifecycleManaged** | ChangeObject | Change object to update |
| **State** | EnumType | Target state |

**Usage Example:**

```bash
POST /ChangeMgmt/ChangeNotices('{id}')/PTC.ChangeMgmt.SetState
Content-Type: application/json
X-CSRF-Token: {token}

{
  "State": {"Value": "RELEASED"}
}
```

---

## Functions

### GetLifeCycleTemplate

Get the lifecycle template for a change object.

**Function Signature:**
```
PTC.ChangeMgmt.GetLifeCycleTemplate(lifecycleManaged) -> LifeCycleTemplate
```

**Usage Example:**

```bash
GET /ChangeMgmt/ChangeNotices('{id}')/PTC.ChangeMgmt.GetLifeCycleTemplate
```

---

### GetValidStateTransitions

Get valid state transitions for a change object.

**Function Signature:**
```
PTC.ChangeMgmt.GetValidStateTransitions(lifecycleManaged) -> EnumTypeList
```

**Usage Example:**

```bash
GET /ChangeMgmt/ChangeNotices('{id}')/PTC.ChangeMgmt.GetValidStateTransitions
```

**Response:**
```json
{
  "@odata.context": "...",
  "value": ["IN_WORK", "SUBMITTED", "APPROVED", "RELEASED", "CANCELLED"]
}
```

---

## Common Query Examples

### Filter by Multiple Criteria

```bash
# Get open change notices created in a date range
GET /ChangeMgmt/ChangeNotices?$filter=State/Value eq 'OPEN' and CreatedOn ge 2026-02-01T00:00:00Z and CreatedOn le 2026-02-28T23:59:59Z

# Get change requests by state
GET /ChangeMgmt/ChangeRequests?$filter=State/Value eq 'SUBMITTED'

# Get change tasks by state
GET /ChangeMgmt/ChangeTasks?$filter=State/Value eq 'IN_WORK'
```

### Complex Queries with Expansion

```bash
# Get change notice with all related data
GET /ChangeMgmt/ChangeNotices?$expand=Context,Creator,ChangeTasks,AffectedObjects,ResultingObjects

# Get change request with change notices
GET /ChangeMgmt/ChangeRequests?$expand=ChangeNotices,AffectedObjects

# Get change activity with affected and resulting objects
GET /ChangeMgmt/ChangeActivities?$expand=AffectedObjects,ResultingObjects,ChangeNotice,ChangeRequest
```

### Sorting and Pagination

```bash
# Get latest change notices
GET /ChangeMgmt/ChangeNotices?$orderby=CreatedOn desc&$top=50

# Get paginated results
GET /ChangeMgmt/ChangeNotices?$skip=0&$top=25

# Get sorted by name with pagination
GET /ChangeMgmt/ChangeNotices?$orderby=Name asc&$skip=25&$top=25
```

---

## Change Process Workflow

Typical change management workflow in Windchill:

1. **Create Change Request (ECR)**
   - Submit request with justification
   - Add affected objects
   - Route for review

2. **Review Change Request**
   - Reviewers evaluate request
   - Approve or reject
   - Add comments

3. **Create Change Notice (ECN)**
   - Create from approved request
   - Define change tasks
   - Assign to implementers

4. **Execute Change Tasks**
   - Update affected objects
   - Create new versions
   - Document changes

5. **Review and Release**
   - Review all changes
   - Approve and release
   - Update resulting objects

---

## Integration Notes

1. **Object Relationships**:
   - ChangeNotice can have multiple ChangeTasks
   - ChangeRequest can have multiple ChangeNotices
   - Each task affects specific objects

2. **Lifecycle Management**:
   - Change objects follow lifecycle templates
   - State transitions vary by template
   - Use GetValidStateTransitions to check valid transitions

3. **Cross-Domain References**:
   - Affected/Resulting objects can be Parts (ProdMgmt)
   - Documents (DocMgmt) can be affected
   - CAD Documents (CADDocumentMgmt) can be affected

4. **Workflow Integration**:
   - Change objects use Windchill Workflow engine
   - Check Workflow domain for work items
   - Activities track workflow progress

---

## Schema Version

Schema Version: 7
