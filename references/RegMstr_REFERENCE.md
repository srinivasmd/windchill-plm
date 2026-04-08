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

The Regulatory Master domain provides access to regulatory and compliance management entities in Windchill including:

### Regulatory Records
- **RegulatorySpecification** - Regulatory specifications and requirements
- **RegulatorySubmission** - Regulatory submission records
- **RegulatoryApproval** - Regulatory approvals and clearances

### Trade Compliance
- **ComplianceDefinition** - Compliance definitions
- **TradeControlClassification** - Trade control classifications
- **Country** - Country definitions and regulations

### Compliance Objects
- **ComplianceObject** - Objects subject to compliance
- **ComplianceRecord** - Compliance tracking records

---

## Entity Types

### RegulatorySpecification

Regulatory specifications defining product requirements.

**Endpoint:** `/RegMstr/RegulatorySpecifications`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Specification name |
| **Number** | String | Specification number |
| **Description** | String | Detailed description |
| **State** | EnumType | Lifecycle state (ReadOnly) |
| **LifeCycleTemplateName** | String | Lifecycle template name (ReadOnly) |
| **RegulationType** | EnumType | Type of regulation |
| **EffectiveDate** | DateTimeOffset | Date specification becomes effective |
| **ExpirationDate** | DateTimeOffset | Date specification expires |
| **Authority** | String | Regulatory authority |
| **Jurisdiction** | String | Jurisdiction (country/region) |
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
- `RelatedProducts` - Collection of Related Products
- `RegulatoryApprovals` - Collection of Regulatory Approvals
- **RegulatorySubmission** - Related Regulatory Submissions

**CRUD Operations:**

```bash
# Get all regulatory specifications
GET /RegMstr/RegulatorySpecifications

# Get specification by number
GET /RegMstr/RegulatorySpecifications?$filter=Number eq 'RS-000001'

# Filter by authority
GET /RegMstr/RegulatorySpecifications?$filter=Authority eq 'FDA'

# Filter by jurisdiction
GET /RegMstr/RegulatorySpecifications?$filter=Jurisdiction eq 'USA'

# Filter by effective date range
GET /RegMstr/RegulatorySpecifications?$filter=EffectiveDate ge 2026-01-01T00:00:00Z and EffectiveDate le 2026-12-31T23:59:59Z

# Expand with related products
GET /RegMstr/RegulatorySpecifications('{id}')?$expand=RelatedProducts

# Create regulatory specification
POST /RegMstr/RegulatorySpecifications
Content-Type: application/json
X-CSRF-Token: {token}

{
  "Name": "FDA 510(k) Specification",
  "Number": "RS-000001",
  "Description": "FDA 510(k) premarket notification requirements",
  "RegulationType": {"Value": "MEDICAL_DEVICE"},
  "Authority": "FDA",
  "Jurisdiction": "USA",
  "EffectiveDate": "2026-01-01T00:00:00Z",
  "FolderLocation": "/Default/Regulatory/Specifications"
}
```

---

### RegulatorySubmission

Regulatory submission records for product approvals.

**Endpoint:** `/RegMstr/RegulatorySubmissions`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Submission name |
| **Number** | String | Submission number |
| **Description** | String | Detailed description |
| **State** | EnumType | Lifecycle state (ReadOnly) |
| **SubmissionType** | EnumType | Type of submission |
| **SubmissionDate** | DateTimeOffset | Date of submission |
| **ExpectedApprovalDate** | DateTimeOffset | Expected approval date |
| **ActualApprovalDate** | DateTimeOffset | Actual approval date |
| **Authority** | String | Regulatory authority |
| **SubmissionStatus** | EnumType | Status of submission |
| **FolderLocation** | String | Folder path in Windchill |
| **MasterID** | String | Master ID (ReadOnly) |
| **CreatedBy** | String | Created by (ReadOnly) |
| **ModifiedBy** | String | Modified by (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- `Context` - Container (PTC.DataAdmin.Container)
- `Creator` - Creator user (PTC.PrincipalMgmt.User)
- `RegulatorySpecification` - Related Regulatory Specification
- `RegulatoryApprovals` - Collection of Regulatory Approvals
- `RelatedProducts` - Collection of Related Products

**CRUD Operations:**

```bash
# Get all regulatory submissions
GET /RegMstr/RegulatorySubmissions

# Get submission by number
GET /RegMstr/RegulatorySubmissions?$filter=Number eq 'RSUB-000001'

# Filter by status
GET /RegMstr/RegulatorySubmissions?$filter=SubmissionStatus/Value eq 'SUBMITTED'

# Filter by authority
GET /RegMstr/RegulatorySubmissions?$filter=Authority eq 'FDA'

# Filter by submission date range
GET /RegMstr/RegulatorySubmissions?$filter=SubmissionDate ge 2026-01-01T00:00:00Z

# Expand with regulatory approvals
GET /RegMstr/RegulatorySubmissions('{id}')?$expand=RegulatoryApprovals,RelatedProducts

# Create regulatory submission
POST /RegMstr/RegulatorySubmissions
Content-Type: application/json
X-CSRF-Token: {token}

{
  "Name": "510(k) Submission - Device X",
  "Number": "RSUB-000001",
  "SubmissionType": {"Value": "510K"},
  "Authority": "FDA",
  "SubmissionDate": "2026-02-08T00:00:00Z",
  "ExpectedApprovalDate": "2026-05-08T00:00:00Z",
  "FolderLocation": "/Default/Regulatory/Submissions"
}
```

---

### RegulatoryApproval

Regulatory approvals and clearances.

**Endpoint:** `/RegMstr/RegulatoryApprovals`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Approval name |
| **Number** | String | Approval number |
| **Description** | String | Detailed description |
| **State** | EnumType | Lifecycle state (ReadOnly) |
| **ApprovalType** | EnumType | Type of approval |
| **ApprovalNumber** | String | Official approval/clearance number |
| **ApprovalDate** | DateTimeOffset | Date of approval |
| **ExpirationDate** | DateTimeOffset | Expiration date |
| **Authority** | String | Regulatory authority |
| **ApprovalStatus** | EnumType | Status of approval |
| **FolderLocation** | String | Folder path in Windchill |
| **MasterID** | String | Master ID (ReadOnly) |
| **CreatedBy** | String | Created by (ReadOnly) |
| **ModifiedBy** | String | Modified by (ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- `Context` - Container (PTC.DataAdmin.Container)
- `Creator` - Creator user (PTC.PrincipalMgmt.User)
- `RegulatorySpecification` - Related Regulatory Specification
- `RegulatorySubmission` - Related Regulatory Submission
- `RelatedProducts` - Collection of Related Products

**CRUD Operations:**

```bash
# Get all regulatory approvals
GET /RegMstr/RegulatoryApprovals

# Get approval by number
GET /RegMstr/RegulatoryApprovals?$filter=Number eq 'RA-000001'

# Filter by approval number (official)
GET /RegMstr/RegulatoryApprovals?$filter=ApprovalNumber eq 'K123456'

# Filter by authority
GET /RegMstr/RegulatoryApprovals?$filter=Authority eq 'FDA'

# Filter by status
GET /RegMstr/RegulatoryApprovals?$filter=ApprovalStatus/Value eq 'APPROVED'

# Filter expiring soon
GET /RegMstr/RegulatoryApprovals?$filter=ExpirationDate le 2026-12-31T23:59:59Z and ExpirationDate ge 2026-01-01T00:00:00Z

# Expand with related products
GET /RegMstr/RegulatoryApprovals('{id}')?$expand=RelatedProducts,RegulatorySubmission

# Create regulatory approval
POST /RegMstr/RegulatoryApprovals
Content-Type: application/json
X-CSRF-Token: {token}

{
  "Name": "FDA 510(k) Clearance",
  "Number": "RA-000001",
  "ApprovalType": {"Value": "510K"},
  "ApprovalNumber": "K123456",
  "Authority": "FDA",
  "ApprovalDate": "2026-02-08T00:00:00Z",
  "ExpirationDate": "2029-02-08T00:00:00Z",
  "FolderLocation": "/Default/Regulatory/Approvals"
}
```

---

### ComplianceDefinition

Compliance definitions for regulatory requirements.

**Endpoint:** `/RegMstr/ComplianceDefinitions`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Definition name |
| **Description** | String | Detailed description |
| **ComplianceType** | EnumType | Type of compliance |
| **Regulation** | String | Applicable regulation |
| **Authority** | String | Regulatory authority |
| **EffectiveDate** | DateTimeOffset | Effective date |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- `Context` - Container (PTC.DataAdmin.Container)
- `ComplianceRecords` - Collection of Compliance Records

**CRUD Operations:**

```bash
# Get all compliance definitions
GET /RegMstr/ComplianceDefinitions

# Filter by compliance type
GET /RegMstr/ComplianceDefinitions?$filter=ComplianceType/Value eq 'EXPORT_CONTROL'

# Filter by regulation
GET /RegMstr/ComplianceDefinitions?$filter=Regulation eq 'EAR'

# Expand with compliance records
GET /RegMstr/ComplianceDefinitions('{id}')?$expand=ComplianceRecords
```

---

### TradeControlClassification

Trade control classifications for products.

**Endpoint:** `/RegMstr/TradeControlClassifications`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Classification name |
| **ClassificationCode** | String | Classification code (ECCN, etc.) |
| **Description** | String | Detailed description |
| **ControlLevel** | EnumType | Level of control |
| **ControlAgency** | String | Control agency |
| **Country** | String | Applicable country |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- `Context` - Container (PTC.DataAdmin.Container)
- `RelatedProducts` - Collection of Classified Products

**CRUD Operations:**

```bash
# Get all trade control classifications
GET /RegMstr/TradeControlClassifications

# Filter by classification code
GET /RegMstr/TradeControlClassifications?$filter=ClassificationCode eq 'EAR99'

# Filter by control level
GET /RegMstr/TradeControlClassifications?$filter=ControlLevel/Value eq 'HIGH'

# Expand with related products
GET /RegMstr/TradeControlClassifications('{id}')?$expand=RelatedProducts
```

---

### Country

Country definitions and regulatory information.

**Endpoint:** `/RegMstr/Countries`

**Operations:** `READ`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Country name |
| **ISOCode** | String | ISO country code |
| **Region** | String | Geographic region |
| **RegulatoryBody** | String | Primary regulatory body |
| **TradeAgreement** | String | Trade agreements |
| **EmbargoStatus** | EnumType | Embargo status |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- `Context` - Container (PTC.DataAdmin.Container)

**CRUD Operations:**

```bash
# Get all countries
GET /RegMstr/Countries

# Filter by ISO code
GET /RegMstr/Countries?$filter=ISOCode eq 'US'

# Filter by region
GET /RegMstr/Countries?$filter=Region eq 'EUROPE'

# Filter by embargo status
GET /RegMstr/Countries?$filter=EmbargoStatus/Value eq 'EMBARGOED'
```

---

## Common Query Examples

### Filter by Multiple Criteria

```bash
# Get FDA submissions pending approval
GET /RegMstr/RegulatorySubmissions?$filter=Authority eq 'FDA' and SubmissionStatus/Value eq 'SUBMITTED'

# Get approved regulations by jurisdiction
GET /RegMstr/RegulatoryApprovals?$filter=Authority eq 'FDA' and ApprovalStatus/Value eq 'APPROVED'

# Get expiring approvals
GET /RegMstr/RegulatoryApprovals?$filter=ExpirationDate le 2026-06-30T23:59:59Z and ApprovalStatus/Value eq 'APPROVED'

# Get specifications by type and authority
GET /RegMstr/RegulatorySpecifications?$filter=RegulationType/Value eq 'MEDICAL_DEVICE' and Authority eq 'FDA'
```

### Complex Queries with Expansion

```bash
# Get specification with approvals and products
GET /RegMstr/RegulatorySpecifications?$expand=RegulatoryApprovals,RelatedProducts

# Get submission with full context
GET /RegMstr/RegulatorySubmissions?$expand=RegulatorySpecification,RegulatoryApprovals,RelatedProducts,Creator

# Get approval with submission and specification
GET /RegMstr/RegulatoryApprovals?$expand=RegulatorySubmission($expand=RegulatorySpecification),RelatedProducts
```

### Sorting and Pagination

```bash
# Get latest submissions
GET /RegMstr/RegulatorySubmissions?$orderby=SubmissionDate desc&$top=50

# Get approvals sorted by expiration
GET /RegMstr/RegulatoryApprovals?$orderby=ExpirationDate asc

# Paginated results
GET /RegMstr/RegulatorySpecifications?$skip=0&$top=25
```

---

## Integration Notes

1. **Cross-Domain References**:
   - RegulatoryApprovals link to Products (ProdMgmt)
   - TradeControlClassifications link to Products
   - Countries are referenced by Places (QMS)

2. **Workflow Integration**:
   - Regulatory objects use Windchill Workflow engine
   - Check Workflow domain for work items

3. **Product Management Integration**:
   - Products can have regulatory specifications
   - Products have trade control classifications

4. **Lifecycle Management**:
   - Regulatory objects follow lifecycle templates
   - Track approval and expiration dates

---

## Schema Version

Schema Version: 6
