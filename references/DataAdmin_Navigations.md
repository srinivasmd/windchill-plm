# DataAdmin Domain - Navigation Properties

This document describes all navigation properties and entity relationships in the DataAdmin domain.

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         PTC.DataAdmin Namespace                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────┐                                                   │
│   │   Container     │◄──────────┐                                       │
│   │  (Base Entity)  │           │                                       │
│   ├─────────────────┤           │                                       │
│   │ - Folders       │           │                                       │
│   │ - Creator       │           │                                       │
│   │ - Organization  │           │                                       │
│   └────┬───────┬────┘           │                                       │
│        │       │                │                                       │
│   ┌────┘       └────┐           │                                       │
│   │                  │           │                                       │
│   ▼                  ▼           │                                       │
│ ┌─────────┐    ┌──────────────┐  │                                       │
│ │Product  │    │   Project    │  │                                       │
│ │Container│    │  Container   │  │                                       │
│ ├─────────┤    ├──────────────┤  │                                       │
│ │+OptionSet │   │              │  │                                       │
│ │+PoolAliases│  │              │  │                                       │
│ │+OptionPool │  │              │  │                                       │
│ └─────────┘    └──────────────┘  │                                       │
│                                   │                                       │
│   ┌─────────┐    ┌──────────────┐│                                       │
│  │ Library  │    │Organization  ││                                       │
│  │Container │    │  Container   ││                                       │
│  ├─────────┤    ├──────────────┤│                                       │
│  │+OptionSet │   │              ││                                       │
│  │+PoolAliases│  │              ││                                       │
│  │+OptionPool │  │              ││                                       │
│  └─────────┘    └──────────────┘│                                       │
│                                   │                                       │
│   ┌─────────┐                     │                                       │
│   │   Site  │─────────────────────┘                                       │
│   └─────────┘                                                              │
│                                                                           │
│   ┌─────────────────┐                                                      │
│   │     Folder      │                                                      │
│   ├─────────────────┤                                                      │
│   │ - Folders       │ (self-referencing)                                  │
│   │ - Contents      │ → FolderContent                                    │
│   │ - FolderContents│ → WindchillEntity                                   │
│   └─────────────────┘                                                      │
│                                                                           │
│   ┌─────────────────┐                                                      │
│   │   Participant   │                                                      │
│   ├─────────────────┤                                                      │
│   │ - Principals    │ → PrincipalMgmt.Principal                          │
│   └─────────────────┘                                                      │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

## Navigation Properties by Entity

### Container
| Navigation | Type | Description |
|------------|------|-------------|
| Folders | Collection(PTC.DataAdmin.Folder) | Child folders within this container |
| Creator | PTC.PrincipalMgmt.User | User who created this container |
| Organization | PTC.PrincipalMgmt.Organization | Organization associated with this container |

### ProductContainer (extends Container)
| Navigation | Type | Description |
|------------|------|-------------|
| AssignedOptionSet | PTC.ProdPlatformMgmt.OptionSet | Option set assigned to this product |
| OptionPoolAliases | Collection(PTC.ProdPlatformMgmt.ExpressionAlias) | Option pool aliases for this product |
| OptionPool | Collection(PTC.ProdPlatformMgmt.OptionPoolItem) | Option pool items for this product |

### ProjectContainer (extends Container)
| Navigation | Type | Description |
|------------|------|-------------|
| *(Inherits all navigations from Container)* | | |

### LibraryContainer (extends Container)
| Navigation | Type | Description |
|------------|------|-------------|
| AssignedOptionSet | PTC.ProdPlatformMgmt.OptionSet | Option set assigned to this library |
| OptionPoolAliases | Collection(PTC.ProdPlatformMgmt.ExpressionAlias) | Option pool aliases for this library |
| OptionPool | Collection(PTC.ProdPlatformMgmt.OptionPoolItem) | Option pool items for this library |

### OrganizationContainer (extends Container)
| Navigation | Type | Description |
|------------|------|-------------|
| *(Inherits all navigations from Container)* | | |

### Site (extends Container)
| Navigation | Type | Description |
|------------|------|-------------|
| *(Inherits all navigations from Container)* | | |

### Folder
| Navigation | Type | Description |
|------------|------|-------------|
| Folders | Collection(PTC.DataAdmin.Folder) | Child folders within this folder (self-referencing) |
| Contents | Collection(PTC.DataAdmin.FolderContent) | Folder contents |
| FolderContents | Collection(PTC.WindchillEntity) | All Windchill entities in this folder |

### Participant
| Navigation | Type | Description |
|------------|------|-------------|
| Principals | Collection(PTC.PrincipalMgmt.Principal) | Principals associated with this participant |

## Cross-Domain References

The DataAdmin domain has navigation properties that reference entities from other domains:

| From Entity | Navigation Property | Target Domain | Target Entity |
|-------------|---------------------|---------------|---------------|
| Container | Creator | PrincipalMgmt | User |
| Container | Organization | PrincipalMgmt | Organization |
| ProductContainer | AssignedOptionSet | ProdPlatformMgmt | OptionSet |
| ProductContainer | OptionPoolAliases | ProdPlatformMgmt | ExpressionAlias |
| ProductContainer | OptionPool | ProdPlatformMgmt | OptionPoolItem |
| LibraryContainer | AssignedOptionSet | ProdPlatformMgmt | OptionSet |
| LibraryContainer | OptionPoolAliases | ProdPlatformMgmt | ExpressionAlias |
| LibraryContainer | OptionPool | ProdPlatformMgmt | OptionPoolItem |
| Folder | FolderContents | PTC Core | WindchillEntity |
| Participant | Principals | PrincipalMgmt | Principal |

## OData Query Examples

### Get container with creator
```
GET /DataAdmin/Containers?$expand=Creator
```

### Get folder with subfolders and contents
```
GET /DataAdmin/Folders?$expand=Folders,Contents,FolderContents
```

### Get product with option set
```
GET /DataAdmin/Products?$expand=AssignedOptionSet,OptionPool
```

### Get participant with principals
```
GET /DataAdmin/Participants?$expand=Principals
```

### Get site with folders
```
GET /DataAdmin/Sites?$expand=Folders($expand=Folders)
```

### Get folder contents by location
```
GET /DataAdmin/Folders?$filter=Location eq '/Default'&$expand=FolderContents
```

### Get containers with organization
```
GET /DataAdmin/Containers?$expand=Organization
```

## Entity Sets

| Entity Set | Entity Type | Description |
|------------|-------------|-------------|
| Containers | Container | All containers |
| Folders | Folder | All folders |
| Participants | Participant | All participants |
| Sites | Site | All sites |
| Products | ProductContainer | All product containers |
| Libraries | LibraryContainer | All library containers |
| Projects | ProjectContainer | All project containers |
| Organizations | OrganizationContainer | All organization containers |