# Manufacturing Process Management Domain (MfgProcMgmt) Reference

Complete reference documentation for the Windchill Manufacturing Process Management OData domain.

## Base URL

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/MfgProcMgmt/
```

## Domain Overview

The Manufacturing Process Management (MfgProcMgmt) domain provides access to manufacturing-related data in Windchill including:

- **Process Plans** - Manufacturing routing definitions
- **Segments** - Groups of operations within a process plan
- **Operations** - Individual manufacturing operations
- **Resources** - Tooling, equipment, and other resources
- **Work Instructions** - Detailed work instructions
- **Work Centers** - Physical manufacturing locations
- **Templates** - Process plan templates

---

## Entity Types

### MfgProcessPlans

Manufacturing process plans (routings) define the sequence of operations to manufacture a product.

**Endpoint:** `/MfgProcMgmt/MfgProcessPlans`

**CRUD Operations:**

```bash
# Get all process plans
GET /MfgProcMgmt/MfgProcessPlans

# Get process plan by ID
GET /MfgProcMgmt/MfgProcessPlans('{id}')

# Filter by number
GET /MfgProcMgmt/MfgProcessPlans?$filter=Number eq 'PLAN-001'

# Create process plan
POST /MfgProcMgmt/MfgProcessPlans
Content-Type: application/json

{
  "Name": "Assembly Process",
  "Number": "PLAN-001",
  "Description": "Main assembly process",
  "ContainerID": "OR:wt.pdmlink.PDMLinkProduct:10082558"
}

# Update process plan
PATCH /MfgProcMgmt/MfgProcessPlans('{id}')

# Delete process plan
DELETE /MfgProcMgmt/MfgProcessPlans('{id}')
```

---

### MfgProcessPlanSegments

Segments are groups of operations within a process plan.

**Endpoint:** `/MfgProcMgmt/MfgProcessPlanSegments`

**CRUD Operations:**

```bash
# Get all segments
GET /MfgProcMgmt/MfgProcessPlanSegments

# Get segments for a process plan
GET /MfgProcMgmt/MfgProcessPlans('{plan_id}')/MfgProcessPlanSegments

# Create segment
POST /MfgProcMgmt/MfgProcessPlanSegments

# Update segment
PATCH /MfgProcMgmt/MfgProcessPlanSegments('{id}')

# Delete segment
DELETE /MfgProcMgmt/MfgProcessPlanSegments('{id}')
```

---

### MfgProcessOperations

Operations are individual manufacturing steps within a segment or process plan.

**Endpoint:** `/MfgProcMgmt/MfgProcessOperations`

**CRUD Operations:**

```bash
# Get all operations
GET /MfgProcMgmt/MfgProcessOperations

# Get operations for a segment
GET /MfgProcMgmt/MfgProcessPlanSegments('{segment_id}')/MfgProcessOperations

# Create operation
POST /MfgProcMgmt/MfgProcessOperations

# Update operation
PATCH /MfgProcMgmt/MfgProcessOperations('{id}')

# Delete operation
DELETE /MfgProcMgmt/MfgProcessOperations('{id}')
```

---

### WorkCenters

Work centers are physical locations where manufacturing operations are performed.

**Endpoint:** `/MfgProcMgmt/WorkCenters`

**CRUD Operations:**

```bash
# Get all work centers
GET /MfgProcMgmt/WorkCenters

# Get work center by ID
GET /MfgProcMgmt/WorkCenters('{id}')

# Create work center
POST /MfgProcMgmt/WorkCenters

# Update work center
PATCH /MfgProcMgmt/WorkCenters('{id}')

# Delete work center
DELETE /MfgProcMgmt/WorkCenters('{id}')
```

---

### WorkInstructions

Work instructions provide detailed step-by-step instructions for performing operations.

**Endpoint:** `/MfgProcMgmt/WorkInstructions`

**CRUD Operations:**

```bash
# Get all work instructions
GET /MfgProcMgmt/WorkInstructions

# Get work instructions for an operation
GET /MfgProcMgmt/MfgProcessOperations('{operation_id}')/WorkInstructions

# Create work instruction
POST /MfgProcMgmt/WorkInstructions

# Update work instruction
PATCH /MfgProcMgmt/WorkInstructions('{id}')

# Delete work instruction
DELETE /MfgProcMgmt/WorkInstructions('{id}')
```

---

### Tooling

Tooling resources represent tools used in manufacturing operations.

**Endpoint:** `/MfgProcMgmt/Tooling`

**CRUD Operations:**

```bash
# Get all tooling
GET /MfgProcMgmt/Tooling

# Get tooling by ID
GET /MfgProcMgmt/Tooling('{id}')

# Create tooling
POST /MfgProcMgmt/Tooling

# Update tooling
PATCH /MfgProcMgmt/Tooling('{id}')

# Delete tooling
DELETE /MfgProcMgmt/Tooling('{id}')
```

---

### Equipment

Equipment resources represent machinery and equipment used in manufacturing.

**Endpoint:** `/MfgProcMgmt/Equipment`

**CRUD Operations:**

```bash
# Get all equipment
GET /MfgProcMgmt/Equipment

# Get equipment by ID
GET /MfgProcMgmt/Equipment('{id}')

# Create equipment
POST /MfgProcMgmt/Equipment

# Update equipment
PATCH /MfgProcMgmt/Equipment('{id}')

# Delete equipment
DELETE /MfgProcMgmt/Equipment('{id}')
```

---

### MfgProcessResources

Resources are the tooling, equipment, and other resources assigned to operations.

**Endpoint:** `/MfgProcMgmt/MfgProcessResources`

**CRUD Operations:**

```bash
# Get all resources
GET /MfgProcMgmt/MfgProcessResources

# Get resources for an operation
GET /MfgProcMgmt/MfgProcessOperations('{operation_id}')/MfgProcessResources

# Create resource
POST /MfgProcMgmt/MfgProcessResources

# Update resource
PATCH /MfgProcMgmt/MfgProcessResources('{id}')

# Delete resource
DELETE /MfgProcMgmt/MfgProcessResources('{id}')
```

---

## Common Query Options

All entities support OData query options:

- `$filter` - Filter results
- `$select` - Select specific properties
- `$expand` - Expand navigation properties
- `$orderby` - Order results
- `$top` - Limit number of results
- `$skip` - Skip results (pagination)

---

## Quick Reference Examples

```bash
# Get all process plans
GET /MfgProcMgmt/MfgProcessPlans

# Get process plans for a specific product
GET /MfgProcMgmt/MfgProcessPlans?$filter=ContainerName eq 'MyProduct'

# Get operations for a process plan with work center details
GET /MfgProcMgmt/MfgProcessPlans('{id}')/MfgProcessOperations?$expand=WorkCenter

# Get all work centers
GET /MfgProcMgmt/WorkCenters

# Create a new process plan
POST /MfgProcMgmt/MfgProcessPlans
{
  "Name": "Assembly Process",
  "Number": "PLAN-001",
  "Description": "Main assembly process",
  "ContainerID": "OR:wt.pdmlink.PDMLinkProduct:10082558"
}
```