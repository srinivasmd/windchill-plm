# ProdPlatformMgmt Actions

This document describes OData actions available in the PTC.ProdPlatformMgmt namespace.

## Overview

ProdPlatformMgmt domain defines **19 actions**.

---

## Unbound Actions

These actions can be called directly on the entity set.

### GetAssignedExpressions

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `ExpressionAssignables` | `WindchillEntity)` | No |

### GetVariantSpecificationsLinkedFromMVIL

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Parts` | `Part)` | No |

### GetAssignedOptionSets

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `OptionSetAssignables` | `OptionSetAssignableEntity)` | No |

### SetStateChoices

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Choices` | `Choice)` | No |
| `State` | `EnumType` | No |

### SetStateVariantSpecifications

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `VariantSpecifications` | `VariantSpecification)` | No |
| `State` | `EnumType` | No |

### ReviseVariantSpecifications

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `VariantSpecifications` | `VariantSpecification)` | No |

### CheckOutVariantSpecifications

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Workables` | `VariantSpecification)` | No |
| `CheckOutNote` | `String` | Yes |

### CheckInVariantSpecifications

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Workables` | `VariantSpecification)` | No |
| `CheckInNote` | `String` | Yes |

### UndoCheckOutVariantSpecifications

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Workables` | `VariantSpecification)` | No |

### SetStateOptionSets

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `OptionSets` | `OptionSet)` | No |
| `State` | `EnumType` | No |

### ReviseOptionSets

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `OptionSets` | `OptionSet)` | No |

## Bound Actions

These actions are bound to specific entity types and must be called on an entity instance.

### SetState

**Bound To:** `Choice`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `State` | `EnumType` | No |

**Returns:** `Choice`

---

### SetState

**Bound To:** `VariantSpecification`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `State` | `EnumType` | No |

**Returns:** `VariantSpecification`

---

### Revise

**Bound To:** `VariantSpecification`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `VersionId` | `String` | Yes |

**Returns:** `VariantSpecification`

---

### CheckIn

**Bound To:** `VariantSpecification`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `CheckInNote` | `String` | Yes |
| `CheckOutNote` | `String` | Yes |
| `KeepCheckedOut` | `Boolean` | Yes |

**Returns:** `VariantSpecification`

---

### CheckOut

**Bound To:** `VariantSpecification`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `CheckOutNote` | `String` | Yes |

**Returns:** `VariantSpecification`

---

### UndoCheckOut

**Bound To:** `VariantSpecification`


**Returns:** `VariantSpecification`

---

### SetState

**Bound To:** `OptionSet`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `State` | `EnumType` | No |

**Returns:** `OptionSet`

---

### Revise

**Bound To:** `OptionSet`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `VersionId` | `String` | Yes |

**Returns:** `OptionSet`

---
