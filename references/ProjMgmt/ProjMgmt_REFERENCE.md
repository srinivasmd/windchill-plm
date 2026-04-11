# ProjMgmt Domain Reference

Project Management in PTC Windchill PLM. This domain handles project plans, activities, milestones, deliverables, and project scheduling.

## Overview

| Property | Value |
|----------|-------|
| Namespace | PTC.ProjMgmt |
| Entity Sets | 2 |
| Entity Types | 2 |
| Actions | 1 |
| Complex Types | 0 |

---

## Entity Sets

| Entity Set | Entity Type | Description |
|------------|-------------|-------------|
| ProjectPlans | ProjectPlan | Project plans |
| Activities | Activity | Project activities, tasks, milestones |

---

## Entity Types

### ProjectPlan

Primary entity for Project Plans. Contains project activities, schedule, cost, and progress information.

**Key:** `ID`

**Base Type:** None

**Properties (22):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `Name` | String | Yes | Project plan name |
| `ID` | String | Yes | Unique identifier (ReadOnly) |
| `CreatedOn` | DateTimeOffset | Yes | Creation timestamp (ReadOnly) |
| `LastModified` | DateTimeOffset | Yes | Last modification timestamp (ReadOnly) |
| `Status` | String | Yes | Current status |
| `State` | EnumType | Yes | Lifecycle state |
| `Risk` | EnumType | Yes | Risk level |
| `PercentWorkComplete` | Double | Yes | Percentage complete |
| `Cost` | Double | Yes | Total cost |
| `FixedCost` | Double | Yes | Fixed cost |
| `RolledUpCost` | Double | Yes | Aggregated cost from activities (ReadOnly) |
| `Duration` | Int64 | Yes | Duration in days/hours |
| `Effort` | Int64 | Yes | Total effort |
| `RemainingEffort` | Int64 | Yes | Remaining effort |
| `ActualStart` | String | Yes | Actual start date |
| `ActualFinish` | String | Yes | Actual finish date |
| `EstimatedStart` | String | Yes | Estimated start date |
| `EstimatedFinish` | String | Yes | Estimated finish date |
| `Deadline` | String | Yes | Project deadline |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| `Activities` | Collection(Activity) | All activities in the plan |
| `ImmediateChildren` | Collection(Activity) | Top-level activities |
| `Context` | Container | Container context |

---

### Activity

Individual activity within a project plan. Can be a task, milestone, deliverable, or summary activity.

**Key:** `ID`

**Base Type:** None

**Properties (24):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `Name` | String | Yes | Activity name |
| `ID` | String | Yes | Unique identifier (ReadOnly) |
| `CreatedOn` | DateTimeOffset | Yes | Creation timestamp (ReadOnly) |
| `LastModified` | DateTimeOffset | Yes | Last modification timestamp (ReadOnly) |
| `LineNumber` | Int64 | Yes | Line number in plan |
| `Status` | String | Yes | Current status |
| `StatusDescription` | String | Yes | Status description |
| `StartDate` | DateTimeOffset | Yes | Planned start date |
| `FinishDate` | DateTimeOffset | Yes | Planned finish date |
| `ActualStartDate` | DateTimeOffset | Yes | Actual start date |
| `ActualFinishDate` | DateTimeOffset | Yes | Actual finish date |
| `Deadline` | DateTimeOffset | Yes | Activity deadline |
| `PercentWorkComplete` | Double | Yes | Percentage complete |
| `Summary` | Boolean | Yes | Is summary activity |
| `Milestone` | Boolean | Yes | Is milestone (ReadOnly) |
| `Deliverable` | Boolean | Yes | Is deliverable (ReadOnly) |
| `IncludeInDHF` | Boolean | Yes | Include in DHF (NonFilterable, NonSortable) |
| `PlanName` | String | Yes | Name of containing plan |
| `TotalCost` | Double | Yes | Total cost |
| `RolledUpCost` | Double | Yes | Aggregated cost from children |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| `Deliverables` | Collection(WindchillEntity) | Deliverables |
| `Children` | Collection(Activity) | Child activities |
| `ActivityOwner` | User | Assigned user |
| `Context` | Container | Container context |

---

## Actions

### AddToPlan

Add an activity to a project plan.

| Action | Bound | Parameters | Description |
|--------|-------|------------|-------------|
| AddToPlan | Yes | ProjectPlan, Activity | Add activity to plan |

---

## Usage Examples

### Query Project Plans

```python
from domains.ProjMgmt import ProjMgmtClient
client = ProjMgmtClient(config_path="config.json")

# Get all project plans
plans = client.get_project_plans(top=50)

# Get by ID
plan = client.get_project_plan_by_id(plan_id)

# Get by name
plan = client.get_project_plan_by_name("Product Development 2026")

# Get with expanded navigation
plan = client.get_project_plan_by_id(plan_id, expand=[
    "Activities",
    "ImmediateChildren",
    "Context"
])
```

### Query Activities

```python
# Get all activities
activities = client.get_activities(top=50)

# Get by ID
activity = client.get_activity_by_id(activity_id)

# Get by name
activities = client.get_activities_by_name("Design Review")

# Get with expanded navigation
activity = client.get_activity_by_id(activity_id, expand=[
    "Children",
    "ActivityOwner",
    "Deliverables",
    "Context"
])
```

### Navigate Activity Hierarchy

```python
# Get activities for a plan
activities = client.get_activities_for_plan(plan_id)

# Get immediate children (top-level)
top_level = client.get_immediate_children(plan_id)

# Get child activities of an activity
children = client.get_activity_children(activity_id)

# Get activity owner
owner = client.get_activity_owner(activity_id)

# Get deliverables
deliverables = client.get_activity_deliverables(activity_id)
```

### Create and Manage

```python
# Create project plan
plan = client.create_project_plan(
    name="New Product Launch",
    deadline="2026-12-31"
)

# Create activity
activity = client.create_activity(
    name="Phase 1: Design",
    start_date="2026-05-01T00:00:00Z",
    finish_date="2026-05-31T00:00:00Z",
    summary=True
)

# Add activity to plan
client.add_activity_to_plan(plan_id, activity_id)

# Update activity progress
client.update_activity(activity_id, percent_work_complete=75.0)

# Create milestone
milestone = client.create_activity(
    name="Design Complete",
    start_date="2026-05-31T00:00:00Z",
    finish_date="2026-05-31T00:00:00Z",
    milestone=True
)
```

### Activity Hierarchy Management

```python
# Create summary activity (parent)
parent = client.create_activity(
    name="Development Phase",
    start_date="2026-06-01T00:00:00Z",
    finish_date="2026-08-31T00:00:00Z",
    summary=True
)

# Create child activities
child1 = client.create_activity(
    name="Backend Development",
    start_date="2026-06-01T00:00:00Z",
    finish_date="2026-07-15T00:00:00Z"
)

child2 = client.create_activity(
    name="Frontend Development",
    start_date="2026-07-01T00:00:00Z",
    finish_date="2026-08-31T00:00:00Z"
)

# Add to plan
client.add_activity_to_plan(plan_id, parent['ID'])
client.add_activity_to_plan(plan_id, child1['ID'])
client.add_activity_to_plan(plan_id, child2['ID'])
```

---

## Related Files

| File | Description |
|------|-------------|
| ProjMgmt_Entities.json | Machine-readable entity definitions |
| ProjMgmt_Navigations.md | Navigation properties reference |
| ProjMgmt_Actions.md | OData actions reference |
| ProjMgmt_Metadata.xml | Raw OData metadata |
