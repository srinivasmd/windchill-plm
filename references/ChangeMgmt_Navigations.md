# ChangeMgmt Domain - Navigation Properties

This document describes all navigation properties and entity relationships in the ChangeMgmt domain.

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PTC.ChangeMgmt Namespace                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐         ChangeTasks          ┌──────────────────┐   │
│  │  ChangeNotice    │──────────────────────────────►│   ChangeTask     │   │
│  ├──────────────────┤                               ├──────────────────┤   │
│  │ - ChangeTasks    │                               │ - Resulting      │   │
│  │ - ChangeRequests │                               │ - ChangeNotice   │   │
│  │ - AffectedObjects│                               └────────┬─────────┘   │
│  │ - ResultingObjects│                                       │             │
│  │ - Context        │                                       │             │
│  │ - Creator        │              ResultingObjects         │             │
│  │ - Modifier       │                                       │             │
│  │ - Folder         │                                       ▼             │
│  └────────┬─────────┘                               ┌──────────────────┐   │
│           │                                         │   Changeable     │   │
│           │                                         ├──────────────────┤   │
│           │ ChangeRequests                          │ - Context        │   │
│           │                                         │ - Creator        │   │
│           ▼                                         │ - Modifier       │   │
│  ┌──────────────────┐        AffectedObjects        └──────────────────┘   │
│  │  ChangeRequest   │────────────────────────────────────────────────────► │
│  ├──────────────────┤                                                      │
│  │ - ChangeNotices  │                                                      │
│  │ - AffectedObjects│                                                      │
│  │ - Context        │                                                      │
│  │ - Creator        │                                                      │
│  │ - Modifier       │                                                      │
│  │ - Folder         │                                                      │
│  └──────────────────┘                                                      │
│                                                                             │
│  ┌──────────────────┐                                                      │
│  │   ChangeOrder    │                                                      │
│  ├──────────────────┤                                                      │
│  │ - Context        │                                                      │
│  │ - Creator        │                                                      │
│  │ - Modifier       │                                                      │
│  └──────────────────┘                                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Navigation Properties by Entity

### ChangeNotice

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context (Product, Library, Project) |
| Creator | PTC.PrincipalMgmt.User | User who created the change notice |
| Modifier | PTC.PrincipalMgmt.User | User who last modified the change notice |
| ChangeRequests | Collection(PTC.ChangeMgmt.ChangeRequest) | Linked change requests (ECR) |
| ChangeTasks | Collection(PTC.ChangeMgmt.ChangeTask) | Child change tasks for implementation |
| ResultingObjects | Collection(PTC.ChangeMgmt.Changeable) | Objects created or modified by this change |
| AffectedObjects | Collection(PTC.ChangeMgmt.Changeable) | Objects impacted by this change |
| Folder | PTC.DataAdmin.Folder | Containing folder |

### ChangeRequest

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context |
| Creator | PTC.PrincipalMgmt.User | User who created the change request |
| Modifier | PTC.PrincipalMgmt.User | User who last modified the change request |
| ChangeNotices | Collection(PTC.ChangeMgmt.ChangeNotice) | Linked change notices (ECN) |
| AffectedObjects | Collection(PTC.ChangeMgmt.Changeable) | Objects impacted by this change request |
| Folder | PTC.DataAdmin.Folder | Containing folder |

### ChangeTask

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context |
| Creator | PTC.PrincipalMgmt.User | User who created the change task |
| Modifier | PTC.PrincipalMgmt.User | User who last modified the change task |
| ChangeNotice | PTC.ChangeMgmt.ChangeNotice | Parent change notice |
| ResultingObjects | Collection(PTC.ChangeMgmt.Changeable) | Objects created or modified by this task |
| Folder | PTC.DataAdmin.Folder | Containing folder |

### Changeable

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context |
| Creator | PTC.PrincipalMgmt.User | User who created the object |
| Modifier | PTC.PrincipalMgmt.User | User who last modified the object |

### ChangeOrder

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context |
| Creator | PTC.PrincipalMgmt.User | User who created |
| Modifier | PTC.PrincipalMgmt.User | User who last modified |

## Cross-Domain References

The ChangeMgmt domain has navigation properties that reference entities from other domains:

| From Entity | Navigation Property | Target Domain | Target Entity |
|-------------|---------------------|---------------|---------------|
| ChangeNotice | Context | DataAdmin | Container |
| ChangeNotice | Creator | PrincipalMgmt | User |
| ChangeNotice | Modifier | PrincipalMgmt | User |
| ChangeNotice | Folder | DataAdmin | Folder |
| ChangeRequest | Context | DataAdmin | Container |
| ChangeRequest | Creator | PrincipalMgmt | User |
| ChangeRequest | Modifier | PrincipalMgmt | User |
| ChangeRequest | Folder | DataAdmin | Folder |
| ChangeTask | Context | DataAdmin | Container |
| ChangeTask | Creator | PrincipalMgmt | User |
| ChangeTask | Modifier | PrincipalMgmt | User |
| ChangeTask | ChangeNotice | ChangeMgmt | ChangeNotice |
| Changeable | Context | DataAdmin | Container |
| Changeable | Creator | PrincipalMgmt | User |
| Changeable | Modifier | PrincipalMgmt | User |
| ChangeOrder | Context | DataAdmin | Container |
| ChangeOrder | Creator | PrincipalMgmt | User |
| ChangeOrder | Modifier | PrincipalMgmt | User |

## OData Query Examples

### Get change notice with all details

```
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=ChangeTasks,ChangeRequests,AffectedObjects,ResultingObjects,Context,Creator,Modifier,Folder
```

### Get change notice with change tasks

```
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=ChangeTasks($expand=Creator,ResultingObjects)
```

### Get change request with linked change notices

```
GET /ChangeMgmt/ChangeRequests('{id}')?$expand=ChangeNotices($expand=ChangeTasks),AffectedObjects
```

### Get change tasks for a change notice

```
GET /ChangeMgmt/ChangeNotices('{id}')/ChangeTasks?$expand=Creator,ResultingObjects
```

### Get affected objects for a change notice

```
GET /ChangeMgmt/ChangeNotices('{id}')/AffectedObjects?$expand=Context,Creator
```

### Get resulting objects for a change task

```
GET /ChangeMgmt/ChangeTasks('{id}')/ResultingObjects?$expand=Context,Creator
```

### Get change notice with context

```
GET /ChangeMgmt/ChangeNotices?$expand=Context,Creator&$filter=State/Value eq 'OPEN'
```

### Get change requests created by a specific user

```
GET /ChangeMgmt/ChangeRequests?$expand=Creator&$filter=Creator/Name eq 'John Doe'
```

### Get change tasks for a specific container

```
GET /ChangeMgmt/ChangeTasks?$expand=Context,ChangeNotice&$filter=Context/Name eq 'Product ABC'
```

### Multi-level expansion

```
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=ChangeTasks($expand=ResultingObjects($expand=Context,Creator),Creator),ChangeRequests($expand=AffectedObjects),Context
```

## Entity Sets

| Entity Set | Entity Type | Description |
|------------|-------------|-------------|
| ChangeNotices | ChangeNotice | All change notices (ECN) |
| ChangeRequests | ChangeRequest | All change requests (ECR) |
| ChangeTasks | ChangeTask | All change tasks |
| ChangeOrders | ChangeOrder | All change orders |

## Common Query Patterns

### Get full change package

```
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=
  ChangeTasks($expand=ResultingObjects($expand=Context),Creator),
  ChangeRequests($expand=AffectedObjects),
  AffectedObjects($expand=Context),
  ResultingObjects($expand=Context),
  Context,
  Creator,
  Modifier
```

### Find changes affecting a specific part

```
GET /ChangeMgmt/ChangeNotices?$expand=AffectedObjects&$filter=AffectedObjects/any(a: a/Number eq 'PART-001')
```

### Get open change tasks by due date

```
GET /ChangeMgmt/ChangeTasks?$expand=ChangeNotice,Creator&$filter=State/Value eq 'IN_PROGRESS'&$orderby=DueDate asc
```

### Get change notices by container

```
GET /ChangeMgmt/ChangeNotices?$expand=Context&$filter=Context/Name eq 'Product Name'&$orderby=CreatedOn desc
```

## Navigation Property Notes

1. **ChangeNotice → ChangeTasks**: One-to-Many. A change notice can have multiple change tasks for implementation.

2. **ChangeNotice → ChangeRequests**: Many-to-Many. A change notice can be linked to multiple change requests and vice versa.

3. **ChangeNotice → AffectedObjects**: One-to-Many. Objects that will be impacted by the change.

4. **ChangeNotice → ResultingObjects**: One-to-Many. New objects created or modified by the change.

5. **ChangeTask → ChangeNotice**: Many-to-One. Each change task belongs to one change notice.

6. **ChangeTask → ResultingObjects**: One-to-Many. Objects created or modified by this specific task.

7. **ChangeRequest → ChangeNotices**: Many-to-Many. A change request can lead to multiple change notices.

8. **ChangeRequest → AffectedObjects**: One-to-Many. Objects identified for impact in the request.
