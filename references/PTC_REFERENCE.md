# Common Domain (PTC) Reference

Complete reference documentation for the Windchill Common PTC OData domain.

## Base URL
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/PTC/

## Metadata URL
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/PTC/$metadata

## Domain Overview

The Common (PTC) domain provides access to shared/common entities in Windchill including:

### Security & Authentication
- CSRF - CSRF token retrieval endpoint

### User & Group Management
- Users - User accounts and information
- Groups - User groups and roles
- Principals - Generic principal objects (users, groups)

### Container & Organization Management
- Containers - Containers (products, libraries, projects)
- Organizations - Organizational units
- OrganizationsContainers - Organization-container relationships
- Locations - Physical locations

### Type & Attribute Management
- TypeDefinitions - Type definitions for custom types
- Attributes - Type attributes
- EnumeratedValues - Enumerated values for type attributes
- TypePropertyDefinitions - Type property definitions
- TypeConstraintDefinitions - Type constraint definitions

### Workflow & Task Management
- Workflows - Workflow definitions
- WorkflowProcesses - Active workflow processes
- WorkflowMilestones - Workflow milestones
- WorkflowVariables - Workflow variables
- WorkflowEvents - Workflow events
- Tasks - Task assignments
- TaskAssignments - Task assignment details

### Change Management
- ChangeRequests - Change request definitions
- ChangeNotices - Change notice definitions
- ChangeActivities - Change activity definitions

### Configuration Management
- Configurations - Configuration objects
- ConfigurationContexts - Configuration contexts
- EffectivityDates - Effectivity dates
- EffectivityRanges - Effectivity ranges

### Lifecycle Management
- LifeCycleTemplates - Lifecycle template definitions
- LifeCycleStates - Lifecycle state definitions
- LifeCycleTransitions - Lifecycle transition rules
- LifeCycleHistory - Lifecycle history records

### Classification Management
- Classifications - Classification categories
- ClassificationNodes - Classification hierarchy nodes
- ClassifiedItems - Items with classifications

### Project Management
- Projects - Project definitions
- ProjectLinks - Project links/associations
- ProjectRoles - Project role definitions
- ProjectMembers - Project membership

### Folder Management
- Folders - Folder definitions
- FolderMembers - Folder member items

### Preference Management
- Preferences - User and system preferences
- PreferenceDefinitions - Preference definitions

### Navigation Management
- NavigationTrees - Navigation tree definitions
- NavigationNodes - Navigation node items

### Audit & History
- Audits - Audit trail records
- History - Object history records

### Localization
- LocaleDefinitions - Locale definitions
- ResourceBundles - Resource bundles
- Translations - Translation records

---

## Security & Authentication

### CSRF Token

Endpoint: /PTC/CSRF
Method: GET

Description: Retrieves a CSRF token required for POST, PATCH, and DELETE operations.

Response:
{
  "CSRF": "token_value_here"
}

Usage Example:
GET /PTC/CSRF

POST /PTC/Users
X-CSRF-Token: token_value_here
Content-Type: application/json
{
  "Name": "newuser",
  "FullName": "New User"
}

---

## Common Query Options

All entities support the following OData query options:

| Option | Description | Example |
|--------|-------------|---------|
| $filter | Filter results | $filter=Name eq 'value' |
| $select | Select specific properties | $select=Name,Description |
| $top | Limit results | $top=50 |
| $skip | Skip results | $skip=10 |
| $orderby | Sort results | $orderby=Name asc |
| $expand | Expand navigation properties | $expand=Groups |

---

## Filter Operators

| Operator | Description | Example |
|----------|-------------|---------|
| eq | Equal | Name eq 'value' |
| ne | Not equal | Name ne 'value' |
| gt | Greater than | ID gt '100' |
| ge | Greater than or equal | ID ge '100' |
| lt | Less than | ID lt '100' |
| le | Less than or equal | ID le '100' |
| and | Logical AND | Name eq 'test' and Type eq 'Product' |
| or | Logical OR | Name eq 'test' or Name eq 'demo' |
| not | Logical NOT | not (Name eq 'test') |
| contains | Contains substring | contains(Name, 'test') |
| startswith | Starts with | startswith(Name, 'test') |
| endswith | Ends with | endswith(Name, 'test') |