# CADDocumentMgmt Domain - Entity Navigation Properties

This document describes the navigation properties between entities in the CADDocumentMgmt domain.

## CADDocument

**Description**: Entity representing the CAD Document

| Navigation Property | Type | Description |
|---------------------|------|-------------|
| Uses | Collection(CADDocumentUse) | CAD Documents this CAD document uses (children/dependencies) |
| References | Collection(CADDocumentReference) | CAD Document references |
| DerivedSources | Collection(DerivedSource) | Derived source CAD documents |
| Drawings | Collection(CADDocument) | Associated drawings |
| Context | Container (DataAdmin) | Container context |
| Organization | Organization (PrincipalMgmt) | Organization |
| AllPrimaryContents | Collection(ContentItem) | Primary contents |
| PartDocAssociations | Collection(PartDocAssociation) | Part-Document associations |
| Thumbnails | Collection(ContentItem) | Thumbnail images |
| Creator | User (PrincipalMgmt) | Creator user |
| Revisions | Collection(CADDocument) | All revisions |
| Folder | Folder (DataAdmin) | Folder location |
| Attachments | Collection(ContentItem) | Attachments |
| Versions | Collection(CADDocument) | All versions |
| Representations | Collection(Representation) (Visualization) | Visualization representations |
| SmallThumbnails | Collection(ContentItem) | Small thumbnail images |
| Modifier | User (PrincipalMgmt) | Modifier user |

## CADDocumentUse

**Description**: CAD Document Uses Link

| Navigation Property | Type | Description |
|---------------------|------|-------------|
| *(None)* | - | - |

## CADDocumentReference

**Description**: CAD Document References Link

| Navigation Property | Type | Description |
|---------------------|------|-------------|
| *(None)* | - | - |

## PartDocAssociation

**Description**: CAD Document Related Parts link

| Navigation Property | Type | Description |
|---------------------|------|-------------|
| RelatedPart | Part (ProdMgmt) | Associated Part |
| RelatedCADDoc | CADDocument | Associated CAD Document |

## DerivedSource

**Description**: Link from the given image CAD Document to the synchronized version of the source

| Navigation Property | Type | Description |
|---------------------|------|-------------|
| SourceCADDocuments | CADDocument | Source CAD documents |

## CADStructure

**Description**: CAD Structure

| Navigation Property | Type | Description |
|---------------------|------|-------------|
| CADDocument | CADDocument | CAD Document |
| CADDocumentUse | CADDocumentUse | CAD Document Use |
| Components | Collection(CADStructure) | Child components |

## CADDocumentsListReportItem

**Description**: Parts List Report

| Navigation Property | Type | Description |
|---------------------|------|-------------|
| CADDocument | CADDocument | CAD Document |

## MovePartDocAssociation

**Description**: CAD Document along with its associations to move

| Navigation Property | Type | Description |
|---------------------|------|-------------|
| RelatedPart | Part (ProdMgmt) | Related Part |
| RelatedCADDoc | CADDocument | Related CAD Document |
| SourceCADDoc | CADDocument | Source CAD Document |

## ECADDocument (extends CADDocument)

**Description**: Generated from type com.ptc.ECADDocument

| Navigation Property | Type | Description |
|---------------------|------|-------------|
| *(Inherits from CADDocument)* | - | - |

## ECADBoard (extends ECADDocument)

**Description**: Generated from type com.ptc.ECADBoard

| Navigation Property | Type | Description |
|---------------------|------|-------------|
| *(Inherits from ECADDocument)* | - | - |

## ECADDerived (extends ECADDocument)

**Description**: Generated from type com.ptc.ECADDerived

| Navigation Property | Type | Description |
|---------------------|------|-------------|
| *(Inherits from ECADDocument)* | - | - |

## ECADSchematic (extends ECADDocument)

**Description**: Generated from type com.ptc.ECADSchematic

| Navigation Property | Type | Description |
|---------------------|------|-------------|
| *(Inherits from ECADDocument)* | - | - |

## ECADDefinition (extends ECADDocument)

**Description**: Generated from type com.ptc.ECADDefinition

| Navigation Property | Type | Description |
|---------------------|------|-------------|
| *(Inherits from ECADDocument)* | - | - |

## ElectricalSchematic (extends ECADDocument)

**Description**: Generated from type com.ptc.ElectricalSchematic

| Navigation Property | Type | Description |
|---------------------|------|-------------|
| *(Inherits from ECADDocument)* | - | - |

## PTCProxyCADDocument (extends CADDocument)

**Description**: Generated from type com.ptc.PTCProxyCADDocument

| Navigation Property | Type | Description |
|---------------------|------|-------------|
| *(Inherits from CADDocument)* | - | - |

## Cross-Domain Navigation

The CADDocumentMgmt domain has navigation properties to the following domains:
- **DataAdmin**: Container, Folder
- **PrincipalMgmt**: Organization, User
- **ProdMgmt**: Part
- **Visualization**: Representation

## OData Query Examples

### Get CAD Document with Uses (children)
```
GET /CADDocumentMgmt/CADDocuments?$filter=Number eq '12345'&$expand=Uses
```

### Get CAD Document with Part Associations
```
GET /CADDocumentMgmt/CADDocuments?$filter=Number eq '12345'&$expand=PartDocAssociations($expand=RelatedPart)
```

### Get CAD Document Structure
```
GET /CADDocumentMgmt/CADDocuments?$filter=Number eq '12345'&$expand=Uses($expand=CADDocument)
```

### Get CAD Document with Thumbnails
```
GET /CADDocumentMgmt/CADDocuments?$filter=Number eq '12345'&$expand=Thumbnails
```

### Get CAD Document with Folder and Creator
```
GET /CADDocumentMgmt/CADDocuments?$filter=Number eq '12345'&$expand=Folder,Creator
```