# Common PTC Entities and Cross-Domain Reference

This document describes common entities shared across Windchill OData domains and cross-domain navigation patterns.

## Shared Entity Types

### PTC.WindchillEntity (Base Type)

Base type for most Windchill entities. Contains common properties:

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) - Primary Key, ReadOnly |
| **Name** | String | Object name |
| **Number** | String | Object number (unique identifier) |
| **ObjectType** | String | Type of object (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

---

### PTC.DataAdmin.Container

Container entity representing Products, Libraries, and Projects.

**Referenced by:** Most entities across all domains

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Container OID (Key, ReadOnly) |
| **Name** | String | Container name |
| **Description** | String | Container description |
| **ContainerType** | String | Type (Product, Library, Project) |
| **CreatedOn** | DateTimeOffset | Creation timestamp |
| **LastModified** | DateTimeOffset | Last modification timestamp |

**Navigation Properties:**
- `Creator` → PTC.PrincipalMgmt.User
- `Modifier` → PTC.PrincipalMgmt.User

**Common Usage:**

```bash
# Get container by ID
GET /DataAdmin/Containers('{id}')

# Get container by name
GET /DataAdmin/Containers?$filter=Name eq 'Product Name'

# Filter by type
GET /DataAdmin/Containers?$filter=ContainerType eq 'Product'
```

---

### PTC.DataAdmin.Folder

Folder entity for organizing objects within containers.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Folder OID (Key, ReadOnly) |
| **Name** | String | Folder name |
| **Path** | String | Full folder path |
| **Description** | String | Folder description |
| **Parent** | PTC.DataAdmin.Folder | Parent folder |

**Navigation Properties:**
- `Container` → PTC.DataAdmin.Container
- `ParentFolder` → PTC.DataAdmin.Folder

---

### PTC.PrincipalMgmt.User

User entity referenced across all domains for ownership and audit trails.

**Referenced by:** All entities with Creator, Modifier, Owner navigation properties

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | User OID (Key, ReadOnly) |
| **Name** | String | Username (login name) |
| **FullName** | String | Display name |
| **Email** | String | Email address |

---

## Cross-Domain Navigation Patterns

### Pattern 1: Context Navigation

Most entities reference their container through the `Context` navigation property:

```bash
# Get entity with its container
GET /ProdMgmt/Parts('{id}')?$expand=Context

# Filter by container
GET /ProdMgmt/Parts?$expand=Context&$filter=Context/Name eq 'Product Name'
```

### Pattern 2: Creator/Modifier Navigation

Audit trail navigation to users:

```bash
# Get entity with creator info
GET /ProdMgmt/Parts('{id}')?$expand=Creator,Modifier

# Filter by creator
GET /ChangeMgmt/ChangeNotices?$expand=Creator&$filter=Creator/Name eq 'jdoe'
```

### Pattern 3: Cross-Domain Object Linking

Linking objects across domains through shared references:

```bash
# Get change notice with affected objects
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=AffectedObjects($expand=Context,Creator)

# Get parts with related documents
GET /ProdMgmt/Parts('{id}')?$expand=DescribedByDocuments($expand=Context)
```

---

## Common OData Query Patterns

### Pagination

```bash
GET /ProdMgmt/Parts?$top=50&$skip=0
GET /ProdMgmt/Parts?$top=50&$skip=50
```

### Filtering

```bash
# Simple filter
GET /ProdMgmt/Parts?$filter=State/Value eq 'RELEASED'

# Compound filter
GET /ProdMgmt/Parts?$filter=State/Value eq 'RELEASED' and CreatedOn ge 2026-01-01T00:00:00Z

# String contains
GET /ProdMgmt/Parts?$filter=contains(Name, 'Assembly')

# In operator (multiple values)
GET /ProdMgmt/Parts?$filter=State/Value eq 'RELEASED' or State/Value eq 'INWORK'
```

### Ordering

```bash
GET /ProdMgmt/Parts?$orderby=CreatedOn desc
GET /ProdMgmt/Parts?$orderby=Name asc, Number asc
```

### Selecting Fields

```bash
GET /ProdMgmt/Parts?$select=ID,Name,Number,State
```

### Expanding Navigation Properties

```bash
# Single expansion
GET /ProdMgmt/Parts('{id}')?$expand=Context

# Multiple expansions
GET /ProdMgmt/Parts('{id}')?$expand=Context,Creator,Modifier

# Nested expansion
GET /ProdMgmt/Parts('{id}')?$expand=Context($expand=Creator),Creator,Modifier

# Expansion with filter
GET /ProdMgmt/Parts?$expand=Uses($filter=Quantity ge 2)
```

### Counting

```bash
# Get count
GET /ProdMgmt/Parts/$count

# Count with filter
GET /ProdMgmt/Parts/$count?$filter=State/Value eq 'RELEASED'

# Include count in results
GET /ProdMgmt/Parts?$count=true&$top=10
```

---

## Common State Values

### Lifecycle States

| State | Description |
|-------|-------------|
| **INWORK** | Object is in development |
| **UNDER_REVIEW** | Object is being reviewed |
| **RELEASED** | Object is released for use |
| **OBSOLETE** | Object is no longer used |
| **CANCELLED** | Object was cancelled |

### State Filtering

```bash
# Filter by state
GET /ProdMgmt/Parts?$filter=State/Value eq 'RELEASED'

# Filter by multiple states
GET /ProdMgmt/Parts?$filter=State/Value eq 'RELEASED' or State/Value eq 'INWORK'

# Filter by state not equal
GET /ProdMgmt/Parts?$filter=State/Value ne 'OBSOLETE'
```

---

## Cross-Domain Entity Reference Matrix

| Domain | Entity | Context | Creator | Modifier | Owner |
|--------|--------|---------|---------|----------|-------|
| ProdMgmt | Part | DataAdmin.Container | PrincipalMgmt.User | PrincipalMgmt.User | PrincipalMgmt.User |
| ProdMgmt | Document | DataAdmin.Container | PrincipalMgmt.User | PrincipalMgmt.User | PrincipalMgmt.User |
| DocMgmt | Document | DataAdmin.Container | PrincipalMgmt.User | PrincipalMgmt.User | PrincipalMgmt.User |
| ChangeMgmt | ChangeNotice | DataAdmin.Container | PrincipalMgmt.User | PrincipalMgmt.User | - |
| ChangeMgmt | ChangeRequest | DataAdmin.Container | PrincipalMgmt.User | PrincipalMgmt.User | - |
| ChangeMgmt | ChangeTask | DataAdmin.Container | PrincipalMgmt.User | PrincipalMgmt.User | - |
| SupplierMgmt | Supplier | DataAdmin.Container | PrincipalMgmt.User | PrincipalMgmt.User | - |
| QMS | QualityAction | DataAdmin.Container | PrincipalMgmt.User | PrincipalMgmt.User | PrincipalMgmt.User |
| QMS | NonConformance | DataAdmin.Container | PrincipalMgmt.User | PrincipalMgmt.User | - |
| RegMstr | Regulation | DataAdmin.Container | PrincipalMgmt.User | PrincipalMgmt.User | - |

---

## Common OID Formats

Windchill Object Identifiers (OIDs) follow this format:

```
OR:{java.class}:{id}
```

### Examples:

| Object Type | OID Format |
|-------------|------------|
| Part | `OR:wt.part.WTPart:12345` |
| Document | `OR:wt.doc.WTDocument:12345` |
| Change Notice | `OR:wt.change2.WTChangeOrder2:12345` |
| Change Request | `OR:wt.change2.WTChangeRequest2:12345` |
| User | `OR:wt.org.WTUser:12345` |
| Group | `OR:wt.org.WTGroup:12345` |
| Container | `OR:wt.inf.container.WTContainer:12345` |

---

## Cross-Domain Query Examples

### Get Part with Container and Creator

```bash
GET /ProdMgmt/Parts('{id}')?$expand=Context($expand=Creator),Creator
```

### Get Change Notice with Affected Parts

```bash
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=AffectedObjects($expand=Context,Creator),Context,Creator
```

### Get Quality Action with Related Objects

```bash
GET /QMS/QualityActions('{id}')?$expand=
  Owner,
  Context($expand=Creator),
  Creator,
  Modifier,
  RelatedQualityObject($expand=Context)
```

### Get Regulation with Compliance Hierarchy

```bash
GET /RegMstr/Regulations('{id}')?$expand=
  RegulatoryRequirements($expand=
    ComplianceRecords($expand=
      ComplianceEvidence,
      Creator
    )
  ),
  Context,
  Creator
```

### Get User's Groups and Organization

```bash
GET /PrincipalMgmt/Users('{id}')?$expand=Groups($expand=ParentGroups),Organization
```

---

## Notes

1. **Container Scope** - Most operations are scoped to a container. Always expand Context to understand the product/project context.

2. **Audit Trail** - Creator and Modifier navigation properties provide audit information for all entities.

3. **State Filtering** - States are enums accessed via `State/Value` in OData queries.

4. **OID Resolution** - OIDs contain type information and can be used to determine the object's domain.

5. **Cross-Domain Links** - Navigation properties can link entities across domains (e.g., Part → Document, ChangeNotice → Part).

6. **Versioning** - Windchill objects support versioning. Version info is typically in IterationInfo.

7. **Soft Delete** - Many objects use lifecycle states rather than hard deletes.
