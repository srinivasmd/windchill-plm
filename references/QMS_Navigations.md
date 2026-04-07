# QMS Domain - Navigation Properties

This document describes all navigation properties and entity relationships in the QMS domain.

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PTC.QMS Namespace                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐      QualityActions     ┌──────────────────┐         │
│  │  QualityObject   │─────────────────────────►│  QualityAction   │         │
│  ├──────────────────┤                          ├──────────────────┤         │
│  │ - QualityActions │                          │ - Owner          │         │
│  │ - Context        │                          │ - Context        │         │
│  │ - Creator        │                          │ - Creator        │         │
│  │ - Modifier       │                          │ - Modifier       │         │
│  └──────────────────┘                          │ - RelatedObject   │         │
│                                                └──────────────────┘         │
│                                                                             │
│  ┌──────────────────┐      CAPA        ┌──────────────────┐                 │
│  │ NonConformance   │─────────────────►│      CAPA        │                 │
│  ├──────────────────┤                  ├──────────────────┤                 │
│  │ - Subject        │                  │ - Subject        │                 │
│  │ - Place          │                  │ - NonConformance │                 │
│  │ - CAPA           │                  │ - Owner          │                 │
│  │ - Context        │                  │ - Context        │                 │
│  │ - Creator        │                  │ - Creator        │                 │
│  └────────┬─────────┘                  └────────┬─────────┘                 │
│           │                                     │                           │
│           │ Subject                             │ Subject                   │
│           ▼                                     ▼                           │
│  ┌──────────────────┐                  ┌──────────────────┐               │
│  │     Subject      │◄─────────────────┤                  │               │
│  ├──────────────────┤                  │                  │               │
│  │ - Context        │                  │                  │               │
│  └──────────────────┘                  └──────────────────┘               │
│                                              ▲                               │
│                                              │ Place                         │
│  ┌──────────────────┐                        │                               │
│  │  QualityContact  │────────────────────────┘                               │
│  ├──────────────────┤                                                        │
│  │ - Place          │                                                        │
│  │ - Context        │                                                        │
│  └──────────────────┘                                                        │
│                                                                             │
│  ┌──────────────────┐                                                        │
│  │      Place       │                                                        │
│  ├──────────────────┤                                                        │
│  │ - Context        │                                                        │
│  └──────────────────┘                                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Navigation Properties by Entity

### QualityAction

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context (Product, Library, Project) |
| Creator | PTC.PrincipalMgmt.User | User who created the action |
| Modifier | PTC.PrincipalMgmt.User | User who last modified the action |
| Owner | PTC.PrincipalMgmt.User | Assigned owner of the action |
| RelatedQualityObject | PTC.QMS.QualityObject | Related quality object |

### QualityObject

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context |
| Creator | PTC.PrincipalMgmt.User | User who created |
| Modifier | PTC.PrincipalMgmt.User | User who last modified |
| QualityActions | Collection(PTC.QMS.QualityAction) | Related quality actions |

### NonConformance

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context |
| Creator | PTC.PrincipalMgmt.User | User who created |
| Modifier | PTC.PrincipalMgmt.User | User who last modified |
| Subject | PTC.QMS.Subject | Related product/subject |
| CAPA | PTC.QMS.QualityAction | Related CAPA |
| Place | PTC.QMS.Place | Location of discovery |

### CAPA

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context |
| Creator | PTC.PrincipalMgmt.User | User who created |
| Modifier | PTC.PrincipalMgmt.User | User who last modified |
| Owner | PTC.PrincipalMgmt.User | Assigned owner |
| Subject | PTC.QMS.Subject | Related product/subject |
| NonConformance | PTC.QMS.NonConformance | Related non-conformance |

### Place

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context |

### QualityContact

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context |
| Place | PTC.QMS.Place | Associated place/location |

### Subject

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context |

## Cross-Domain References

| From Entity | Navigation Property | Target Domain | Target Entity |
|-------------|---------------------|---------------|---------------|
| QualityAction | Context | DataAdmin | Container |
| QualityAction | Creator | PrincipalMgmt | User |
| QualityAction | Modifier | PrincipalMgmt | User |
| QualityAction | Owner | PrincipalMgmt | User |
| QualityObject | Context | DataAdmin | Container |
| QualityObject | Creator | PrincipalMgmt | User |
| QualityObject | Modifier | PrincipalMgmt | User |
| NonConformance | Context | DataAdmin | Container |
| NonConformance | Creator | PrincipalMgmt | User |
| NonConformance | Modifier | PrincipalMgmt | User |
| CAPA | Context | DataAdmin | Container |
| CAPA | Creator | PrincipalMgmt | User |
| CAPA | Modifier | PrincipalMgmt | User |
| CAPA | Owner | PrincipalMgmt | User |
| Place | Context | DataAdmin | Container |
| QualityContact | Context | DataAdmin | Container |
| Subject | Context | DataAdmin | Container |

## OData Query Examples

### Get quality action with full details

```
GET /QMS/QualityActions('{id}')?$expand=Owner,Context,Creator,Modifier,RelatedQualityObject
```

### Get quality object with actions

```
GET /QMS/QualityObjects('{id}')?$expand=QualityActions($expand=Owner),Creator,Context
```

### Get non-conformance with CAPA

```
GET /QMS/NonConformances('{id}')?$expand=CAPA($expand=Owner,Subject),Subject,Place,Context
```

### Get CAPA with non-conformance and subject

```
GET /QMS/CAPAs('{id}')?$expand=NonConformance($expand=Place),Subject,Owner,Context
```

### Get quality contact with place

```
GET /QMS/QualityContacts('{id}')?$expand=Place,Context
```

### Get quality actions for a quality object

```
GET /QMS/QualityObjects('{id}')/QualityActions?$expand=Owner
```

### Get non-conformances by subject

```
GET /QMS/NonConformances?$expand=Subject&$filter=Subject/Number eq 'SUBJ-001'
```

### Multi-level expansion

```
GET /QMS/NonConformances('{id}')?$expand=
  CAPA($expand=Owner,Subject($expand=Context)),
  Subject($expand=Context),
  Place,
  Context,
  Creator
```

## Entity Sets

| Entity Set | Entity Type | Description |
|------------|-------------|-------------|
| QualityActions | QualityAction | All quality actions |
| QualityObjects | QualityObject | All quality objects |
| Places | Place | All places/locations |
| QualityContacts | QualityContact | All quality contacts |
| Subjects | Subject | All subjects |
| NonConformances | NonConformance | All non-conformances |
| CAPAs | CAPA | All CAPA records |

## Common Query Patterns

### Get open quality actions with owner details

```
GET /QMS/QualityActions?$filter=State/Value eq 'OPEN'&$expand=Owner,Context&$orderby=DueDate asc
```

### Get overdue actions

```
GET /QMS/QualityActions?$filter=DueDate lt 2026-01-01T00:00:00Z and State/Value ne 'COMPLETED'&$expand=Owner,Context
```

### Get non-conformances by place

```
GET /QMS/NonConformances?$expand=Place,Subject&$filter=Place/Name eq 'Manufacturing Site A'
```

### Get CAPAs by owner

```
GET /QMS/CAPAs?$expand=Owner,Subject&$filter=Owner/Name eq 'jdoe'
```

### Get quality objects with pending actions

```
GET /QMS/QualityObjects?$expand=QualityActions($filter=State/Value eq 'OPEN' or State/Value eq 'IN_PROGRESS')
```

## Navigation Property Notes

1. **QualityObject → QualityActions**: One-to-Many. A quality object can have multiple related quality actions.

2. **NonConformance → CAPA**: One-to-One. A non-conformance can have one associated CAPA.

3. **CAPA → NonConformance**: One-to-One. A CAPA is linked to its source non-conformance.

4. **NonConformance → Subject**: Many-to-One. Multiple non-conformances can reference the same subject.

5. **CAPA → Subject**: Many-to-One. Multiple CAPAs can reference the same subject.

6. **QualityContact → Place**: Many-to-One. Multiple contacts can be associated with a place.

7. **NonConformance → Place**: Many-to-One. Multiple non-conformances can be discovered at the same place.
