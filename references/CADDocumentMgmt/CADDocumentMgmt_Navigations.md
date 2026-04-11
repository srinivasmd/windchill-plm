# CADDocumentMgmt Navigation Properties

This document describes navigation properties for entities in this domain.

## CADDocument

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Uses | CADDocumentUse |  | Yes |
| References | CADDocumentReference |  | Yes |
| DerivedSources | DerivedSource |  | Yes |
| Drawings | CADDocument |  | No |
| Context | Container |  | No |
| Organization | Organization |  | No |
| AllPrimaryContents | ContentItem |  | Yes |
| PartDocAssociations | PartDocAssociation |  | Yes |
| Thumbnails | ContentItem |  | Yes |
| Creator | User |  | No |
| Revisions | CADDocument |  | No |
| Folder | Folder |  | No |
| Attachments | ContentItem |  | Yes |
| Versions | CADDocument |  | No |
| Representations | Representation |  | No |
| SmallThumbnails | ContentItem |  | Yes |
| Modifier | User |  | No |

## MovePartDocAssociation

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| RelatedPart | Part |  | No |
| RelatedCADDoc | CADDocument |  | No |
| SourceCADDoc | CADDocument |  | No |

## PartDocAssociation

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| RelatedPart | Part |  | No |
| RelatedCADDoc | CADDocument |  | No |

## CADDocumentsListReportItem

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| CADDocument | CADDocument |  | No |

## DerivedSource

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| SourceCADDocuments | CADDocument |  | No |

## CADStructure

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| CADDocument | CADDocument |  | No |
| CADDocumentUse | CADDocumentUse |  | No |
| Components | CADStructure |  | Yes |
