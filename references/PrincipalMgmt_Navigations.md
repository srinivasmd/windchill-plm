# PrincipalMgmt Domain - Navigation Properties

This document describes all navigation properties and entity relationships in the PrincipalMgmt domain.

## Entity Relationship Diagram

```
┌───────────────────────────────────────────────────────────────────────────────┐
│ PTC.PrincipalMgmt Namespace                                                    │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────────────┐      Members      ┌──────────────────┐                 │
│  │      Group       │◄─────────────────►│       User       │                 │
│  ├──────────────────┤                   ├──────────────────┤                 │
│  │ - Members        │                   │ - Groups         │                 │
│  │ - ParentGroups   │                   │ - Organization   │                 │
│  │ - ChildGroups    │                   │ - Context        │                 │
│  │ - Context        │                   └──────────────────┘                 │
│  └────────┬─────────┘                           ▲                            │
│           │                                     │                            │
│           │ ParentGroups                        │ Organization               │
│           │                                     │                            │
│           ▼                                     │                            │
│  ┌──────────────────┐                           │                            │
│  │      Group       │                           │                            │
│  │  (Parent Group)  │                           │                            │
│  └──────────────────┘                           │                            │
│                                                 │                            │
│  ┌──────────────────┐      Users        ┌──────┴─────────┐                  │
│  │   Organization   │───────────────────►│      User      │                  │
│  ├──────────────────┤                    └────────────────┘                  │
│  │ - Users          │                                                        │
│  │ - Groups         │                                                        │
│  │ - Context        │                                                        │
│  └──────────────────┘                                                        │
│                                                                               │
│  ┌──────────────────┐                  ┌──────────────────┐                  │
│  │  UserPrincipal   │──────────────────►│      User        │                  │
│  ├──────────────────┤      User        ├──────────────────┤                  │
│  │ - User           │                  │                  │                  │
│  └──────────────────┘                  └──────────────────┘                  │
│                                                                               │
│  ┌──────────────────┐                  ┌──────────────────┐                  │
│  │ GroupPrincipal   │──────────────────►│      Group       │                  │
│  ├──────────────────┤      Group       ├──────────────────┤                  │
│  │ - Group          │                  │                  │                  │
│  └──────────────────┘                  └──────────────────┘                  │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
```

## Navigation Properties by Entity

### User

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context (Product, Library, Project) |
| Groups | Collection(PTC.PrincipalMgmt.Group) | Groups the user belongs to |
| Organization | PTC.PrincipalMgmt.Organization | User's organization |

### Group

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context |
| Members | Collection(PTC.PrincipalMgmt.User) | Users in this group |
| ParentGroups | Collection(PTC.PrincipalMgmt.Group) | Parent groups (group hierarchy) |
| ChildGroups | Collection(PTC.PrincipalMgmt.Group) | Child groups (group hierarchy) |

### Organization

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context |
| Users | Collection(PTC.PrincipalMgmt.User) | Users in organization |
| Groups | Collection(PTC.PrincipalMgmt.Group) | Groups in organization |

### UserPrincipal

| Navigation | Type | Description |
|------------|------|-------------|
| User | PTC.PrincipalMgmt.User | Associated user |

### GroupPrincipal

| Navigation | Type | Description |
|------------|------|-------------|
| Group | PTC.PrincipalMgmt.Group | Associated group |

## Cross-Domain References

The PrincipalMgmt domain has navigation properties that reference entities from other domains:

| From Entity | Navigation Property | Target Domain | Target Entity |
|-------------|---------------------|---------------|---------------|
| User | Context | DataAdmin | Container |
| Group | Context | DataAdmin | Container |
| Organization | Context | DataAdmin | Container |

## OData Query Examples

### Get user with groups

```
GET /PrincipalMgmt/Users('{id}')?$expand=Groups
```

### Get user with organization

```
GET /PrincipalMgmt/Users('{id}')?$expand=Organization
```

### Get user with full details

```
GET /PrincipalMgmt/Users('{id}')?$expand=Groups($expand=ParentGroups),Organization,Context
```

### Get group with members

```
GET /PrincipalMgmt/Groups('{id}')?$expand=Members
```

### Get group with parent and child groups

```
GET /PrincipalMgmt/Groups('{id}')?$expand=ParentGroups,ChildGroups,Members
```

### Get organization with users

```
GET /PrincipalMgmt/Organizations('{id}')?$expand=Users
```

### Get organization with groups

```
GET /PrincipalMgmt/Organizations('{id}')?$expand=Groups($expand=Members)
```

### Get users in a group

```
GET /PrincipalMgmt/Groups('{id}')/Members?$expand=Organization
```

### Get groups for a user

```
GET /PrincipalMgmt/Users('{id}')/Groups?$expand=ParentGroups
```

### Multi-level expansion

```
GET /PrincipalMgmt/Users('{id}')?$expand=
  Groups($expand=ParentGroups($expand=Members),ChildGroups($expand=Members)),
  Organization($expand=Groups($expand=Members))
```

### Get users by group name

```
GET /PrincipalMgmt/Users?$expand=Groups&$filter=Groups/any(g: g/Name eq 'Designers')
```

### Get group hierarchy

```
GET /PrincipalMgmt/Groups?$expand=ParentGroups,ChildGroups,Members
```

## Entity Sets

| Entity Set | Entity Type | Description |
|------------|-------------|-------------|
| Users | User | All users |
| Groups | Group | All groups |
| Organizations | Organization | All organizations |
| UserPrincipals | UserPrincipal | All user principals |
| GroupPrincipals | GroupPrincipal | All group principals |

## Common Query Patterns

### Get user by username

```
GET /PrincipalMgmt/Users?$filter=Name eq 'jdoe'&$expand=Groups,Organization
```

### Get user by email

```
GET /PrincipalMgmt/Users?$filter=Email eq 'john.doe@company.com'&$expand=Groups
```

### Get all users in a department

```
GET /PrincipalMgmt/Users?$filter=Department eq 'Engineering'&$expand=Organization
```

### Get active users

```
GET /PrincipalMgmt/Users?$filter=Disabled eq false&$expand=Groups&$orderby=Name asc
```

### Get service accounts

```
GET /PrincipalMgmt/Users?$filter=ServiceUser eq true&$expand=Groups
```

### Get group with full member details

```
GET /PrincipalMgmt/Groups('{id}')?$expand=Members($expand=Organization,Groups)
```

### Get nested group hierarchy

```
GET /PrincipalMgmt/Groups?$expand=ParentGroups($expand=ParentGroups),ChildGroups($expand=ChildGroups)
```

### Count members in a group

```
GET /PrincipalMgmt/Groups('{id}')/Members/$count
```

### Get users in organization

```
GET /PrincipalMgmt/Organizations('{id}')/Users?$filter=Disabled eq false&$expand=Groups
```

## Navigation Property Notes

1. **User → Groups**: Many-to-Many. A user can belong to multiple groups.

2. **Group → Members**: Many-to-Many. A group can have multiple members.

3. **Group → ParentGroups**: Many-to-Many. Groups can have multiple parent groups for hierarchy.

4. **Group → ChildGroups**: Many-to-Many. Groups can have multiple child groups for hierarchy.

5. **User → Organization**: Many-to-One. A user belongs to one organization.

6. **Organization → Users**: One-to-Many. An organization can have multiple users.

7. **Organization → Groups**: One-to-Many. An organization can have multiple groups.

8. **UserPrincipal → User**: One-to-One. Principal to user reference.

9. **GroupPrincipal → Group**: One-to-One. Principal to group reference.
