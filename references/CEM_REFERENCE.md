# Customer Experience Management (CEM) Domain Reference

Complete reference documentation for the Windchill Customer Experience Management OData domain.

## Base URL

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/CEM/
```

## Metadata URL

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/CEM/$metadata
```

## Domain Overview

The Customer Experience Management (CEM) domain provides access to customer experience records and related products in Windchill including:

### Customer Experience Management
- **CustomerExperience** - Customer experience records

### Related Products
- **RelatedProduct** - Products related to customer experiences

### Actions
- **SetStateCustomerExperiences** - Set state for multiple customer experiences
- **SetState** - Set state for a single customer experience
- **EditCustomerExperiencesSecurityLabels** - Edit security labels for customer experiences

### Functions
- **GetLifeCycleTemplate** - Get lifecycle template for a customer experience
- **GetValidStateTransitions** - Get valid state transitions for a customer experience

---

## Entity Types

### CustomerExperience

Customer experience records representing customer feedback, complaints, or interactions.

**Endpoint:** `/CEM/CustomerExperiences`

**Operations:** `READ`, `CREATE`, `UPDATE`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **Name** | String | Customer experience name |
| **Number** | String | Customer experience number |
| **Summary** | String | Summary of the experience |
| **AdditionalInformation** | String | Additional information |
| **Date** | DateTimeOffset | Date of the event |
| **DateApproximate** | Boolean | Is date approximate |
| **Circumstance** | EnumType | Circumstance of the event |
| **CountryOfEvent** | EnumType | Country where the event occurred |
| **CountryOfOrigin** | EnumType | Country of origin |
| **EventLocation** | EnumType | Event location |
| **HowReported** | EnumType | How the experience was reported |
| **PrimaryCode** | String | Primary code |
| **PrimaryCodePath** | String | Primary code path (ReadOnly) |
| **State** | EnumType | Lifecycle state (ReadOnly) |
| **LifeCycleTemplateName** | String | Lifecycle template name (ReadOnly, NonFilterable, NonSortable) |
| **MasterID** | String | Master ID (ReadOnly) |
| **CreatedBy** | String | Created by (ReadOnly) |
| **ModifiedBy** | String | Modified by (ReadOnly) |
| **TypeIcon** | Icon | Type icon (ReadOnly, NonFilterable, NonSortable) |
| **ObjectType** | String | Object type (ReadOnly, NonFilterable, NonSortable) |

**Navigation Properties:**
- `Context` - Container (PTC.DataAdmin.Container)
- `Creator` - Creator user (PTC.PrincipalMgmt.User)
- `Modifier` - Modifier user (PTC.PrincipalMgmt.User)
- `EntryLocation` - Entry location (PTC.QMS.Place)
- `PrimaryRelatedPersonOrLocation` - Primary related person/location (PTC.QMS.QualityContact)
- `AdditionalRelatedPersonnelOrLocations` - Additional related personnel/locations (Collection of PTC.QMS.QualityContact)
- `PrimaryRelatedProduct` - Primary related product (PTC.CEM.RelatedProduct)
- `AdditionalRelatedProducts` - Additional related products (Collection of PTC.CEM.RelatedProduct)

**CRUD Operations:**

```bash
# Get all customer experiences
GET /CEM/CustomerExperiences

# Get customer experience by ID
GET /CEM/CustomerExperiences('{id}')

# Get customer experience by number
GET /CEM/CustomerExperiences?$filter=Number eq 'CE-000001'

# Get customer experience by name
GET /CEM/CustomerExperiences?$filter=Name eq 'Customer Feedback'

# Search by number or name
GET /CEM/CustomerExperiences?$filter=contains(Number, 'CE') or contains(Name, 'Feedback')

# Filter by state
GET /CEM/CustomerExperiences?$filter=State/Value eq 'OPEN'

# Filter by date
GET /CEM/CustomerExperiences?$filter=Date ge 2026-01-01T00:00:00Z

# Expand with context
GET /CEM/CustomerExperiences('{id}')?$expand=Context

# Expand with creator
GET /CEM/CustomerExperiences('{id}')?$expand=Creator

# Expand with entry location
GET /CEM/CustomerExperiences('{id}')?$expand=EntryLocation

# Expand with primary related person/location
GET /CEM/CustomerExperiences('{id}')?$expand=PrimaryRelatedPersonOrLocation

# Expand with primary related product
GET /CEM/CustomerExperiences('{id}')?$expand=PrimaryRelatedProduct

# Expand with additional related products
GET /CEM/CustomerExperiences('{id}')?$expand=AdditionalRelatedProducts

# Expand with all navigation properties
GET /CEM/CustomerExperiences('{id}')?$expand=Context,Creator,Modifier,EntryLocation,PrimaryRelatedPersonOrLocation,PrimaryRelatedProduct,AdditionalRelatedProducts,AdditionalRelatedPersonnelOrLocations

# Select specific properties
GET /CEM/CustomerExperiences?$select=ID,Name,Number,Summary,State,Date

# Top results
GET /CEM/CustomerExperiences?$top=100

# Order by
GET /CEM/CustomerExperiences?$orderby=Date desc
GET /CEM/CustomerExperiences?$orderby=Name asc

# Create customer experience
POST /CEM/CustomerExperiences
Content-Type: application/json
X-CSRF-Token: {token}

{
  "Name": "Customer Complaint - Product Failure",
  "Number": "CE-000001",
  "Summary": "Customer reported product failure within warranty period",
  "AdditionalInformation": "Product serial number: XYZ-12345",
  "Date": "2026-02-08T10:00:00Z",
  "DateApproximate": false,
  "Circumstance": {"Value": "PRODUCT_FAILURE"},
  "CountryOfEvent": {"Value": "USA"},
  "EventLocation": {"Value": "CUSTOMER_SITE"},
  "HowReported": {"Value": "EMAIL"}
}

# Note: When creating a CustomerExperience, a PrimaryRelatedPersonOrLocation must be provided
# This is typically done through the nested object structure or via separate operations

# Update customer experience
PATCH /CEM/CustomerExperiences('{id}')
Content-Type: application/json
X-CSRF-Token: {token}

{
  "Summary": "Updated summary",
  "AdditionalInformation": "Additional details added"
}

# Note: DELETE operation is not supported for CustomerExperience
```

---

### RelatedProduct

Products related to customer experiences (e.g., products mentioned in complaints, returns, etc.).

**Endpoint:** Navigation property from `CustomerExperience`

**Operations:** `READ`, `CREATE`, `UPDATE`, `DELETE`

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (ReadOnly) |
| **ReportedName** | String | Reported product name |
| **ReportedNumber** | String | Reported product number |
| **Quantity** | Double | Quantity (Required) |
| **UnitOfMeasure** | EnumType | Unit of measure (Required) |
| **SerialLotNumber** | String | Serial or lot number |
| **OtherLotBatchNumber** | String | Other lot/batch number |
| **UniqueIdentifier** | String | Unique identifier |
| **WarrantyType** | EnumType | Warranty type |
| **ExpectedReturn** | Boolean | Is return expected |
| **DateReturnExpected** | DateTimeOffset | Expected return date |
| **ReturnAuthorizationNumber** | String | Return authorization number |
| **LetterRequested** | Boolean | Is letter requested |
| **ActualOrSample** | EnumType | Actual or sample |
| **Primary** | Boolean | Is primary related product |
| **CreatedOn** | DateTimeOffset | Created timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modified timestamp (ReadOnly) |
| **ObjectType** | String | Object type (ReadOnly, NonFilterable, NonSortable) |

**Navigation Properties:**
- `Subject` - Subject (PTC.QMS.Subject) - The actual product reference if available
- `ManufacturingLocation` - Manufacturing location (PTC.QMS.Place)

**CRUD Operations:**

```bash
# Get related products for a customer experience
GET /CEM/CustomerExperiences('{id}')/PrimaryRelatedProduct
GET /CEM/CustomerExperiences('{id}')/AdditionalRelatedProducts

# Get related products with expansion
GET /CEM/CustomerExperiences('{id}')/AdditionalRelatedProducts?$expand=Subject,ManufacturingLocation

# Create related product (via customer experience update)
POST /CEM/CustomerExperiences('{id}')/AdditionalRelatedProducts
Content-Type: application/json
X-CSRF-Token: {token}

{
  "ReportedName": "Widget Assembly",
  "ReportedNumber": "WA-12345",
  "Quantity": 10.0,
  "UnitOfMeasure": {"Value": "EACH"},
  "SerialLotNumber": "SN-12345",
  "Primary": false,
  "WarrantyType": {"Value": "STANDARD"}
}

# Note: ReportNumber and ReportedName are required when a Subject reference is not provided

# Update related product
PATCH /CEM/CustomerExperiences('{id}')/AdditionalRelatedProducts('{related_product_id}')
Content-Type: application/json
X-CSRF-Token: {token}

{
  "Quantity": 5.0,
  "ExpectedReturn": true,
  "DateReturnExpected": "2026-03-01T00:00:00Z"
}

# Delete related product
DELETE /CEM/CustomerExperiences('{id}')/AdditionalRelatedProducts('{related_product_id}')
X-CSRF-Token: {token}
```

---

## Actions

### SetStateCustomerExperiences

Set the lifecycle state for multiple customer experiences.

**Action Signature:**
```
SetStateCustomerExperiences(CustomerExperiences, State) -> Collection(CustomerExperience)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| **CustomerExperiences** | Collection(CustomerExperience) | Collection of customer experiences |
| **State** | EnumType | Target state |

**Usage Example:**

```bash
POST /CEM/SetStateCustomerExperiences
Content-Type: application/json
X-CSRF-Token: {token}

{
  "CustomerExperiences": [
    {"ID": "OR:wt.csm.CSMCustomerExperience:12345"},
    {"ID": "OR:wt.csm.CSMCustomerExperience:12346"}
  ],
  "State": {"Value": "CLOSED"}
}
```

---

### SetState

Set the lifecycle state for a single customer experience.

**Action Signature:**
```
PTC.CEM.SetState(lifecycleManaged, State) -> CustomerExperience
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| **lifecycleManaged** | CustomerExperience | Customer experience to update |
| **State** | EnumType | Target state |

**Usage Example:**

```bash
POST /CEM/CustomerExperiences('{id}')/PTC.CEM.SetState
Content-Type: application/json
X-CSRF-Token: {token}

{
  "State": {"Value": "IN_PROGRESS"}
}
```

---

### EditCustomerExperiencesSecurityLabels

Edit security labels for customer experiences.

**Action Signature:**
```
EditCustomerExperiencesSecurityLabels(CustomerExperiences) -> Collection(CustomerExperience)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| **CustomerExperiences** | Collection(CustomerExperience) | Collection of customer experiences |

**Usage Example:**

```bash
POST /CEM/EditCustomerExperiencesSecurityLabels
Content-Type: application/json
X-CSRF-Token: {token}

{
  "CustomerExperiences": [
    {"ID": "OR:wt.csm.CSMCustomerExperience:12345"}
  ]
}
```

---

## Functions

### GetLifeCycleTemplate

Get the lifecycle template for a customer experience.

**Function Signature:**
```
PTC.CEM.GetLifeCycleTemplate(lifecycleManaged) -> LifeCycleTemplate
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| **lifecycleManaged** | CustomerExperience | Customer experience |

**Usage Example:**

```bash
GET /CEM/CustomerExperiences('{id}')/PTC.CEM.GetLifeCycleTemplate
```

---

### GetValidStateTransitions

Get valid state transitions for a customer experience.

**Function Signature:**
```
PTC.CEM.GetValidStateTransitions(lifecycleManaged) -> EnumTypeList
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| **lifecycleManaged** | CustomerExperience | Customer experience |

**Usage Example:**

```bash
GET /CEM/CustomerExperiences('{id}')/PTC.CEM.GetValidStateTransitions
```

**Response:**
```json
{
  "@odata.context": "...",
  "value": ["IN_PROGRESS", "CLOSED", "CANCELLED"]
}
```

---

## Common Query Examples

### Filter by Multiple Criteria

```bash
# Get open customer experiences from a specific date range
GET /CEM/CustomerExperiences?$filter=State/Value eq 'OPEN' and Date ge 2026-02-01T00:00:00Z and Date le 2026-02-28T23:59:59Z

# Get customer experiences by country
GET /CEM/CustomerExperiences?$filter=CountryOfEvent/Value eq 'USA'

# Get customer experiences reported by email
GET /CEM/CustomerExperiences?$filter=HowReported/Value eq 'EMAIL'
```

### Complex Queries with Expansion

```bash
# Get customer experiences with all related data
GET /CEM/CustomerExperiences?$expand=Context,Creator,EntryLocation,PrimaryRelatedPersonOrLocation,PrimaryRelatedProduct,AdditionalRelatedProducts

# Get customer experiences with specific related product details
GET /CEM/CustomerExperiences?$expand=AdditionalRelatedProducts($expand=Subject,ManufacturingLocation)
```

### Sorting and Pagination

```bash
# Get latest customer experiences
GET /CEM/CustomerExperiences?$orderby=Date desc&$top=50

# Get paginated results
GET /CEM/CustomerExperiences?$skip=0&$top=25

# Get sorted by name with pagination
GET /CEM/CustomerExperiences?$orderby=Name asc&$skip=25&$top=25
```

---

## Complex Types

### EnumType

Enumeration type with Value and Display properties.

```json
{
  "Value": "OPEN",
  "Display": "Open"
}
```

### Icon

Icon type for type icons.

---

## Integration Notes

1. **Required Fields for Creation**: When creating a CustomerExperience, a `PrimaryRelatedPersonOrLocation` must be provided.

2. **Related Product Requirements**: When creating a RelatedProduct without a Subject reference, `ReportedNumber` and `ReportedName` are required.

3. **Lifecycle Management**: Customer experiences support lifecycle state transitions through the SetState actions.

4. **Cross-Domain References**: CEM domain references entities from:
   - PTC.DataAdmin (Container)
   - PTC.PrincipalMgmt (User)
   - PTC.QMS (Place, QualityContact, Subject)

5. **Notifiable**: Customer experiences support notifications (PTC.Capabilities).

---

## Schema Version

Schema Version: 7