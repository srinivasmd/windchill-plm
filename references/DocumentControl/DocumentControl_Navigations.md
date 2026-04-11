# DocumentControl Navigation Properties

This document describes navigation properties for entities in the PTC.DocumentControl namespace.

## Overview

DocumentControl domain defines **2 entities** with navigation properties.

---

## ControlDocument

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `Context` | `Container` | - | No |
| `Versions` | `ControlDocument` | - | No |
| `Organization` | `Organization` | - | No |
| `PrimaryContent` | `ContentItem` | - | Yes |
| `Thumbnails` | `ContentItem` | - | Yes |
| `Creator` | `User` | - | No |
| `Representations` | `Representation` | - | No |
| `SmallThumbnails` | `ContentItem` | - | Yes |
| `Revisions` | `ControlDocument` | - | No |
| `Attachments` | `ContentItem` | - | Yes |
| `Modifier` | `User` | - | No |

**OData $expand Example:**
```
GET /DocumentControl/TrainingRecords('{id}')?$expand=Context,Versions,Organization
```

## TrainingRecord

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `SubjectControlDocument` | `ControlDocument` | - | No |
| `Assignee` | `Principal` | - | No |
| `Context` | `Container` | - | No |
| `Creator` | `User` | - | No |
| `Modifier` | `User` | - | No |

**OData $expand Example:**
```
GET /DocumentControl/TrainingRecords('{id}')?$expand=SubjectControlDocument,Assignee,Context
```
