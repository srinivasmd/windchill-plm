# Regulation Master (RegMstr) Domain Reference

Complete reference documentation for the Windchill Regulation Master OData domain.

## Base URL

```
https://windchill.example.com/Windchill/servlet/odata/RegMstr/
```

## Metadata URL

```
https://windchill.example.com/Windchill/servlet/odata/RegMstr/$metadata
```

## Domain Overview

The Regulation Master (RegMstr) domain provides access to Windchill's regulatory compliance and regulation management entities:

### Regulation Objects
- **Regulations** - Regulatory requirements and standards
- **RegulatoryRequirements** - Individual requirements within regulations
- **ComplianceRecords** - Compliance tracking records

### Standards and Specifications
- **Standards** - Industry standards (ISO, ASTM, etc.)
- **Specifications** - Technical specifications

### Compliance Tracking
- **ComplianceItems** - Items subject to compliance
- **ComplianceEvidence** - Evidence of compliance

---

## Entity Types

### Regulation

Regulation entity representing regulatory requirements and standards.

**Endpoint:** `/RegMstr/Regulations`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Regulation name |
| **Number** | String | Regulation number/identifier |
| **Description** | String | Regulation description |
| **State** | EnumType | Lifecycle state |
| **LifeCycleTemplateName** | String | Lifecycle template name (ReadOnly) |
| **RegulatoryAgency** | String | Issuing regulatory agency (e.g., FDA, EMA, ISO) |
| **RegulationType** | String | Type of regulation (e.g., Medical Device, Automotive) |
| **EffectiveDate** | DateTimeOffset | Date regulation takes effect |
| **ExpirationDate** | DateTimeOffset | Date regulation expires (if applicable) |
| **Version** | String | Regulation version |
| **Status** | String | Current status (Active, Draft, Obsolete) |
| **Jurisdiction** | String | Geographic jurisdiction (e.g., US, EU, Global) |
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
- `RegulatoryRequirements` → Collection(PTC.RegMstr.RegulatoryRequirement) (Child requirements)

**CRUD Operations:**

```bash
# Get all regulations
GET /RegMstr/Regulations

# Get regulation by ID
GET /RegMstr/Regulations('{id}')

# Get regulation by number
GET /RegMstr/Regulations?$filter=Number eq 'FDA-21CFR820'

# Filter by agency
GET /RegMstr/Regulations?$filter=RegulatoryAgency eq 'FDA'

# Filter by jurisdiction
GET /RegMstr/Regulations?$filter=Jurisdiction eq 'EU'

# Get active regulations
GET /RegMstr/Regulations?$filter=Status eq 'Active'

# Get with requirements
GET /RegMstr/Regulations('{id}')?$expand=RegulatoryRequirements

# Select specific properties
GET /RegMstr/Regulations?$select=ID,Name,Number,RegulatoryAgency,Status

# Order by effective date
GET /RegMstr/Regulations?$orderby=EffectiveDate desc

# Top results
GET /RegMstr/Regulations?$top=50
```

---

### RegulatoryRequirement

Individual requirement within a regulation.

**Endpoint:** `/RegMstr/RegulatoryRequirements`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Requirement name |
| **Number** | String | Requirement number/identifier |
| **Description** | String | Requirement description |
| **State** | EnumType | Lifecycle state |
| **LifeCycleTemplateName** | String | Lifecycle template name (ReadOnly) |
| **RequirementText** | String | Full text of the requirement |
| **Section** | String | Section reference |
| **Paragraph** | String | Paragraph reference |
| **RequirementType** | String | Type of requirement |
| **Priority** | String | Priority level |
| **ComplianceLevel** | String | Required compliance level (Mandatory, Recommended) |
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
- `Regulation` → PTC.RegMstr.Regulation (Parent regulation)
- `ComplianceRecords` → Collection(PTC.RegMstr.ComplianceRecord) (Compliance tracking)

**CRUD Operations:**

```bash
# Get all requirements
GET /RegMstr/RegulatoryRequirements

# Get requirement by ID
GET /RegMstr/RegulatoryRequirements('{id}')

# Get requirements for a regulation
GET /RegMstr/RegulatoryRequirements?$filter=Regulation/Number eq 'FDA-21CFR820'

# Filter by section
GET /RegMstr/RegulatoryRequirements?$filter=Section eq '820.30'

# Get with regulation
GET /RegMstr/RegulatoryRequirements('{id}')?$expand=Regulation

# Get with compliance records
GET /RegMstr/RegulatoryRequirements?$expand=ComplianceRecords
```

---

### ComplianceRecord

Record tracking compliance status for requirements.

**Endpoint:** `/RegMstr/ComplianceRecords`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Compliance record name |
| **Number** | String | Compliance record number |
| **Description** | String | Description |
| **State** | EnumType | Lifecycle state |
| **LifeCycleTemplateName** | String | Lifecycle template name (ReadOnly) |
| **ComplianceStatus** | String | Compliance status (Compliant, Non-Compliant, Partial, Pending) |
| **VerificationMethod** | String | Method used for verification |
| **VerificationDate** | DateTimeOffset | Date of verification |
| **VerifiedBy** | String | User who verified |
| **ExpirationDate** | DateTimeOffset | Expiration date for compliance |
| **ReviewDate** | DateTimeOffset | Scheduled review date |
| **Notes** | String | Additional notes |
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
- `RegulatoryRequirement` → PTC.RegMstr.RegulatoryRequirement (Related requirement)
- `ComplianceEvidence` → Collection(PTC.RegMstr.ComplianceEvidence) (Evidence documents)

**CRUD Operations:**

```bash
# Get all compliance records
GET /RegMstr/ComplianceRecords

# Get compliance record by ID
GET /RegMstr/ComplianceRecords('{id}')

# Filter by status
GET /RegMstr/ComplianceRecords?$filter=ComplianceStatus eq 'Compliant'

# Get non-compliant records
GET /RegMstr/ComplianceRecords?$filter=ComplianceStatus eq 'Non-Compliant'

# Get pending review
GET /RegMstr/ComplianceRecords?$filter=ReviewDate le 2026-02-01T00:00:00Z

# Get with requirement
GET /RegMstr/ComplianceRecords('{id}')?$expand=RegulatoryRequirement

# Get with evidence
GET /RegMstr/ComplianceRecords?$expand=ComplianceEvidence
```

---

### Standard

Industry standard (ISO, ASTM, IEC, etc.).

**Endpoint:** `/RegMstr/Standards`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Standard name |
| **Number** | String | Standard number (e.g., ISO 13485) |
| **Description** | String | Standard description |
| **State** | EnumType | Lifecycle state |
| **StandardType** | String | Type of standard |
| **IssuingBody** | String | Issuing organization (ISO, ASTM, IEC) |
| **Version** | String | Standard version |
| **EffectiveDate** | DateTimeOffset | Effective date |
| **Status** | String | Current status |
| **CreatedBy** | String | User who created (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` → PTC.DataAdmin.Container (Container context)

**CRUD Operations:**

```bash
# Get all standards
GET /RegMstr/Standards

# Get standard by number
GET /RegMstr/Standards?$filter=Number eq 'ISO 13485'

# Filter by issuing body
GET /RegMstr/Standards?$filter=IssuingBody eq 'ISO'

# Get active standards
GET /RegMstr/Standards?$filter=Status eq 'Active'
```

---

### Specification

Technical specification document.

**Endpoint:** `/RegMstr/Specifications`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Specification name |
| **Number** | String | Specification number |
| **Description** | String | Specification description |
| **State** | EnumType | Lifecycle state |
| **SpecificationType** | String | Type of specification |
| **Version** | String | Version |
| **EffectiveDate** | DateTimeOffset | Effective date |
| **CreatedBy** | String | User who created (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` → PTC.DataAdmin.Container (Container context)

---

### ComplianceItem

Item subject to compliance requirements.

**Endpoint:** `/RegMstr/ComplianceItems`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Item name |
| **Number** | String | Item number |
| **Description** | String | Item description |
| **ItemType** | String | Type of item |
| **ComplianceStatus** | String | Overall compliance status |
| **CreatedBy** | String | User who created (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` → PTC.DataAdmin.Container (Container context)
- `ComplianceRecords` → Collection(PTC.RegMstr.ComplianceRecord) (Related records)

---

### ComplianceEvidence

Evidence document proving compliance.

**Endpoint:** `/RegMstr/ComplianceEvidences`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Evidence name |
| **Number** | String | Evidence number |
| **Description** | String | Evidence description |
| **EvidenceType** | String | Type of evidence (Test Report, Certificate, Document) |
| **DocumentReference** | String | Reference to supporting document |
| **IssueDate** | DateTimeOffset | Date evidence was issued |
| **ExpirationDate** | DateTimeOffset | Expiration date |
| **CreatedBy** | String | User who created (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly) |

**Navigation Properties:**
- `Context` → PTC.DataAdmin.Container (Container context)
- `ComplianceRecord` → PTC.RegMstr.ComplianceRecord (Related record)

---

## Common Query Examples

### Get Active FDA Regulations

```bash
GET /RegMstr/Regulations?$filter=RegulatoryAgency eq 'FDA' and Status eq 'Active'&$expand=RegulatoryRequirements
```

### Get Requirements for EU MDR

```bash
GET /RegMstr/Regulations?$filter=contains(Name, 'MDR') and Jurisdiction eq 'EU'&$expand=RegulatoryRequirements
```

### Get Non-Compliant Records

```bash
GET /RegMstr/ComplianceRecords?$filter=ComplianceStatus eq 'Non-Compliant'&$expand=RegulatoryRequirement,ComplianceEvidence
```

### Get Compliance Records Due for Review

```bash
GET /RegMstr/ComplianceRecords?$filter=ReviewDate le 2026-02-01T00:00:00Z&$expand=RegulatoryRequirement($expand=Regulation)
```

### Get ISO Standards

```bash
GET /RegMstr/Standards?$filter=IssuingBody eq 'ISO' and Status eq 'Active'
```

### Get Full Regulation Structure

```bash
GET /RegMstr/Regulations('{id}')?$expand=
  RegulatoryRequirements($expand=
    ComplianceRecords($expand=
      ComplianceEvidence
    )
  ),
  Context,
  Creator
```

---

## Entity Relationships

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PTC.RegMstr Namespace                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐   RegulatoryRequirements   ┌──────────────────┐       │
│  │    Regulation    │────────────────────────────►│ Regulatory       │       │
│  ├──────────────────┤                             │ Requirement      │       │
│  │ - RegulatoryReqs │                             ├──────────────────┤       │
│  │ - Context        │                             │ - Regulation     │       │
│  │ - Creator        │                             │ - ComplianceRecs │       │
│  └──────────────────┘                             │ - Context        │       │
│                                                   └────────┬─────────┘       │
│                                                            │                  │
│                                                            │ ComplianceRecs   │
│                                                            ▼                  │
│                                                   ┌──────────────────┐       │
│                                                   │ ComplianceRecord │       │
│                                                   ├──────────────────┤       │
│                                                   │ - RegulatoryReq  │       │
│                                                   │ - ComplianceEv   │       │
│                                                   │ - Context        │       │
│                                                   └────────┬─────────┘       │
│                                                            │                  │
│                                                            │ Evidence         │
│                                                            ▼                  │
│                                                   ┌──────────────────┐       │
│                                                   │ Compliance       │       │
│                                                   │ Evidence         │       │
│                                                   ├──────────────────┤       │
│                                                   │ - ComplianceRec  │       │
│                                                   │ - Context        │       │
│                                                   └──────────────────┘       │
│                                                                             │
│  ┌──────────────────┐                  ┌──────────────────┐                 │
│  │     Standard     │                  │  Specification   │                 │
│  ├──────────────────┤                  ├──────────────────┤                 │
│  │ - Context        │                  │ - Context        │                 │
│  └──────────────────┘                  └──────────────────┘                 │
│                                                                             │
│  ┌──────────────────┐      ComplianceRecords   ┌──────────────────┐        │
│  │ ComplianceItem   │─────────────────────────►│ ComplianceRecord │        │
│  ├──────────────────┤                          ├──────────────────┤        │
│  │ - ComplianceRecs │                          │ - Context        │        │
│  │ - Context        │                          └──────────────────┘        │
│  └──────────────────┘                                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Cross-Domain References

| From Entity | Navigation Property | Target Domain | Target Entity |
|-------------|---------------------|---------------|---------------|
| Regulation | Context | DataAdmin | Container |
| Regulation | Creator | PrincipalMgmt | User |
| Regulation | Modifier | PrincipalMgmt | User |
| RegulatoryRequirement | Context | DataAdmin | Container |
| RegulatoryRequirement | Creator | PrincipalMgmt | User |
| ComplianceRecord | Context | DataAdmin | Container |
| ComplianceRecord | Creator | PrincipalMgmt | User |
| Standard | Context | DataAdmin | Container |
| Specification | Context | DataAdmin | Container |
| ComplianceItem | Context | DataAdmin | Container |
| ComplianceEvidence | Context | DataAdmin | Container |

---

## Compliance Status Values

### ComplianceRecord.Status Values
- **Compliant** - Meets all requirements
- **Non-Compliant** - Does not meet requirements
- **Partial** - Partially meets requirements
- **Pending** - Under review
- **Not_Applicable** - Not applicable to this item

### Regulation.Status Values
- **Active** - Currently in effect
- **Draft** - Under development
- **Proposed** - Proposed but not yet effective
- **Obsolete** - No longer in effect
- **Withdrawn** - Withdrawn by issuing agency

---

## Pagination

Use `$top` and `$skip` for pagination:

```bash
GET /RegMstr/Regulations?$top=50&$skip=0
GET /RegMstr/Regulations?$top=50&$skip=50
```

---

## Notes

1. **READ-ONLY Access** - Regulation objects are typically read through OData. Regulation management is done through Windchill UI.

2. **Hierarchy Structure** - Regulations contain RegulatoryRequirements, which are linked to ComplianceRecords.

3. **Evidence Tracking** - ComplianceEvidence documents provide proof of compliance for ComplianceRecords.

4. **Standards Integration** - Standards (ISO, ASTM) are separate entities that may be referenced by regulations.

5. **Jurisdiction Support** - Regulations can be filtered by jurisdiction (US, EU, Global, etc.) for regulatory compliance management.

6. **Review Scheduling** - ComplianceRecords have ReviewDate for scheduling periodic compliance reviews.

7. **Object Identifiers** - IDs are OIDs in format `OR:wt.regulation.Regulation:xxxxx`.
