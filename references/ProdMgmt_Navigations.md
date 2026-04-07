# ProdMgmt Domain - Navigation Properties

This document describes all navigation properties and entity relationships in the ProdMgmt domain.

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         PTC.ProdMgmt Namespace                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────┐      UsedBy        ┌─────────┐                           │
│   │  Part   │◄───────────────────│ PartUse │◄────┐                    │
│   ├─────────┤                    ├─────────┤     │                    │
│   │- UsedBy │                    │- Uses   │     │                    │
│   │- Uses   │                    │- UsedBy │     │                    │
│   │- Parent │                    │- Occurrences│  │                    │
│   └────┬────┘                    └────┬────┘     │                    │
│        │                              │         │                    │
│        │ Uses                         │ Uses    │                    │
│        │                              │         │                    │
│        ▼                              ▼         │                    │
│   ┌─────────┐                    ┌─────────┐    │                    │
│   │ PartUse │───────────────────│  Part   │────┘                    │
│   └─────────┘      Uses          └─────────┘                         │
│       │                                                                │
│       │ SubstituteFor                                                   │
│       │                                                                │
│       ▼                                                                │
│   ┌────────────────────┐                                               │
│   │ PartSubstituteLink │                                               │
│   ├────────────────────┤                                               │
│   │- SubstitutePart    │ → Part                                       │
│   │- Substitute        │ → ReplacementPart                             │
│   │- SubstituteFor     │ → PartUse                                    │
│   └────────────────────┘                                               │
│                                                                         │
│   ┌──────────────────┐                                                 │
│   │  ManagedBaseline │                                                 │
│   ├──────────────────┤                                                 │
│   │- BaselineItems   │ → Baselineable                                 │
│   │- Context         │ → DataAdmin.Container                          │
│   │- Folder          │ → DataAdmin.Folder                             │
│   └──────────────────┘                                                 │
│                                                                         │
│   ┌──────────────┐                                                     │
│   │ Baselineable │                                                     │
│   ├──────────────┤                                                     │
│   │- Context     │ → DataAdmin.Container                               │
│   │- Creator     │ → PrincipalMgmt.User                                │
│   │- Modifier    │ → PrincipalMgmt.User                                │
│   └──────────────┘                                                     │
│                                                                         │
│   ┌─────────────────┐                                                  │
│   │ UsageOccurrence │                                                  │
│   ├─────────────────┤                                                  │
│   │- UsedBy         │ → PartUse                                       │
│   └─────────────────┘                                                  │
│                                                                         │
└───────────────────────────────────────────────────────────────────────────┘
```

## Navigation Properties by Entity

### Part
| Navigation | Type | Description |
|------------|------|-------------|
| UsedBy | Collection(PTC.ProdMgmt.PartUse) | Part usages where this part is used as a child (parent assemblies that include this part) |
| Uses | Collection(PTC.ProdMgmt.PartUse) | Part usages where this part is used as a parent (child components in this part's BOM) |
| Parent | PTC.ProdMgmt.PartUse | Parent part usage link (read-only) |

### PartUse (PartUsageLink)
| Navigation | Type | Description |
|------------|------|-------------|
| Uses | PTC.ProdMgmt.Part | The child part being used (component in BOM) |
| UsedBy | PTC.ProdMgmt.Part | The parent part that uses this component (assembly) |
| Occurrences | Collection(PTC.ProdMgmt.UsageOccurrence) | Usage occurrences for this part usage |

### PartSubstituteLink
| Navigation | Type | Description |
|------------|------|-------------|
| SubstitutePart | PTC.ProdMgmt.Part | Version of the substitute part |
| Substitute | PTC.ProdMgmt.ReplacementPart | Common attributes of the substitute part |
| SubstituteFor | PTC.ProdMgmt.PartUse | Part usage link where the substitute can be used |

### Baselineable
| Navigation | Type | Description |
|------------|------|-------------|
| Context | PTC.DataAdmin.Container | Container context |
| Creator | PTC.PrincipalMgmt.User | User who created this object |
| Modifier | PTC.PrincipalMgmt.User | User who last modified this object |

### ManagedBaseline
| Navigation | Type | Description |
|------------|------|-------------|
| BaselineItems | Collection(PTC.ProdMgmt.Baselineable) | Items in the baseline |
| Context | PTC.DataAdmin.Container | Container context |
| Folder | PTC.DataAdmin.Folder | Folder containing the baseline |

### UsageOccurrence
| Navigation | Type | Description |
|------------|------|-------------|
| UsedBy | PTC.ProdMgmt.PartUse | Part usage that contains this occurrence |

### ReplacementPart
| Navigation | Type | Description |
|------------|------|-------------|
| *(No navigation properties)* | | |

### PartsReportListItem
| Navigation | Type | Description |
|------------|------|-------------|
| Parent | PTC.ProdMgmt.PartsReportListItem | Parent item in the report |

### RootStructureItems (extends Part)
| Navigation | Type | Description |
|------------|------|-------------|
| *(Inherits all navigations from Part)* | | |

### Snowmobile (extends RootStructureItems)
| Navigation | Type | Description |
|------------|------|-------------|
| *(Inherits all navigations from RootStructureItems/Part)* | | |

## Cross-Domain References

The ProdMgmt domain has navigation properties that reference entities from other domains:

| From Entity | Navigation Property | Target Domain | Target Entity |
|-------------|---------------------|---------------|---------------|
| Baselineable | Context | DataAdmin | Container |
| Baselineable | Creator | PrincipalMgmt | User |
| Baselineable | Modifier | PrincipalMgmt | User |
| ManagedBaseline | Context | DataAdmin | Container |
| ManagedBaseline | Folder | DataAdmin | Folder |

## OData Query Examples

### Get part with its BOM (children)
```
GET /ProdMgmt/Parts?$expand=Uses($expand=Uses)
```

### Get part with parent assemblies
```
GET /ProdMgmt/Parts?$expand=UsedBy($expand=UsedBy)
```

### Get part with both children and parents
```
GET /ProdMgmt/Parts?$expand=UsedBy,Uses
```

### Get BOM for a specific part
```
GET /ProdMgmt/Parts('{part_id}')/Uses?$expand=Uses
```

### Get parent assemblies for a specific part
```
GET /ProdMgmt/Parts('{part_id}')/UsedBy?$expand=UsedBy
```

### Get part usage with child and parent parts
```
GET /ProdMgmt/PartUsages?$expand=Uses,UsedBy
```

### Get part usage with occurrences
```
GET /ProdMgmt/PartUsages?$expand=Uses,UsedBy,Occurrences
```

### Get substitute parts for a part usage
```
GET /ProdMgmt/PartSubstituteLinks?$expand=SubstitutePart,SubstituteFor($expand=UsedBy)
```

### Get baseline items
```
GET /ProdMgmt/ManagedBaselines?$expand=BaselineItems,Context,Folder
```

### Get baseline with creator/modifier
```
GET /ProdMgmt/Baselineables?$expand=Context,Creator,Modifier
```

### Get snowmobiles with BOM
```
GET /ProdMgmt/Snowmobiles?$expand=Uses($expand=Uses)
```

### Get root structure items
```
GET /ProdMgmt/RootStructureItems?$expand=Uses,UsedBy
```

## Entity Sets

| Entity Set | Entity Type | Description |
|------------|-------------|-------------|
| Parts | Part | All parts |
| PartUsages | PartUse | All part usage links (BOM relationships) |
| PartSubstituteLinks | PartSubstituteLink | All part substitute links |
| Baselineables | Baselineable | All baselineable objects |
| ManagedBaselines | ManagedBaseline | All managed baselines |
| RootStructureItems | RootStructureItems | All root structure items |
| Snowmobiles | Snowmobile | All snowmobile parts |

## Common Query Patterns

### Get full multi-level BOM for a part
```
GET /ProdMgmt/Parts('{part_id}')/Uses?$expand=Uses($expand=Uses($expand=Uses))
```

### Find where a part is used (impact analysis)
```
GET /ProdMgmt/Parts('{part_id}')/UsedBy?$expand=UsedBy($expand=UsedBy)
```

### Get part with all related entities
```
GET /ProdMgmt/Parts('{part_id}')?$expand=Uses($expand=Uses,UsedBy,Occurrences),UsedBy($expand=Uses,UsedBy)
```

### Get all parts in a container with BOM
```
GET /ProdMgmt/Parts?$filter=Context/ID eq '{container_id}'&$expand=Uses($expand=Uses)
```

### Get parts created by a specific user
```
GET /ProdMgmt/Baselineables?$filter=Creator/Name eq 'John Doe'&$expand=Creator,Context
```

### Get substitute parts for a specific part usage
```
GET /ProdMgmt/PartSubstituteLinks?$filter=SubstituteFor/ID eq '{part_usage_id}'&$expand=SubstitutePart,SubstituteFor($expand=Uses,UsedBy)
```