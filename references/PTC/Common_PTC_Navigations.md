# Common (PTC) Navigation Properties

## Overview

The PTC namespace provides common navigation properties and shared entity types used across all Windchill OData domains. These are base types and navigation patterns that appear in multiple domains.

---

## Common Navigation Properties

### Owner

User who owns the object (applies to most business objects).

```bash
GET /{Domain}/{Entity}('{id}')/Owner
```

**Returns:** User object from PrincipalMgmt

**Example:**
```json
{
  "ID": "OR:wt.org.WTUser:12345",
  "Name": "pat",
  "FullName": "Pat Johnson",
  "Email": "pat@company.com"
}
```

### Creator

User who created the object.

```bash
GET /{Domain}/{Entity}('{id}')/Creator
```

**Returns:** User object from PrincipalMgmt

### Modifier

User who last modified the object.

```bash
GET /{Domain}/{Entity}('{id}')/Modifier
```

**Returns:** User object from PrincipalMgmt

### Container

Container/context (Product, Library, Project, etc.).

```bash
GET /{Domain}/{Entity}('{id}')/Container
```

**Returns:** Container object

### Folder

Folder location.

```bash
GET /{Domain}/{Entity}('{id}')/Folder
```

**Returns:** Folder object

### Attachments

Document attachments.

```bash
GET /{Domain}/{Entity}('{id}')/Attachments
```

**Returns:** Collection of Document objects

---

## Version Navigation Properties

### Master

Master object (for version-controlled objects).

```bash
GET /{Domain}/{Entity}('{id}')/Master
```

**Returns:** Master object

### Iterations

All iterations of the object.

```bash
GET /{Domain}/{Entity}('{id}')/Iterations
```

**Returns:** Collection of iteration objects

### Versions

All versions of the object.

```bash
GET /{Domain}/{Entity}('{id}')/Versions
```

**Returns:** Collection of version objects

### NextVersion

Next version of the object.

```bash
GET /{Domain}/{Entity}('{id}')/NextVersion
```

**Returns:** Single version object

### PreviousVersion

Previous version of the object.

```bash
GET /{Domain}/{Entity}('{id}')/PreviousVersion
```

**Returns:** Single version object

---

## Lifecycle Navigation Properties

### LifeCycleState

Current lifecycle state information.

```bash
GET /{Domain}/{Entity}('{id}')/LifeCycleState
```

**Returns:** State object

### LifeCycleTemplate

Lifecycle template definition.

```bash
GET /{Domain}/{Entity}('{id}')/LifeCycleTemplate
```

**Returns:** LifeCycleTemplate object

### PromotionNotices

Promotion notices for this object.

```bash
GET /{Domain}/{Entity}('{id}')/PromotionNotices
```

**Returns:** Collection of PromotionNotice objects

---

## Workflow Navigation Properties

### WorkflowProcess

Active workflow process.

```bash
GET /{Domain}/{Entity}('{id}')/WorkflowProcess
```

**Returns:** WorkflowProcess object

### WorkItems

Work items for this object.

```bash
GET /{Domain}/{Entity}('{id}')/WorkItems
```

**Returns:** Collection of WorkItem objects

---

## Team Navigation Properties

### Team

Team assigned to the object.

```bash
GET /{Domain}/{Entity}('{id}')/Team
```

**Returns:** Team object

### TeamMembers

Members of the team.

```bash
GET /{Domain}/{Entity}('{id}')/TeamMembers
```

**Returns:** Collection of User objects

---

## Common Expansion Patterns

### Expand Owner and Modifier

```bash
GET /{Domain}/{Entity}('{id}')?$expand=Owner,Modifier
```

### Expand Container

```bash
GET /{Domain}/{Entity}('{id}')?$expand=Container
```

### Expand Version History

```bash
GET /{Domain}/{Entity}('{id}')?$expand=Versions($expand=Creator)
```

### Expand Workflow Context

```bash
GET /{Domain}/{Entity}('{id}')?$expand=WorkItems($expand=Owner),WorkflowProcess
```

### Expand Full Context

```bash
GET /{Domain}/{Entity}('{id}')?$expand=Owner,Creator,Modifier,Container,Folder
```

---

## Cross-Domain Navigation Patterns

### Navigation to PrincipalMgmt

Most business objects can navigate to their user references:

| Source Navigation | Target Domain | Target Entity |
|-------------------|---------------|---------------|
| Owner | PrincipalMgmt | Users |
| Creator | PrincipalMgmt | Users |
| Modifier | PrincipalMgmt | Users |
| Assignee | PrincipalMgmt | Users |

### Navigation to DocMgmt

Documents attached to business objects:

| Source Navigation | Target Domain | Target Entity |
|-------------------|---------------|---------------|
| Attachments | DocMgmt | Documents |
| Content | DocMgmt | Content |
| PrimaryContent | DocMgmt | Content |

### Navigation to Workflow

Workflow-related navigation:

| Source Navigation | Target Domain | Target Entity |
|-------------------|---------------|---------------|
| WorkItems | Workflow | WorkItems |
| WorkflowProcess | Workflow | Processes |
| VotingEvents | Workflow | VotingEvents |

---

## Common Filter Patterns

### Filter by Owner

```bash
$filter=Owner/Name eq 'pat'
```

### Filter by Container

```bash
$filter=Container/Name eq 'Product A'
```

### Filter by State

```bash
$filter=State/Value eq 'RELEASED'
```

### Filter by Created Date Range

```bash
$filter=CreatedOn ge 2024-01-01 and CreatedOn le 2024-12-31
```

### Filter by Modifier

```bash
$filter=ModifiedBy eq 'pat'
```

---

## Standard Properties

All Windchill business objects inherit these common properties from WindchillEntity:

| Property | Type | Description |
|----------|------|-------------|
| ID | String | Unique identifier (OID) |
| Identity | String | Object identity (read-only) |
| CreatedOn | DateTimeOffset | Creation timestamp |
| CreatedBy | String | Creator username |
| LastModified | DateTimeOffset | Last modification timestamp |
| ModifiedBy | String | Last modifier username |
| State | Object | Lifecycle state |
| Name | String | Object name |
| Number | String | Object number |

---

## OID Format

Object IDs in Windchill follow the format: `OR:JavaClassName:internalId`

Examples:
- `OR:wt.part.WTPart:12345` - Part object
- `OR:wt.doc.WTDocument:67890` - Document object
- `OR:wt.change2.WTChangeOrder2:11111` - Change Notice
- `OR:wt.org.WTUser:22222` - User object
- `OR:wt.supplier.Supplier:33333` - Supplier object
