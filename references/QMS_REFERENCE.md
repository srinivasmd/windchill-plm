# Quality Management System (QMS) Domain Reference

Complete reference documentation for the Windchill Quality Management System OData domain.

## Base URL

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/QMS/
```

## Metadata URL

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/QMS/$metadata
```

## Domain Overview

The Quality Management System (QMS) domain provides access to quality management entities in Windchill including:

### Quality Records
- **QualityAction** - Quality action items
- **QualityIssue** - Quality issues and incidents
- **QualityProcedure** - Quality procedures
- **QualityPlan** - Quality plans

### Quality Contacts
- **QualityContact** - Quality contact information
- **Place** - Places and locations

### CAPA
- **CorrectiveAction** - Corrective actions
- **PreventiveAction** - Preventive actions

### Audit
- **Audit** - Quality audits
- **AuditFinding** - Audit findings
- **AuditChecklist** - Audit checklists

### Nonconformance
- **Nonconformance** - Nonconformance reports
- **NCDisposition** - Nonconformance dispositions

---

## Entity Types

### QualityAction

Quality action items for tracking quality-related tasks.

**Endpoint:** `/QMS/QualityActions`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Quality Action name |
| **Number** | String | Quality Action number |
| **Description** | String | Detailed description |
| **State** | EnumType | Lifecycle state (ReadOnly) |
| **LifeCycleTemplateName** | String | Lifecycle template name (ReadOnly) |
| **Priority** | EnumType | Priority level |
| **Category** | EnumType | Category of action |
| **DueDate** | DateTimeOffset | Due date for completion |
| **CompletionDate** | DateTimeOffset | Actual completion date |
| **FolderLocation** | String | Folder path in Windchill |
| **MasterID** | String | Master ID (ReadOnly) |
| **CreatedBy** | String | Created by (ReadOnly) |
| **ModifiedBy** | String | Modified by (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` - Container (PTC.DataAdmin.Container)
- `Creator` - Creator user (PTC.PrincipalMgmt.User)
- `Modifier` - Modifier user (PTC.PrincipalMgmt.User)
- `Owner` - Owner user (PTC.PrincipalMgmt.User)
- `QualityIssue` - Related Quality Issue
- `RelatedProducts` - Collection of Related Products

**CRUD Operations:**

```bash
# Get all quality actions
GET /QMS/QualityActions

# Get quality action by number
GET /QMS/QualityActions?$filter=Number eq 'QA-000001'

# Filter by state
GET /QMS/QualityActions?$filter=State/Value eq 'OPEN'

# Filter by priority
GET /QMS/QualityActions?$filter=Priority/Value eq 'HIGH'

# Filter by due date
GET /QMS/QualityActions?$filter=DueDate le 2026-03-01T00:00:00Z

# Expand with owner
GET /QMS/QualityActions('{id}')?$expand=Owner

# Create quality action
POST /QMS/QualityActions
Content-Type: application/json
X-CSRF-Token: {token}

{
  "Name": "Quality Action - Product Inspection",
  "Number": "QA-000001",
  "Description": "Conduct product inspection for quality compliance",
  "Priority": {"Value": "HIGH"},
  "DueDate": "2026-03-15T00:00:00Z",
  "FolderLocation": "/Default/Quality/Actions"
}
```

---

### QualityIssue

Quality issues and incidents tracking.

**Endpoint:** `/QMS/QualityIssues`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Quality Issue name |
| **Number** | String | Quality Issue number |
| **Description** | String | Detailed description of the issue |
| **State** | EnumType | Lifecycle state (ReadOnly) |
| **LifeCycleTemplateName** | String | Lifecycle template name (ReadOnly) |
| **Severity** | EnumType | Severity level |
| **Category** | EnumType | Category of issue |
| **Source** | EnumType | Source of the issue |
| **ReportedDate** | DateTimeOffset | Date issue was reported |
| **ResolutionDate** | DateTimeOffset | Date issue was resolved |
| **FolderLocation** | String | Folder path in Windchill |
| **MasterID** | String | Master ID (ReadOnly) |
| **CreatedBy** | String | Created by (ReadOnly) |
| **ModifiedBy** | String | Modified by (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` - Container (PTC.DataAdmin.Container)
- `Creator` - Creator user (PTC.PrincipalMgmt.User)
- `Modifier` - Modifier user (PTC.PrincipalMgmt.User)
- `Reporter` - Reporter user (PTC.PrincipalMgmt.User)
- `QualityActions` - Collection of Quality Actions
- `RelatedProducts` - Collection of Related Products
- `Nonconformances` - Collection of Nonconformances

**CRUD Operations:**

```bash
# Get all quality issues
GET /QMS/QualityIssues

# Get quality issue by number
GET /QMS/QualityIssues?$filter=Number eq 'QI-000001'

# Filter by state
GET /QMS/QualityIssues?$filter=State/Value eq 'OPEN'

# Filter by severity
GET /QMS/QualityIssues?$filter=Severity/Value eq 'CRITICAL'

# Expand with quality actions
GET /QMS/QualityIssues('{id}')?$expand=QualityActions

# Create quality issue
POST /QMS/QualityIssues
Content-Type: application/json
X-CSRF-Token: {token}

{
  "Name": "Quality Issue - Product Defect",
  "Number": "QI-000001",
  "Description": "Product defect reported by customer",
  "Severity": {"Value": "HIGH"},
  "Source": {"Value": "CUSTOMER_FEEDBACK"},
  "ReportedDate": "2026-02-08T10:00:00Z",
  "FolderLocation": "/Default/Quality/Issues"
}
```

---

### QualityContact

Quality contact information for quality management.

**Endpoint:** `/QMS/QualityContacts`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Contact name |
| **Email** | String | Contact email |
| **Phone** | String | Contact phone |
| **Organization** | String | Organization name |
| **Role** | String | Contact role |
| **Type** | EnumType | Contact type (INTERNAL, EXTERNAL) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- `User` - Related User (PTC.PrincipalMgmt.User)
- `Place` - Related Place (PTC.QMS.Place)

**CRUD Operations:**

```bash
# Get all quality contacts
GET /QMS/QualityContacts

# Get contact by name
GET /QMS/QualityContacts?$filter=Name eq 'John Smith'

# Filter by type
GET /QMS/QualityContacts?$filter=Type/Value eq 'INTERNAL'

# Expand with user
GET /QMS/QualityContacts('{id}')?$expand=User,Place
```

---

### Place

Places and locations for quality management.

**Endpoint:** `/QMS/Places`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Place name |
| **Description** | String | Place description |
| **Type** | EnumType | Place type (SITE, FACILITY, LOCATION) |
| **Address** | String | Physical address |
| **City** | String | City |
| **StateProvince** | String | State or province |
| **Country** | EnumType | Country |
| **PostalCode** | String | Postal code |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- `Context` - Container (PTC.DataAdmin.Container)
- `QualityContacts` - Collection of Quality Contacts at this place

**CRUD Operations:**

```bash
# Get all places
GET /QMS/Places

# Get place by name
GET /QMS/Places?$filter=Name eq 'Manufacturing Site A'

# Filter by type
GET /QMS/Places?$filter=Type/Value eq 'SITE'

# Filter by country
GET /QMS/Places?$filter=Country/Value eq 'USA'

# Expand with contacts
GET /QMS/Places('{id}')?$expand=QualityContacts
```

---

### Nonconformance

Nonconformance reports for tracking deviations from specifications.

**Endpoint:** `/QMS/Nonconformances`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Nonconformance name |
| **Number** | String | Nonconformance number |
| **Description** | String | Detailed description |
| **State** | EnumType | Lifecycle state (ReadOnly) |
| **LifeCycleTemplateName** | String | Lifecycle template name (ReadOnly) |
| **NCType** | EnumType | Nonconformance type |
| **Severity** | EnumType | Severity level |
| **Quantity** | Double | Quantity affected |
| **DetectedDate** | DateTimeOffset | Date detected |
| **ResolvedDate** | DateTimeOffset | Date resolved |
| **FolderLocation** | String | Folder path in Windchill |
| **MasterID** | String | Master ID (ReadOnly) |
| **CreatedBy** | String | Created by (ReadOnly) |
| **ModifiedBy** | String | Modified by (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- `Context` - Container (PTC.DataAdmin.Container)
- `Creator` - Creator user (PTC.PrincipalMgmt.User)
- `QualityIssue` - Related Quality Issue
- `Dispositions` - Collection of NC Dispositions
- `RelatedProduct** - Related Product

**CRUD Operations:**

```bash
# Get all nonconformances
GET /QMS/Nonconformances

# Get nonconformance by number
GET /QMS/Nonconformances?$filter=Number eq 'NC-000001'

# Filter by state
GET /QMS/Nonconformances?$filter=State/Value eq 'OPEN'

# Filter by type
GET /QMS/Nonconformances?$filter=NCType/Value eq 'MATERIAL'

# Expand with dispositions
GET /QMS/Nonconformances('{id}')?$expand=Dispositions

# Create nonconformance
POST /QMS/Nonconformances
Content-Type: application/json
X-CSRF-Token: {token}

{
  "Name": "Material Nonconformance",
  "Number": "NC-000001",
  "Description": "Material does not meet specifications",
  "NCType": {"Value": "MATERIAL"},
  "Severity": {"Value": "HIGH"},
  "Quantity": 100.0,
  "DetectedDate": "2026-02-08T10:00:00Z",
  "FolderLocation": "/Default/Quality/Nonconformances"
}
```

---

### Audit

Quality audit records.

**Endpoint:** `/QMS/Audits`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Audit name |
| **Number** | String | Audit number |
| **Description** | String | Audit description |
| **State** | EnumType | Lifecycle state (ReadOnly) |
| **AuditType** | EnumType | Type of audit (INTERNAL, EXTERNAL) |
| **AuditDate** | DateTimeOffset | Date of audit |
| **AuditScope** | String | Audit scope |
| **Auditor** | String | Auditor name |
| **Status** | EnumType | Audit status |
| **FolderLocation** | String | Folder path in Windchill |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- `Context` - Container (PTC.DataAdmin.Container)
- `Creator` - Creator user (PTC.PrincipalMgmt.User)
- `Findings` - Collection of Audit Findings
- `Checklist** - Audit Checklist

**CRUD Operations:**

```bash
# Get all audits
GET /QMS/Audits

# Get audit by number
GET /QMS/Audits?$filter=Number eq 'AUD-000001'

# Filter by type
GET /QMS/Audits?$filter=AuditType/Value eq 'INTERNAL'

# Filter by status
GET /QMS/Audits?$filter=Status/Value eq 'COMPLETED'

# Expand with findings
GET /QMS/Audits('{id}')?$expand=Findings
```

---

### AuditFinding

Audit findings from quality audits.

**Endpoint:** `/QMS/AuditFindings`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Finding name |
| **Number** | String | Finding number |
| **Description** | String | Detailed description |
| **FindingType** | EnumType | Type of finding |
| **Severity** | EnumType | Severity level |
| **CorrectiveActionRequired** | Boolean | Whether corrective action required |
| **DueDate** | DateTimeOffset | Due date for resolution |
| **ResolutionDate** | DateTimeOffset | Resolution date |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- `Audit` - Parent Audit
- `CorrectiveAction** - Corrective Action

**CRUD Operations:**

```bash
# Get all audit findings
GET /QMS/AuditFindings

# Get findings for an audit
GET /QMS/Audits('{id}')/Findings

# Filter by severity
GET /QMS/AuditFindings?$filter=Severity/Value eq 'MAJOR'
```

---

## Common Query Examples

### Filter by Multiple Criteria

```bash
# Get open quality actions with high priority due soon
GET /QMS/QualityActions?$filter=State/Value eq 'OPEN' and Priority/Value eq 'HIGH' and DueDate le 2026-03-31T00:00:00Z

# Get critical quality issues reported in a date range
GET /QMS/QualityIssues?$filter=Severity/Value eq 'CRITICAL' and ReportedDate ge 2026-01-01T00:00:00Z and ReportedDate le 2026-02-28T23:59:59Z

# Get nonconformances by type and state
GET /QMS/Nonconformances?$filter=NCType/Value eq 'MATERIAL' and State/Value eq 'OPEN'
```

### Complex Queries with Expansion

```bash
# Get quality issue with all related data
GET /QMS/QualityIssues?$expand=Creator,QualityActions,Nonconformances,RelatedProducts

# Get audit with findings and corrective actions
GET /QMS/Audits?$expand=Findings($expand=CorrectiveAction),Creator

# Get nonconformance with dispositions and related product
GET /QMS/Nonconformances?$expand=Dispositions,RelatedProduct,QualityIssue
```

### Sorting and Pagination

```bash
# Get latest quality issues
GET /QMS/QualityIssues?$orderby=ReportedDate desc&$top=50

# Get paginated results
GET /QMS/QualityActions?$skip=0&$top=25

# Get sorted by priority
GET /QMS/QualityActions?$orderby=Priority,DueDate asc
```

---

## Integration Notes

1. **Cross-Domain References**:
   - QualityContact references User (PrincipalMgmt)
   - QualityContact references Place (QMS)
   - Related products can be from ProdMgmt

2. **CEM Integration**:
   - Customer Experience Management (CEM) references QMS entities
   - EntryLocation references Place
   - PrimaryRelatedPersonOrLocation references QualityContact

3. **Workflow Integration**:
   - Quality objects use Windchill Workflow engine
   - Check Workflow domain for work items related to quality objects

4. **Change Management Integration**:
   - Quality issues can trigger change requests
   - Nonconformances can be linked to change objects

5. **Lifecycle Management**:
   - Quality objects follow lifecycle templates
   - Use GetValidStateTransitions to check valid transitions

---

## Schema Version

Schema Version: 7
