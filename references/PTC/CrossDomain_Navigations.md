# Cross-Domain Navigation Reference

This document describes navigation patterns that cross Windchill OData domain boundaries.

## Common Navigation Properties

Most Windchill entities share these common navigation properties:

| Navigation | Type | Description |
|------------|------|-------------|
| **Context** | PTC.DataAdmin.Container | Container context (Product, Library, Project) |
| **Creator** | PTC.PrincipalMgmt.User | User who created the object |
| **Modifier** | PTC.PrincipalMgmt.User | User who last modified the object |
| **Owner** | PTC.PrincipalMgmt.User | Assigned owner (where applicable) |
| **Folder** | PTC.DataAdmin.Folder | Containing folder |

---

## Domain Cross-Reference Matrix

### ProdMgmt Domain

| Entity | Cross-Domain Navigation | Target Domain | Target Entity |
|--------|------------------------|---------------|---------------|
| Part | Context | DataAdmin | Container |
| Part | Creator | PrincipalMgmt | User |
| Part | Modifier | PrincipalMgmt | User |
| Part | DescribedByDocuments | DocMgmt | Document |
| Part | Uses | ProdMgmt | Part |
| Part | SupplierParts | SupplierMgmt | SupplierPart |

### DocMgmt Domain

| Entity | Cross-Domain Navigation | Target Domain | Target Entity |
|--------|------------------------|---------------|---------------|
| Document | Context | DataAdmin | Container |
| Document | Creator | PrincipalMgmt | User |
| Document | Modifier | PrincipalMgmt | User |
| Document | Describes | ProdMgmt | Part |

### ChangeMgmt Domain

| Entity | Cross-Domain Navigation | Target Domain | Target Entity |
|--------|------------------------|---------------|---------------|
| ChangeNotice | Context | DataAdmin | Container |
| ChangeNotice | Creator | PrincipalMgmt | User |
| ChangeNotice | Modifier | PrincipalMgmt | User |
| ChangeNotice | AffectedObjects | ChangeMgmt | Changeable |
| ChangeNotice | ResultingObjects | ChangeMgmt | Changeable |
| ChangeRequest | Context | DataAdmin | Container |
| ChangeRequest | Creator | PrincipalMgmt | User |
| ChangeTask | Context | DataAdmin | Container |
| ChangeTask | Creator | PrincipalMgmt | User |

### SupplierMgmt Domain

| Entity | Cross-Domain Navigation | Target Domain | Target Entity |
|--------|------------------------|---------------|---------------|
| Supplier | Context | DataAdmin | Container |
| Supplier | Creator | PrincipalMgmt | User |
| Supplier | Modifier | PrincipalMgmt | User |
| SupplierPart | Part | ProdMgmt | Part |
| SupplierPart | Supplier | SupplierMgmt | Supplier |

### QMS Domain

| Entity | Cross-Domain Navigation | Target Domain | Target Entity |
|--------|------------------------|---------------|---------------|
| QualityAction | Context | DataAdmin | Container |
| QualityAction | Creator | PrincipalMgmt | User |
| QualityAction | Owner | PrincipalMgmt | User |
| NonConformance | Context | DataAdmin | Container |
| NonConformance | Creator | PrincipalMgmt | User |
| CAPA | Context | DataAdmin | Container |
| CAPA | Owner | PrincipalMgmt | User |

### RegMstr Domain

| Entity | Cross-Domain Navigation | Target Domain | Target Entity |
|--------|------------------------|---------------|---------------|
| Regulation | Context | DataAdmin | Container |
| Regulation | Creator | PrincipalMgmt | User |
| RegulatoryRequirement | Context | DataAdmin | Container |
| RegulatoryRequirement | Creator | PrincipalMgmt | User |
| ComplianceRecord | Context | DataAdmin | Container |
| ComplianceRecord | Creator | PrincipalMgmt | User |

---

## Cross-Domain Query Patterns

### Pattern 1: Entity with Container Context

```
GET /{Domain}/{EntitySet}('{id}')?$expand=Context($expand=Creator)
```

Example:
```bash
GET /ProdMgmt/Parts('OR:wt.part.WTPart:12345')?$expand=Context($expand=Creator)
```

### Pattern 2: Entity with Audit Trail

```
GET /{Domain}/{EntitySet}('{id}')?$expand=Creator,Modifier
```

Example:
```bash
GET /ChangeMgmt/ChangeNotices('OR:wt.change2.WTChangeOrder2:12345')?$expand=Creator,Modifier,Context
```

### Pattern 3: Cross-Domain Object Linking

```
GET /{Domain1}/{EntitySet}('{id}')?$expand={Navigation}(?$expand=Context,Creator)
```

Example (Part with Documents):
```bash
GET /ProdMgmt/Parts('OR:wt.part.WTPart:12345')?$expand=DescribedByDocuments($expand=Context,Creator)
```

### Pattern 4: Change Impact Analysis

```
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=
  AffectedObjects($expand=Context,Creator),
  ResultingObjects($expand=Context,Creator),
  ChangeTasks($expand=Creator)
```

### Pattern 5: Supplier Part with Part and Supplier

```
GET /SupplierMgmt/SupplierParts('{id}')?$expand=
  Part($expand=Context),
  Supplier($expand=Context)
```

### Pattern 6: Quality Compliance Chain

```
GET /RegMstr/Regulations('{id}')?$expand=
  RegulatoryRequirements($expand=
    ComplianceRecords($expand=
      ComplianceEvidence,
      Creator
    )
  ),
  Context,
  Creator
```

---

## Common Cross-Domain Queries

### Get Part with Full Context

```bash
GET /ProdMgmt/Parts('{id}')?$expand=
  Context($expand=Creator),
  Creator,
  Modifier,
  DescribedByDocuments($expand=Creator),
  Uses($expand=Part($expand=Context))
```

### Get Change Notice with Full Impact

```bash
GET /ChangeMgmt/ChangeNotices('{id}')?$expand=
  Context($expand=Creator),
  Creator,
  Modifier,
  ChangeRequests($expand=AffectedObjects),
  ChangeTasks($expand=ResultingObjects,Creator),
  AffectedObjects($expand=Context,Creator),
  ResultingObjects($expand=Context,Creator)
```

### Get Supplier with Parts

```bash
GET /SupplierMgmt/Suppliers('{id}')?$expand=
  Context($expand=Creator),
  Creator,
  Modifier,
  SupplierParts($expand=Part($expand=Context))
```

### Get CAPA with Full Chain

```bash
GET /QMS/CAPAs('{id}')?$expand=
  Context($expand=Creator),
  Owner,
  NonConformance($expand=
    Subject,
    Place,
    Creator
  ),
  Subject($expand=Context),
  Creator
```

### Get Regulation with Compliance Status

```bash
GET /RegMstr/Regulations('{id}')?$expand=
  Context($expand=Creator),
  Creator,
  RegulatoryRequirements($expand=
    ComplianceRecords($filter=ComplianceStatus eq 'Non-Compliant'&$expand=
      ComplianceEvidence,
      Creator
    )
  )
```

---

## Navigation Property Notes

1. **Container Context** - Always consider expanding Context to understand the product/project scope.

2. **Audit Trail** - Creator and Modifier provide full audit information across all domains.

3. **Change Impact** - ChangeMgmt domain links to objects across other domains through AffectedObjects/ResultingObjects.

4. **Supplier Integration** - SupplierMgmt links to ProdMgmt Parts through SupplierPart.

5. **Quality Chain** - QMS entities link to each other (NonConformance → CAPA → Evidence) and reference products via Subject.

6. **Compliance Hierarchy** - RegMstr provides a hierarchy: Regulation → Requirements → ComplianceRecords → Evidence.

---

## Filtering Across Domains

### Filter by Container

```bash
GET /ProdMgmt/Parts?$expand=Context&$filter=Context/Name eq 'Product A'
```

### Filter by Creator

```bash
GET /ChangeMgmt/ChangeNotices?$expand=Creator&$filter=Creator/Name eq 'jdoe'
```

### Filter by State Across Domains

```bash
GET /ProdMgmt/Parts?$filter=State/Value eq 'RELEASED'
GET /ChangeMgmt/ChangeNotices?$filter=State/Value eq 'OPEN'
GET /QMS/QualityActions?$filter=State/Value eq 'IN_PROGRESS'
```

---

## Performance Considerations

1. **Limit Expansions** - Avoid expanding too many levels. Use multiple queries if needed.

2. **Use Select** - Combine `$expand` with `$select` to reduce payload:

```bash
GET /ProdMgmt/Parts?$expand=Context($select=ID,Name),Creator($select=ID,Name,FullName)&$select=ID,Name,Number
```

3. **Filter First** - Apply filters before expanding to reduce result set:

```bash
GET /ProdMgmt/Parts?$filter=State/Value eq 'RELEASED'&$expand=Context,Creator
```

4. **Pagination** - Always use `$top` and `$skip` for large result sets:

```bash
GET /ProdMgmt/Parts?$top=50&$skip=0&$expand=Context,Creator
```
