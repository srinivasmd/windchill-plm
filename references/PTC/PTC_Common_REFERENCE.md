---
Type: Common Entity Types
Use: Reference for shared PTC entity types and OID format
---

> **Common Entity Types Reference**: Documents shared entity types and OID format used across all domains.

# PTC Common Entities Reference

Reference documentation for common PTC entities shared across domains.

## Overview

These entities are referenced by multiple Windchill domains and provide common functionality like containers, folders, and content management.

---

## PTC.DataAdmin.Container

A Container represents a logical container for organizing objects (Product, Library, Project, etc.).

**Navigation Usage:** Most entities have a `Context` navigation property pointing to their container.

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Container identifier |
| **Name** | String | Container name |
| **Description** | String | Container description |
| **Type** | String | Container type (Product, Library, Project) |

**Usage Example:**

```bash
# Get container for an entity
GET /ProdMgmt/Parts('{id}')?$expand=Context

# Filter by container
GET /ProdMgmt/Parts?$filter=Context/Name eq 'Product A'
```

---

## PTC.DataAdmin.Folder

A Folder represents a hierarchical location for organizing objects within a container.

**Navigation Usage:** Most entities have a `Folder` navigation property.

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Folder identifier |
| **Name** | String | Folder name |
| **Path** | String | Full folder path |
| **ParentFolder** | Folder | Parent folder (nested structure) |

**Usage Example:**

```bash
# Get folder for an entity
GET /ProdMgmt/Parts('{id}')?$expand=Folder

# Filter by folder path
GET /ProdMgmt/Parts?$filter=FolderName eq '/Default/Parts'
```

---

## PTC.ContentItem

A ContentItem represents an attached file or document.

**Navigation Usage:** Most entities have an `Attachments` navigation property returning ContentItems.

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Content item identifier |
| **Name** | String | File name |
| **Format** | String | File format/MIME type |
| **Size** | Long | File size in bytes |
| **CreatedBy** | String | Creator username |
| **CreatedOn** | DateTimeOffset | Upload timestamp |

**Usage Example:**

```bash
# Get attachments for an entity
GET /ProdMgmt/Parts('{id}')?$expand=Attachments

# Download attachment content
GET /ProdMgmt/Parts('{id}')/Attachments('{content_id}')/$value
```

---

## PTC.EnumType

An enumeration value used throughout the system.

**Structure:**

```json
{
  "Value": "ENUM_VALUE",
  "Display": "Human Readable Value"
}
```

**Common Enum Types:**

### Lifecycle State

| Value | Display |
|-------|---------|
| **INWORK** | In Work |
| **RELEASED** | Released |
| **CANCELLED** | Cancelled |
| **OBSOLETE** | Obsolete |
| **LOCKED** | Locked |

### Change State

| Value | Display |
|-------|---------|
| **OPEN** | Open |
| **INWORK** | In Work |
| **ISSUED** | Issued |
| **CLOSED** | Closed |
| **CANCELLED** | Cancelled |
| **HELD** | Held |

### Priority

| Value | Display |
|-------|---------|
| **LOW** | Low |
| **MEDIUM** | Medium |
| **HIGH** | High |
| **CRITICAL** | Critical |

### Severity

| Value | Display |
|-------|---------|
| **MINOR** | Minor |
| **MODERATE** | Moderate |
| **MAJOR** | Major |
| **CRITICAL** | Critical |

---

## Common Patterns

### Filtering by State

```bash
# Filter by state value
GET /ProdMgmt/Parts?$filter=State/Value eq 'RELEASED'

# Filter by state display
GET /ProdMgmt/Parts?$filter=State/Display eq 'Released'
```

### Using $select for Performance

```bash
# Only select needed properties
GET /ProdMgmt/Parts?$select=ID,Name,Number,State
```

### Using $expand for Related Data

```bash
# Expand navigation properties
GET /ProdMgmt/Parts('{id}')?$expand=Context,Folder,Attachments

# Nested expand
GET /ProdMgmt/Parts('{id}')?$expand=Uses($expand=Uses)
```

### Pagination

```bash
# Skip and top for pagination
GET /ProdMgmt/Parts?$skip=0&$top=50

# Get total count
GET /ProdMgmt/Parts?$count=true
```

### Sorting

```bash
# Sort by single field
GET /ProdMgmt/Parts?$orderby=Number asc

# Sort by multiple fields
GET /ProdMgmt/Parts?$orderby=State/Value asc,Number asc
```

### Search with contains

```bash
# Search by name
GET /ProdMgmt/Parts?$filter=contains(Name, 'Bracket')

# Case-insensitive search
GET /ProdMgmt/Parts?$filter=contains(tolower(Name), 'bracket')
```

---

## Object ID Format

Windchill uses Object IDs (OIDs) in the format:

```
OR:<ObjectType>:<ContainerID>:<ObjectID>
```

**Examples:**
- `OR:wt.part.WTPart:123456:789012` - Part object
- `OR:wt.change2.WTChangeOrder:123456:789013` - Change Notice
- `OR:wt.doc.WTDocument:123456:789014` - Document

---

## Notes

1. **Navigation Properties**: Always use `$expand` to include navigation properties in queries.

2. **Performance**: Minimize `$expand` and `$select` properties to improve performance.

3. **CSRF Token**: Required for all write operations (POST, PATCH, DELETE).

4. **Batch Operations**: Use `$batch` endpoint for multiple operations in a single request.

---

## Schema Version

Schema Version: Various (check domain metadata for version details)