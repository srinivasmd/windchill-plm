---
Domain: Workflow
Client: `from domains.Workflow import WorkflowClient`
---

> **Use the WorkflowClient**: `from domains.Workflow import WorkflowClient`
>
> This reference documents the entity types and properties. For programmatic access, use the domain client.

# Workflow Domain (Workflow) Reference

This domain provides access to Windchill workflow management entities including work items, activities, voting events, and process templates.

## Workflow API Endpoint

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/Workflow/
```

## Metadata

OData metadata is available at:
```
GET /Workflow/$metadata
```

## Workflow Domain Entities

The Workflow domain includes the following main entity types:

| Entity | Description | Operations |
|--------|-------------|------------|
| **WorkItems** | Work items (tasks, approvals, reviews) | READ |
| **VotingEventAudit** | Voting event audit information | READ |
| **WfEventAudit** | Workflow event audit information | READ |
| **Activity** | Workflow activities (task assignments) | READ |
| **Subject** | Workflow subject (business object) | READ |
| **WorkItemProcessTemplate** | Workflow process templates | READ |
| **ProjectWorkItem** | Project-related work items | READ |
| **WfActivity** | Base activity entity | READ |

## Entity Details

### WorkItems

Primary entity for workflow tasks and assignments.

**Common Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **ObjectType** | String | Type of work item (e.g., "Task") |
| **TaskName** | String | Display name of the task |
| **Description** | String | Task description |
| **Status** | EnumType | Status (e.g., "PENDING", "ASSIGNED", "COMPLETED") |
| **Priority** | String | Priority level |
| **Role** | EnumType | User role for this work item |
| **Required** | Boolean | Whether this is a required task |
| **Reassigned** | Boolean | Whether task was reassigned |
| **SigningRequired** | Boolean | Whether digital signature required |
| **OpenAssignments** | Boolean | Whether there are open assignments |
| **ProcessData** | Complex | Process data including routing choices, variables |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- **Owner** → PTC.PrincipalMgmt.User (User assigned to this work item)
- **Activity** → PTC.Workflow.Activity (Parent activity)
- **Subject** → PTC.Workflow.Subject (Business object being processed)
- **OriginalOwner** → PTC.PrincipalMgmt.User (Original assignee)
- **ProcessTemplate** → PTC.Workflow.WorkItemProcessTemplate (Template used)
- **CompletedBy** → PTC.PrincipalMgmt.User (User who completed the task)

**ProcessData Complex Type:**
| Property | Type | Description |
|----------|------|-------------|
| **WorkitemComment** | String | Comments entered by user |
| **WorkitemRoutingChoices** | String[] | Available routing options |
| **WorkitemVotingOptions** | String[] | Available voting options |
| **Variables** | Variable[] | Workflow variables |

**Variable Complex Type:**
| Property | Type | Description |
|----------|------|-------------|
| **Name** | String | Variable name |
| **Value** | String | Variable value |
| **TypeName** | String | Java type name |
| **DisplayName** | String | Display name |

### Activity

Workflow activity containing one or more work items.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Activity name |
| **Instructions** | String | Activity instructions |
| **Deadline** | DateTimeOffset | Activity deadline |
| **IsOverdue** | Boolean | Whether activity is overdue |
| **ProcessData** | Complex | Process data (same structure as WorkItem) |
| **UserEventList** | String[] | Available user events |
| **ValidVotes** | String[] | Valid voting options |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TripCount** | Integer | Trip counter (ReadOnly) |

**Navigation Properties:**
- **WorkItems** → Collection(PTC.Workflow.WorkItem) (Child work items)
- **VotingEventAudits** → Collection(PTC.Workflow.VotingEventAudit) (Voting history)
- **Context** → PTC.DataAdmin.Container (Container context)

### VotingEventAudit

Audit information for voting events.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Comment** | String | Comment for the vote |
| **Decision** | VotingEventDecision | Voting decision details |
| **Required** | Boolean | Whether this vote was required |
| **Role** | EnumType | User role |
| **Signed** | Boolean | Whether vote was signed |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TripCount** | Integer | Trip counter (ReadOnly) |

**VotingEventDecision Complex Type:**
| Property | Type | Description |
|----------|------|-------------|
| **RoutingEvents** | String[] | Selected routing choices |
| **Vote** | String | Vote value |

**Navigation Properties:**
- **Assignee** → PTC.PrincipalMgmt.User (User who voted)

### Subject

The business object being processed in workflow.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **SubjectName** | String | Display name of subject |
| **Type** | String | Type of business object |
| **State** | EnumType | Lifecycle state |
| **LifeCycleTemplateName** | String | Lifecycle template name |
| **Icon** | Icon | Icon metadata |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

### WorkItemProcessTemplate

Workflow process template definition.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **MasterID** | String | Master object ID |
| **Name** | String | Template name |
| **CreatedBy** | String | Creator username |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **ModifiedBy** | String | Last modifier username |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- **Creator** → PTC.PrincipalMgmt.User (User who created template)
- **Modifier** → PTC.PrincipalMgmt.User (User who last modified template)

### WfEventAudit

Base audit entity for workflow events.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TripCount** | Integer | Trip counter (ReadOnly) |

**Navigation Properties:**
- **CompletedBy** → PTC.PrincipalMgmt.User (User who completed event)

### ProjectWorkItem

Project-related work items (extends WorkItem).

Inherits all properties from WorkItem.

## Common Query Patterns

### Get All Work Items

```bash
GET /Workflow/WorkItems
```

### Get Work Item by ID

```bash
GET /Workflow/WorkItems('OR:wt.workflow.work.WorkItem:953269')
```

### Filter Work Items by Status

```bash
GET /Workflow/WorkItems?$filter=Status/Value eq 'PENDING'
```

### Filter Work Items by Role

```bash
GET /Workflow/WorkItems?$filter=Role/Value eq 'REVIEWER'
```

### Get Work Items for a Specific User (Owner)

```bash
GET /Workflow/WorkItems?$filter=Owner/Name eq 'Pat'
```

### Get Open Work Items

```bash
GET /Workflow/WorkItems?$filter=OpenAssignments eq true
```

### Filter Work Items by Priority

```bash
GET /Workflow/WorkItems?$filter=Priority eq 'Highest'
```

### Get Work Items Created in Date Range

```bash
GET /Workflow/WorkItems?$filter=CreatedOn ge 2024-01-01T00:00:00Z and CreatedOn le 2024-12-31T23:59:59Z
```

### Get Work Items with Expanded Navigation

```bash
GET /Workflow/WorkItems('OR:wt.workflow.work.WorkItem:953269')?$expand=Owner,Activity,Subject,ProcessTemplate,CompletedBy
```

### Get Multiple Work Items with Expansion

```bash
GET /Workflow/WorkItems?$top=10&$expand=Owner,Activity,Subject
```

### Get Activity for a Work Item

```bash
GET /Workflow/WorkItems('OR:wt.workflow.work.WorkItem:953269')/Activity
```

### Get Activity with Work Items and Voting Events

```bash
GET /Workflow/WorkItems('OR:wt.workflow.work.WorkItem:953269')/Activity?$expand=WorkItems,VotingEventAudits
```

### Get Voting Event Audits for an Activity

```bash
GET /Workflow/Activities('OR:wt.workflow.work.WfAssignedActivity:953267')/VotingEventAudits
```

### Get Subject for a Work Item

```bash
GET /Workflow/WorkItems('OR:wt.workflow.work.WorkItem:953269')/Subject
```

### Get Process Template

```bash
GET /Workflow/WorkItems('OR:wt.workflow.work.WorkItem:953269')/ProcessTemplate
```

### Select Specific Properties

```bash
GET /Workflow/WorkItems?$select=ID,TaskName,Status,Priority,Role,Owner/Name&$expand=Owner
```

### Order Work Items

```bash
GET /Workflow/WorkItems?$orderby=CreatedOn desc
GET /Workflow/WorkItems?$orderby=Priority,Status
```

### Top N Work Items

```bash
GET /Workflow/WorkItems?$top=20
```

### Work Items Count

```bash
GET /Workflow/WorkItems/$count
```

### Count Work Items by Status

```bash
GET /Workflow/WorkItems/$count?$filter=Status/Value eq 'PENDING'
```

## Workflow Status Values

Common work item statuses include:
- **PENDING** - Waiting to be assigned
- **ASSIGNED** - Assigned to a user
- **IN_PROGRESS** - In progress
- **COMPLETED** - Completed
- **REJECTED** - Rejected
- **REROUTE** - Rerouted
- **PAUSED** - Paused

## Common Role Values

Common workflow roles include:
- **REVIEWER** - Reviewer role
- **APPROVER** - Approver role
- **ASSIGNEE** - Assignee role
- **OBSERVER** - Observer role
- **IMPLEMENTER** - Implementer role

## Priority Values

Common priority values:
- **Highest**
- **High**
- **Medium**
- **Low**
- **Lowest**

## Process Data Variables

Process data can contain custom workflow variables:
- **Name** - Variable name
- **Value** - Variable value
- **TypeName** - Java type (e.g., "java.lang.String", "java.lang.Boolean")
- **DisplayName** - Display label

Common workflow variables include:
- **special_instructions** - Special instructions for task
- **routing_instructions** - Routing instructions
- **custom_field** - Custom field defined in process template

## Voting Events

Voting events track user decisions in workflow:
- **RoutingEvents** - User's chosen routing path (e.g., "Complete", "Rework", "Reject")
- **Vote** - Vote value (if applicable)
- **Comment** - User comments
- **Required** - Whether vote was required
- **Signed** - Whether vote was digitally signed
- **Role** - User's role in voting

## Example Use Cases

### Example 1: Get All Pending Review Tasks for a User

```bash
GET /Workflow/WorkItems?$filter=Status/Value eq 'PENDING' and Role/Value eq 'REVIEWER' and Owner/Name eq 'Pat'&$expand=Owner,Activity,Subject&$orderby=Priority desc
```

### Example 2: Get All Work Items for a Change Notice

```bash
# Get work items where subject is a specific ChangeActivity2
GET /Workflow/WorkItems?$filter=Subject/Type eq 'wt.change2.WTChangeActivity2'&$expand=Owner,Subject,Activity
```

### Example 3: Get Overdue Activities

```bash
GET /Workflow/Activities?$filter=IsOverdue eq true&$expand=WorkItems,Context
```

### Example 4: Get Voting History for a Work Item

```bash
GET /Workflow/WorkItems('OR:wt.workflow.work.WorkItem:953269')/Activity?$expand=VotingEventAudits
```

### Example 5: Get All Completed Work Items in Date Range

```bash
GET /Workflow/WorkItems?$filter=Status/Value eq 'COMPLETED' and LastModified ge 2024-01-01 and LastModified le 2024-12-31&$expand=Owner,CompletedBy,Subject&$orderby=LastModified desc
```

### Example 6: Get Work Items for a Process Template

```bash
GET /Workflow/WorkItems?$filter=ProcessTemplate/Name eq 'Change Activity Workflow'&$expand=Owner,Activity,Subject
```

## Navigation Between Entities

The Workflow domain has several relationships to other domains:

| From Entity | Navigation | To Entity | Description |
|-------------|------------|-----------|-------------|
| WorkItem | Owner | PrincipalMgmt.User | User assigned to work item |
| WorkItem | Activity | Workflow.Activity | Parent activity |
| WorkItem | Subject | Workflow.Subject | Business object |
| WorkItem | ProcessTemplate | Workflow.WorkItemProcessTemplate | Template |
| WorkItem | CompletedBy | PrincipalMgmt.User | User who completed task |
| Activity | WorkItems | Collection(WorkItem) | Child work items |
| Activity | VotingEventAudits | Collection(VotingEventAudit) | Voting history |
| Activity | Context | DataAdmin.Container | Container context |
| VotingEventAudit | Assignee | PrincipalMgmt.User | User who voted |
| WfEventAudit | CompletedBy | PrincipalMgmt.User | User who completed |
| WorkItemProcessTemplate | Creator | PrincipalMgmt.User | Template creator |
| WorkItemProcessTemplate | Modifier | PrincipalMgmt.User | Template modifier |

## Pagination

Use `$top` and `$skip` for pagination:

```bash
GET /Workflow/WorkItems?$top=50&$skip=0
GET /Workflow/WorkItems?$top=50&$skip=50
```

## Filtering Options

Complex filters using `and`, `or`, `not`:

```bash
GET /Workflow/WorkItems?$filter=(
  Status/Value eq 'PENDING' and
  Role/Value eq 'REVIEWER' and
  OpenAssignments eq true
) or (
  Status/Value eq 'IN_PROGRESS' and
  Priority eq 'Highest'
)
```

String filters using `startswith`, `endswith`, `contains`:

```bash
GET /Workflow/WorkItems?$filter=startswith(TaskName, 'Review')
GET /Workflow/WorkItems?$filter=contains(Description, 'change notice')
```

## Notes

1. ** READ-ONLY Access** - The Workflow domain is primarily read-only. Work items are typically managed through Windchill UI or other API endpoints, not through OData.

2. ** Navigation Performance** - Expanding multiple navigation properties can impact performance. Only expand what you need.

3. ** OData Version** - The Workflow domain uses OData v5.

4. ** Timezone** - All timestamps are in UTC. Use `@PTC.AppliedContainerContext.LocalTimeZone` for local timezone information.

5. ** Object Identifiers** - IDs are OIDs (Object Identifiers) in the format `OR:<ObjectType>:<NumericID>`. Always use these for dereferencing navigation properties.

6. ** Process Data** - ProcessData is a complex structure that can vary between process templates. Always inspect it before use.

7. ** Status and Role Enums** - Status and Role are enum types with both `Value` and `Display` properties.
