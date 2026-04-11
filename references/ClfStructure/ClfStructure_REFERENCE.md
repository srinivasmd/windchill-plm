# ClfStructure Domain Reference

ClfStructure domain in PTC Windchill PLM.

## Overview

| Property | Value |
|----------|-------|
| Namespace | PTC.ClfStructure |
| Entity Sets | 1 |
| Entity Types | 2 |
| Actions | 0 |
| Complex Types | 3 |

---

## Entity Sets

- **ClfNodes**: PTC.ClfStructure.ClfNode

## Entity Types

### ClfNode

**Properties (9):**

| Property | Type | Nullable | Annotations |
|----------|------|----------|-------------|
| `ID` | `String` | Yes | - |
| `DisplayName` | `String` | Yes | - |
| `InternalName` | `String` | Yes | - |
| `Description` | `String` | Yes | - |
| `HierarchicalPath` | `String` | Yes | - |
| `Keywords` | `String` | Yes | - |
| `Instantiable` | `Boolean` | Yes | - |
| `Image` | `String` | Yes | - |
| `ClfNodeAttributes` | `ClfAttributeType)` | Yes | NonFilterable, NonSortable |

**Navigation Properties (3):**

- `ChildNodes` -> ClfNode
- `ParentNode` -> ClfNode
- `ClassifiedObjects` -> ClassifiedObject

---

### ClassifiedObject

**Properties (4):**

| Property | Type | Nullable | Annotations |
|----------|------|----------|-------------|
| `ID` | `String` | Yes | - |
| `Name` | `String` | Yes | NonFilterable, NonSortable |
| `ClfBindingAttributeAndNodeValues` | `ClassificationBindingAttributeValueType)` | Yes | NonFilterable, NonSortable |
| `ClassificationAttributes` | `ClassificationAttributeValueType)` | Yes | NonSortable |

---

## Complex Types

### ClfAttributeType

- `DisplayName`: String
- `InternalName`: String
- `DefaultValues`: Collection(String)
- `Type`: String
- `QuantityOfMeasure`: String
- `Unit`: String
- `Required`: Boolean

### ClassificationAttributeValueType

- `DisplayName`: String
- `InternalName`: String
- `Type`: String
- `Value`: String
- `DisplayValue`: String

### ClassificationBindingAttributeValueType

- `clfBindingAttributeDisplayName`: String
- `clfBindingAttributeInternalName`: String
- `clfNodeID`: String
- `clfNodeDisplayName`: String
- `clfNodeInternalName`: String

## Related Files

| File | Description |
|------|-------------|
| ClfStructure_Entities.json | Machine-readable entity definitions |
| ClfStructure_Navigations.md | Navigation properties reference |
| ClfStructure_Actions.md | OData actions reference |
| ClfStructure_Metadata.xml | Raw OData metadata |
