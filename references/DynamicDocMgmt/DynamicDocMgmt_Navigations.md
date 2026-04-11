# DynamicDocMgmt Navigation Properties

This document describes navigation properties for entities in this domain.

## DynamicDocumentMember

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `Uses` | `DynamicDocument` | - | No |
| `UsedBy` | `DynamicDocument` | - | No |

**OData $expand Example:**
```
GET /DynamicDocMgmt/DynamicDocumentMembers('{id}')?$expand=Uses,UsedBy
```

## DynamicDocument

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `MemberLinks` | `DynamicDocumentMember` | - | Yes |
| `UsedBy` | `DynamicDocument` | - | No |
| `ReferenceLinks` | `DynamicDocumentReference` | - | Yes |
| `ReferencedBy` | `DynamicDocument` | - | No |
| `Translations` | `DynamicDocument` | - | No |
| `Xliff` | `DynamicDocument` | - | No |
| `Context` | `Container` | - | No |
| `Versions` | `DynamicDocument` | - | No |
| `Organization` | `Organization` | - | No |
| `PrimaryContent` | `ContentItem` | - | Yes |
| `Thumbnails` | `ContentItem` | - | Yes |
| `Creator` | `User` | - | No |
| `Representations` | `Representation` | - | No |
| `SmallThumbnails` | `ContentItem` | - | Yes |
| `Revisions` | `DynamicDocument` | - | No |
| `Folder` | `Folder` | - | No |
| `Attachments` | `ContentItem` | - | Yes |
| `Modifier` | `User` | - | No |

**OData $expand Example:**
```
GET /DynamicDocMgmt/DynamicDocuments('{id}')?$expand=MemberLinks,UsedBy,ReferenceLinks
```

## DynamicDocumentReference

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `References` | `DynamicDocument` | - | No |
| `ReferencedBy` | `DynamicDocument` | - | No |

**OData $expand Example:**
```
GET /DynamicDocMgmt/DynamicDocumentReferences('{id}')?$expand=References,ReferencedBy
```
