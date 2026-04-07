# RegMstr Domain - Navigation Properties

This document describes all navigation properties and entity relationships in the RegMstr domain.

## Entity Relationship Diagram

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
│  │ - Modifier       │                             │ - Context        │       │
│  └──────────────────┘                             │ - Creator        │       │
│                                                   │ - Modifier       │       │
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
│                                                   │ - Creator        │       │
│                                                   │ - Modifier       │       │
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
│  ┌──────────────────┐      ComplianceRecords   ┌──────────────────┐        │
│  │ ComplianceItem   │─────────────────────────►│ ComplianceRecord │        │
│  ├──────────────────┤                          ├──────────────────┤        │
│  │ - ComplianceRecs │                          │ - Context        │        │
│  │ - Context        │                          └──────────────────┘        │
│  └──────────────────┘                                                      │
│                                                                             │
│  ┌──────────────────┐                  ┌──────────────────┐                 │
│  │     Standard     │                  │  Specification   │                 │
│  ├──────────────────┤                  ├──────────────────┤                 │
│  │ - Context        │                  │ - Context        │                 │
│  └──────────────────┘                  └──────────────────┘                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Navigation Properties by Entity

### Regulation

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context (Product, Library, Project) |
| Creator | PTC.PrincipalMgmt.User | User who created the regulation |
| Modifier | PTC.PrincipalMgmt.User | User who last modified the regulation |
| RegulatoryRequirements | Collection(PTC.RegMstr.RegulatoryRequirement) | Child requirements |

### RegulatoryRequirement

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context |
| Creator | PTC.PrincipalMgmt.User | User who created |
| Modifier | PTC.PrincipalMgmt.User | User who last modified |
| Regulation | PTC.RegMstr.Regulation | Parent regulation |
| ComplianceRecords | Collection(PTC.RegMstr.ComplianceRecord) | Compliance tracking records |

### ComplianceRecord

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context |
| Creator | PTC.PrincipalMgmt.User | User who created |
| Modifier | PTC.PrincipalMgmt.User | User who last modified |
| RegulatoryRequirement | PTC.RegMstr.RegulatoryRequirement | Related requirement |
| ComplianceEvidence | Collection(PTC.RegMstr.ComplianceEvidence) | Evidence documents |

### Standard

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context |

### Specification

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context |

### ComplianceItem

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context |
| ComplianceRecords | Collection(PTC.RegMstr.ComplianceRecord) | Related records |

### ComplianceEvidence

| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context |
| ComplianceRecord | PTC.RegMstr.ComplianceRecord | Related compliance record |

## Cross-Domain References

| From Entity | Navigation Property | Target Domain | Target Entity |
|-------------|---------------------|---------------|---------------|
| Regulation | Context | DataAdmin | Container |
| Regulation | Creator | PrincipalMgmt | User |
| Regulation | Modifier | PrincipalMgmt | User |
| RegulatoryRequirement | Context | DataAdmin | Container |
| RegulatoryRequirement | Creator | PrincipalMgmt | User |
| RegulatoryRequirement | Modifier | PrincipalMgmt | User |
| ComplianceRecord | Context | DataAdmin | Container |
| ComplianceRecord | Creator | PrincipalMgmt | User |
| ComplianceRecord | Modifier | PrincipalMgmt | User |
| Standard | Context | DataAdmin | Container |
| Specification | Context | DataAdmin | Container |
| ComplianceItem | Context | DataAdmin | Container |
| ComplianceEvidence | Context | DataAdmin | Container |

## OData Query Examples

### Get regulation with requirements

```
GET /RegMstr/Regulations('{id}')?$expand=RegulatoryRequirements
```

### Get requirement with regulation and compliance records

```
GET /RegMstr/RegulatoryRequirements('{id}')?$expand=Regulation,ComplianceRecords($expand=ComplianceEvidence)
```

### Get compliance record with full context

```
GET /RegMstr/ComplianceRecords('{id}')?$expand=RegulatoryRequirement($expand=Regulation),ComplianceEvidence,Creator,Context
```

### Get regulation hierarchy

```
GET /RegMstr/Regulations('{id}')?$expand=
  RegulatoryRequirements($expand=
    ComplianceRecords($expand=
      ComplianceEvidence
    )
  ),
  Context,
  Creator
```

### Get compliance evidence for a record

```
GET /RegMstr/ComplianceRecords('{id}')/ComplianceEvidence?$expand=Context
```

### Get requirements for a regulation

```
GET /RegMstr/Regulations('{id}')/RegulatoryRequirements?$expand=ComplianceRecords
```

### Get non-compliant records with requirements

```
GET /RegMstr/ComplianceRecords?$filter=ComplianceStatus eq 'Non-Compliant'&$expand=RegulatoryRequirement($expand=Regulation),ComplianceEvidence
```

### Get regulations by agency with requirements

```
GET /RegMstr/Regulations?$filter=RegulatoryAgency eq 'FDA'&$expand=RegulatoryRequirements($expand=ComplianceRecords)
```

### Multi-level expansion

```
GET /RegMstr/Regulations('{id}')?$expand=
  RegulatoryRequirements($expand=
    ComplianceRecords($expand=
      ComplianceEvidence($expand=Context),
      Creator,
      Modifier
    ),
    Creator
  ),
  Context,
  Creator,
  Modifier
```

## Entity Sets

| Entity Set | Entity Type | Description |
|------------|-------------|-------------|
| Regulations | Regulation | All regulations |
| RegulatoryRequirements | RegulatoryRequirement | All regulatory requirements |
| ComplianceRecords | ComplianceRecord | All compliance records |
| Standards | Standard | All standards |
| Specifications | Specification | All specifications |
| ComplianceItems | ComplianceItem | All compliance items |
| ComplianceEvidences | ComplianceEvidence | All compliance evidence |

## Common Query Patterns

### Get active regulations by jurisdiction

```
GET /RegMstr/Regulations?$filter=Status eq 'Active' and Jurisdiction eq 'EU'&$expand=RegulatoryRequirements&$orderby=EffectiveDate desc
```

### Get pending compliance reviews

```
GET /RegMstr/ComplianceRecords?$filter=ReviewDate le 2026-02-01T00:00:00Z&$expand=RegulatoryRequirement($expand=Regulation)
```

### Get expired compliance evidence

```
GET /RegMstr/ComplianceEvidences?$filter=ExpirationDate lt 2026-01-01T00:00:00Z&$expand=ComplianceRecord($expand=RegulatoryRequirement)
```

### Get compliance status by requirement

```
GET /RegMstr/RegulatoryRequirements?$expand=ComplianceRecords($expand=ComplianceEvidence)
```

### Get ISO standards by status

```
GET /RegMstr/Standards?$filter=IssuingBody eq 'ISO' and Status eq 'Active'&$orderby=Number asc
```

## Navigation Property Notes

1. **Regulation → RegulatoryRequirements**: One-to-Many. A regulation contains multiple requirements.

2. **RegulatoryRequirement → Regulation**: Many-to-One. Each requirement belongs to one regulation.

3. **RegulatoryRequirement → ComplianceRecords**: One-to-Many. A requirement can have multiple compliance records (for different products/contexts).

4. **ComplianceRecord → RegulatoryRequirement**: Many-to-One. Each compliance record is for a specific requirement.

5. **ComplianceRecord → ComplianceEvidence**: One-to-Many. A compliance record can have multiple evidence documents.

6. **ComplianceEvidence → ComplianceRecord**: Many-to-One. Each evidence document supports one compliance record.

7. **ComplianceItem → ComplianceRecords**: One-to-Many. A compliance item can have multiple compliance records for different requirements.
