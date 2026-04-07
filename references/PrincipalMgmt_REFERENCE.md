# Principal Management (PrincipalMgmt) Domain Reference

Complete reference documentation for the Windchill Principal Management OData domain.

## Base URL

```
https://windchill.example.com/Windchill/servlet/odata/PrincipalMgmt/
```

## Metadata URL

```
https://windchill.example.com/Windchill/servlet/odata/PrincipalMgmt/$metadata
```

## Domain Overview

The Principal Management (PrincipalMgmt) domain provides access to Windchill's user and group management entities:

### User Management
- **Users** - Windchill user accounts
- **UserPrincipal** - User principal objects

### Group Management
- **Groups** - User groups
- **GroupPrincipal** - Group principal objects

### Organization
- **Organizations** - Organizations
- **OrganizationPrincipal** - Organization principal objects

---

## Entity Types

### User

Windchill user account representing an individual user.

**Endpoint:** `/PrincipalMgmt/Users`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Username (login name) |
| **FullName** | String | Full display name |
| **Email** | String | Email address |
| **Phone** | String | Phone number |
| **Department** | String | Department |
| **Title** | String | Job title |
| **Organization** | String | Organization name |
| **Description** | String | User description |
| **Disabled** | Boolean | Whether account is disabled |
| **ServiceUser** | Boolean | Whether this is a service account |
| **ExternalDirectory** | Boolean | Whether from external directory |
| **LastLogin** | DateTimeOffset | Last login timestamp |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` → PTC.DataAdmin.Container (Container context)
- `Groups` → Collection(PTC.PrincipalMgmt.Group) (Groups user belongs to)
- `Organization` → PTC.PrincipalMgmt.Organization (User's organization)

**CRUD Operations:**

```bash
# Get all users
GET /PrincipalMgmt/Users

# Get user by ID
GET /PrincipalMgmt/Users('{id}')

# Get user by name (username)
GET /PrincipalMgmt/Users?$filter=Name eq 'jdoe'

# Search by full name
GET /PrincipalMgmt/Users?$filter=contains(FullName, 'John')

# Get active users
GET /PrincipalMgmt/Users?$filter=Disabled eq false

# Get user with groups
GET /PrincipalMgmt/Users('{id}')?$expand=Groups

# Get user with organization
GET /PrincipalMgmt/Users?$expand=Organization

# Select specific properties
GET /PrincipalMgmt/Users?$select=ID,Name,FullName,Email

# Order by name
GET /PrincipalMgmt/Users?$orderby=Name asc

# Top results
GET /PrincipalMgmt/Users?$top=100
```

---

### Group

User group for organizing users and assigning permissions.

**Endpoint:** `/PrincipalMgmt/Groups`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Group name |
| **Description** | String | Group description |
| **GroupType** | String | Type of group |
| **ServiceGroup** | Boolean | Whether this is a service group |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` → PTC.DataAdmin.Container (Container context)
- `Members` → Collection(PTC.PrincipalMgmt.User) (Users in this group)
- `ParentGroups` → Collection(PTC.PrincipalMgmt.Group) (Parent groups)
- `ChildGroups` → Collection(PTC.PrincipalMgmt.Group) (Child groups)

**CRUD Operations:**

```bash
# Get all groups
GET /PrincipalMgmt/Groups

# Get group by ID
GET /PrincipalMgmt/Groups('{id}')

# Get group by name
GET /PrincipalMgmt/Groups?$filter=Name eq 'Designers'

# Search by name
GET /PrincipalMgmt/Groups?$filter=contains(Name, 'Admin')

# Get group with members
GET /PrincipalMgmt/Groups('{id}')?$expand=Members

# Get group with parent groups
GET /PrincipalMgmt/Groups('{id}')?$expand=ParentGroups

# Get group with child groups
GET /PrincipalMgmt/Groups('{id}')?$expand=ChildGroups

# Select specific properties
GET /PrincipalMgmt/Groups?$select=ID,Name,Description

# Order by name
GET /PrincipalMgmt/Groups?$orderby=Name asc
```

---

### Organization

Organization entity for company/department structure.

**Endpoint:** `/PrincipalMgmt/Organizations`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Organization name |
| **Description** | String | Organization description |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` → PTC.DataAdmin.Container (Container context)
- `Users` → Collection(PTC.PrincipalMgmt.User) (Users in organization)
- `Groups` → Collection(PTC.PrincipalMgmt.Group) (Groups in organization)

**CRUD Operations:**

```bash
# Get all organizations
GET /PrincipalMgmt/Organizations

# Get organization by ID
GET /PrincipalMgmt/Organizations('{id}')

# Get organization by name
GET /PrincipalMgmt/Organizations?$filter=Name eq 'Engineering'

# Get organization with users
GET /PrincipalMgmt/Organizations('{id}')?$expand=Users

# Get organization with groups
GET /PrincipalMgmt/Organizations('{id}')?$expand=Groups
```

---

### UserPrincipal

User principal object (extended user information).

**Endpoint:** `/PrincipalMgmt/UserPrincipals`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Principal name |
| **PrincipalType** | String | Principal type |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- `User` → PTC.PrincipalMgmt.User (Associated user)

---

### GroupPrincipal

Group principal object (extended group information).

**Endpoint:** `/PrincipalMgmt/GroupPrincipals`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Principal name |
| **PrincipalType** | String | Principal type |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- `Group` → PTC.PrincipalMgmt.Group (Associated group)

---

## Common Query Examples

### Get All Active Users

```bash
GET /PrincipalMgmt/Users?$filter=Disabled eq false&$orderby=Name asc
```

### Find Users by Email Domain

```bash
GET /PrincipalMgmt/Users?$filter=contains(Email, '@company.com')
```

### Get Users in a Group

```bash
GET /PrincipalMgmt/Groups('{group_id}')/Members
```

### Get Groups for a User

```bash
GET /PrincipalMgmt/Users('{user_id}')/Groups
```

### Find Group Administrators

```bash
GET /PrincipalMgmt/Groups?$filter=contains(Name, 'Admin')&$expand=Members
```

### Get Users in Organization

```bash
GET /PrincipalMgmt/Organizations('{org_id}')/Users?$filter=Disabled eq false
```

### Search Users by Department

```bash
GET /PrincipalMgmt/Users?$filter=Department eq 'Engineering'&$expand=Organization
```

### Get User with All Groups

```bash
GET /PrincipalMgmt/Users('{id}')?$expand=Groups($expand=ParentGroups),Organization
```

### Count Users in a Group

```bash
GET /PrincipalMgmt/Groups('{id}')/Members/$count
```

### Get Service Accounts

```bash
GET /PrincipalMgmt/Users?$filter=ServiceUser eq true
```

---

## Entity Relationships

```
┌─────────────────────────────────────────────────────────────────────────┐
│ PTC.PrincipalMgmt Namespace                                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌────────────────┐      Members      ┌────────────────┐               │
│  │     Group      │◄─────────────────►│      User      │               │
│  ├────────────────┤                   ├────────────────┤               │
│  │ - Members      │                   │ - Groups       │               │
│  │ - ParentGroups │                   │ - Organization │               │
│  │ - ChildGroups  │                   │ - Context      │               │
│  │ - Context      │                   └────────────────┘               │
│  └────────┬───────┘                           ▲                        │
│           │                                   │                        │
│           │ ParentGroups                      │ Organization           │
│           │                                   │                        │
│           ▼                                   │                        │
│  ┌────────────────┐                           │                        │
│  │     Group      │                           │                        │
│  │ (Parent Group) │                           │                        │
│  └────────────────┘                           │                        │
│                                               │                        │
│  ┌────────────────┐      Users      ┌────────┴───────┐                │
│  │  Organization  │─────────────────►│      User      │                │
│  ├────────────────┤                  └────────────────┘                │
│  │ - Users        │                                                     │
│  │ - Groups       │                                                     │
│  │ - Context      │                                                     │
│  └────────────────┘                                                     │
│                                                                         │
│  ┌────────────────┐                  ┌────────────────┐                │
│  │ UserPrincipal  │──────────────────►│      User      │                │
│  └────────────────┘      User        └────────────────┘                │
│                                                                         │
│  ┌────────────────┐                  ┌────────────────┐                │
│  │ GroupPrincipal │──────────────────►│     Group      │                │
│  └────────────────┘      Group       └────────────────┘                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Cross-Domain References

| From Entity | Navigation Property | Target Domain | Target Entity |
|-------------|---------------------|---------------|---------------|
| User | Context | DataAdmin | Container |
| Group | Context | DataAdmin | Container |
| Organization | Context | DataAdmin | Container |

---

## Pagination

Use `$top` and `$skip` for pagination:

```bash
GET /PrincipalMgmt/Users?$top=50&$skip=0
GET /PrincipalMgmt/Users?$top=50&$skip=50
```

---

## Notes

1. **READ-ONLY Access** - User and group objects are typically read through OData. User management is done through Windchill UI or JNDI/LDAP integration.

2. **Authentication** - Users are often managed through external directory services (LDAP, Active Directory) integrated with Windchill.

3. **Service Users** - Service accounts are special users used for system operations and integrations.

4. **Group Hierarchy** - Groups can have parent and child groups, creating a hierarchical structure.

5. **Object Identifiers** - IDs are OIDs in format `OR:wt.org.WTUser:xxxxx` for users.

6. **Naming Convention** - The `Name` property is typically the username/login name, while `FullName` is the display name.

7. **Context Reference** - Users and groups can be associated with specific containers (Products, Projects, Libraries).
