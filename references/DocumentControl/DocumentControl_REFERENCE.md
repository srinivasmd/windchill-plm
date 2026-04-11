# DocumentControl Domain Reference

DocumentControl domain in PTC Windchill PLM.

## Overview

| Property | Value |
|----------|-------|
| Namespace | PTC.DocumentControl |
| Entity Sets | 1 |
| Entity Types | 2 |
| Actions | 2 |
| Complex Types | 0 |

---

## Entity Sets

- **TrainingRecords**: PTC.DocumentControl.TrainingRecord

## Entity Types

### ControlDocument

**Properties (19):**

| Property | Type | Nullable | Annotations |
|----------|------|----------|-------------|
| `CreatedBy` | `String` | Yes | ReadOnly |
| `Description` | `String` | Yes | - |
| `Identity` | `String` | Yes | NonFilterable, NonSortable |
| `Latest` | `Boolean` | Yes | ReadOnly |
| `LifeCycleTemplateName` | `String` | Yes | Immutable, NonFilterable, NonSortable |
| `LinkToTraining` | `String` | Yes | NonFilterable, NonSortable |
| `MasterID` | `String` | Yes | ReadOnly |
| `ModifiedBy` | `String` | Yes | ReadOnly |
| `Name` | `String` | Yes | - |
| `Number` | `String` | Yes | - |
| `OrganizationName` | `String` | Yes | ReadOnly, NonSortable, NonFilterable |
| `Revision` | `String` | Yes | ReadOnly |
| `State` | `EnumType` | Yes | ReadOnly |
| `TrainingDeadline` | `String` | Yes | NonFilterable, NonSortable |
| `TrainingInterval` | `Int64` | Yes | NonFilterable, NonSortable |
| `TrainingIntervalLeadtime` | `Int64` | Yes | NonFilterable, NonSortable |
| `TrainingonRelease` | `Boolean` | Yes | NonFilterable, NonSortable |
| `Version` | `String` | Yes | ReadOnly, NonFilterable, NonSortable |
| `VersionID` | `String` | Yes | ReadOnly, NonFilterable, NonSortable |

**Navigation Properties (11):**

- `Context` -> Container
- `Versions` -> ControlDocument
- `Organization` -> Organization
- `PrimaryContent` -> ContentItem
- `Thumbnails` -> ContentItem
- `Creator` -> User
- `Representations` -> Representation
- `SmallThumbnails` -> ContentItem
- `Revisions` -> ControlDocument
- `Attachments` -> ContentItem
- `Modifier` -> User

---

### TrainingRecord

**Properties (11):**

| Property | Type | Nullable | Annotations |
|----------|------|----------|-------------|
| `Comment` | `String` | Yes | - |
| `CompletedDate` | `DateTimeOffset` | Yes | - |
| `CreatedBy` | `String` | Yes | ReadOnly |
| `ExpirationDate` | `DateTimeOffset` | Yes | - |
| `LifeCycleTemplateName` | `String` | Yes | Immutable, NonFilterable, NonSortable |
| `MasterID` | `String` | Yes | ReadOnly |
| `ModifiedBy` | `String` | Yes | ReadOnly |
| `Name` | `String` | No | - |
| `Number` | `String` | No | - |
| `ObjectType` | `String` | Yes | ReadOnly, NonFilterable, NonSortable |
| `State` | `EnumType` | Yes | ReadOnly |

**Navigation Properties (5):**

- `SubjectControlDocument` -> ControlDocument
- `Assignee` -> Principal
- `Context` -> Container
- `Creator` -> User
- `Modifier` -> User

---

## Related Files

| File | Description |
|------|-------------|
| DocumentControl_Entities.json | Machine-readable entity definitions |
| DocumentControl_Navigations.md | Navigation properties reference |
| DocumentControl_Actions.md | OData actions reference |
| DocumentControl_Metadata.xml | Raw OData metadata |
