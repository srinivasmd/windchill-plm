# NC Navigation Properties

This document describes navigation properties for entities in this domain.

## OtherItem

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `ImmediateActions` | `ImmediateAction` | - | Yes |

**OData $expand Example:**
```
GET /NC/Nonconformances('{id}')?$expand=ImmediateActions
```

## AffectedObject

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `Subject` | `Subject` | - | No |
| `ImmediateActions` | `ImmediateAction` | - | No |

**OData $expand Example:**
```
GET /NC/Nonconformances('{id}')?$expand=Subject,ImmediateActions
```

## Nonconformance

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `OriginatingLocation` | `Place` | - | No |
| `OriginatedBy` | `User` | - | No |
| `AffectedObjects` | `AffectedObject` | - | Yes |
| `OtherItems` | `OtherItem` | - | Yes |
| `Context` | `Container` | - | No |
| `PrimaryRelatedPersonOrLocation` | `QualityContact` | - | No |
| `Creator` | `User` | - | No |
| `Attachments` | `ContentItem` | - | Yes |
| `Modifier` | `User` | - | No |
| `AdditionalRelatedPersonnelOrLocations` | `QualityContact` | - | No |

**OData $expand Example:**
```
GET /NC/Nonconformances('{id}')?$expand=OriginatingLocation,OriginatedBy,AffectedObjects
```
