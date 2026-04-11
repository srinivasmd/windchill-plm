# CAPA Domain Reference

Corrective and Preventive Action (CAPA) management in PTC Windchill PLM.

## Overview

| Property | Value |
|----------|-------|
| Namespace | PTC.CAPA |
| Entity Sets | 1 |
| Entity Types | 6 |
| Actions | 6 |

---

## Entity Sets

- **CAPAs**: PTC.CAPA.CAPA

## Entity Types

### CAPA

The main CAPA entity representing a Corrective and Preventive Action.

**Key Properties:**
- `Number`: Unique identifier (read-only)
- `Name`: CAPA name
- `Description`: CAPA description
- `DueDate`: Target completion date
- `InvestigationCompleted`: Boolean flag
- `State`: Lifecycle state

**Properties (25):**

| Property | Type | Nullable | Annotations |
|----------|------|----------|-------------|
| `CAPAKey` | `String` | Yes | ReadOnly |
| `ControlAuthority` | `EnumType` | Yes | - |
| `CreatedBy` | `String` | Yes | ReadOnly |
| `Description` | `String` | Yes | - |
| `DueDate` | `DateTimeOffset` | Yes | ReadOnly |
| `InvestigationCompleted` | `Boolean` | No | - |
| `LifeCycleTemplateName` | `String` | Yes | Immutable, NonFilterable, NonSortable |
| `MasterID` | `String` | Yes | ReadOnly |
| `ModifiedBy` | `String` | Yes | ReadOnly |
| `Name` | `String` | No | - |
| `Number` | `String` | Yes | ReadOnly |
| `ObjectType` | `String` | Yes | ReadOnly, NonFilterable, NonSortable |
| `ProductAffected` | `Boolean` | Yes | ReadOnly |
| `ReferenceRecordID` | `String` | Yes | - |
| `ReferenceRecordType` | `EnumType` | Yes | - |
| ... | (10 more properties) | | |

**Navigation Properties (12):**

- `PrimarySite` -> CAPASite
- `AdditionalSites` -> CAPASite
- `AffectedObjects` -> AffectedObject
- `Plan` -> CAPAActionPlan
- `Context` -> Container
- `PrimaryRelatedPersonOrLocation` -> QualityContact
- `Thumbnails` -> ContentItem
- `Creator` -> User
- `SmallThumbnails` -> ContentItem
- `Attachments` -> ContentItem
- `Modifier` -> User
- `AdditionalRelatedPersonnelOrLocations` -> QualityContact

---

### CAPASite

Site/location associated with a CAPA.

**Properties (4):**

| Property | Type | Nullable | Annotations |
|----------|------|----------|-------------|
| `CreatedOn` | `DateTimeOffset` | Yes | ReadOnly |
| `ID` | `String` | Yes | ReadOnly |
| `LastModified` | `DateTimeOffset` | Yes | ReadOnly |
| `PrimaryOriginating` | `Boolean` | Yes | ReadOnly |

**Navigation Properties (1):**

- `Place` -> Place

---

### ActionSubject

Subject associated with an action (person, place, or thing).

**Properties (3):**

| Property | Type | Nullable | Annotations |
|----------|------|----------|-------------|
| `CreatedOn` | `DateTimeOffset` | Yes | ReadOnly |
| `ID` | `String` | Yes | ReadOnly |
| `LastModified` | `DateTimeOffset` | Yes | ReadOnly |

**Navigation Properties (1):**

- `Subject` -> Subject

---

### CAPAActionPlan

Action Plan associated with a CAPA containing multiple actions.

**Key Properties:**
- `Name`: Plan name
- `Description`: Plan description
- `ApprovalRequired`: Whether approval is needed

**Properties (19):**

| Property | Type | Nullable | Annotations |
|----------|------|----------|-------------|
| `ApprovalRequired` | `Boolean` | Yes | ReadOnly, NonFilterable, NonSortable |
| `CreatedBy` | `String` | Yes | ReadOnly |
| `CreatedOn` | `DateTimeOffset` | Yes | ReadOnly |
| `Description` | `String` | Yes | - |
| `ID` | `String` | Yes | ReadOnly |
| `LastModified` | `DateTimeOffset` | Yes | ReadOnly |
| `Latest` | `Boolean` | Yes | ReadOnly |
| `LifeCycleTemplateName` | `String` | Yes | Immutable, NonFilterable, NonSortable |
| `MasterID` | `String` | Yes | ReadOnly |
| `ModifiedBy` | `String` | Yes | ReadOnly |
| `Name` | `String` | Yes | - |
| `Number` | `String` | Yes | ReadOnly |
| `ObjectType` | `String` | Yes | ReadOnly, NonFilterable, NonSortable |
| `PlanAdditionalInformation` | `String` | Yes | - |
| `Revision` | `String` | Yes | ReadOnly, NonFilterable, NonSortable |
| ... | (4 more properties) | | |

**Navigation Properties (5):**

- `Actions` -> Action
- `Versions` -> CAPAActionPlan
- `Creator` -> User
- `Revisions` -> CAPAActionPlan
- `Modifier` -> User

---

### Action

Individual action within a CAPA Action Plan.

**Key Properties:**
- `Name`: Action name
- `Description`: Action description
- `DueDate`: Target completion date
- `Owner`: Responsible person
- `Status`: Action status

**Properties (26):**

| Property | Type | Nullable | Annotations |
|----------|------|----------|-------------|
| `ActionID` | `String` | Yes | ReadOnly |
| `ActionType` | `EnumType` | No | - |
| `ApprovalRequired` | `Boolean` | Yes | ReadOnly |
| `ChangeNoticeRequired` | `Boolean` | No | - |
| `ChangeNoticeType` | `String` | Yes | Description |
| `ConfirmationMeasure` | `String` | Yes | NonFilterable, NonSortable |
| `ConfirmationRequired` | `Boolean` | No | - |
| `ConfirmationType` | `EnumType` | Yes | Description, NonFilterable, NonSortable |
| `CreatedBy` | `String` | Yes | ReadOnly |
| `CreatedOn` | `DateTimeOffset` | Yes | ReadOnly |
| `Description` | `String` | Yes | - |
| `EffectivenessApprovalRequired` | `Boolean` | Yes | Description, NonFilterable, NonSortable |
| `EffectivenessEndDate` | `DateTimeOffset` | Yes | NonFilterable, NonSortable |
| `EffectivenessMeasure` | `String` | Yes | NonFilterable, NonSortable |
| `EffectivenessRequired` | `Boolean` | No | - |
| ... | (11 more properties) | | |

**Navigation Properties (4):**

- `ChangeNoticeContext` -> Container
- `ActionSubjects` -> ActionSubject
- `Creator` -> User
- `Modifier` -> User

---

### AffectedObject

Object affected by the CAPA (e.g., parts, documents).

**Properties (20):**

| Property | Type | Nullable | Annotations |
|----------|------|----------|-------------|
| `CapaLotNumber` | `String` | Yes | ReadOnly, NonFilterable, NonSortable |
| `CreatedOn` | `DateTimeOffset` | Yes | ReadOnly |
| `ID` | `String` | Yes | ReadOnly |
| `LastModified` | `DateTimeOffset` | Yes | ReadOnly |
| `LotControlled` | `Boolean` | Yes | - |
| `LotSerialNumber` | `String` | Yes | - |
| `LotSerialRangeFrom` | `String` | Yes | - |
| `LotSerialRangeTo` | `String` | Yes | - |
| `ManufacturedFrom` | `DateTimeOffset` | Yes | - |
| `ManufacturedQuantity` | `String` | Yes | - |
| `ManufacturedTo` | `DateTimeOffset` | Yes | - |
| `ManufacturedUnits` | `EnumType` | Yes | - |
| `Name` | `String` | Yes | ReadOnly, NonFilterable, NonSortable |
| `Number` | `String` | Yes | ReadOnly, NonFilterable, NonSortable |
| `ObjectType` | `String` | Yes | ReadOnly, NonFilterable, NonSortable |
| ... | (5 more properties) | | |

**Navigation Properties (1):**

- `Subject` -> Subject

---

## Related Files

| File | Description |
|------|-------------|
| CAPA_Entities.json | Machine-readable entity definitions |
| CAPA_Navigations.md | Navigation properties reference |
| CAPA_Actions.md | OData actions reference |
| CAPA_Metadata.xml | Raw OData metadata |
