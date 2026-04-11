# DocMgmt Navigation Properties

This document describes navigation properties for entities in this domain.

## DocumentUsageLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| DocUsedBy | Document |  | No |
| DocUses | Document |  | No |

## Document

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| DocUsageLinks | DocumentUsageLink |  | Yes |
| Context | Container |  | No |
| Organization | Organization |  | No |
| ReferencedByEngMatCatalogReferenceLink | EngMatCatalogReferenceLink |  | No |
| PrimaryContent | ContentItem |  | Yes |
| Thumbnails | ContentItem |  | Yes |
| Creator | User |  | No |
| Folder | Folder |  | No |
| Revisions | Document |  | No |
| Attachments | ContentItem |  | Yes |
| Versions | Document |  | No |
| DescribesEngMatCatalogDescribeLink | EngMatCatalogDescribeLink |  | No |
| Representations | Representation |  | No |
| SmallThumbnails | ContentItem |  | Yes |
| Modifier | User |  | No |

## DocStructure

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Document | Document |  | No |
| DocumentUse | DocumentUse |  | No |
| Structure | DocStructure |  | Yes |
