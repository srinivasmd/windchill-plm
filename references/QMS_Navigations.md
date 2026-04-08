# QMS Domain Navigation Properties

## Navigation Relationships

This document describes the navigation properties between entities in the QMS domain and cross-domain references.

---

## QualityAction Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Context` | Container | DataAdmin | Container context |
| `Creator` | User | PrincipalMgmt | Creator user |
| `Modifier` | User | PrincipalMgmt | Modifier user |
| `Owner` | User | PrincipalMgmt | Owner user |
| `QualityIssue` | QualityIssue | QMS | Related Quality Issue |
| `RelatedProducts` | Collection(RelatedProduct) | QMS | Related Products |

### Navigation Examples

```bash
# Get owner
GET /QMS/QualityActions('{id}')/Owner

# Get related quality issue
GET /QMS/QualityActions('{id}')/QualityIssue

# Get related products
GET /QMS/QualityActions('{id}')/RelatedProducts

# Expand all navigations
GET /QMS/QualityActions('{id}')?$expand=Owner,QualityIssue,RelatedProducts

# Nested expansion
GET /QMS/QualityActions('{id}')?$expand=QualityIssue($expand=Nonconformances),Owner
```

---

## QualityIssue Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Context` | Container | DataAdmin | Container context |
| `Creator` | User | PrincipalMgmt | Creator user |
| `Modifier` | User | PrincipalMgmt | Modifier user |
| `Reporter` | User | PrincipalMgmt | Reporter user |
| `QualityActions` | Collection(QualityAction) | QMS | Quality Actions |
| `RelatedProducts` | Collection(RelatedProduct) | QMS | Related Products |
| `Nonconformances` | Collection(Nonconformance) | QMS | Nonconformances |

### Navigation Examples

```bash
# Get reporter
GET /QMS/QualityIssues('{id}')/Reporter

# Get quality actions
GET /QMS/QualityIssues('{id}')/QualityActions

# Get nonconformances
GET /QMS/QualityIssues('{id}')/Nonconformances

# Get related products
GET /QMS/QualityIssues('{id}')/RelatedProducts

# Expand all navigations
GET /QMS/QualityIssues('{id}')?$expand=Creator,Reporter,QualityActions,Nonconformances

# Nested expansion with actions
GET /QMS/QualityIssues('{id}')?$expand=QualityActions($expand=Owner),Nonconformances($expand=Dispositions)
```

---

## QualityContact Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `User` | User | PrincipalMgmt | Related User |
| `Place` | Place | QMS | Related Place |

### Navigation Examples

```bash
# Get user
GET /QMS/QualityContacts('{id}')/User

# Get place
GET /QMS/QualityContacts('{id}')/Place

# Expand both
GET /QMS/QualityContacts('{id}')?$expand=User,Place
```

---

## Place Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Context` | Container | DataAdmin | Container context |
| `QualityContacts` | Collection(QualityContact) | QMS | Quality Contacts at this place |

### Navigation Examples

```bash
# Get quality contacts at this place
GET /QMS/Places('{id}')/QualityContacts

# Expand with contacts
GET /QMS/Places('{id}')?$expand=QualityContacts($expand=User)
```

---

## Nonconformance Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Context` | Container | DataAdmin | Container context |
| `Creator` | User | PrincipalMgmt | Creator user |
| `QualityIssue` | QualityIssue | QMS | Related Quality Issue |
| `Dispositions` | Collection(NCDisposition) | QMS | Dispositions |
| `RelatedProduct` | RelatedProduct | QMS | Related Product |

### Navigation Examples

```bash
# Get related quality issue
GET /QMS/Nonconformances('{id}')/QualityIssue

# Get dispositions
GET /QMS/Nonconformances('{id}')/Dispositions

# Get related product
GET /QMS/Nonconformances('{id}')/RelatedProduct

# Expand all navigations
GET /QMS/Nonconformances('{id}')?$expand=QualityIssue,Dispositions,RelatedProduct

# Nested expansion
GET /QMS/Nonconformances('{id}')?$expand=QualityIssue($expand=QualityActions),Dispositions
```

---

## Audit Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Context` | Container | DataAdmin | Container context |
| `Creator` | User | PrincipalMgmt | Creator user |
| `Findings` | Collection(AuditFinding) | QMS | Audit Findings |
| `Checklist` | AuditChecklist | QMS | Audit Checklist |

### Navigation Examples

```bash
# Get findings
GET /QMS/Audits('{id}')/Findings

# Get checklist
GET /QMS/Audits('{id}')/Checklist

# Expand with findings
GET /QMS/Audits('{id}')?$expand=Findings,Creator

# Nested expansion with corrective actions
GET /QMS/Audits('{id}')?$expand=Findings($expand=CorrectiveAction)
```

---

## AuditFinding Navigations

### Outbound Navigations

| Navigation Property | Target Entity | Target Domain | Description |
|---------------------|---------------|---------------|-------------|
| `Audit` | Audit | QMS | Parent Audit |
| `CorrectiveAction` | QualityAction | QMS | Corrective Action |

### Navigation Examples

```bash
# Get parent audit
GET /QMS/AuditFindings('{id}')/Audit

# Get corrective action
GET /QMS/AuditFindings('{id}')/CorrectiveAction

# Expand both
GET /QMS/AuditFindings('{id}')?$expand=Audit,CorrectiveAction
```

---

## Cross-Domain Navigation Paths

### QMS to PrincipalMgmt

```bash
# Path: QualityAction -> Owner (User)
GET /QMS/QualityActions('{id}')/Owner

# Path: QualityIssue -> Reporter (User)
GET /QMS/QualityIssues('{id}')/Reporter

# Path: QualityContact -> User
GET /QMS/QualityContacts('{id}')/User

# Expand with user details
GET /QMS/QualityActions?$expand=Owner($select=Name,FullName,Email)
```

### QMS to CEM

```bash
# CEM references QMS entities
# Path: CustomerExperience -> EntryLocation (Place)
GET /CEM/CustomerExperiences('{id}')/EntryLocation

# Path: CustomerExperience -> PrimaryRelatedPersonOrLocation (QualityContact)
GET /CEM/CustomerExperiences('{id}')/PrimaryRelatedPersonOrLocation

# Expand CEM with QMS entities
GET /CEM/CustomerExperiences?$expand=EntryLocation,PrimaryRelatedPersonOrLocation
```

### QMS to Workflow

```bash
# Get work items for quality objects
GET /Workflow/WorkItems?$filter=Subject/Type eq 'wt.quality.QualityAction'

# Get work items for a specific quality issue
GET /Workflow/WorkItems?$filter=contains(Subject/SubjectName, 'QI-')
```

---

## Relationship Diagram

```
┌─────────────────┐
│ QualityIssue    │
│                 │
└────────┬────────┘
         │
         │ QualityActions, Nonconformances
         ▼
┌─────────────────┐        ┌─────────────────┐
│ QualityAction   │        │ Nonconformance  │
│                 │        │                 │
└────────┬────────┘        └────────┬────────┘
         │                          │
         │ Owner                    │ Dispositions
         ▼                          ▼
┌─────────────────┐        ┌─────────────────┐
│ User            │        │ NCDisposition   │
│ (PrincipalMgmt) │        │                 │
└─────────────────┘        └─────────────────┘

Audit Hierarchy:
┌─────────────────┐
│ Audit           │
│                 │
└────────┬────────┘
         │
         │ Findings
         ▼
┌─────────────────┐        ┌─────────────────┐
│ AuditFinding    │───────►│ QualityAction   │
│                 │        │ (Corrective)    │
└─────────────────┘        └─────────────────┘

Contact/Place:
┌─────────────────┐        ┌─────────────────┐
│ QualityContact  │◄──────►│ Place           │
│                 │        │                 │
└────────┬────────┘        └─────────────────┘
         │
         │ User
         ▼
┌─────────────────┐
│ User            │
│ (PrincipalMgmt) │
└─────────────────┘
```

---

## Common Navigation Patterns

### Get Quality Issue with Full Context

```bash
GET /QMS/QualityIssues('{id}')?$expand=
    Creator,
    Reporter,
    QualityActions($expand=Owner),
    Nonconformances($expand=Dispositions),
    RelatedProducts
```

### Get Audit with Findings and Actions

```bash
GET /QMS/Audits('{id}')?$expand=
    Creator,
    Findings($expand=CorrectiveAction($expand=Owner))
```

### Get Nonconformance with Resolution Path

```bash
GET /QMS/Nonconformances('{id}')?$expand=
    QualityIssue($expand=QualityActions),
    Dispositions,
    RelatedProduct
```

### Get Place with All Contacts

```bash
GET /QMS/Places('{id}')?$expand=
    QualityContacts($expand=User)
```

---

## Cross-Domain Reference Summary

| Source Domain | Source Entity | Navigation | Target Domain | Target Entity |
|---------------|---------------|------------|---------------|---------------|
| QMS | QualityAction | Owner | PrincipalMgmt | User |
| QMS | QualityAction | Creator | PrincipalMgmt | User |
| QMS | QualityIssue | Reporter | PrincipalMgmt | User |
| QMS | QualityContact | User | PrincipalMgmt | User |
| CEM | CustomerExperience | EntryLocation | QMS | Place |
| CEM | CustomerExperience | PrimaryRelatedPersonOrLocation | QMS | QualityContact |
| CEM | RelatedProduct | ManufacturingLocation | QMS | Place |

---

## Notes

1. **Quality Issue Hierarchy**: QualityIssue is the central entity that links to QualityActions and Nonconformances.

2. **Audit Findings**: Audit findings can link to QualityActions for corrective actions.

3. **Cross-Domain Integration**:
   - CEM domain references QMS Place and QualityContact
   - Workflow domain tracks work items for quality objects
   - ChangeMgmt can be triggered by quality issues

4. **Navigation Performance**: Expand only the navigation properties you need for optimal performance.

5. **Contact Information**: QualityContact provides a flexible way to track both internal and external contacts.

6. **Location Hierarchy**: Place entities can represent sites, facilities, or specific locations.
