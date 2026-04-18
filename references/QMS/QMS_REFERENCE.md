---
Domain: QMS
Client: `from domains.QMS import QMSClient`
---

> **Use the QMSClient**: `from domains.QMS import QMSClient`
>
> This reference documents the entity types and properties. For programmatic access, use the domain client.

# Quality Management System (QMS) Domain Reference

Complete reference documentation for the Windchill Quality Management System (QMS) OData domain.

## Base URL

```
https://windchill.example.com/Windchill/servlet/odata/QMS/
```

## Metadata URL

```
https://windchill.example.com/Windchill/servlet/odata/QMS/$metadata
```

## Domain Overview

The Quality Management System (QMS) domain provides access to Windchill's quality management objects including:
- **CAPA** - Corrective and Preventive Actions
- **NonConformance** - Non-conformance reports
- **QualityActions** - Quality improvement actions
- **Audits** - Quality audits
- **QualityContacts** - Quality-related contacts
- **Places** - Locations relevant to quality management

---

## Entity Types

### CAPA (Corrective and Preventive Action)

A CAPA is a systematic approach to investigate the root cause of non-conformances and implement corrective and preventive actions.

**Endpoint:** `/QMS/CAPAs`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | CAPA name |
| **Number** | String | CAPA number (unique) |
| **Description** | String | Description of the CAPA |
| **State** | EnumType | Lifecycle state |
| **Priority** | EnumType | CAPA priority |
| **Severity** | EnumType | CAPA severity |
| **RootCause** | String | Root cause analysis |
| **CorrectiveAction** | String | Corrective action description |
| **PreventiveAction** | String | Preventive action description |
| **DueDate** | DateTimeOffset | Target completion date |
| **CompletionDate** | DateTimeOffset | Actual completion date |
| **CreatedBy** | String | Creator username (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **ModifiedBy** | String | Last modifier username (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **Context** | PTC.DataAdmin.Container | Container context |
| **Creator** | PTC.PrincipalMgmt.User | User who created the CAPA |
| **Modifier** | PTC.PrincipalMgmt.User | User who last modified |
| **RelatedNonConformances** | Collection | Related non-conformance reports |
| **Attachments** | Collection(PTC.ContentItem) | Attached documents |

**CRUD Operations:**

```bash
# Get all CAPAs
GET /QMS/CAPAs

# Get CAPA by number
GET /QMS/CAPAs?$filter=Number eq 'CAPA-2024-001'

# Get open CAPAs
GET /QMS/CAPAs?$filter=State/Value eq 'OPEN'

# Get high priority CAPAs
GET /QMS/CAPAs?$filter=Priority/Value eq 'HIGH'

# Get CAPA with related items
GET /QMS/CAPAs('{id}')?$expand=Creator,RelatedNonConformances

# Create CAPA
POST /QMS/CAPAs
Content-Type: application/json
CSRF_NONCE: {token}

{
  "Name": "Product Quality Issue CAPA",
  "Number": "CAPA-2024-001",
  "Description": "Address product quality issue",
  "Priority": {"Value": "HIGH"},
  "RootCause": "Root cause analysis results",
  "CorrectiveAction": "Steps to correct the issue",
  "PreventiveAction": "Steps to prevent recurrence"
}
```

---

### NonConformance

A Non-Conformance Report (NCR) documents a product or process that does not meet specifications or requirements.

**Endpoint:** `/QMS/NonConformances`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Non-conformance name |
| **Number** | String | Non-conformance number |
| **Description** | String | Description of the non-conformance |
| **State** | EnumType | Lifecycle state |
| **Severity** | EnumType | Non-conformance severity |
| **Category** | EnumType | Non-conformance category |
| **QuantityAffected** | Double | Quantity of items affected |
| **DiscoveryDate** | DateTimeOffset | Date non-conformance was discovered |
| **CreatedBy** | String | Creator username (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **Context** | PTC.DataAdmin.Container | Container context |
| **Creator** | PTC.PrincipalMgmt.User | User who created |
| **Disposition** | PTC.QMS.Disposition | Disposition details |
| **RelatedCAPAs** | Collection | Related CAPAs |
| **Attachments** | Collection(PTC.ContentItem) | Attached documents |

**CRUD Operations:**

```bash
# Get all non-conformances
GET /QMS/NonConformances

# Get non-conformance by number
GET /QMS/NonConformances?$filter=Number eq 'NCR-2024-001'

# Get open non-conformances
GET /QMS/NonConformances?$filter=State/Value eq 'OPEN'

# Filter by severity
GET /QMS/NonConformances?$filter=Severity/Value eq 'MAJOR'

# Get with related CAPAs
GET /QMS/NonConformances('{id}')?$expand=RelatedCAPAs,Disposition
```

---

### QualityAction

A quality action represents a specific task or activity to address quality issues.

**Endpoint:** `/QMS/QualityActions`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Action name |
| **Number** | String | Action number |
| **Description** | String | Action description |
| **State** | EnumType | Lifecycle state |
| **ActionType** | EnumType | Type of action |
| **DueDate** | DateTimeOffset | Target completion date |
| **CompletionDate** | DateTimeOffset | Actual completion date |
| **CreatedBy** | String | Creator username (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **Context** | PTC.DataAdmin.Container | Container context |
| **Assignee** | PTC.PrincipalMgmt.User | Assigned user |
| **ParentCAPA** | PTC.QMS.CAPA | Parent CAPA |
| **Attachments** | Collection(PTC.ContentItem) | Attached documents |

---

### QualityContact

A contact person or entity related to quality management activities.

**Endpoint:** `/QMS/QualityContacts`

**Operations:** `READ`, `CREATE`, `UPDATE`, `DELETE`

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Contact name |
| **ContactType** | EnumType | Type of contact (Customer, Supplier, Internal) |
| **Email** | String | Contact email |
| **Phone** | String | Contact phone |
| **Organization** | String | Organization name |
| **CreatedBy** | String | Creator username (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **Context** | PTC.DataAdmin.Container | Container context |
| **Place** | PTC.QMS.Place | Associated location |

---

### Place

A location relevant to quality management (manufacturing site, customer location, etc.).

**Endpoint:** `/QMS/Places`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Place name |
| **PlaceType** | EnumType | Type of place |
| **Address** | String | Street address |
| **City** | String | City |
| **State** | String | State/Province |
| **Country** | String | Country |
| **PostalCode** | String | Postal/ZIP code |
| **CreatedBy** | String | Creator username (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **Context** | PTC.DataAdmin.Container | Container context |

---

### Audit

A quality audit record for tracking audit activities and findings.

**Endpoint:** `/QMS/Audits`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Audit name |
| **Number** | String | Audit number |
| **Description** | String | Audit description |
| **State** | EnumType | Lifecycle state |
| **AuditType** | EnumType | Type of audit |
| **AuditDate** | DateTimeOffset | Date of audit |
| **AuditScope** | String | Scope of the audit |
| **CreatedBy** | String | Creator username (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **Context** | PTC.DataAdmin.Container | Container context |
| **Auditor** | PTC.PrincipalMgmt.User | Auditor user |
| **Findings** | Collection(PTC.QMS.AuditFinding) | Audit findings |

---

### AuditFinding

A specific finding from a quality audit.

**Endpoint:** `/QMS/AuditFindings`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Finding name |
| **Description** | String | Finding description |
| **Severity** | EnumType | Finding severity |
| **Status** | EnumType | Finding status |
| **FindingType** | EnumType | Type of finding |
| **CreatedBy** | String | Creator username (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **Audit** | PTC.QMS.Audit | Parent audit |
| **CorrectiveActions** | Collection | Corrective actions |

---

## Common Query Examples

### Get Open CAPAs Sorted by Priority

```bash
GET /QMS/CAPAs?$filter=State/Value eq 'OPEN'&$orderby=Priority/Value desc
```

### Get Non-Conformances in Date Range

```bash
GET /QMS/NonConformances?$filter=DiscoveryDate ge 2024-01-01T00:00:00Z and DiscoveryDate le 2024-12-31T23:59:59Z
```

### Get CAPAs Due This Month

```bash
GET /QMS/CAPAs?$filter=DueDate ge 2024-01-01T00:00:00Z and DueDate le 2024-01-31T23:59:59Z and State/Value ne 'CLOSED'
```

### Get Quality Actions by Assignee

```bash
GET /QMS/QualityActions?$filter=Assignee/Name eq 'jsmith'&$expand=Assignee
```

### Get Places by Country

```bash
GET /QMS/Places?$filter=Country eq 'USA'
```

### Get Audit Findings by Severity

```bash
GET /QMS/AuditFindings?$filter=Severity/Value eq 'MAJOR'&$expand=Audit
```

---

## Lifecycle States

Common lifecycle states for QMS objects:

| State | Description |
|-------|-------------|
| **OPEN** | Created, awaiting action |
| **IN_PROGRESS** | Being actively worked on |
| **REVIEW** | Under review |
| **CLOSED** | Completed and closed |
| **CANCELLED** | Cancelled without completion |

---

## QMS Process Flow

```
Non-Conformance Report (NCR)
    └── May trigger → CAPA
                        └── Contains → QualityActions
                                        └── Assigned to → Users
                                        └── Related to → Places/Contacts
```

---

## Notes

1. **CSRF Token Required**: All write operations require the `CSRF_NONCE` header.

2. **Regulatory Compliance**: QMS objects are often subject to regulatory requirements (FDA, ISO, etc.). Ensure proper audit trail and documentation.

3. **State Transitions**: Use appropriate actions for state transitions, not direct PATCH operations.

4. **Cross-Domain References**: QMS domain references entities from:
   - PTC.DataAdmin (Container)
   - PTC.PrincipalMgmt (User)
   - PTC.CEM (Customer Experience)

---

## Schema Version

Schema Version: Various (check metadata for version details)
