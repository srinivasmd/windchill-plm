---
Domain: RegMstr
Client: `from domains.RegMstr import RegMstrClient`
---

> **Use the RegMstrClient**: `from domains.RegMstr import RegMstrClient`
>
> This reference documents the entity types and properties. For programmatic access, use the domain client.

# Regulatory Master (RegMstr) Domain Reference

Complete reference documentation for the Windchill Regulatory Master OData domain.

## Base URL

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/RegMstr/
```

## Metadata URL

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/RegMstr/$metadata
```

## Domain Overview

The Regulatory Master domain provides access to Windchill's regulatory compliance and registration management:
- **RegulatorySpecification** - Regulatory specifications and requirements
- **RegulatoryRegistration** - Product registrations with regulatory bodies
- **RegulatorySubmission** - Submissions to regulatory authorities
- **RegulatoryRequirement** - Individual regulatory requirements

---

## Entity Types

### RegulatorySpecification

A Regulatory Specification defines the regulatory requirements and specifications for products.

**Endpoint:** `/RegMstr/RegulatorySpecifications`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Specification name |
| **Number** | String | Specification number (unique) |
| **Description** | String | Description of the specification |
| **State** | EnumType | Lifecycle state |
| **SpecificationType** | EnumType | Type of specification |
| **EffectiveDate** | DateTimeOffset | Date when specification becomes effective |
| **ExpirationDate** | DateTimeOffset | Date when specification expires |
| **CreatedBy** | String | Creator username (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **ModifiedBy** | String | Last modifier username (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **Context** | PTC.DataAdmin.Container | Container context |
| **RegulatoryRequirements** | Collection | Associated requirements |
| **Registrations** | Collection | Related registrations |
| **Attachments** | Collection(PTC.ContentItem) | Attached documents |

**CRUD Operations:**

```bash
# Get all regulatory specifications
GET /RegMstr/RegulatorySpecifications

# Get specification by number
GET /RegMstr/RegulatorySpecifications?$filter=Number eq 'RS-2024-001'

# Get active specifications
GET /RegMstr/RegulatorySpecifications?$filter=State/Value eq 'RELEASED'

# Get specifications effective in date range
GET /RegMstr/RegulatorySpecifications?$filter=EffectiveDate ge 2024-01-01T00:00:00Z and EffectiveDate le 2024-12-31T23:59:59Z

# Get specification with requirements
GET /RegMstr/RegulatorySpecifications('{id}')?$expand=RegulatoryRequirements

# Create regulatory specification
POST /RegMstr/RegulatorySpecifications
Content-Type: application/json
CSRF_NONCE: {token}

{
  "Name": "Medical Device Regulatory Specification",
  "Number": "RS-2024-001",
  "Description": "Regulatory requirements for medical device",
  "SpecificationType": {"Value": "DEVICE"},
  "EffectiveDate": "2024-01-01T00:00:00Z"
}
```

---

### RegulatoryRegistration

A Regulatory Registration tracks product registrations with regulatory authorities (FDA, CE Mark, etc.).

**Endpoint:** `/RegMstr/RegulatoryRegistrations`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Registration name |
| **Number** | String | Registration number |
| **Description** | String | Registration description |
| **State** | EnumType | Lifecycle state |
| **RegistrationType** | EnumType | Type of registration |
| **RegulatoryAuthority** | String | Regulatory authority (FDA, CE, etc.) |
| **RegistrationNumber** | String | Official registration number |
| **SubmissionDate** | DateTimeOffset | Date of submission |
| **ApprovalDate** | DateTimeOffset | Date of approval |
| **ExpirationDate** | DateTimeOffset | Registration expiration date |
| **Status** | EnumType | Registration status |
| **CreatedBy** | String | Creator username (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **ModifiedBy** | String | Last modifier username (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **Context** | PTC.DataAdmin.Container | Container context |
| **RegulatorySpecifications** | Collection | Associated specifications |
| **Submissions** | Collection | Related submissions |
| **Products** | Collection | Registered products |
| **Attachments** | Collection(PTC.ContentItem) | Attached documents |

**CRUD Operations:**

```bash
# Get all registrations
GET /RegMstr/RegulatoryRegistrations

# Get registration by number
GET /RegMstr/RegulatoryRegistrations?$filter=Number eq 'REG-001'

# Filter by regulatory authority
GET /RegMstr/RegulatoryRegistrations?$filter=RegulatoryAuthority eq 'FDA'

# Get active registrations
GET /RegMstr/RegulatoryRegistrations?$filter=Status/Value eq 'APPROVED'

# Get expiring registrations
GET /RegMstr/RegulatoryRegistrations?$filter=ExpirationDate le 2024-12-31T23:59:59Z and Status/Value eq 'APPROVED'

# Get registration with specifications
GET /RegMstr/RegulatoryRegistrations('{id}')?$expand=RegulatorySpecifications,Products

# Create registration
POST /RegMstr/RegulatoryRegistrations
Content-Type: application/json
CSRF_NONCE: {token}

{
  "Name": "FDA 510(k) Registration",
  "Number": "REG-2024-001",
  "RegulatoryAuthority": "FDA",
  "RegistrationNumber": "K123456",
  "RegistrationType": {"Value": "510K"},
  "SubmissionDate": "2024-01-15T00:00:00Z"
}
```

---

### RegulatorySubmission

A Regulatory Submission tracks submissions made to regulatory authorities.

**Endpoint:** `/RegMstr/RegulatorySubmissions`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Submission name |
| **Number** | String | Submission number |
| **Description** | String | Submission description |
| **State** | EnumType | Lifecycle state |
| **SubmissionType** | EnumType | Type of submission |
| **SubmissionDate** | DateTimeOffset | Date of submission |
| **ResponseDate** | DateTimeOffset | Date of response from authority |
| **Status** | EnumType | Submission status |
| **CreatedBy** | String | Creator username (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **Context** | PTC.DataAdmin.Container | Container context |
| **Registration** | PTC.RegMstr.RegulatoryRegistration | Parent registration |
| **Documents** | Collection | Submitted documents |
| **Attachments** | Collection(PTC.ContentItem) | Attached documents |

**CRUD Operations:**

```bash
# Get all submissions
GET /RegMstr/RegulatorySubmissions

# Get submissions for a registration
GET /RegMstr/RegulatorySubmissions?$filter=Registration/Number eq 'REG-001'

# Get pending submissions
GET /RegMstr/RegulatorySubmissions?$filter=Status/Value eq 'PENDING'

# Get submission with documents
GET /RegMstr/RegulatorySubmissions('{id}')?$expand=Documents,Registration
```

---

### RegulatoryRequirement

An individual regulatory requirement from a specification.

**Endpoint:** `/RegMstr/RegulatoryRequirements`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Key Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Name** | String | Requirement name |
| **Number** | String | Requirement number |
| **Description** | String | Requirement description |
| **State** | EnumType | Lifecycle state |
| **RequirementType** | EnumType | Type of requirement |
| **Severity** | EnumType | Requirement severity |
| **ComplianceStatus** | EnumType | Current compliance status |
| **CreatedBy** | String | Creator username (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **Context** | PTC.DataAdmin.Container | Container context |
| **RegulatorySpecification** | PTC.RegMstr.RegulatorySpecification | Parent specification |
| **Attachments** | Collection(PTC.ContentItem) | Attached documents |

**CRUD Operations:**

```bash
# Get all requirements
GET /RegMstr/RegulatoryRequirements

# Get requirements for a specification
GET /RegMstr/RegulatoryRequirements?$filter=RegulatorySpecification/Number eq 'RS-001'

# Filter by compliance status
GET /RegMstr/RegulatoryRequirements?$filter=ComplianceStatus/Value eq 'COMPLIANT'

# Get requirements by severity
GET /RegMstr/RegulatoryRequirements?$filter=Severity/Value eq 'CRITICAL'

# Get requirement with specification
GET /RegMstr/RegulatoryRequirements('{id}')?$expand=RegulatorySpecification
```

---

## Common Query Examples

### Get Active Registrations by Authority

```bash
GET /RegMstr/RegulatoryRegistrations?$filter=RegulatoryAuthority eq 'FDA' and Status/Value eq 'APPROVED'
```

### Get Registrations Expiring in Next 90 Days

```bash
GET /RegMstr/RegulatoryRegistrations?$filter=ExpirationDate ge 2024-01-01T00:00:00Z and ExpirationDate le 2024-03-31T23:59:59Z and Status/Value eq 'APPROVED'
```

### Get Non-Compliant Requirements

```bash
GET /RegMstr/RegulatoryRequirements?$filter=ComplianceStatus/Value eq 'NON_COMPLIANT'
```

### Get Pending Submissions

```bash
GET /RegMstr/RegulatorySubmissions?$filter=Status/Value eq 'PENDING'&$expand=Registration
```

### Get Complete Registration with All Related Data

```bash
GET /RegMstr/RegulatoryRegistrations('{id}')?$expand=RegulatorySpecifications($expand=RegulatoryRequirements),Submissions
```

---

## Regulatory Authorities

Common regulatory authorities supported:

| Authority | Description |
|-----------|-------------|
| **FDA** | U.S. Food and Drug Administration |
| **CE** | European CE Marking |
| **MHLW** | Japanese Ministry of Health, Labour and Welfare |
| **TGA** | Australian Therapeutic Goods Administration |
| **Health Canada** | Canadian health regulatory authority |
| **NMPA** | China National Medical Products Administration |
| **ANVISA** | Brazilian Health Regulatory Agency |

---

## Registration Types

Common registration types:

| Type | Description |
|------|-------------|
| **510K** | FDA 510(k) premarket notification |
| **PMA** | FDA Premarket Approval |
| **CE_MARK** | European CE Marking certification |
| **NDA** | New Drug Application |
| **IDE** | Investigational Device Exemption |
| **PMN** | Premarket Notification |

---

## Lifecycle States

Common lifecycle states for Regulatory objects:

| State | Description |
|-------|-------------|
| **DRAFT** | Initial creation, not yet submitted |
| **IN_REVIEW** | Under internal review |
| **SUBMITTED** | Submitted to regulatory authority |
| **APPROVED** | Approved by authority |
| **REJECTED** | Rejected by authority |
| **WITHDRAWN** | Withdrawn from consideration |
| **EXPIRED** | Registration has expired |

---

## Regulatory Process Flow

```
RegulatorySpecification
    └── Contains → RegulatoryRequirements
    └── Links to → RegulatoryRegistration
                    └── Has → RegulatorySubmissions
                              └── Contains → Documents
```

---

## Notes

1. **CSRF Token Required**: All write operations require the `CSRF_NONCE` header.

2. **Regulatory Compliance**: These objects are subject to regulatory requirements. Ensure proper audit trail and versioning.

3. **State Transitions**: Use appropriate actions for state transitions to maintain compliance audit trail.

4. **Cross-Domain References**: RegMstr domain references entities from:
   - PTC.DataAdmin (Container)
   - PTC.ProdMgmt (Parts)
   - PTC.DocMgmt (Documents)

5. **Document Management**: Regulatory documents often require specific retention and versioning requirements.

---

## Schema Version

Schema Version: Various (check metadata for version details)