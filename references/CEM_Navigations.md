# CEM Domain Navigation Properties

This document describes all navigation properties and entity relationships in the PTC Customer Experience Management (CEM) domain.

## Entity: CustomerExperience

The main entity representing a customer experience record.

### Navigation Properties

| Property | Type | Description |
|----------|------|-------------|
| `AdditionalRelatedProducts` | Collection(PTC.CEM.RelatedProduct) | Additional products related to the customer experience |
| `PrimaryRelatedProduct` | PTC.CEM.RelatedProduct | Primary product related to the customer experience |
| `EntryLocation` | PTC.QMS.Place | Location where the customer experience was entered |
| `Context` | PTC.DataAdmin.Container | Container context for the customer experience |
| `PrimaryRelatedPersonOrLocation` | PTC.QMS.QualityContact | Primary person or location related to the customer experience |
| `Creator` | PTC.PrincipalMgmt.User | User who created the customer experience (read-only) |
| `Modifier` | PTC.PrincipalMgmt.User | User who last modified the customer experience (read-only) |
| `AdditionalRelatedPersonnelOrLocations` | Collection(PTC.QMS.QualityContact) | Additional personnel or locations related to the customer experience |

### External Domain References

| Navigation Property | Target Domain | Target Entity |
|---------------------|---------------|---------------|
| EntryLocation | QMS | Place |
| PrimaryRelatedPersonOrLocation | QMS | QualityContact |
| AdditionalRelatedPersonnelOrLocations | QMS | QualityContact |
| Creator | PrincipalMgmt | User |
| Modifier | PrincipalMgmt | User |
| Context | DataAdmin | Container |

---

## Entity: RelatedProduct

Represents products related to a customer experience.

### Navigation Properties

| Property | Type | Description |
|----------|------|-------------|
| `Subject` | PTC.QMS.Subject | Subject (product/part) related to the customer experience |
| `ManufacturingLocation` | PTC.QMS.Place | Manufacturing location of the related product |

### External Domain References

| Navigation Property | Target Domain | Target Entity |
|---------------------|---------------|---------------|
| Subject | QMS | Subject |
| ManufacturingLocation | QMS | Place |

---

## Entity Relationships Diagram

```
CustomerExperience
├── AdditionalRelatedProducts (Collection) → RelatedProduct
│   ├── Subject → PTC.QMS.Subject
│   └── ManufacturingLocation → PTC.QMS.Place
├── PrimaryRelatedProduct → RelatedProduct
│   ├── Subject → PTC.QMS.Subject
│   └── ManufacturingLocation → PTC.QMS.Place
├── EntryLocation → PTC.QMS.Place
├── Context → PTC.DataAdmin.Container
├── PrimaryRelatedPersonOrLocation → PTC.QMS.QualityContact
├── AdditionalRelatedPersonnelOrLocations (Collection) → PTC.QMS.QualityContact
├── Creator → PTC.PrincipalMgmt.User
└── Modifier → PTC.PrincipalMgmt.User
```

---

## OData Query Examples

### Get Customer Experiences with Related Products

```http
GET /Windchill/servlet/odata/CEM/CustomerExperiences?$expand=PrimaryRelatedProduct,AdditionalRelatedProducts
```

### Get Customer Experience with All Navigations

```http
GET /Windchill/servlet/odata/CEM/CustomerExperiences?$expand=PrimaryRelatedProduct,AdditionalRelatedProducts,EntryLocation,Context,PrimaryRelatedPersonOrLocation,AdditionalRelatedPersonnelOrLocations,Creator,Modifier
```

### Get Customer Experiences by Number with Related Products

```http
GET /Windchill/servlet/odata/CEM/CustomerExperiences?$filter=Number eq 'CE-001'&$expand=PrimaryRelatedProduct,AdditionalRelatedProducts
```

### Get Related Products with Subject and Manufacturing Location

```http
GET /Windchill/servlet/odata/CEM/CustomerExperiences?$expand=PrimaryRelatedProduct($expand=Subject,ManufacturingLocation)
```

### Get Customer Experiences with Creator Information

```http
GET /Windchill/servlet/odata/CEM/CustomerExperiences?$expand=Creator
```

### Filter by Related Product

```http
GET /Windchill/servlet/odata/CEM/CustomerExperiences?$expand=PrimaryRelatedProduct&$filter=PrimaryRelatedProduct/ReportedNumber eq 'PART-123'
```

---

## Actions and Functions

### Actions

| Action | Description | Parameters | Return Type |
|--------|-------------|------------|-------------|
| SetStateCustomerExperiences | Sets the state of multiple customer experiences | CustomerExperiences (Collection), State | Collection(CustomerExperience) |
| SetState | Sets the state of a customer experience (bound) | lifecycleManaged, State | CustomerExperience |
| EditCustomerExperiencesSecurityLabels | Edit security labels for customer experiences | CustomerExperiences (Collection) | Collection(CustomerExperience) |

### Functions

| Function | Description | Parameters | Return Type |
|----------|-------------|------------|-------------|
| GetLifeCycleTemplate | Gets the lifecycle template for the customer experience | lifecycleManaged | LifeCycleTemplate |
| GetValidStateTransitions | Gets valid state transitions for the customer experience | lifecycleManaged | EnumTypeList |

### Action Example: Set State

```http
POST /Windchill/servlet/odata/CEM/SetStateCustomerExperiences
Content-Type: application/json

{
  "CustomerExperiences": ["OR:wt.cem.CustomerExperience:12345"],
  "State": "REVIEW"
}
```

### Function Example: Get Lifecycle Template

```http
GET /Windchill/servlet/odata/CEM/CustomerExperiences('OR:wt.cem.CustomerExperience:12345')/PTC.CEM.GetLifeCycleTemplate()
```

---

## Notes

- **Required Field**: When creating a CustomerExperience, `PrimaryRelatedPersonOrLocation` must be provided.
- **Subject Reference**: For RelatedProduct, `ReportedNumber` and `ReportedName` are required when a Subject reference is not provided.
- **Capabilities**: CustomerExperience is "Notifiable" - supports notifications.
- **Operations**: CustomerExperience supports READ, CREATE, UPDATE. RelatedProduct supports READ, CREATE, UPDATE, DELETE.