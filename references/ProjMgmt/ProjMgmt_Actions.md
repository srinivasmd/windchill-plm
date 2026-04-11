# ProjMgmt Actions Reference

This document lists all OData actions for the ProjMgmt domain.

---

## AddToPlan (Bound)

Add an activity to a project plan.

**Bound To:** `ProjectPlan`

**Parameters:**

| Parameter | Type | Nullable | Description |
|-----------|------|----------|-------------|
| ProjectPlan | ProjectPlan | No | Target project plan |
| Activity | Activity | No | Activity to add |

**Returns:** Activity (the added activity)

---

## Usage Examples

### Add Activity to Plan

```python
from domains.ProjMgmt import ProjMgmtClient
client = ProjMgmtClient(config_path="config.json")

# Create a new activity
new_activity = client.create_activity(
    name="Design Review",
    start_date="2026-05-01T00:00:00Z",
    finish_date="2026-05-15T00:00:00Z"
)

# Add activity to plan
added_activity = client.add_activity_to_plan(plan_id, new_activity['ID'])
print(f"Added activity: {added_activity['Name']}")
```

### Create Activity and Add to Plan in One Step

```python
# Create activity directly in plan
activity = client.create_activity_in_plan(
    plan_id=plan_id,
    name="Testing Phase",
    start_date="2026-06-01T00:00:00Z",
    finish_date="2026-06-30T00:00:00Z",
    milestone=False,
    deliverable=False
)
```

---

## Action Details

### AddToPlan

This is the primary action for adding activities to a project plan. The activity must already exist in the system (can be created via the Activities entity set).

**Request Format:**

```
POST /ProjMgmt/ProjectPlans('{plan_id}')/PTC.ProjMgmt.AddToPlan
Content-Type: application/json

{
    "ProjectPlan": "OR:wt.projmgmt.ProjectPlan:12345",
    "Activity": "OR:wt.projmgmt.ProjectActivity:67890"
}
```

**Response:**

The action returns the Activity entity that was added to the plan, including all its properties.

---

## Common Patterns

### Building a Project Hierarchy

```python
# Get the plan
plan = client.get_project_plan_by_id(plan_id)

# Create root activity
root = client.create_activity(
    name="Phase 1: Requirements",
    start_date="2026-05-01T00:00:00Z",
    finish_date="2026-05-31T00:00:00Z"
)
client.add_activity_to_plan(plan_id, root['ID'])

# Create child activity
child = client.create_activity(
    name="Gather Requirements",
    start_date="2026-05-01T00:00:00Z",
    finish_date="2026-05-15T00:00:00Z"
)

# Add as child (Activity hierarchy is managed separately)
# Children navigation property on parent activity
```

### Setting Activity Owner

```python
# Get activity with owner
activity = client.get_activity_by_id(activity_id, expand=["ActivityOwner"])

# Update activity owner (typically done through update)
# Note: ActivityOwner may be read-only in some configurations
```
