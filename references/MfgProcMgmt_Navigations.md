# MfgProcMgmt Navigation Properties

This document describes all navigation properties and relationships between entities in the Manufacturing Process Management (MfgProcMgmt) domain.

## Entity Relationships Overview

```
MfgProcessPlan
    ├── Creator → User
    ├── Modifier → User
    ├── Segments → MfgProcessPlanSegment[]
    ├── Operations → MfgProcessOperation[]
    ├── PrimaryContent → Content
    ├── Attachments → Content[]
    └── Thumbnails → Thumbnail[]

MfgProcessPlanSegment
    ├── ProcessPlan → MfgProcessPlan
    ├── Operations → MfgProcessOperation[]
    ├── Creator → User
    └── Modifier → User

MfgProcessOperation
    ├── ProcessPlan → MfgProcessPlan
    ├── Segment → MfgProcessPlanSegment
    ├── WorkCenter → WorkCenter
    ├── WorkInstructions → WorkInstruction[]
    ├── Resources → MfgProcessResource[]
    ├── Creator → User
    └── Modifier → User

WorkCenter
    ├── Operations → MfgProcessOperation[]
    ├── Creator → User
    └── Modifier → User

WorkInstruction
    ├── Operation → MfgProcessOperation
    ├── PrimaryContent → Content
    ├── Attachments → Content[]
    ├── Creator → User
    └── Modifier → User

Tooling
    ├── Operations → MfgProcessOperation[]
    ├── Creator → User
    └── Modifier → User

Equipment
    ├── Operations → MfgProcessOperation[]
    ├── Creator → User
    └── Modifier → User

MfgProcessResource
    ├── Operation → MfgProcessOperation
    ├── Tooling → Tooling
    ├── Equipment → Equipment
    ├── Creator → User
    └── Modifier → User
```

---

## Navigation Details by Entity

### MfgProcessPlan

| Navigation | Target | Type | Description |
|------------|--------|------|-------------|
| Creator | User | Single | User who created the process plan |
| Modifier | User | Single | User who last modified the process plan |
| Segments | MfgProcessPlanSegment | Collection | Segments within the process plan |
| Operations | MfgProcessOperation | Collection | Operations within the process plan |
| PrimaryContent | Content | Single | Primary content attachment |
| Attachments | Content | Collection | All content attachments |
| Thumbnails | Thumbnail | Collection | Thumbnail images |

---

### MfgProcessPlanSegment

| Navigation | Target | Type | Description |
|------------|--------|------|-------------|
| ProcessPlan | MfgProcessPlan | Single | Parent process plan |
| Operations | MfgProcessOperation | Collection | Operations within this segment |
| Creator | User | Single | User who created the segment |
| Modifier | User | Single | User who last modified the segment |

---

### MfgProcessOperation

| Navigation | Target | Type | Description |
|------------|--------|------|-------------|
| ProcessPlan | MfgProcessPlan | Single | Parent process plan |
| Segment | MfgProcessPlanSegment | Single | Parent segment |
| WorkCenter | WorkCenter | Single | Work center for this operation |
| WorkInstructions | WorkInstruction | Collection | Work instructions for this operation |
| Resources | MfgProcessResource | Collection | Resources assigned to this operation |
| Creator | User | Single | User who created the operation |
| Modifier | User | Single | User who last modified the operation |

---

### WorkCenter

| Navigation | Target | Type | Description |
|------------|--------|------|-------------|
| Operations | MfgProcessOperation | Collection | Operations performed at this work center |
| Creator | User | Single | User who created the work center |
| Modifier | User | Single | User who last modified the work center |

---

### WorkInstruction

| Navigation | Target | Type | Description |
|------------|--------|------|-------------|
| Operation | MfgProcessOperation | Single | Parent operation |
| PrimaryContent | Content | Single | Primary content attachment |
| Attachments | Content | Collection | All content attachments |
| Creator | User | Single | User who created the work instruction |
| Modifier | User | Single | User who last modified the work instruction |

---

### Tooling

| Navigation | Target | Type | Description |
|------------|--------|------|-------------|
| Operations | MfgProcessOperation | Collection | Operations that use this tool |
| Creator | User | Single | User who created the tooling |
| Modifier | User | Single | User who last modified the tooling |

---

### Equipment

| Navigation | Target | Type | Description |
|------------|--------|------|-------------|
| Operations | MfgProcessOperation | Collection | Operations that use this equipment |
| Creator | User | Single | User who created the equipment |
| Modifier | User | Single | User who last modified the equipment |

---

### MfgProcessResource

| Navigation | Target | Type | Description |
|------------|--------|------|-------------|
| Operation | MfgProcessOperation | Single | Operation this resource is assigned to |
| Tooling | Tooling | Single | Tooling resource (if applicable) |
| Equipment | Equipment | Single | Equipment resource (if applicable) |
| Creator | User | Single | User who created the resource |
| Modifier | User | Single | User who last modified the resource |

---

## OData Query Examples with Navigation Properties

### Get Process Plan with Segments and Operations

```bash
GET /MfgProcMgmt/MfgProcessPlans?$expand=Segments,Operations
```

### Get Process Plan with Operations and Work Centers

```bash
GET /MfgProcMgmt/MfgProcessPlans?$expand=Operations($expand=WorkCenter)
```

### Get Operation with Work Instructions and Resources

```bash
GET /MfgProcMgmt/MfgProcessOperations?$expand=WorkInstructions,Resources
```

### Get Work Center with Operations

```bash
GET /MfgProcMgmt/WorkCenters?$expand=Operations
```

### Get Process Plan with All Related Data

```bash
GET /MfgProcMgmt/MfgProcessPlans?$expand=Segments($expand=Operations($expand=WorkCenter,WorkInstructions,Resources))
```

### Get Operations for a Specific Work Center

```bash
GET /MfgProcMgmt/WorkCenters('{work_center_id}')/Operations
```

### Get Work Instructions for an Operation

```bash
GET /MfgProcMgmt/MfgProcessOperations('{operation_id}')/WorkInstructions
```

### Get Resources for an Operation

```bash
GET /MfgProcMgmt/MfgProcessOperations('{operation_id}')/Resources
```

### Get Operations using Specific Tooling

```bash
GET /MfgProcMgmt/Tooling('{tooling_id}')/Operations
```

### Get Operations using Specific Equipment

```bash
GET /MfgProcMgmt/Equipment('{equipment_id}')/Operations
```

---

## Cross-Domain Navigation

Some navigation properties reference entities from other domains:

- **User** → References from ProdMgmt domain
- **Content** → References from DocMgmt domain
- **Thumbnail** → References from DocMgmt domain

When expanding these navigations, you may need to use the full OData type name:

```bash
GET /MfgProcMgmt/MfgProcessPlans?$expand=Creator,Modifier
```