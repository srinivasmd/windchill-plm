# PrincipalMgmt Domain Navigation Properties

## Navigation Relationships

This document describes the navigation properties between entities in the PrincipalMgmt domain and cross-domain references.

---

## User Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Context` | Container | DataAdmin | Container context |
| `Organization` | Organization | PrincipalMgmt | Organization the user belongs to |
| `Groups` | Collection(Group) | PrincipalMgmt | Groups the user belongs to |
| `Roles` | Collection(Role) | PrincipalMgmt | Roles assigned to the user |

### Navigation Examples

```bash
# Get user's organization
GET /PrincipalMgmt/Users('{id}')/Organization

# Get user's groups
GET /PrincipalMgmt/Users('{id}')/Groups

# Get user's roles
GET /PrincipalMgmt/Users('{id}')/Roles

# Expand all navigations
GET /PrincipalMgmt/Users('{id}')?$expand=Organization,Groups,Roles

# Nested expansion
GET /PrincipalMgmt/Users('{id}')?$expand=Groups($expand=Roles)
```

---

## Group Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Context` | Container | DataAdmin | Container context |
| `ParentGroup` | Group | PrincipalMgmt | Parent group (nested groups) |
| `ChildGroups` | Collection(Group) | PrincipalMgmt | Child groups |
| `Members` | Collection(User) | PrincipalMgmt | Users in this group |
| `Roles` | Collection(Role) | PrincipalMgmt | Roles assigned to this group |

### Navigation Examples

```bash
# Get parent group
GET /PrincipalMgmt/Groups('{id}')/ParentGroup

# Get child groups
GET /PrincipalMgmt/Groups('{id}')/ChildGroups

# Get group members
GET /PrincipalMgmt/Groups('{id}')/Members

# Get group roles
GET /PrincipalMgmt/Groups('{id}')/Roles

# Expand all navigations
GET /PrincipalMgmt/Groups('{id}')?$expand=ParentGroup,ChildGroups,Members,Roles

# Nested expansion with member details
GET /PrincipalMgmt/Groups('{id}')?$expand=Members($expand=Organization,Roles),ChildGroups($expand=Members)
```

---

## Organization Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Context` | Container | DataAdmin | Container context |
| `ParentOrganization` | Organization | PrincipalMgmt | Parent organization |
| `ChildOrganizations` | Collection(Organization) | PrincipalMgmt | Child organizations |
| `Users` | Collection(User) | PrincipalMgmt | Users in this organization |
| `Groups` | Collection(Group) | PrincipalMgmt | Groups in this organization |

### Navigation Examples

```bash
# Get parent organization
GET /PrincipalMgmt/Organizations('{id}')/ParentOrganization

# Get child organizations
GET /PrincipalMgmt/Organizations('{id}')/ChildOrganizations

# Get organization users
GET /PrincipalMgmt/Organizations('{id}')/Users

# Get organization groups
GET /PrincipalMgmt/Organizations('{id}')/Groups

# Expand all navigations
GET /PrincipalMgmt/Organizations('{id}')?$expand=ParentOrganization,ChildOrganizations,Users,Groups

# Nested expansion
GET /PrincipalMgmt/Organizations('{id}')?$expand=Users($expand=Groups,Roles),ChildOrganizations($expand=Users)
```

---

## Role Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Context` | Container | DataAdmin | Container context |
| `Users` | Collection(User) | PrincipalMgmt | Users with this role |
| `Groups` | Collection(Group) | PrincipalMgmt | Groups with this role |

### Navigation Examples

```bash
# Get users with a role
GET /PrincipalMgmt/Roles('{id}')/Users

# Get groups with a role
GET /PrincipalMgmt/Roles('{id}')/Groups

# Expand all navigations
GET /PrincipalMgmt/Roles('{id}')?$expand=Users,Groups
```

---

## Cross-Domain Navigation Paths

### Workflow to User

```bash
# Path: WorkItem -> Owner (User)
GET /Workflow/WorkItems('{id}')/Owner

# Path: WorkItem -> CompletedBy (User)
GET /Workflow/WorkItems('{id}')/CompletedBy

# Path: Activity -> Context -> Creator
GET /Workflow/Activities('{id}')?$expand=CompletedBy
```

### Change Management to User

```bash
# Path: ChangeNotice -> Creator (User)
GET /ChangeMgmt/ChangeNotices('{id}')/Creator

# Path: ChangeNotice -> Modifier (User)
GET /ChangeMgmt/ChangeNotices('{id}')/Modifier

# Expand with user details
GET /ChangeMgmt/ChangeNotices?$expand=Creator,Modifier
```

### Product Management to User

```bash
# Path: Part -> Creator (User)
GET /ProdMgmt/Parts('{id}')/Creator

# Path: Document -> Modifier (User)
GET /DocMgmt/Documents('{id}')/Modifier
```

---

## Relationship Diagram

```
┌─────────────────┐
│ Organization    │
│                 │
└────────┬────────┘
         │
         │ Users, Groups
         ▼
┌─────────────────┐       ┌─────────────────┐
│ User            │◄─────►│ Group           │
│                 │       │                 │
└────────┬────────┘       └────────┬────────┘
         │                         │
         │ Roles                   │ Roles
         ▼                         ▼
┌─────────────────────────────────────────┐
│              Role                        │
│                                          │
└──────────────────────────────────────────┘

Group Hierarchy:
┌─────────────────┐
│ ParentGroup     │
│                 │
└────────┬────────┘
         │
         │ ChildGroups
         ▼
┌─────────────────┐
│ ChildGroup      │
│                 │
└─────────────────┘

Organization Hierarchy:
┌────────────────────┐
│ ParentOrganization │
│                    │
└────────┬───────────┘
         │
         │ ChildOrganizations
         ▼
┌────────────────────┐
│ ChildOrganization  │
│                    │
└────────────────────┘
```

---

## Common Navigation Patterns

### Get User with Full Context

```bash
GET /PrincipalMgmt/Users('{id}')?$expand=
    Organization,
    Groups($expand=Roles),
    Roles
```

### Get Group Hierarchy

```bash
# Get full group tree
GET /PrincipalMgmt/Groups?$expand=ParentGroup,ChildGroups

# Get nested groups with members
GET /PrincipalMgmt/Groups('{id}')?$expand=
    ParentGroup,
    ChildGroups($expand=Members),
    Members($expand=Organization)
```

### Get Organization with All Users

```bash
# Get organization with users and their groups
GET /PrincipalMgmt/Organizations('{id}')?$expand=
    Users($expand=Groups,Roles),
    Groups($expand=Members)
```

### Find All Users in Group Hierarchy

```bash
# Get group with nested groups and all members
GET /PrincipalMgmt/Groups('{id}')?$expand=
    Members,
    ChildGroups($expand=Members,ChildGroups($expand=Members))
```

---

## Cross-Domain Reference Summary

| Source Domain | Source Entity | Navigation | Target Domain | Target Entity |
|---------------|---------------|------------|---------------|---------------|
| Workflow | WorkItem | Owner | PrincipalMgmt | User |
| Workflow | WorkItem | CompletedBy | PrincipalMgmt | User |
| Workflow | WorkItem | OriginalOwner | PrincipalMgmt | User |
| ChangeMgmt | ChangeNotice | Creator | PrincipalMgmt | User |
| ChangeMgmt | ChangeNotice | Modifier | PrincipalMgmt | User |
| ChangeMgmt | ChangeRequest | Creator | PrincipalMgmt | User |
| ProdMgmt | Part | Creator | PrincipalMgmt | User |
| ProdMgmt | Part | Modifier | PrincipalMgmt | User |
| DocMgmt | Document | Creator | PrincipalMgmt | User |
| DocMgmt | Document | Modifier | PrincipalMgmt | User |
| CEM | CustomerExperience | Creator | PrincipalMgmt | User |
| Workflow | WorkItemProcessTemplate | Creator | PrincipalMgmt | User |
| QMS | QualityContact | User | PrincipalMgmt | User |

---

## Notes

1. **READ-ONLY Access**: The PrincipalMgmt domain is read-only through OData. User and group management requires Windchill UI or admin tools.

2. **Nested Hierarchies**: Both Groups and Organizations support nesting. Use ParentGroup/ChildGroups and ParentOrganization/ChildOrganizations for traversal.

3. **Performance Consideration**: Expanding large collections (Users, Members) can impact performance. Use `$top` and `$filter` to limit results.

4. **Bidirectional Relationships**: User <-> Group is bidirectional. You can navigate from either direction.

5. **Role Assignment**: Users can have roles directly or through groups. Check both User/Roles and Group/Roles.

6. **Cross-Domain Performance**: When navigating from other domains to User, the system may cache results. For the latest information, query PrincipalMgmt directly.
