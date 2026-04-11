# NC Actions

This document describes OData actions available in the PTC.NC namespace.

## Overview

NC domain defines **7 actions**.

---

## Unbound Actions

These actions can be called directly on the entity set.

### SetStateNonconformances

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Nonconformances` | `Nonconformance)` | No |
| `State` | `EnumType` | No |

### EditNonconformancesSecurityLabels

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Nonconformances` | `Nonconformance)` | No |

## Bound Actions

These actions are bound to specific entity types and must be called on an entity instance.

### SetState

**Bound To:** `Nonconformance`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `State` | `EnumType` | No |

**Returns:** `Nonconformance`

---

### UndoReservation

**Bound To:** `Nonconformance`


**Returns:** `Nonconformance`

---

### Reserve

**Bound To:** `Nonconformance`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Duration` | `Int32` | Yes |

**Returns:** `Nonconformance`

---

### UploadStage1Action

**Bound To:** `Nonconformance`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `NoOfFiles` | `Int32` | No |
| `DelegateName` | `String` | Yes |

**Returns:** `CacheDescriptor)`

---

### UploadStage3Action

**Bound To:** `Nonconformance`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `ContentInfo` | `ContentInfo)` | No |

**Returns:** `ApplicationData)`

---
