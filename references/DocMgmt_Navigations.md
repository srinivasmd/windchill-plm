# DocMgmt Navigation Properties

This document describes the navigation properties (relationships) between entities in the PTC Document Management OData domain.

## Entity Navigation Properties

### Document

The Document entity is the core entity in Document Management and has the following navigation properties:

| Navigation Property | Target Entity | Type | Read-Only | Contains Target | Description |
|---------------------|---------------|------|-----------|-----------------|-------------|
| `DocUsageLinks` | DocumentUsageLink | Collection | Yes | Yes | Links showing documents that use or are used by this document |
| `Context` | Container | Single | No | No | The container (context) where this document resides |
| `Organization` | Organization | Single | No | No | The organization that owns this document |
| `ReferencedByEngMatCatalogReferenceLink` | EngMatCatalogReferenceLink | Collection | Yes | No | Links to engineering material catalog references |
| `PrimaryContent` | ContentItem | Single | No | Yes | The primary content (file) of this document |
| `Thumbnails` | ContentItem | Collection | No | Yes | Thumbnail images for this document |
| `Creator` | User | Single | Yes | No | The user who created this document |
| `Folder` | Folder | Single | No | No | The folder where this document is stored |
| `Revisions` | Document | Collection | Yes | No | All revisions of this document |
| `Attachments` | ContentItem | Collection | No | Yes | Attached content items |
| `Versions` | Document | Collection | Yes | No | All versions of this document |
| `DescribesEngMatCatalogDescribeLink` | EngMatCatalogDescribeLink | Collection | Yes | No | Engineering material catalog describe links |
| `Representations` | Representation | Collection | Yes | No | Visualization representations |
| `SmallThumbnails` | ContentItem | Collection | No | Yes | Small thumbnail images |
| `Modifier` | User | Single | Yes | No | The user who last modified this document |

### DocumentUsageLink

Represents a usage relationship between two documents.

| Navigation Property | Target Entity | Type | Read-Only | Contains Target | Description |
|---------------------|---------------|------|-----------|-----------------|-------------|
| `DocUsedBy` | Document | Single | Yes | No | The document that uses another document |
| `DocUses` | Document | Single | Yes | No | The document that is being used |

### DocStructure

Represents the hierarchical structure of documents.

| Navigation Property | Target Entity | Type | Read-Only | Contains Target | Description |
|---------------------|---------------|------|-----------|-----------------|-------------|
| `Document` | Document | Single | No | No | The document in this structure node |
| `DocumentUse` | DocumentUse | Single | No | No | The document usage relationship |
| `Structure` | DocStructure | Collection | No | Yes | Child structure nodes |

## Navigation Examples

### Getting Document Revisions

```http
GET /Windchill/servlet/odata/DocMgmt/Documents('OR:wt.doc.WTDocument:12345')/Revisions
```

### Getting Document Creator

```http
GET /Windchill/servlet/odata/DocMgmt/Documents('OR:wt.doc.WTDocument:12345')/Creator
```

### Getting Document Primary Content

```http
GET /Windchill/servlet/odata/DocMgmt/Documents('OR:wt.doc.WTDocument:12345')/PrimaryContent
```

### Getting Document Usage Links

```http
GET /Windchill/servlet/odata/DocMgmt/Documents('OR:wt.doc.WTDocument:12345')/DocUsageLinks
```

### Expanding Navigation Properties in a Query

```http
GET /Windchill/servlet/odata/DocMgmt/Documents?$expand=Creator,Modifier,Folder,Organization
```

## Cross-Domain Navigations

Some navigation properties reference entities from other OData domains:

| Navigation Property | Target Domain | Target Entity |
|---------------------|---------------|---------------|
| `Context` | DataAdmin | Container |
| `Organization` | PrincipalMgmt | Organization |
| `Creator` | PrincipalMgmt | User |
| `Modifier` | PrincipalMgmt | User |
| `Folder` | DataAdmin | Folder |
| `ReferencedByEngMatCatalogReferenceLink` | ConfigurableLinks | EngMatCatalogReferenceLink |
| `DescribesEngMatCatalogDescribeLink` | ConfigurableLinks | EngMatCatalogDescribeLink |
| `Representations` | Visualization | Representation |

## Related Domain References

- **PTC.DataAdmin** - Container and Folder entities
- **PTC.PrincipalMgmt** - User and Organization entities
- **PTC.ConfigurableLinks** - Engineering material catalog links
- **PTC.Visualization** - Representation entities
- **PTC** - Core entities like ContentItem

---

*Generated from PTC DocMgmt OData metadata v7*