# Factory Actions

This document describes OData actions available in the PTC.Factory namespace.

## Overview

Factory domain defines **42 actions**.

---

## Unbound Actions

These actions can be called directly on the entity set.

### ReviseDocuments

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Documents` | `Document)` | No |

### SetStateDocuments

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Documents` | `Document)` | No |
| `State` | `EnumType` | No |

### CheckOutDocuments

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Workables` | `Document)` | No |
| `CheckOutNote` | `String` | Yes |

### CheckInDocuments

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Workables` | `Document)` | No |
| `CheckInNote` | `String` | Yes |

### UndoCheckOutDocuments

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Workables` | `Document)` | No |

### ReviseStandardProcedures

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `StandardProcedures` | `StandardProcedure)` | No |

### SetStateStandardProcedures

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `StandardProcedures` | `StandardProcedure)` | No |
| `State` | `EnumType` | No |

### CheckOutStandardProcedures

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Workables` | `StandardProcedure)` | No |
| `CheckOutNote` | `String` | Yes |

### CheckInStandardProcedures

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Workables` | `StandardProcedure)` | No |
| `CheckInNote` | `String` | Yes |

### UndoCheckOutStandardProcedures

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Workables` | `StandardProcedure)` | No |

### SetStateStandardControlCharacteristics

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `StandardControlCharacteristics` | `StandardControlCharacteristic)` | No |
| `State` | `EnumType` | No |

### ReviseStandardControlCharacteristics

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `StandardControlCharacteristics` | `StandardControlCharacteristic)` | No |

### CheckOutStandardControlCharacteristics

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Workables` | `StandardControlCharacteristic)` | No |
| `CheckOutNote` | `String` | Yes |

### CheckInStandardControlCharacteristics

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Workables` | `StandardControlCharacteristic)` | No |
| `CheckInNote` | `String` | Yes |

### UndoCheckOutStandardControlCharacteristics

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Workables` | `StandardControlCharacteristic)` | No |

### SetStateStandardOperations

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `StandardOperations` | `StandardOperation)` | No |
| `State` | `EnumType` | No |

### ReviseStandardOperations

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `StandardOperations` | `StandardOperation)` | No |

### CheckOutStandardOperations

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Workables` | `StandardOperation)` | No |
| `CheckOutNote` | `String` | Yes |

### CheckInStandardOperations

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Workables` | `StandardOperation)` | No |
| `CheckInNote` | `String` | Yes |

### UndoCheckOutStandardOperations

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Workables` | `StandardOperation)` | No |

## Bound Actions

These actions are bound to specific entity types and must be called on an entity instance.

### Revise

**Bound To:** `Document`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `VersionId` | `String` | Yes |

### SetState

**Bound To:** `Document`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `State` | `EnumType` | No |

### CheckIn

**Bound To:** `Document`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `CheckInNote` | `String` | Yes |
| `CheckOutNote` | `String` | Yes |
| `KeepCheckedOut` | `Boolean` | Yes |

### CheckOut

**Bound To:** `Document`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `CheckOutNote` | `String` | Yes |

### UndoCheckOut

**Bound To:** `Document`


### Revise

**Bound To:** `StandardProcedure`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `VersionId` | `String` | Yes |

### SetState

**Bound To:** `StandardProcedure`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `State` | `EnumType` | No |

### CheckIn

**Bound To:** `StandardProcedure`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `CheckInNote` | `String` | Yes |
| `CheckOutNote` | `String` | Yes |
| `KeepCheckedOut` | `Boolean` | Yes |

### CheckOut

**Bound To:** `StandardProcedure`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `CheckOutNote` | `String` | Yes |

### UndoCheckOut

**Bound To:** `StandardProcedure`


### updateSCCRelatedLinks

**Bound To:** `StandardControlCharacteristic`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `TestRun` | `Boolean` | No |
| `UpdateRequests` | `UpdateRequest)` | No |

### SetState

**Bound To:** `StandardControlCharacteristic`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `State` | `EnumType` | No |

### Revise

**Bound To:** `StandardControlCharacteristic`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `VersionId` | `String` | Yes |

### CheckIn

**Bound To:** `StandardControlCharacteristic`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `CheckInNote` | `String` | Yes |
| `CheckOutNote` | `String` | Yes |
| `KeepCheckedOut` | `Boolean` | Yes |

### CheckOut

**Bound To:** `StandardControlCharacteristic`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `CheckOutNote` | `String` | Yes |

### UndoCheckOut

**Bound To:** `StandardControlCharacteristic`


### updateSOPRelatedLinks

**Bound To:** `StandardOperation`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `TestRun` | `Boolean` | No |
| `UpdateRequests` | `UpdateRequest)` | No |

### SetState

**Bound To:** `StandardOperation`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `State` | `EnumType` | No |

### Revise

**Bound To:** `StandardOperation`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `VersionId` | `String` | Yes |

### CheckIn

**Bound To:** `StandardOperation`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `CheckInNote` | `String` | Yes |
| `CheckOutNote` | `String` | Yes |
| `KeepCheckedOut` | `Boolean` | Yes |

### CheckOut

**Bound To:** `StandardOperation`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `CheckOutNote` | `String` | Yes |

### UndoCheckOut

**Bound To:** `StandardOperation`

