# DynamicDocMgmt Actions

This document describes OData actions available in the PTC.DynamicDocMgmt namespace.

## Overview

DynamicDocMgmt domain defines **32 actions**.

---

## Unbound Actions

These actions can be called directly on the entity set.

### CreateXliffLink

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `oidForC3diDocument` | `String` | No |
| `oidForXliffDocument` | `String` | No |

### SetStateBurstConfigurations

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `BurstConfigurations` | `BurstConfiguration)` | No |
| `State` | `EnumType` | No |

### ReviseBurstConfigurations

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `BurstConfigurations` | `BurstConfiguration)` | No |

### SetStateNotes

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Notes` | `Note)` | No |
| `State` | `EnumType` | No |

### ReviseNotes

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Notes` | `Note)` | No |

### SetStateDynamicDocuments

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `DynamicDocuments` | `DynamicDocument)` | No |
| `State` | `EnumType` | No |

### ReviseDynamicDocuments

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `DynamicDocuments` | `DynamicDocument)` | No |

### EditDynamicDocumentsSecurityLabels

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `DynamicDocuments` | `DynamicDocument)` | No |

### CreateDynamicDocuments

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `DynamicDocuments` | `DynamicDocument)` | No |

### UpdateDynamicDocuments

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `DynamicDocuments` | `DynamicDocument)` | No |

## Bound Actions

These actions are bound to specific entity types and must be called on an entity instance.

### UploadStage1Action

**Bound To:** `BurstConfiguration`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `NoOfFiles` | `Int32` | No |
| `DelegateName` | `String` | Yes |

### UploadStage3Action

**Bound To:** `BurstConfiguration`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `ContentInfo` | `ContentInfo)` | No |

### SetState

**Bound To:** `BurstConfiguration`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `State` | `EnumType` | No |

### Revise

**Bound To:** `BurstConfiguration`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `VersionId` | `String` | Yes |

### CheckOut

**Bound To:** `BurstConfiguration`


### UndoCheckOut

**Bound To:** `BurstConfiguration`


### CheckIn

**Bound To:** `BurstConfiguration`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `CheckInNote` | `String` | Yes |
| `KeepCheckedOut` | `Boolean` | Yes |

### UploadStage3Action

**Bound To:** `Note`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `ContentInfo` | `ContentInfo)` | No |

### UploadStage1Action

**Bound To:** `Note`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `NoOfFiles` | `Int32` | No |
| `DelegateName` | `String` | Yes |

### SetState

**Bound To:** `Note`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `State` | `EnumType` | No |

### Revise

**Bound To:** `Note`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `VersionId` | `String` | Yes |

### CheckOut

**Bound To:** `Note`


### UndoCheckOut

**Bound To:** `Note`


### CheckIn

**Bound To:** `Note`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `CheckInNote` | `String` | Yes |
| `KeepCheckedOut` | `Boolean` | Yes |

### UploadStage1Action

**Bound To:** `DynamicDocument`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `NoOfFiles` | `Int32` | No |
| `DelegateName` | `String` | Yes |

### UploadStage3Action

**Bound To:** `DynamicDocument`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `ContentInfo` | `ContentInfo)` | No |

### SetState

**Bound To:** `DynamicDocument`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `State` | `EnumType` | No |

### Revise

**Bound To:** `DynamicDocument`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `VersionId` | `String` | Yes |

### CheckOut

**Bound To:** `DynamicDocument`


### UndoCheckOut

**Bound To:** `DynamicDocument`


### CheckIn

**Bound To:** `DynamicDocument`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `CheckInNote` | `String` | Yes |
| `KeepCheckedOut` | `Boolean` | Yes |

### UpdateCommonProperties

**Bound To:** `DynamicDocument`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Updates` | `DynamicDocument` | No |
