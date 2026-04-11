# EffectivityMgmt Domain Reference

EffectivityMgmt management in PTC Windchill PLM.

## Overview

| Property | Value |
|----------|-------|
| Namespace | PTC.EffectivityMgmt |
| Entity Sets | 1 |
| Entity Types | 9 |
| Actions | 2 |

---

## Entity Sets

- **PartEffectivityContexts**: PartEffectivityContext

## Entity Types

### PartEffectivityContext

**Properties (12):**

| Property | Type | Nullable |
|----------|------|----------|
| `AltReplacementType` | `String` | Yes |
| `ConfigurableModule` | `EnumType` | Yes |
| `DefaultTraceCode` | `EnumType` | No |
| `DefaultUnit` | `EnumType` | No |
| `EndItem` | `Boolean` | No |
| `Identity` | `String` | Yes |
| `Name` | `String` | No |
| `Number` | `String` | Yes |
| `ObjectType` | `String` | Yes |
| `OrganizationName` | `String` | Yes |
| ... | (2 more) | |

**Navigation Properties (2):**

- `Context` -> Container
- `Organization` -> Organization

---

### DateEffectivity

**Properties (1):**

| Property | Type | Nullable |
|----------|------|----------|
| `DateRange` | `DateRange` | Yes |

---

### EffectivityManagedEntity

**Properties (7):**

| Property | Type | Nullable |
|----------|------|----------|
| `CreatedBy` | `String` | Yes |
| `CreatedOn` | `DateTimeOffset` | Yes |
| `ID` | `String` | Yes |
| `Identity` | `String` | Yes |
| `LastModified` | `DateTimeOffset` | Yes |
| `MasterID` | `String` | Yes |
| `ModifiedBy` | `String` | Yes |

**Navigation Properties (3):**

- `Effectivities` -> Effectivity
- `Creator` -> User
- `Modifier` -> User

---

### UnitEffectivity

**Properties (1):**

| Property | Type | Nullable |
|----------|------|----------|
| `UnitRange` | `UnitRange` | Yes |

---

### Effectivity

**Properties (1):**

| Property | Type | Nullable |
|----------|------|----------|
| `EffectivityQualifier` | `EnumType` | Yes |

**Navigation Properties (1):**

- `EffectivityContext` -> PartEffectivityContext

---

## Related Files

| File | Description |
|------|-------------|
| EffectivityMgmt_Entities.json | Machine-readable entity definitions |
| EffectivityMgmt_Navigations.md | Navigation properties reference |
| EffectivityMgmt_Actions.md | OData actions reference |
| EffectivityMgmt_Metadata.xml | Raw OData metadata |
