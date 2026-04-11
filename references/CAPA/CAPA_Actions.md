# CAPA Actions

This document describes OData actions available in the PTC.CAPA namespace.

## Overview

CAPA domain defines **6 actions**.

---

## Unbound Actions

These actions can be called directly on the entity set.

### SetStateCAPAs

Sets the lifecycle state for multiple CAPAs.
**Parameters:**

| Parameter | Type | Nullable | Description |
|-----------|------|----------|-------------|
| `CAPAs` | `CAPA)` | No | - |
| `State` | `EnumType` | No | - |

**Example:**
```http
POST /CAPA/CAPAs/PTC.CAPA.SetStateCAPAs
Content-Type: application/json

{
  "CAPAs": <value>, "State": <value>
}
```

### EditCAPAsSecurityLabels

Edits security labels for CAPAs.
**Parameters:**

| Parameter | Type | Nullable | Description |
|-----------|------|----------|-------------|
| `CAPAs` | `CAPA)` | No | - |

**Example:**
```http
POST /CAPA/CAPAs/PTC.CAPA.EditCAPAsSecurityLabels
Content-Type: application/json

{
  "CAPAs": <value>
}
```

## Bound Actions

These actions are bound to specific entity types and must be called on an entity instance.

### SetState

Sets the lifecycle state for a CAPA.
**Bound To:** `CAPA`

**Parameters:**

| Parameter | Type | Nullable | Description |
|-----------|------|----------|-------------|
| `State` | `EnumType` | No | Target lifecycle state |

**Returns:** `CAPA`

**Example:**
```http
POST /CAPA/CAPAs('{capa_id}')/PTC.CAPA.SetState
Content-Type: application/json

{
  "State": <value>
}
```

### UploadStage1Action

Stage 1 of file upload process for CAPA attachments.
**Bound To:** `CAPA`

**Parameters:**

| Parameter | Type | Nullable | Description |
|-----------|------|----------|-------------|
| `NoOfFiles` | `Int32` | No | Number of files to upload |
| `DelegateName` | `String` | Yes | Upload delegate name |

**Returns:** `CacheDescriptor)`

**Example:**
```http
POST /CAPA/CAPAs('{capa_id}')/PTC.CAPA.UploadStage1Action
Content-Type: application/json

{
  "NoOfFiles": <value>, "DelegateName": <value>
}
```

### UploadStage3Action

Stage 3 of file upload process - finalizes the upload.
**Bound To:** `CAPA`

**Parameters:**

| Parameter | Type | Nullable | Description |
|-----------|------|----------|-------------|
| `ContentInfo` | `ContentInfo)` | No | Content metadata for upload |

**Returns:** `ApplicationData)`

**Example:**
```http
POST /CAPA/CAPAs('{capa_id}')/PTC.CAPA.UploadStage3Action
Content-Type: application/json

{
  "ContentInfo": <value>
}
```

### PlanApprovalRequired

Sets whether approval is required for a CAPA Action Plan.
**Bound To:** `CAPAActionPlan`

**Parameters:**

| Parameter | Type | Nullable | Description |
|-----------|------|----------|-------------|
| `Required` | `Boolean` | No | Whether approval is required |

**Returns:** `CAPAActionPlan`

**Example:**
```http
POST /CAPA/CAPAs('{capa_id}')/PTC.CAPA.PlanApprovalRequired
Content-Type: application/json

{
  "Required": <value>
}
```
