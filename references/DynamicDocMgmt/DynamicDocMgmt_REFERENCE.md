# DynamicDocMgmt Domain Reference

DynamicDocMgmt management in PTC Windchill PLM.

## Overview

| Property | Value |
|----------|-------|
| Namespace | PTC.DynamicDocMgmt |
| Entity Sets | 3 |
| Entity Types | 18 |
| Actions | 32 |

---

## Entity Sets

- **DynamicDocuments**: DynamicDocument
- **Notes**: Note
- **BurstConfigurations**: BurstConfiguration

## Entity Types

### ContentInfo

**Properties (6):**

| Property | Type | Nullable |
|----------|------|----------|
| `StreamId` | `Int64` | Yes |
| `FileSize` | `Int64` | Yes |
| `EncodedInfo` | `String` | Yes |
| `FileName` | `String` | Yes |
| `MimeType` | `String` | Yes |
| `PrimaryContent` | `Boolean` | Yes |

---

### DynamicDocumentMember

**Properties (13):**

| Property | Type | Nullable |
|----------|------|----------|
| `AsStoredChildName` | `String` | Yes |
| `ComponentName` | `String` | Yes |
| `DepType` | `DynamicDocDepTypeInfo` | Yes |
| `FeatureID` | `Int32` | Yes |
| `FeatureNumber` | `Int64` | Yes |
| `HasFixedConstraint` | `Boolean` | Yes |
| `LayerID` | `Int64` | Yes |
| `ObjectType` | `String` | Yes |
| `Placed` | `Boolean` | Yes |
| `Quantity` | `Double` | Yes |
| ... | (3 more) | |

**Navigation Properties (2):**

- `Uses` -> DynamicDocument
- `UsedBy` -> DynamicDocument

---

### DynamicDocument

**Properties (34):**

| Property | Type | Nullable |
|----------|------|----------|
| `AuthoringApplication` | `EnumType` | Yes |
| `AuthoringLanguage` | `String` | Yes |
| `BeltLength` | `Double` | Yes |
| `CADName` | `String` | No |
| `CabinetName` | `String` | Yes |
| `Category` | `EnumType` | No |
| `CheckOutStatus` | `String` | Yes |
| `CheckoutInfo` | `String` | Yes |
| `CheckoutState` | `String` | Yes |
| `Comments` | `String` | Yes |
| ... | (24 more) | |

**Navigation Properties (18):**

- `MemberLinks` -> DynamicDocumentMember
- `UsedBy` -> DynamicDocument
- `ReferenceLinks` -> DynamicDocumentReference
- `ReferencedBy` -> DynamicDocument
- `Translations` -> DynamicDocument
- `Xliff` -> DynamicDocument
- `Context` -> Container
- `Versions` -> DynamicDocument
- `Organization` -> Organization
- `PrimaryContent` -> ContentItem
- `Thumbnails` -> ContentItem
- `Creator` -> User
- `Representations` -> Representation
- `SmallThumbnails` -> ContentItem
- `Revisions` -> DynamicDocument
- `Folder` -> Folder
- `Attachments` -> ContentItem
- `Modifier` -> User

---

### DynamicDocumentReference

**Properties (5):**

| Property | Type | Nullable |
|----------|------|----------|
| `AsStoredChildName` | `String` | Yes |
| `DepType` | `DynamicDocDepTypeInfo` | Yes |
| `ObjectType` | `String` | Yes |
| `ReferenceType` | `EnumType` | Yes |
| `Required` | `Boolean` | Yes |

**Navigation Properties (2):**

- `References` -> DynamicDocument
- `ReferencedBy` -> DynamicDocument

---

## Related Files

| File | Description |
|------|-------------|
| DynamicDocMgmt_Entities.json | Machine-readable entity definitions |
| DynamicDocMgmt_Navigations.md | Navigation properties reference |
| DynamicDocMgmt_Actions.md | OData actions reference |
| DynamicDocMgmt_Metadata.xml | Raw OData metadata |
