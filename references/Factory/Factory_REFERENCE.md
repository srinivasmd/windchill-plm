# Factory Domain Reference

Factory management in PTC Windchill PLM.

## Overview

| Property | Value |
|----------|-------|
| Namespace | PTC.Factory |
| Entity Sets | 6 |
| Entity Types | 14 |
| Actions | 42 |

---

## Entity Sets

- **Documents**: Document
- **StandardControlCharacteristics**: StandardControlCharacteristic
- **Resources**: Resource
- **StandardProcedures**: StandardProcedure
- **StandardOperations**: StandardOperation
- **ReferenceDocuments**: ReferenceDocument

## Entity Types

### Document

**Properties (24):**

| Property | Type | Nullable |
|----------|------|----------|
| `ChangeStatus` | `Icon` | Yes |
| `CheckOutStatus` | `String` | Yes |
| `CheckoutState` | `String` | Yes |
| `Comments` | `String` | Yes |
| `CreatedBy` | `String` | Yes |
| `CreatedOn` | `DateTimeOffset` | Yes |
| `Description` | `String` | Yes |
| `GeneralStatus` | `Icon` | Yes |
| `ID` | `String` | Yes |
| `Identity` | `String` | Yes |
| ... | (14 more) | |

**Navigation Properties (6):**

- `Context` -> Container
- `Versions` -> Document
- `Creator` -> User
- `Representations` -> Representation
- `Revisions` -> Document
- `Modifier` -> User

---

### StandardProcedureUsage

**Properties (4):**

| Property | Type | Nullable |
|----------|------|----------|
| `CreatedOn` | `DateTimeOffset` | Yes |
| `ExpressionData` | `String` | Yes |
| `ID` | `String` | Yes |
| `LastModified` | `DateTimeOffset` | Yes |

**Navigation Properties (1):**

- `SPL` -> StandardProcedure

---

### SCCStandardProcedureUsage

**Properties (4):**

| Property | Type | Nullable |
|----------|------|----------|
| `CreatedOn` | `DateTimeOffset` | Yes |
| `ExpressionData` | `String` | Yes |
| `ID` | `String` | Yes |
| `LastModified` | `DateTimeOffset` | Yes |

**Navigation Properties (1):**

- `SCCSPL` -> StandardProcedure

---

### Resource

**Properties (10):**

| Property | Type | Nullable |
|----------|------|----------|
| `CreatedBy` | `String` | Yes |
| `CreatedOn` | `DateTimeOffset` | Yes |
| `Description` | `String` | Yes |
| `ID` | `String` | Yes |
| `LastModified` | `DateTimeOffset` | Yes |
| `MasterID` | `String` | Yes |
| `ModifiedBy` | `String` | Yes |
| `Name` | `String` | Yes |
| `Number` | `String` | Yes |
| `Version` | `String` | Yes |

**Navigation Properties (2):**

- `Creator` -> User
- `Modifier` -> User

---

### StandardProcedure

**Properties (20):**

| Property | Type | Nullable |
|----------|------|----------|
| `CheckOutStatus` | `String` | Yes |
| `CheckoutState` | `String` | Yes |
| `Comments` | `String` | Yes |
| `CreatedBy` | `String` | Yes |
| `CreatedOn` | `DateTimeOffset` | Yes |
| `Description` | `String` | Yes |
| `ID` | `String` | Yes |
| `LastModified` | `DateTimeOffset` | Yes |
| `Latest` | `Boolean` | Yes |
| `LifeCycleTemplateName` | `String` | Yes |
| ... | (10 more) | |

**Navigation Properties (5):**

- `Context` -> Container
- `Versions` -> StandardProcedure
- `Creator` -> User
- `Revisions` -> StandardProcedure
- `Modifier` -> User

---

### ResourceUsage

**Properties (4):**

| Property | Type | Nullable |
|----------|------|----------|
| `CreatedOn` | `DateTimeOffset` | Yes |
| `ExpressionData` | `String` | Yes |
| `ID` | `String` | Yes |
| `LastModified` | `DateTimeOffset` | Yes |

**Navigation Properties (1):**

- `Tools` -> Resource

---

### SCCResourceUsage

**Properties (4):**

| Property | Type | Nullable |
|----------|------|----------|
| `CreatedOn` | `DateTimeOffset` | Yes |
| `ExpressionData` | `String` | Yes |
| `ID` | `String` | Yes |
| `LastModified` | `DateTimeOffset` | Yes |

**Navigation Properties (1):**

- `SCCTools` -> Resource

---

### SCCReferenceDocument

**Properties (4):**

| Property | Type | Nullable |
|----------|------|----------|
| `CreatedOn` | `DateTimeOffset` | Yes |
| `ExpressionData` | `String` | Yes |
| `ID` | `String` | Yes |
| `LastModified` | `DateTimeOffset` | Yes |

**Navigation Properties (1):**

- `SCCRefDocuments` -> Document

---

### DescribedByDocument

**Properties (4):**

| Property | Type | Nullable |
|----------|------|----------|
| `CreatedOn` | `DateTimeOffset` | Yes |
| `ExpressionData` | `String` | Yes |
| `ID` | `String` | Yes |
| `LastModified` | `DateTimeOffset` | Yes |

**Navigation Properties (1):**

- `DescribedBy` -> Document

---

### StandardControlCharacteristic

**Properties (41):**

| Property | Type | Nullable |
|----------|------|----------|
| `AlternateNumber` | `String` | Yes |
| `AwaitingPromotion` | `Boolean` | Yes |
| `BOMType` | `String` | Yes |
| `Category` | `String` | Yes |
| `CheckOutStatus` | `String` | Yes |
| `CheckedOutBy` | `String` | Yes |
| `CheckinComments` | `String` | Yes |
| `CheckoutState` | `String` | Yes |
| `Comments` | `String` | Yes |
| `Context` | `String` | Yes |
| ... | (31 more) | |

**Navigation Properties (9):**

- `SCCDDLinks` -> SCCDescribedByDocument
- `SCCDRLinks` -> SCCReferenceDocument
- `SCCResourceLinks` -> SCCResourceUsage
- `SCCSPLinks` -> SCCStandardProcedureUsage
- `Context` -> Container
- `Versions` -> StandardControlCharacteristic
- `Creator` -> User
- `Revisions` -> StandardControlCharacteristic
- `Modifier` -> User

---

### StandardOperation

**Properties (21):**

| Property | Type | Nullable |
|----------|------|----------|
| `CheckOutStatus` | `String` | Yes |
| `CheckoutState` | `String` | Yes |
| `Comments` | `String` | Yes |
| `CreatedBy` | `String` | Yes |
| `CreatedOn` | `DateTimeOffset` | Yes |
| `Description` | `String` | Yes |
| `ID` | `String` | Yes |
| `LastModified` | `DateTimeOffset` | Yes |
| `Latest` | `Boolean` | Yes |
| `LifeCycleTemplateName` | `String` | Yes |
| ... | (11 more) | |

**Navigation Properties (6):**

- `SOPSCCLinks` -> SOPToSCCLink
- `Context` -> Container
- `Versions` -> StandardOperation
- `Creator` -> User
- `Revisions` -> StandardOperation
- `Modifier` -> User

---

### SOPToSCCLink

**Properties (6):**

| Property | Type | Nullable |
|----------|------|----------|
| `CreatedOn` | `DateTimeOffset` | Yes |
| `GraphicData` | `GraphicData` | Yes |
| `ID` | `String` | Yes |
| `LastModified` | `DateTimeOffset` | Yes |
| `ModelItemContainerMasterReference` | `String` | Yes |
| `ModelItemMasterReference` | `String` | Yes |

**Navigation Properties (5):**

- `StandardCCs` -> StandardControlCharacteristic
- `DDLinks` -> DescribedByDocument
- `DRLinks` -> ReferenceDocument
- `SPLinks` -> StandardProcedureUsage
- `ResourceLinks` -> ResourceUsage

---

### ReferenceDocument

**Properties (4):**

| Property | Type | Nullable |
|----------|------|----------|
| `CreatedOn` | `DateTimeOffset` | Yes |
| `ExpressionData` | `String` | Yes |
| `ID` | `String` | Yes |
| `LastModified` | `DateTimeOffset` | Yes |

**Navigation Properties (1):**

- `RefDocuments` -> Document

---

### SCCDescribedByDocument

**Properties (4):**

| Property | Type | Nullable |
|----------|------|----------|
| `CreatedOn` | `DateTimeOffset` | Yes |
| `ExpressionData` | `String` | Yes |
| `ID` | `String` | Yes |
| `LastModified` | `DateTimeOffset` | Yes |

**Navigation Properties (1):**

- `SCCDocuments` -> Document

---

## Related Files

| File | Description |
|------|-------------|
| Factory_Entities.json | Machine-readable entity definitions |
| Factory_Navigations.md | Navigation properties reference |
| Factory_Actions.md | OData actions reference |
| Factory_Metadata.xml | Raw OData metadata |
