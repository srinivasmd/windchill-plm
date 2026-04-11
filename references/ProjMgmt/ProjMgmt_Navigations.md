# ProjMgmt Navigation Properties

This document lists all navigation properties for ProjMgmt domain entities.

---

## ProjectPlan

Primary entity for Project Plans. Contains project activities, schedule, and cost information.

| Navigation | Type | Description |
|------------|------|-------------|
| `Activities` | Collection(Activity) | All activities in the project plan |
| `ImmediateChildren` | Collection(Activity) | Top-level activities (children of root) |
| `Context` | Container | Container context |

---

## Activity

Individual activity within a project plan. Can be a task, milestone, or deliverable.

| Navigation | Type | Description |
|------------|------|-------------|
| `Deliverables` | Collection(WindchillEntity) | Deliverables associated with activity |
| `Children` | Collection(Activity) | Child activities (subtasks) |
| `ActivityOwner` | User | User responsible for the activity |
| `Context` | Container | Container context |

---

## Navigation Property Types

### Collection Navigation

- `Activities` - Returns all activities in the plan (hierarchical)
- `ImmediateChildren` - Returns only top-level activities
- `Children` - Returns sub-activities of an activity
- `Deliverables` - Returns deliverable objects

### Single Entity Navigation

- `ActivityOwner` - Returns the User assigned to the activity
- `Context` - Returns the container/context

---

## Usage Examples

### Get Project Plan with Activities

```python
from domains.ProjMgmt import ProjMgmtClient
client = ProjMgmtClient(config_path="config.json")

# Get Project Plan with expanded navigation
plan = client.get_project_plan_by_id(plan_id, expand=[
    "Activities",
    "ImmediateChildren",
    "Context"
])

# Get all activities for a plan
activities = client.get_activities_for_plan(plan_id)

# Get immediate children (top-level)
top_level = client.get_immediate_children(plan_id)
```

### Get Activity with Details

```python
# Get Activity with navigation
activity = client.get_activity_by_id(activity_id, expand=[
    "Children",
    "ActivityOwner",
    "Deliverables",
    "Context"
])

# Get activity owner
owner = client.get_activity_owner(activity_id)

# Get child activities
children = client.get_activity_children(activity_id)

# Get deliverables
deliverables = client.get_activity_deliverables(activity_id)
```

### Navigate Activity Hierarchy

```python
# Get root activity
root = client.get_activity_by_id(activity_id)

# Get children
children = client.get_activity_children(activity_id)

# For each child, get their children
for child in children:
    sub_children = client.get_activity_children(child['ID'])
    print(f"{child['Name']}: {len(sub_children)} sub-activities")
```
