# Quality Management System (QMS) Domain Reference

Complete reference documentation for the Windchill Quality Management System OData domain.

## Base URL

```
https://windchill.example.com/Windchill/servlet/odata/QMS/
```

## Metadata URL

```
https://windchill.example.com/Windchill/servlet/odata/QMS/$metadata
```

## Domain Overview

The Quality Management System (QMS) domain provides access to Windchill's quality management entities:

### Quality Objects
- **QualityActions** - Quality actions and corrective actions
- **QualityObject** - Base quality object type
- **QualityProcess** - Quality process definitions

### Customer Experience Integration
- **Place** - Places/locations for quality events
- **QualityContact** - Quality contacts (persons/locations)

### Product Quality
- **Subject** - Quality subject (product reference)
- **NonConformance** - Non-conformance records
- **CAPA** - Corrective and Preventive Actions

---

## Entity Types

### QualityAction

Quality action for tracking corrective and preventive actions.

**Endpoint:** `/QMS/QualityActions`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Action name |
| **Number** | String | Action number |
| **Description** | String | Action description |
| **State** | EnumType | Lifecycle state |
| **LifeCycleTemplateName** | String | Lifecycle template name (ReadOnly) |
| **ActionType** | String | Type of action |
| **Priority** | String | Priority level |
| **DueDate** | DateTimeOffset | Due date for completion |
| **CompletionDate** | DateTimeOffset | Actual completion date |
| **RootCause** | String | Root cause analysis |
| **CorrectiveAction** | String | Corrective action description |
| **PreventiveAction** | String | Preventive action description |
| **VerificationMethod** | String | Verification method |
| **Effectiveness** | String | Effectiveness status |
| **CreatedBy** | String | User who created (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **ModifiedBy** | String | User who last modified (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` → PTC.DataAdmin.Container (Container context)
- `Creator` → PTC.PrincipalMgmt.User (User who created)
- `Modifier` → PTC.PrincipalMgmt.User (User who last modified)
- `Owner` → PTC.PrincipalMgmt.User (Assigned owner)
- `RelatedQualityObject` → PTC.QMS.QualityObject (Related quality object)

**CRUD Operations:**

```bash
# Get all quality actions
GET /QMS/QualityActions

# Get quality action by ID
GET /QMS/QualityActions('{id}')

# Get quality action by number
GET /QMS/QualityActions?$filter=Number eq 'QA-00001'

# Filter by state
GET /QMS/QualityActions?$filter=State/Value eq 'OPEN'

# Get open quality actions
GET /QMS/QualityActions?$filter=State/Value eq 'OPEN' or State/Value eq 'IN_PROGRESS'

# Get with owner and context
GET /QMS/QualityActions('{id}')?$expand=Owner,Context

# Get with related quality object
GET /QMS/QualityActions?$expand=RelatedQualityObject,Owner

# Select specific properties
GET /QMS/QualityActions?$select=ID,Name,Number,State,DueDate,Priority

# Order by due date
GET /QMS/QualityActions?$orderby=DueDate asc

# Top results
GET /QMS/QualityActions?$top=50
```

---

### QualityObject

Base quality object for quality management records.

**Endpoint:** `/QMS/QualityObjects`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Object name |
| **Number** | String | Object number |
| **Description** | String | Object description |
| **State** | EnumType | Lifecycle state |
| **LifeCycleTemplateName** | String | Lifecycle template name (ReadOnly) |
| **QualityType** | String | Quality type |
| **Severity** | String | Severity level |
| **Status** | String | Status |
| **CreatedBy** | String | User who created (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **ModifiedBy** | String | User who last modified (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` → PTC.DataAdmin.Container (Container context)
- `Creator` → PTC.PrincipalMgmt.User (User who created)
- `Modifier` → PTC.PrincipalMgmt.User (User who last modified)
- `QualityActions` → Collection(PTC.QMS.QualityAction) (Related quality actions)

---

### Place

Location/place for quality events (manufacturing site, customer location, etc.).

**Endpoint:** `/QMS/Places`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Place name |
| **Number** | String | Place number |
| **Description** | String | Place description |
| **Address** | String | Physical address |
| **City** | String | City |
| **State** | String | State/Province |
| **Country** | String | Country |
| **PostalCode** | String | Postal/ZIP code |
| **PlaceType** | String | Type of place (e.g., Manufacturing, Customer Site) |
| **CreatedBy** | String | User who created (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` → PTC.DataAdmin.Container (Container context)

**CRUD Operations:**

```bash
# Get all places
GET /QMS/Places

# Get place by ID
GET /QMS/Places('{id}')

# Filter by country
GET /QMS/Places?$filter=Country eq 'USA'

# Filter by type
GET /QMS/Places?$filter=PlaceType eq 'Manufacturing'

# Search by name
GET /QMS/Places?$filter=contains(Name, 'Plant')
```

---

### QualityContact

Contact person or location related to quality events.

**Endpoint:** `/QMS/QualityContacts`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Contact name |
| **ContactType** | String | Type of contact |
| **Email** | String | Email address |
| **Phone** | String | Phone number |
| **Role** | String | Role in quality process |
| **Organization** | String | Organization name |
| **CreatedBy** | String | User who created (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` → PTC.DataAdmin.Container (Container context)
- `Place` → PTC.QMS.Place (Associated place/location)

---

### Subject

Quality subject representing a product or item in quality processes.

**Endpoint:** `/QMS/Subjects`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Subject name |
| **Number** | String | Subject number |
| **SubjectType** | String | Type of subject |
| **Description** | String | Subject description |
| **ProductNumber** | String | Associated product number |
| **ProductName** | String | Associated product name |
| **SerialNumber** | String | Serial number |
| **LotNumber** | String | Lot/batch number |
| **CreatedBy** | String | User who created (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` → PTC.DataAdmin.Container (Container context)

**CRUD Operations:**

```bash
# Get all subjects
GET /QMS/Subjects

# Get subject by ID
GET /QMS/Subjects('{id}')

# Search by product number
GET /QMS/Subjects?$filter=ProductNumber eq 'PART-001'

# Search by serial number
GET /QMS/Subjects?$filter=SerialNumber eq 'SN-12345'

# Search by lot number
GET /QMS/Subjects?$filter=LotNumber eq 'LOT-2024-001'
```

---

### NonConformance

Non-conformance record for tracking quality issues.

**Endpoint:** `/QMS/NonConformances`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Non-conformance name |
| **Number** | String | Non-conformance number |
| **Description** | String | Description of non-conformance |
| **State** | EnumType | Lifecycle state |
| **NCType** | String | Type of non-conformance |
| **Severity** | String | Severity level |
| **DiscoveryDate** | DateTimeOffset | Date discovered |
| **DiscoveryLocation** | String | Where discovered |
| **QuantityAffected** | Double | Quantity affected |
| **Disposition** | String | Disposition decision |
| **CreatedBy** | String | User who created (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **ModifiedBy** | String | User who last modified (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` → PTC.DataAdmin.Container (Container context)
- `Creator` → PTC.PrincipalMgmt.User (User who created)
- `Modifier` → PTC.PrincipalMgmt.User (User who last modified)
- `Subject` → PTC.QMS.Subject (Related product/subject)
- `CAPA` → PTC.QMS.QualityAction (Related CAPA)
- `Place` → PTC.QMS.Place (Location of discovery)

---

### CAPA (Corrective and Preventive Action)

CAPA record for tracking corrective and preventive actions.

**Endpoint:** `/QMS/CAPAs`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | CAPA name |
| **Number** | String | CAPA number |
| **Description** | String | Description of CAPA |
| **State** | EnumType | Lifecycle state |
| **CAPAType** | String | Type of CAPA (Corrective, Preventive, or Both) |
| **Priority** | String | Priority level |
| **DueDate** | DateTimeOffset | Due date |
| **CompletionDate** | DateTimeOffset | Completion date |
| **RootCauseAnalysis** | String | Root cause analysis |
| **CorrectiveAction** | String | Corrective action taken |
| **PreventiveAction** | String | Preventive action taken |
| **VerificationStatus** | String | Verification status |
| **EffectivenessStatus** | String | Effectiveness status |
| **CreatedBy** | String | User who created (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **ModifiedBy** | String | User who last modified (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` → PTC.DataAdmin.Container (Container context)
- `Creator` → PTC.PrincipalMgmt.User (User who created)
- `Modifier` → PTC.PrincipalMgmt.User (User who last modified)
- `Owner` → PTC.PrincipalMgmt.User (Assigned owner)
- `Subject` → PTC.QMS.Subject (Related product/subject)
- `NonConformance` → PTC.QMS.NonConformance (Related non-conformance)

---

## Common Query Examples

### Get Open Quality Actions

```bash
GET /QMS/QualityActions?$filter=State/Value eq 'OPEN' or State/Value eq 'IN_PROGRESS'&$expand=Owner,RelatedQualityObject&$orderby=DueDate asc
```

### Get Quality Actions by Priority

```bash
GET /QMS/QualityActions?$filter=Priority eq 'High'&$expand=Owner,Context
```

### Get Overdue Quality Actions

```bash
GET /QMS/QualityActions?$filter=DueDate lt 2026-01-01T00:00:00Z and State/Value ne 'COMPLETED'&$expand=Owner
```

### Get Non-Conformances by Product

```bash
GET /QMS/NonConformances?$expand=Subject&$filter=Subject/ProductNumber eq 'PART-001'
```

### Get CAPAs for a Non-Conformance

```bash
GET /QMS/NonConformances('{id}')/CAPA?$expand=Owner,Subject
```

### Get Quality Objects with Actions

```bash
GET /QMS/QualityObjects?$expand=QualityActions($expand=Owner)
```

### Get Places by Country

```bash
GET /QMS/Places?$filter=Country eq 'USA'&$orderby=Name asc
```

### Get Subjects by Lot Number

```bash
GET /QMS/Subjects?$filter=LotNumber eq 'LOT-2024-001'&$expand=Context
```

---

## Entity Relationships

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PTC.QMS Namespace                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐      QualityActions     ┌──────────────────┐         │
│  │  QualityObject   │─────────────────────────►│  QualityAction   │         │
│  ├──────────────────┤                          ├──────────────────┤         │
│  │ - QualityActions │                          │ - Owner          │         │
│  │ - Context        │                          │ - Context        │         │
│  │ - Creator        │                          │ - Creator        │         │
│  └──────────────────┘                          │ - Modifier       │         │
│                                                │ - RelatedObject   │         │
│                                                └──────────────────┘         │
│                                                                             │
│  ┌──────────────────┐      CAPA        ┌──────────────────┐                 │
│  │ NonConformance   │─────────────────►│      CAPA        │                 │
│  ├──────────────────┤                  ├──────────────────┤                 │
│  │ - Subject        │                  │ - Subject        │                 │
│  │ - Place          │                  │ - NonConformance │                 │
│  │ - CAPA           │                  │ - Owner          │                 │
│  │ - Context        │                  │ - Context        │                 │
│  └──────────────────┘                  └──────────────────┘                 │
│         │                                                                    │
│         │ Subject                                                            │
│         ▼                                                                    │
│  ┌──────────────────┐                  ┌──────────────────┐                 │
│  │     Subject      │                  │      Place       │                 │
│  ├──────────────────┤                  ├──────────────────┤                 │
│  │ - Context        │                  │ - Context        │                 │
│  └──────────────────┘                  └──────────────────┘                 │
│                                              ▲                               │
│                                              │ Place                         │
│  ┌──────────────────┐                        │                               │
│  │  QualityContact  │────────────────────────┘                               │
│  ├──────────────────┤                                                        │
│  │ - Place          │                                                        │
│  │ - Context        │                                                        │
│  └──────────────────┘                                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Cross-Domain References

| From Entity | Navigation Property | Target Domain | Target Entity |
|-------------|---------------------|---------------|---------------|
| QualityAction | Context | DataAdmin | Container |
| QualityAction | Creator | PrincipalMgmt | User |
| QualityAction | Modifier | PrincipalMgmt | User |
| QualityAction | Owner | PrincipalMgmt | User |
| QualityObject | Context | DataAdmin | Container |
| QualityObject | Creator | PrincipalMgmt | User |
| NonConformance | Context | DataAdmin | Container |
| NonConformance | Creator | PrincipalMgmt | User |
| CAPA | Context | DataAdmin | Container |
| CAPA | Owner | PrincipalMgmt | User |
| Place | Context | DataAdmin | Container |
| QualityContact | Context | DataAdmin | Container |
| Subject | Context | DataAdmin | Container |

---

## State Values

### Quality Action States
- **OPEN** - Open for assignment
- **IN_PROGRESS** - Being worked on
- **PENDING_VERIFICATION** - Pending verification
- **COMPLETED** - Completed
- **CLOSED** - Closed
- **CANCELLED** - Cancelled

### Non-Conformance States
- **OPEN** - Open for review
- **UNDER_INVESTIGATION** - Being investigated
- **DISPOSITION_PENDING** - Pending disposition
- **DISPOSITIONED** - Disposition determined
- **CLOSED** - Closed

### CAPA States
- **OPEN** - Open
- **INVESTIGATION** - Under investigation
- **CORRECTIVE_ACTION** - Corrective action in progress
- **PREVENTIVE_ACTION** - Preventive action in progress
- **VERIFICATION** - Verification in progress
- **CLOSED** - Closed

---

## Pagination

Use `$top` and `$skip` for pagination:

```bash
GET /QMS/QualityActions?$top=50&$skip=0
GET /QMS/QualityActions?$top=50&$skip=50
```

---

## Notes

1. **READ-ONLY Access** - Quality objects are typically read through OData. Quality management operations are done through Windchill UI or specialized APIs.

2. **Lifecycle Management** - All quality objects follow Windchill lifecycle templates with defined state transitions.

3. **CAPA Integration** - CAPA records are closely linked to non-conformances and quality actions.

4. **Subject Reference** - Subjects link quality objects to specific products, lots, or serial numbers.

5. **Place Tracking** - Places track locations where quality events occur or are discovered.

6. **Cross-Domain References** - QMS domain references DataAdmin (Container) and PrincipalMgmt (User) for context and ownership.
