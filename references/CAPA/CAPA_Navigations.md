# CAPA Navigation Properties

This document describes navigation properties for entities in the PTC.CAPA namespace.

## Overview

CAPA domain defines **6 entities** with navigation properties.

---

## CAPA

Corrective and Preventive Action - the main entity for CAPA management.

| Navigation Property | Type | Partner | Contains Target | Description |
|---------------------|------|---------|-----------------|-------------|
| `PrimarySite` | `CAPASite` | - | Yes | Primary site/location for the CAPA |
| `AdditionalSites` | `CAPASite` | - | Yes | Additional sites associated with the CAPA |
| `AffectedObjects` | `AffectedObject` | - | Yes | Objects affected by the CAPA |
| `Plan` | `CAPAActionPlan` | - | Yes | Action Plan for the CAPA |
| `Context` | `Container` | - | No | Container context |
| `PrimaryRelatedPersonOrLocation` | `QualityContact` | - | No |  |
| `Thumbnails` | `ContentItem` | - | Yes | Thumbnail images |
| `Creator` | `User` | - | No | User who created/modified |
| `SmallThumbnails` | `ContentItem` | - | Yes | Thumbnail images |
| `Attachments` | `ContentItem` | - | Yes | File attachments |
| `Modifier` | `User` | - | No | User who created/modified |
| `AdditionalRelatedPersonnelOrLocations` | `QualityContact` | - | No |  |

**OData $expand Example:**
```
GET /CAPA/CAPAs('{id}')?$expand=PrimarySite,AdditionalSites,AffectedObjects
```

## CAPASite

Site/location associated with a CAPA.

| Navigation Property | Type | Partner | Contains Target | Description |
|---------------------|------|---------|-----------------|-------------|
| `Place` | `Place` | - | No | Place/location reference |

**OData $expand Example:**
```
GET /CAPA/CAPAs('{id}')?$expand=Place
```

## ActionSubject

Subject associated with an Action.

| Navigation Property | Type | Partner | Contains Target | Description |
|---------------------|------|---------|-----------------|-------------|
| `Subject` | `Subject` | - | No | Subject reference |

**OData $expand Example:**
```
GET /CAPA/CAPAs('{id}')?$expand=Subject
```

## CAPAActionPlan

Action Plan associated with a CAPA.

| Navigation Property | Type | Partner | Contains Target | Description |
|---------------------|------|---------|-----------------|-------------|
| `Actions` | `Action` | - | Yes | Actions in the plan |
| `Versions` | `CAPAActionPlan` | - | No |  |
| `Creator` | `User` | - | No | User who created/modified |
| `Revisions` | `CAPAActionPlan` | - | No |  |
| `Modifier` | `User` | - | No | User who created/modified |

**OData $expand Example:**
```
GET /CAPA/CAPAs('{id}')?$expand=Actions,Versions,Creator
```

## Action

Individual action within a CAPA Action Plan.

| Navigation Property | Type | Partner | Contains Target | Description |
|---------------------|------|---------|-----------------|-------------|
| `ChangeNoticeContext` | `Container` | - | No |  |
| `ActionSubjects` | `ActionSubject` | - | Yes | Subjects for the action |
| `Creator` | `User` | - | No | User who created/modified |
| `Modifier` | `User` | - | No | User who created/modified |

**OData $expand Example:**
```
GET /CAPA/CAPAs('{id}')?$expand=ChangeNoticeContext,ActionSubjects,Creator
```

## AffectedObject

Object affected by the CAPA.

| Navigation Property | Type | Partner | Contains Target | Description |
|---------------------|------|---------|-----------------|-------------|
| `Subject` | `Subject` | - | No | Subject reference |

**OData $expand Example:**
```
GET /CAPA/CAPAs('{id}')?$expand=Subject
```
