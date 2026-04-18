---
Domain: PrincipalMgmt
Client: `from domains.PrincipalMgmt import PrincipalMgmtClient`
---

> **Use the PrincipalMgmtClient**: `from domains.PrincipalMgmt import PrincipalMgmtClient`
>
> This reference documents the entity types and properties. For programmatic access, use the domain client.

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

The Principal Management domain provides access to Windchill's user and group management:
- **Users** - Windchill user accounts
- **Groups** - User groups for access control
- **Organizations** - Organizational structures

---

## Entity Types

### User

A Windchill user account representing a person who can access the system.

**Endpoint:** `/PrincipalMgmt/Users`

**Operations:** `READ`

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Username (login ID) |
| **FullName** | String | User's full name |
| **Email** | String | User's email address |
| **Organization** | String | Organization name |
| **Disabled** | Boolean | Whether user account is disabled |
| **CreatedBy** | String | Creator username (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **ModifiedBy** | String | Last modifier username (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **Context** | PTC.DataAdmin.Container | Container context |
| **Groups** | Collection(PTC.PrincipalMgmt.Group) | Groups user belongs to |
| **Organization** | PTC.PrincipalMgmt.Organization | User's organization |

**CRUD Operations:**

```bash
# Get all users
GET /PrincipalMgmt/Users

# Get user by ID
GET /PrincipalMgmt/Users('{id}')

# Get user by name (username)
GET /PrincipalMgmt/Users?$filter=Name eq 'jsmith'

# Search users by full name
GET /PrincipalMgmt/Users?$filter=contains(FullName, 'John')

# Get user with groups
GET /PrincipalMgmt/Users('{id}')?$expand=Groups

# Get active users
GET /PrincipalMgmt/Users?$filter=Disabled eq false

# Select specific properties
GET /PrincipalMgmt/Users?$select=Name,FullName,Email
```

---

### Group

A collection of users for organizational and access control purposes.

**Endpoint:** `/PrincipalMgmt/Groups`

**Operations:** `READ`

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Group name |
| **Description** | String | Group description |
| **CreatedBy** | String | Creator username (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **ModifiedBy** | String | Last modifier username (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **Context** | PTC.DataAdmin.Container | Container context |
| **Members** | Collection(PTC.PrincipalMgmt.User) | Users in this group |
| **ParentGroup** | PTC.PrincipalMgmt.Group | Parent group (for nested groups) |

**CRUD Operations:**

```bash
# Get all groups
GET /PrincipalMgmt/Groups

# Get group by name
GET /PrincipalMgmt/Groups?$filter=Name eq 'Engineering'

# Get group with members
GET /PrincipalMgmt/Groups('{id}')?$expand=Members

# Search groups by name
GET /PrincipalMgmt/Groups?$filter=contains(Name, 'Admin')
```

---

### Organization

An organizational entity in Windchill.

**Endpoint:** `/PrincipalMgmt/Organizations`

**Operations:** `READ`

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Organization name |
| **Description** | String | Organization description |
| **CreatedBy** | String | Creator username (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **Context** | PTC.DataAdmin.Container | Container context |
| **Users** | Collection(PTC.PrincipalMgmt.User) | Users in organization |

---

## Common Query Examples

### Get User by Username

```bash
GET /PrincipalMgmt/Users?$filter=Name eq 'jsmith'
```

### Get All Members of a Group

```bash
GET /PrincipalMgmt/Groups('{group_id}')?$expand=Members($select=Name,FullName,Email)
```

### Get Groups for a User

```bash
GET /PrincipalMgmt/Users('{user_id}')?$expand=Groups
```

### Search Users by Email Domain

```bash
GET /PrincipalMgmt/Users?$filter=contains(Email, '@company.com')
```

### Get Active Users Sorted by Name

```bash
GET /PrincipalMgmt/Users?$filter=Disabled eq false&$orderby=FullName asc
```

---

## Notes

1. **Read-Only Access**: Principal management entities are typically read-only through the OData API. User management is usually done through Windchill UI or administration tools.

2. **Authentication Context**: The authenticated user's information is available through the API context.

3. **Organization Context**: Users are typically associated with an organization that defines their access scope.

---

## Schema Version

Schema Version: Various (check metadata for version details)
