# NC Domain Reference

Nonconformance (NC) management in PTC Windchill PLM. This domain handles nonconformance tracking, immediate actions, affected objects, and related quality processes.

## Overview

| Property | Value |
|----------|-------|
| Namespace | PTC.NC |
| Entity Sets | 1 |
| Entity Types | 4 |
| Actions | 7 |
| Complex Types | 0 |

---

## Entity Sets

- **Nonconformances**: Nonconformance

---

## Entity Types

### Nonconformance

Primary entity for tracking nonconformance issues in quality management.

**Key:** `ID`

**Properties (21):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `AssignedTo` | String | Yes | User assigned to the NC |
| `Attachments` | String | Yes | Attachment references |
| `Comments` | String | Yes | Additional comments |
| `CompletionDate` | DateTimeOffset | Yes | Date when NC was completed |
| `CostImpact` | Double | Yes | Financial impact of the NC |
| `CreatedOn` | DateTimeOffset | Yes | Creation timestamp (ReadOnly) |
| `CustomerName` | String | Yes | Customer name if applicable |
| `Description` | String | No | Description of the nonconformance |
| `Disposition` | String | Yes | Disposition decision |
| `ID` | String | Yes | Unique identifier (ReadOnly) |
| `IdentifiedDate` | DateTimeOffset | Yes | Date NC was identified |
| `Impact` | PTC.EnumType | Yes | Impact level |
| `ItemType` | PTC.EnumType | Yes | Type of item affected |
| `LastModified` | DateTimeOffset | Yes | Last modified timestamp (ReadOnly) |
| `Location` | String | Yes | Location where NC occurred |
| `NCNumber` | String | Yes | NC tracking number |
| `Origin` | String | Yes | Origin of the nonconformance |
| `Priority` | PTC.EnumType | Yes | Priority level |
| `Severity` | PTC.EnumType | Yes | Severity level |
| `Source` | String | Yes | Source of the NC report |
| `State` | PTC.EnumType | Yes | Lifecycle state |

**Navigation Properties (10):**

| Navigation | Type | Description |
|------------|------|-------------|
| `AffectedObjects` | Collection(AffectedObject) | Objects affected by the NC |
| `ImmediateActions` | Collection(ImmediateAction) | Immediate actions taken |
| `OtherItems` | Collection(OtherItem) | Other related items |
| `Creator` | User | User who created the NC |
| `Modifier` | User | User who last modified |
| `Owner` | User | Owner of the NC |
| `Assignee` | User | Assigned user |
| `Container` | Container | Container context |
| `Folder` | Folder | Folder location |
| `Process` | Process | Associated process |

---

### AffectedObject

Represents an object affected by a nonconformance.

**Key:** `ID`

**Properties (17):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `Comments` | String | Yes | Comments about the affected object |
| `CreatedOn` | DateTimeOffset | Yes | Creation timestamp (ReadOnly) |
| `Description` | String | No | Description |
| `Disposition` | String | Yes | Disposition for this object |
| `ID` | String | Yes | Unique identifier (ReadOnly) |
| `Impact` | PTC.EnumType | Yes | Impact level |
| `ItemType` | PTC.EnumType | Yes | Type of affected item |
| `LastModified` | DateTimeOffset | Yes | Last modified (ReadOnly) |
| `Name` | String | Yes | Object name |
| `Number` | String | Yes | Object number |
| `ObjectType` | String | Yes | Object type (ReadOnly, NonFilterable) |
| `PartNumber` | String | Yes | Part number if applicable |
| `Quantity` | Double | Yes | Quantity affected |
| `Revision` | String | Yes | Revision of the object |
| `SerialNumber` | String | Yes | Serial number if applicable |
| `State` | PTC.EnumType | Yes | State of the affected object |
| `Version` | String | Yes | Version information |

**Navigation Properties (2):**

| Navigation | Type | Description |
|------------|------|-------------|
| `ParentNC` | Nonconformance | Parent nonconformance |
| `RelatedObject` | ManagedObject | The actual affected object |

---

### ImmediateAction

Represents an immediate action taken for a nonconformance.

**Key:** `ID`

**Properties (9):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `ActionDate` | DateTimeOffset | Yes | Date of the action |
| `ActionType` | PTC.EnumType | Yes | Type of action taken |
| `Comments` | String | Yes | Action comments |
| `CompletedDate` | DateTimeOffset | Yes | Completion date |
| `CreatedOn` | DateTimeOffset | Yes | Creation timestamp (ReadOnly) |
| `Description` | String | No | Action description |
| `ID` | String | Yes | Unique identifier (ReadOnly) |
| `LastModified` | DateTimeOffset | Yes | Last modified (ReadOnly) |
| `Status` | PTC.EnumType | Yes | Action status |

---

### OtherItem

Represents other items related to a nonconformance.

**Key:** `ID`

**Properties (13):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `Comments` | String | Yes | Item comments |
| `CreatedOn` | DateTimeOffset | Yes | Creation timestamp (ReadOnly) |
| `Description` | String | No | Item description |
| `ID` | String | Yes | Unique identifier (ReadOnly) |
| `ItemID` | String | No | Item identifier |
| `ItemState` | PTC.EnumType | Yes | Item state |
| `ItemType` | PTC.EnumType | Yes | Item type |
| `LastModified` | DateTimeOffset | Yes | Last modified (ReadOnly) |
| `ObjectType` | String | Yes | Object type (ReadOnly, NonFilterable) |
| `PurchaseOrderNumber` | String | Yes | PO number if applicable |
| `Quantity` | Double | No | Quantity |
| `Unit` | PTC.EnumType | No | Unit of measure |
| `UnitID` | String | Yes | Unit identifier |

**Navigation Properties (1):**

| Navigation | Type | Description |
|------------|------|-------------|
| `ImmediateActions` | Collection(ImmediateAction) | Actions for this item |

---

## Actions (7)

### Unbound Actions

#### SetStateNonconformances

Set state for multiple nonconformances.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Nonconformances` | Collection(String) | No |
| `State` | String | No |

---

### Bound Actions

#### SetState

Set the lifecycle state of a nonconformance.

**Bound To:** `Nonconformance`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `State` | String | No |

---

#### Reserve

Reserve (check out) a nonconformance for editing.

**Bound To:** `Nonconformance`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `ReservationNote` | String | Yes |

---

#### UndoReservation

Undo reservation (undo check out) for a nonconformance.

**Bound To:** `Nonconformance`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Nonconformance` | Nonconformance | No |

---

#### UploadStage1Action

Upload stage 1 action for a nonconformance.

**Bound To:** `Nonconformance`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `ContentID` | String | No |
| `FileName` | String | No |
| `FileContent` | Binary | No |

---

#### UploadStage3Action

Complete upload for a nonconformance.

**Bound To:** `Nonconformance`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `ContentID` | String | No |
| `FileName` | String | No |

---

#### EditNonconformancesSecurityLabels

Edit security labels for nonconformances.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `SecurityLabels` | Collection(SecurityLabel) | No |

---

## Usage Examples

### Query Nonconformances

```python
from domains.NC import NCClient
client = NCClient(config_path="config.json")

# Get all nonconformances
ncs = client.get_nonconformances(top=50)

# Get by number
nc = client.get_nonconformance_by_number("NC-2024-001")

# Get by state
open_ncs = client.get_nonconformances_by_state("OPEN")
closed_ncs = client.get_nonconformances_by_state("CLOSED")

# Get with expanded navigation
nc = client.get_nonconformance_by_id(nc_id, expand=[
    "AffectedObjects",
    "ImmediateActions",
    "Creator",
    "Owner"
])
```

### Create Nonconformance

```python
# Create a new nonconformance
nc = client.create_nonconformance(
    description="Material defect in batch A-123",
    identified_date="2024-01-15T10:00:00Z",
    source="Incoming Inspection",
    priority="HIGH",
    severity="MAJOR",
    location="Warehouse A",
    assigned_to="OR:wt.org.WTUser:12345"
)
```

### Manage Affected Objects

```python
# Add affected object
affected = client.add_affected_object(
    nc_id=nc["ID"],
    name="Part-001",
    number="PART-001",
    part_number="PART-001",
    quantity=100,
    disposition="Scrap"
)

# Get affected objects
objects = client.get_affected_objects(nc_id)
```

### Manage Immediate Actions

```python
# Add immediate action
action = client.add_immediate_action(
    nc_id=nc["ID"],
    description="Quarantine affected batch",
    action_type="CONTAINMENT",
    action_date="2024-01-15T12:00:00Z"
)

# Get immediate actions
actions = client.get_immediate_actions(nc_id)
```

### Lifecycle Management

```python
# Set state
client.set_nonconformance_state(nc_id, "IN_REVIEW")

# Reserve (check out)
client.reserve_nonconformance(nc_id, reservation_note="Reviewing NC")

# Undo reservation
client.undo_reservation_nonconformance(nc_id)
```

### File Attachments

```python
# Upload attachment
client.upload_attachment(
    nc_id=nc["ID"],
    file_name="inspection_report.pdf",
    file_path="/path/to/file.pdf"
)
```

---

## Related Files

| File | Description |
|------|-------------|
| NC_Entities.json | Machine-readable entity definitions |
| NC_Navigations.md | Navigation properties reference |
| NC_Actions.md | OData actions reference |
| NC_Metadata.xml | Raw OData metadata |
