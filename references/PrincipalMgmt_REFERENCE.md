# Principal Management (PrincipalMgmt) Domain Reference

Complete reference documentation for the Windchill Principal Management OData domain.

## Base URL

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/PrincipalMgmt/
```

## Metadata URL

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/PrincipalMgmt/$metadata
```

## Domain Overview

The Principal Management domain provides access to Windchill user and group management including:

### User Management
- **User** - Windchill users and their profiles
- **Organization** - Organizational units
- **WTUser** - Base user type

### Group Management
- **Group** - User groups and teams
- **Role** - Role definitions

---

## Entity Types

### User

Windchill user account with profile information.

**Endpoint:** `/PrincipalMgmt/Users`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Username (login name) |
| **FullName** | String | User's full display name |
| **Email** | String | User's email address |
| **FirstName** | String | User's first name |
| **LastName** | String | User's last name |
| **Title** | String | Job title |
| **Organization** | String | Organization name |
| **Department** | String | Department name |
| **Location** | String | Physical location |
| **Phone** | String | Phone number |
| **Fax** | String | Fax number |
| **Pager** | String | Pager number |
| **Disabled** | Boolean | Whether account is disabled |
| **ServiceUser** | Boolean | Whether this is a service account |
| **CreatedOn** | DateTimeOffset | Account creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` - Container (PTC.DataAdmin.Container)
- `Organization` - Organization (PTC.PrincipalMgmt.Organization)
- `Groups` - Collection of Groups the user belongs to
- `Roles` - Collection of Roles assigned to the user

**CRUD Operations:**

```bash
# Get all users
GET /PrincipalMgmt/Users

# Get user by ID
GET /PrincipalMgmt/Users('{id}')

# Get user by name (username)
GET /PrincipalMgmt/Users?$filter=Name eq 'admin'

# Get user by full name
GET /PrincipalMgmt/Users?$filter=FullName eq 'John Smith'

# Search users by name
GET /PrincipalMgmt/Users?$filter=contains(Name, 'john') or contains(FullName, 'John')

# Filter by email
GET /PrincipalMgmt/Users?$filter=Email eq 'john@example.com'

# Filter by organization
GET /PrincipalMgmt/Users?$filter=Organization eq 'Engineering'

# Filter active users only
GET /PrincipalMgmt/Users?$filter=Disabled eq false

# Expand with organization
GET /PrincipalMgmt/Users('{id}')?$expand=Organization

# Expand with groups
GET /PrincipalMgmt/Users('{id}')?$expand=Groups

# Expand with all navigations
GET /PrincipalMgmt/Users('{id}')?$expand=Context,Organization,Groups,Roles

# Select specific properties
GET /PrincipalMgmt/Users?$select=ID,Name,FullName,Email,Title

# Order by name
GET /PrincipalMgmt/Users?$orderby=Name asc
GET /PrincipalMgmt/Users?$orderby=FullName asc

# Top N users
GET /PrincipalMgmt/Users?$top=100

# Count users
GET /PrincipalMgmt/Users/$count

# Count active users
GET /PrincipalMgmt/Users/$count?$filter=Disabled eq false
```

---

### Group

User group for access control and team management.

**Endpoint:** `/PrincipalMgmt/Groups`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Group name |
| **Description** | String | Group description |
| **GroupType** | EnumType | Type of group (STATIC, DYNAMIC) |
| **ServiceGroup** | Boolean | Whether this is a service group |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` - Container (PTC.DataAdmin.Container)
- `ParentGroup` - Parent group (nested groups)
- `ChildGroups` - Collection of child groups
- `Members` - Collection of Users in this group
- `Roles` - Collection of Roles assigned to this group

**CRUD Operations:**

```bash
# Get all groups
GET /PrincipalMgmt/Groups

# Get group by ID
GET /PrincipalMgmt/Groups('{id}')

# Get group by name
GET /PrincipalMgmt/Groups?$filter=Name eq 'Engineering Team'

# Search groups by name
GET /PrincipalMgmt/Groups?$filter=contains(Name, 'Engineering')

# Get group with members
GET /PrincipalMgmt/Groups('{id}')?$expand=Members

# Get group with child groups
GET /PrincipalMgmt/Groups('{id}')?$expand=ChildGroups

# Get group with parent group
GET /PrincipalMgmt/Groups('{id}')?$expand=ParentGroup

# Expand all relationships
GET /PrincipalMgmt/Groups('{id}')?$expand=Context,ParentGroup,ChildGroups,Members,Roles

# Select specific properties
GET /PrincipalMgmt/Groups?$select=ID,Name,Description

# Order by name
GET /PrincipalMgmt/Groups?$orderby=Name asc

# Count groups
GET /PrincipalMgmt/Groups/$count
```

---

### Organization

Organizational unit for user management.

**Endpoint:** `/PrincipalMgmt/Organizations`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Organization name |
| **Description** | String | Organization description |
| **OrganizationType** | EnumType | Type of organization |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` - Container (PTC.DataAdmin.Container)
- `ParentOrganization` - Parent organization
- `ChildOrganizations` - Collection of child organizations
- `Users` - Collection of Users in this organization
- `Groups` - Collection of Groups in this organization

**CRUD Operations:**

```bash
# Get all organizations
GET /PrincipalMgmt/Organizations

# Get organization by name
GET /PrincipalMgmt/Organizations?$filter=Name eq 'Engineering'

# Get organization with users
GET /PrincipalMgmt/Organizations('{id}')?$expand=Users

# Get organization with groups
GET /PrincipalMgmt/Organizations('{id}')?$expand=Groups

# Expand all relationships
GET /PrincipalMgmt/Organizations('{id}')?$expand=Context,ParentOrganization,ChildOrganizations,Users,Groups
```

---

### Role

Role definition for access control.

**Endpoint:** `/PrincipalMgmt/Roles`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Role name |
| **Description** | String | Role description |
| **RoleType** | EnumType | Type of role (SYSTEM, CUSTOM) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` - Container (PTC.DataAdmin.Container)
- `Users` - Collection of Users with this role
- `Groups` - Collection of Groups with this role

**CRUD Operations:**

```bash
# Get all roles
GET /PrincipalMgmt/Roles

# Get role by name
GET /PrincipalMgmt/Roles?$filter=Name eq 'Designer'

# Get role with users
GET /PrincipalMgmt/Roles('{id}')?$expand=Users

# Get role with groups
GET /PrincipalMgmt/Roles('{id}')?$expand=Groups
```

---

## Common Query Examples

### Find Users by Various Criteria

```bash
# Find users by partial name match
GET /PrincipalMgmt/Users?$filter=contains(FullName, 'Smith')

# Find users by department
GET /PrincipalMgmt/Users?$filter=Department eq 'Engineering'

# Find users by title
GET /PrincipalMgmt/Users?$filter=Title eq 'Engineer'

# Find active users in an organization
GET /PrincipalMgmt/Users?$filter=Organization eq 'Engineering' and Disabled eq false

# Find service accounts
GET /PrincipalMgmt/Users?$filter=ServiceUser eq true
```

### Find Group Memberships

```bash
# Get all groups a user belongs to
GET /PrincipalMgmt/Users('{id}')/Groups

# Get all members of a group
GET /PrincipalMgmt/Groups('{id}')/Members

# Get nested group memberships
GET /PrincipalMgmt/Groups('{id}')?$expand=ChildGroups($expand=Members)
```

### Find Role Assignments

```bash
# Get all roles for a user
GET /PrincipalMgmt/Users('{id}')/Roles

# Get all users with a specific role
GET /PrincipalMgmt/Roles?$filter=Name eq 'Admin'&$expand=Users

# Get all groups with a specific role
GET /PrincipalMgmt/Roles?$filter=Name eq 'Designer'&$expand=Groups
```

### Organizational Hierarchy

```bash
# Get organizational hierarchy
GET /PrincipalMgmt/Organizations?$expand=ParentOrganization,ChildOrganizations

# Get all users in an organization tree
GET /PrincipalMgmt/Organizations('{id}')?$expand=Users,ChildOrganizations($expand=Users)
```

---

## Cross-Domain References

The PrincipalMgmt domain is referenced by many other domains:

### Workflow Domain
- WorkItem Owner references User
- WorkItem CompletedBy references User
- Activity assignees reference User

### Change Management Domain
- ChangeNotice Creator/Modifier references User
- ChangeRequest Creator/Modifier references User

### Product Management Domain
- Part Creator/Modifier references User
- Document Creator/Modifier references User

### Quality Management Domain
- QualityContact references User

---

## Integration Notes

1. **READ-ONLY Access**: The PrincipalMgmt domain is primarily read-only through OData. User and group management is typically done through Windchill UI or admin tools.

2. **Caching**: User information is frequently cached by other domains. Use navigation properties to get the latest user information.

3. **Service Accounts**: Service users (system accounts) have the ServiceUser flag set to true.

4. **Disabled Users**: Check the Disabled flag before assuming a user is active.

5. **Group Hierarchy**: Groups can be nested using ParentGroup/ChildGroups navigation.

6. **Organization Hierarchy**: Organizations can be nested using ParentOrganization/ChildOrganizations navigation.

---

## Schema Version

Schema Version: 6
