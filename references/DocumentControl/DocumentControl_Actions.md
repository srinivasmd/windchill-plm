# DocumentControl Actions

This document describes OData actions available in the PTC.DocumentControl namespace.

## Overview

DocumentControl domain defines **2 actions**.

---

## Unbound Actions

### SetStateTrainingRecords

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `TrainingRecords` | `TrainingRecord)` | No |
| `State` | `EnumType` | No |

**Example:**
```http
POST /DocumentControl/TrainingRecords/PTC.DocumentControl.SetStateTrainingRecords
```

## Bound Actions

### SetState

**Bound To:** `TrainingRecord`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `State` | `EnumType` | No |

**Returns:** `TrainingRecord`
