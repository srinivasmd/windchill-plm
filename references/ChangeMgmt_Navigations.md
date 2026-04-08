# ChangeMgmt Domain Navigation Properties

## Navigation Relationships

This document describes the navigation properties between entities in the ChangeMgmt domain and cross-domain references.

---

## ChangeNotice Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Context` | Container | DataAdmin | Container context (Product, Library, Project) |
| `Creator` | User | PrincipalMgmt | User who created the change notice |
| `Modifier` | User | PrincipalMgmt | User who last modified the change notice |
| `ChangeRequest` | ChangeRequest | ChangeMgmt | Related Change Request |
| `ChangeTasks` | Collection(ChangeTask) | ChangeMgmt | Collection of Change Tasks |
| `AffectedObjects` | Collection(AffectedObject) | ChangeMgmt | Objects affected by this change |
| `ResultingObjects` | Collection(ResultingObject) | ChangeMgmt | Objects resulting from this change |
| `ChangeActivities` | Collection(ChangeActivity2) | ChangeMgmt | Related Change Activities |

### Navigation Examples

```bash
# Get container context
GET /ChangeMgmt/ChangeNotices('{id}')/Context

# Get creator
GET /ChangeMgmt/ChangeNotices('{id}')/Creator

# Get change tasks
GET /ChangeMgmt/ChangeNotices('{id}')/ChangeTasks

# Get affected objects
GET /ChangeMgmt/ChangeNotices('{id}')/AffectedObjects

# Get resulting objects
GET /ChangeMgmt/ChangeNotices('{id}')/ResultingObjects

# Expand multiple navigations
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=Context,Creator,ChangeTasks,AffectedObjects

# Nested expansion
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=ChangeTasks($expand=AffectedObjects)
```

---

## ChangeRequest Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Context` | Container | DataAdmin | Container context |
| `Creator` | User | PrincipalMgmt | User who created the request |
| `Modifier` | User | PrincipalMgmt | User who last modified the request |
| `ChangeNotices` | Collection(ChangeNotice) | ChangeMgmt | Related Change Notices |
| `AffectedObjects` | Collection(AffectedObject) | ChangeMgmt | Objects affected by this request |
| `ChangeActivities` | Collection(ChangeActivity2) | ChangeMgmt | Related Change Activities |

### Navigation Examples

```bash
# Get change notices from a change request
GET /ChangeMgmt/ChangeRequests('{id}')/ChangeNotices

# Get affected objects
GET /ChangeMgmt/ChangeRequests('{id}')/AffectedObjects

# Expand with change notices
GET /ChangeMgmt/ChangeRequests('{id}')?$expand=ChangeNotices,AffectedObjects
```

---

## ChangeTask Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Context` | Container | DataAdmin | Container context |
| `Creator` | User | PrincipalMgmt | User who created the task |
| `Modifier` | User | PrincipalMgmt | User who last modified the task |
| `ChangeNotice` | ChangeNotice | ChangeMgmt | Parent Change Notice |
| `AffectedObjects` | Collection(AffectedObject) | ChangeMgmt | Objects affected by this task |
| `ResultingObjects` | Collection(ResultingObject) | ChangeMgmt | Objects resulting from this task |

### Navigation Examples

```bash
# Get parent change notice
GET /ChangeMgmt/ChangeTasks('{id}')/ChangeNotice

# Get affected objects for a task
GET /ChangeMgmt/ChangeTasks('{id}')/AffectedObjects

# Get resulting objects for a task
GET /ChangeMgmt/ChangeTasks('{id}')/ResultingObjects

# Expand with parent change notice
GET /ChangeMgmt/ChangeTasks('{id}')?$expand=ChangeNotice,AffectedObjects,ResultingObjects
```

---

## ChangeActivity2 Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Context` | Container | DataAdmin | Container context |
| `Creator` | User | PrincipalMgmt | User who created the activity |
| `Modifier` | User | PrincipalMgmt | User who last modified the activity |
| `ChangeNotice` | ChangeNotice | ChangeMgmt | Related Change Notice |
| `ChangeRequest` | ChangeRequest | ChangeMgmt | Related Change Request |
| `AffectedObjects` | Collection(AffectedObject) | ChangeMgmt | Objects affected by this activity |
| `ResultingObjects` | Collection(ResultingObject) | ChangeMgmt | Objects resulting from this activity |

### Navigation Examples

```bash
# Get related change notice
GET /ChangeMgmt/ChangeActivities('{id}')/ChangeNotice

# Get related change request
GET /ChangeMgmt/ChangeActivities('{id}')/ChangeRequest

# Get affected objects
GET /ChangeMgmt/ChangeActivities('{id}')/AffectedObjects

# Expand all relationships
GET /ChangeMgmt/ChangeActivities('{id}')?$expand=ChangeNotice,ChangeRequest,AffectedObjects,ResultingObjects
```

---

## AffectedObject Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Changeable` | Part or Document | ProdMgmt/DocMgmt | The actual object being affected |
| `ChangeActivity2` | ChangeActivity2 | ChangeMgmt | Related Change Activity |
| `ChangeNotice` | ChangeNotice | ChangeMgmt | Related Change Notice |

### Navigation Examples

```bash
# Get the actual affected object (Part or Document)
GET /ChangeMgmt/ChangeNotices('{id}')/AffectedObjects('{affected_id}')/Changeable

# Expand with the actual object
GET /ChangeMgmt/ChangeNotices('{id}')/AffectedObjects?$expand=Changeable
```

---

## ResultingObject Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `ResultingChangeable` | Part or Document | ProdMgmt/DocMgmt | The actual resulting object |
| `ChangeActivity2` | ChangeActivity2 | ChangeMgmt | Related Change Activity |
| `ChangeNotice` | ChangeNotice | ChangeMgmt | Related Change Notice |

### Navigation Examples

```bash
# Get the actual resulting object (Part or Document)
GET /ChangeMgmt/ChangeNotices('{id}')/ResultingObjects('{resulting_id}')/ResultingChangeable

# Expand with the actual object
GET /ChangeMgmt/ChangeNotices('{id}')/ResultingObjects?$expand=ResultingChangeable
```

---

## Cross-Domain Navigation Paths

### Change to Part

```bash
# Path: ChangeNotice -> AffectedObjects -> Changeable (Part)
GET /ChangeMgmt/ChangeNotices('{id}')/AffectedObjects?$expand=Changeable

# Path: ChangeNotice -> ResultingObjects -> ResultingChangeable (Part)
GET /ChangeMgmt/ChangeNotices('{id}')/ResultingObjects?$expand=ResultingChangeable

# Nested expansion to get part details
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=AffectedObjects($expand=Changeable($select=Number,Name,Version))
```

### Change to Document

```bash
# Path: ChangeNotice -> AffectedObjects -> Changeable (Document)
GET /ChangeMgmt/ChangeNotices('{id}')/AffectedObjects?$expand=Changeable

# Get documents affected by a change
GET /ChangeMgmt/ChangeNotices('{id}')/AffectedObjects?$filter=ObjectType eq 'wt.doc.WTDocument'&$expand=Changeable
```

### Change to CAD Document

```bash
# Path: ChangeNotice -> AffectedObjects -> Changeable (CAD Document)
GET /ChangeMgmt/ChangeNotices('{id}')/AffectedObjects?$filter=contains(ObjectType, 'EPMAuthoringApp')&$expand=Changeable
```

---

## Relationship Diagram

```
┌─────────────────┐
│ ChangeRequest   │
│  (ECR)          │
└────────┬────────┘
         │
         │ ChangeNotices
         ▼
┌─────────────────┐        ChangeTasks        ┌─────────────────┐
│ ChangeNotice    │◄─────────────────────────►│ ChangeTask      │
│  (ECN)          │                           │                 │
└────────┬────────┘                           └────────┬────────┘
         │                                             │
         │ AffectedObjects                             │ AffectedObjects
         │ ResultingObjects                            │ ResultingObjects
         ▼                                             ▼
┌─────────────────┐                           ┌─────────────────┐
│ AffectedObject  │                           │ ResultingObject │
└────────┬────────┘                           └────────┬────────┘
         │                                             │
         │ Changeable                                  │ ResultingChangeable
         ▼                                             ▼
┌─────────────────┐                           ┌─────────────────┐
│ Part/Document   │                           │ Part/Document   │
│ (ProdMgmt/      │                           │ (ProdMgmt/      │
│  DocMgmt)       │                           │  DocMgmt)       │
└─────────────────┘                           └─────────────────┘
```

---

## Common Navigation Patterns

### Get Complete Change Information

```bash
# Get change notice with all related objects
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=
    Context,
    Creator,
    ChangeTasks($expand=AffectedObjects,ResultingObjects),
    AffectedObjects($expand=Changeable),
    ResultingObjects($expand=ResultingChangeable)
```

### Get Change Request with Notices and Objects

```bash
# Get change request with all change notices and affected objects
GET /ChangeMgmt/ChangeRequests('{id}')?$expand=
    ChangeNotices($expand=ChangeTasks,AffectedObjects),
    AffectedObjects($expand=Changeable)
```

### Get All Changes for a Part

```bash
# First get the part ID from ProdMgmt
# Then query affected objects
GET /ChangeMgmt/AffectedObjects?$filter=Changeable/ID eq '{part_id}'&$expand=ChangeNotice,ChangeActivity2
```

---

## Notes

1. **Navigation Performance**: Expanding multiple navigation properties can impact performance. Only expand what you need.

2. **Cross-Domain Navigations**: Changeable and ResultingChangeable can reference entities in ProdMgmt, DocMgmt, or CADDocumentMgmt domains.

3. **Bidirectional Relationships**: ChangeNotice <-> ChangeTask is bidirectional. You can navigate from either direction.

4. **Collection vs Single**: Some navigation properties return collections (ChangeTasks, AffectedObjects), others return single entities (Creator, Modifier).

5. **Filtering on Navigation Properties**: You can filter based on navigation properties:
   ```bash
   GET /ChangeMgmt/ChangeNotices?$filter=Creator/Name eq 'admin'
   GET /ChangeMgmt/ChangeTasks?$filter=ChangeNotice/Number eq 'CN-000001'
   ```
