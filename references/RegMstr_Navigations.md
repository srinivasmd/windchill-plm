# RegMstr Domain Navigation Properties

## Navigation Relationships

This document describes the navigation properties between entities in the RegMstr domain and cross-domain references.

---

## RegulatorySpecification Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Context` | Container | DataAdmin | Container context |
| `Creator` | User | PrincipalMgmt | Creator user |
| `Modifier` | User | PrincipalMgmt | Modifier user |
| `RelatedProducts` | Collection(RelatedProduct) | RegMstr | Related Products |
| `RegulatoryApprovals` | Collection(RegulatoryApproval) | RegMstr | Regulatory Approvals |
| `RegulatorySubmission` | RegulatorySubmission | RegMstr | Related Submission |

### Navigation Examples

```bash
# Get related products
GET /RegMstr/RegulatorySpecifications('{id}')/RelatedProducts

# Get regulatory approvals
GET /RegMstr/RegulatorySpecifications('{id}')/RegulatoryApprovals

# Get related submission
GET /RegMstr/RegulatorySpecifications('{id}')/RegulatorySubmission

# Expand all navigations
GET /RegMstr/RegulatorySpecifications('{id}')?$expand=RelatedProducts,RegulatoryApprovals,RegulatorySubmission

# Nested expansion
GET /RegMstr/RegulatorySpecifications('{id}')?$expand=RegulatoryApprovals($expand=RelatedProducts),Creator
```

---

## RegulatorySubmission Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Context` | Container | DataAdmin | Container context |
| `Creator` | User | PrincipalMgmt | Creator user |
| `RegulatorySpecification` | RegulatorySpecification | RegMstr | Related Specification |
| `RegulatoryApprovals` | Collection(RegulatoryApproval) | RegMstr | Regulatory Approvals |
| `RelatedProducts` | Collection(RelatedProduct) | RegMstr | Related Products |

### Navigation Examples

```bash
# Get related specification
GET /RegMstr/RegulatorySubmissions('{id}')/RegulatorySpecification

# Get regulatory approvals
GET /RegMstr/RegulatorySubmissions('{id}')/RegulatoryApprovals

# Get related products
GET /RegMstr/RegulatorySubmissions('{id}')/RelatedProducts

# Expand all navigations
GET /RegMstr/RegulatorySubmissions('{id}')?$expand=RegulatorySpecification,RegulatoryApprovals,RelatedProducts

# Nested expansion
GET /RegMstr/RegulatorySubmissions('{id}')?$expand=RegulatorySpecification($expand=RegulatoryApprovals),RegulatoryApprovals($expand=RelatedProducts)
```

---

## RegulatoryApproval Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Context` | Container | DataAdmin | Container context |
| `Creator` | User | PrincipalMgmt | Creator user |
| `RegulatorySpecification` | RegulatorySpecification | RegMstr | Related Specification |
| `RegulatorySubmission` | RegulatorySubmission | RegMstr | Related Submission |
| `RelatedProducts` | Collection(RelatedProduct) | RegMstr | Related Products |

### Navigation Examples

```bash
# Get related specification
GET /RegMstr/RegulatoryApprovals('{id}')/RegulatorySpecification

# Get related submission
GET /RegMstr/RegulatoryApprovals('{id}')/RegulatorySubmission

# Get related products
GET /RegMstr/RegulatoryApprovals('{id}')/RelatedProducts

# Expand all navigations
GET /RegMstr/RegulatoryApprovals('{id}')?$expand=RegulatorySpecification,RegulatorySubmission,RelatedProducts
```

---

## ComplianceDefinition Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Context` | Container | DataAdmin | Container context |
| `ComplianceRecords` | Collection(ComplianceRecord) | RegMstr | Compliance Records |

### Navigation Examples

```bash
# Get compliance records
GET /RegMstr/ComplianceDefinitions('{id}')/ComplianceRecords

# Expand with records
GET /RegMstr/ComplianceDefinitions('{id}')?$expand=ComplianceRecords
```

---

## TradeControlClassification Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Context` | Container | DataAdmin | Container context |
| `RelatedProducts` | Collection(RelatedProduct) | RegMstr | Classified Products |

### Navigation Examples

```bash
# Get classified products
GET /RegMstr/TradeControlClassifications('{id}')/RelatedProducts

# Expand with products
GET /RegMstr/TradeControlClassifications('{id}')?$expand=RelatedProducts
```

---

## Cross-Domain Navigation Paths

### RegMstr to PrincipalMgmt

```bash
# Path: RegulatorySpecification -> Creator (User)
GET /RegMstr/RegulatorySpecifications('{id}')/Creator

# Path: RegulatorySubmission -> Creator (User)
GET /RegMstr/RegulatorySubmissions('{id}')/Creator

# Expand with user details
GET /RegMstr/RegulatoryApprovals?$expand=Creator($select=Name,FullName,Email)
```

### RegMstr to ProdMgmt

```bash
# RelatedProducts can link to Parts in ProdMgmt
GET /RegMstr/RegulatoryApprovals('{id}')/RelatedProducts

# Get products with regulatory approvals
GET /RegMstr/RegulatoryApprovals?$expand=RelatedProducts
```

---

## Relationship Diagram

```
Regulatory Hierarchy:

┌────────────────────────┐
│ RegulatorySpecification │
│                        │
└────────────┬───────────┘
             │
             │ RegulatorySubmission, RegulatoryApprovals
             ▼
┌────────────────────────┐        ┌────────────────────────┐
│ RegulatorySubmission   │───────►│ RegulatoryApproval     │
│                        │        │                        │
└────────────┬───────────┘        └────────────┬───────────┘
             │                                 │
             │ RelatedProducts                 │ RelatedProducts
             ▼                                 ▼
┌─────────────────────────────────────────────────────────┐
│                    RelatedProducts                       │
│                  (Link to ProdMgmt Parts)                │
└─────────────────────────────────────────────────────────┘

Compliance Hierarchy:

┌────────────────────────┐
│ ComplianceDefinition   │
│                        │
└────────────┬───────────┘
             │
             │ ComplianceRecords
             ▼
┌────────────────────────┐
│ ComplianceRecord       │
│                        │
└────────────────────────┘

Trade Control:

┌─────────────────────────────┐
│ TradeControlClassification  │
│                             │
└─────────────┬───────────────┘
              │
              │ RelatedProducts
              ▼
┌─────────────────────────────────────────────────────────┐
│                    RelatedProducts                       │
│                  (Link to ProdMgmt Parts)                │
└─────────────────────────────────────────────────────────┘
```

---

## Common Navigation Patterns

### Get Regulatory Approval with Full Context

```bash
GET /RegMstr/RegulatoryApprovals('{id}')?$expand=
    RegulatorySpecification,
    RegulatorySubmission($expand=RelatedProducts),
    RelatedProducts,
    Creator
```

### Get Specification with Approvals and Products

```bash
GET /RegMstr/RegulatorySpecifications('{id}')?$expand=
    RegulatoryApprovals($expand=RelatedProducts),
    RegulatorySubmission,
    RelatedProducts
```

### Get Submission with Complete Chain

```bash
GET /RegMstr/RegulatorySubmissions('{id}')?$expand=
    RegulatorySpecification($expand=RegulatoryApprovals),
    RegulatoryApprovals($expand=RelatedProducts),
    RelatedProducts,
    Creator
```

### Get Classification with Products

```bash
GET /RegMstr/TradeControlClassifications?$expand=
    RelatedProducts
```

---

## Cross-Domain Reference Summary

| Source Domain | Source Entity | Navigation | Target Domain | Target Entity |
|---------------|---------------|------------|---------------|---------------|
| RegMstr | RegulatorySpecification | Creator | PrincipalMgmt | User |
| RegMstr | RegulatorySubmission | Creator | PrincipalMgmt | User |
| RegMstr | RegulatoryApproval | Creator | PrincipalMgmt | User |
| RegMstr | * | RelatedProducts | ProdMgmt | Part |

---

## Notes

1. **Regulatory Hierarchy**: RegulatorySpecification -> RegulatorySubmission -> RegulatoryApproval

2. **Product Linkage**: RelatedProducts links regulatory objects to products in ProdMgmt

3. **Approval Tracking**: Track approval dates and expiration dates for renewals

4. **Compliance vs Regulatory**: ComplianceDefinition for trade control, Regulatory* for product approvals

5. **Country Information**: Use Country entity for jurisdiction and embargo status

6. **Trade Control**: TradeControlClassification for export control and classification codes (ECCN)

7. **Cross-Domain Performance**: Expanding RelatedProducts can return large collections - use $top to limit
