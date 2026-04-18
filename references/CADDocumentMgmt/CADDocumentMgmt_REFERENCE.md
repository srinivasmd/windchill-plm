---
Domain: CADDocumentMgmt
Client: `from domains.CADDocumentMgmt import CADDocumentMgmtClient`
---

> **Use the CADDocumentMgmtClient**: `from domains.CADDocumentMgmt import CADDocumentMgmtClient`
>
> This reference documents the entity types and properties. For programmatic access, use the domain client.

# CAD Document Management Domain Reference

## Base URL
```
https://windchill.example.com/Windchill/servlet/odata/CADDocumentMgmt/
```

## Metadata URL
```
https://windchill.example.com/Windchill/servlet/odata/CADDocumentMgmt/$metadata
```

## Domain Overview
The CAD Document Management domain provides access to CAD documents and their relationships in Windchill including:

### CAD Document Types
- **CADDocument** - Base CAD document entity
- **ECADDocument** - ECAD (Electronic CAD) documents
- **ECADBoard** - ECAD board documents
- **ECADSchematic** - ECAD schematic documents
- **ECADDerived** - ECAD derived documents
- **ECADDefinition** - ECAD definition documents
- **ElectricalSchematic** - Electrical schematic documents
- **PTCProxyCADDocument** - PTC proxy CAD documents

### CAD Document Relationships
- **CADDocumentReference** - CAD document references (dependencies)
- **CADDocumentUse** - CAD document uses (components)
- **DerivedSource** - Derived source links
- **PartDocAssociation** - CAD Document to Part associations
- **CADStructure** - CAD structure hierarchy
- **MovePartDocAssociation** - Move part-doc association wrapper

### Reporting
- **CADDocumentsListReportItem** - Parts list report items

---

## Entity Types

### CADDocument

**Endpoint:** `/CADDocumentMgmt/CADDocuments`
**Operations:** `READ`

**Properties:**
| Property | Type | Description |
|----------|------|-------------|
| ID | String | Object identifier (OID) |
| Name | String | CAD document name |
| Number | String | CAD document number |
| FileName | String | File name (Required) |
| Description | String | Description |
| Revision | String | Revision (ReadOnly) |
| Version | String | Version (ReadOnly) |
| VersionID | String | Version ID (ReadOnly) |
| MasterID | String | Master ID (ReadOnly) |
| Latest | Boolean | Is latest version (ReadOnly) |
| Identity | String | Identity (ReadOnly) |
| State | EnumType | Lifecycle state (ReadOnly) |
| LifeCycleTemplateName | String | Lifecycle template name (ReadOnly) |
| Category | EnumType | CAD document category (Required) |
| SubCategory | EnumType | CAD document subcategory |
| AuthoringApplication | EnumType | Authoring application |
| OwnerApplication | EnumType | Owner application (ReadOnly) |
| AuthAppVersion | Int32 | Authoring application version (ReadOnly) |
| CADMass | QuantityOfMeasureType | CAD mass |
| CADVolume | QuantityOfMeasureType | CAD volume |
| Material | String | Material |
| CheckOutStatus | String | Check out status (ReadOnly) |
| CheckoutState | String | Checkout state (ReadOnly) |
| Comments | String | Comments (ReadOnly) |
| CreatedBy | String | Created by (ReadOnly) |
| ModifiedBy | String | Modified by (ReadOnly) |
| CreatedOn | DateTime | Created timestamp (ReadOnly) |
| LastModified | DateTime | Last modified timestamp (ReadOnly) |
| OrganizationName | String | Organization name (ReadOnly) |
| FolderName | String | Folder name (ReadOnly) |
| FolderLocation | String | Folder location (ReadOnly) |
| Derived | Boolean | Is derived |
| Generic | Boolean | Is generic (ReadOnly) |
| Instance | Boolean | Is instance (ReadOnly) |
| Verified | Boolean | Is verified |
| MissingDependents | Boolean | Has missing dependents |
| FamilyTableStatus | Int32 | Family table status (ReadOnly) |
| PHANTOM | Boolean | Is phantom |
| REFERENCE | Boolean | Is reference |
| PARTNUMBER | String | Part number |
| REV | String | Revision |
| NDVersion | String | ND version (ReadOnly) |
| WorkInProgressState | WorkInProgressType | Work in progress state (ReadOnly) |
| ChangeStatus | Icon | Change status (ReadOnly) |
| GeneralStatus | Icon | General status (ReadOnly) |
| ShareStatus | Icon | Share status (ReadOnly) |
| TypeDisplayName | String | Type display name (ReadOnly) |
| TypeIcon | Icon | Type icon (ReadOnly) |
| ObjectType | String | Object type (ReadOnly) |

**Navigation Properties:**
- Context - Container (PTC.DataAdmin.Container)
- Organization - Organization (PTC.PrincipalMgmt.Organization)
- Folder - Folder (PTC.DataAdmin.Folder)
- Creator - Creator user (PTC.PrincipalMgmt.User)
- Modifier - Modifier user (PTC.PrincipalMgmt.User)
- Uses - CAD document uses (Collection of CADDocumentUse)
- References - CAD document references (Collection of CADDocumentReference)
- DerivedSources - Derived sources (Collection of DerivedSource)
- Drawings - Drawings (Collection of CADDocument)
- Revisions - Revisions (Collection of CADDocument)
- Versions - Versions (Collection of CADDocument)
- PartDocAssociations - Part-doc associations (Collection of PartDocAssociation)
- AllPrimaryContents - Primary contents (Collection of ContentItem)
- Attachments - Attachments (Collection of ContentItem)
- Thumbnails - Thumbnails (Collection of ContentItem)
- SmallThumbnails - Small thumbnails (Collection of ContentItem)
- Representations - Representations (Collection of PTC.Visualization.Representation)

**Query Operations:**
```
GET /CADDocumentMgmt/CADDocuments
GET /CADDocumentMgmt/CADDocuments('{id}')
GET /CADDocumentMgmt/CADDocuments?$filter=Number eq '12345'
GET /CADDocumentMgmt/CADDocuments?$filter=Name eq 'MyAssembly'
GET /CADDocumentMgmt/CADDocuments?$filter=contains(Number, '123') or contains(Name, 'Assembly')
GET /CADDocumentMgmt/CADDocuments?$filter=Category/Value eq 'ASSEMBLY'
GET /CADDocumentMgmt/CADDocuments?$filter=State/Value eq 'RELEASED'
GET /CADDocumentMgmt/CADDocuments?$filter=Latest eq true
GET /CADDocumentMgmt/CADDocuments('{id}')?$expand=Context
GET /CADDocumentMgmt/CADDocuments('{id}')?$expand=Folder
GET /CADDocumentMgmt/CADDocuments('{id}')?$expand=Uses
GET /CADDocumentMgmt/CADDocuments('{id}')?$expand=References
GET /CADDocumentMgmt/CADDocuments('{id}')?$expand=PartDocAssociations
GET /CADDocumentMgmt/CADDocuments('{id}')?$expand=Drawings
GET /CADDocumentMgmt/CADDocuments('{id}')?$expand=Representations
GET /CADDocumentMgmt/CADDocuments?$select=ID,Name,Number,FileName,State,Category
GET /CADDocumentMgmt/CADDocuments?$top=100
GET /CADDocumentMgmt/CADDocuments?$orderby=Name asc
```

---

### ECADDocument

**Endpoint:** `/CADDocumentMgmt/CADDocuments` (filtered by type)
**Operations:** `READ`

 Inherits all properties from CADDocument plus:

| Property | Type | Description |
|----------|------|-------------|
| ADWBlockLibPath | String | ADW block library path |
| ADWFlowType | String | ADW flow type |
| ADWMetadataVersion | String | ADW metadata version |
| ADWRootDesign | String | ADW root design |
| ADWType | String | ADW type |
| PTC_ECAD_ADW_MANAGED_DESIGN | Boolean | PTC ECAD ADW managed design |
| PTC_ECAD_ASSEMBLY_PART_NAME | String | PTC ECAD assembly part name |
| PTC_ECAD_ASSEMBLY_PART_NUMBER | String | PTC ECAD assembly part number |
| PTC_ECAD_BOARD_PART_NAME | String | PTC ECAD board part name |
| PTC_ECAD_BOARD_PART_NUMBER | String | PTC ECAD board part number |

**Query Operations:**
```
GET /CADDocumentMgmt/CADDocuments?$filter=ObjectType eq 'wt.epm.EPMDocument' and Category/Value eq 'ECAD'
```

---

### ECADBoard

**Endpoint:** `/CADDocumentMgmt/CADDocuments` (filtered by type)
**Operations:** `READ`

 Inherits all properties from ECADDocument

**Query Operations:**
```
GET /CADDocumentMgmt/CADDocuments?$filter=ObjectType eq 'wt.epm.EPMDocument' and Category/Value eq 'ECAD_BOARD'
```

---

### ECADSchematic

**Endpoint:** `/CADDocumentMgmt/CADDocuments` (filtered by type)
**Operations:** `READ`

 Inherits all properties from ECADDocument

**Query Operations:**
```
GET /CADDocumentMgmt/CADDocuments?$filter=ObjectType eq 'wt.epm.EPMDocument' and Category/Value eq 'ECAD_SCHEMATIC'
```

---

### ECADDerived

**Endpoint:** `/CADDocumentMgmt/CADDocuments` (filtered by type)
**Operations:** `READ`

 Inherits all properties from ECADDocument plus:

| Property | Type | Description |
|----------|------|-------------|
| ECADAssemblies | Collection(String) | ECAD assemblies |

**Query Operations:**
```
GET /CADDocumentMgmt/CADDocuments?$filter=ObjectType eq 'wt.epm.EPMDocument' and Category/Value eq 'ECAD_DERIVED'
```

---

### ECADDefinition

**Endpoint:** `/CADDocumentMgmt/CADDocuments` (filtered by type)
**Operations:** `READ`

 Inherits all properties from ECADDocument

**Query Operations:**
```
GET /CADDocumentMgmt/CADDocuments?$filter=ObjectType eq 'wt.epm.EPMDocument' and Category/Value eq 'ECAD_DEFINITION'
```

---

### ElectricalSchematic

**Endpoint:** `/CADDocumentMgmt/CADDocuments` (filtered by type)
**Operations:** `READ`

 Inherits all properties from ECADDocument

**Query Operations:**
```
GET /CADDocumentMgmt/CADDocuments?$filter=ObjectType eq 'wt.epm.EPMDocument' and Category/Value eq 'ELECTRICAL_SCHEMATIC'
```

---

### PTCProxyCADDocument

**Endpoint:** `/CADDocumentMgmt/CADDocuments` (filtered by type)
**Operations:** `READ`

 Inherits all properties from CADDocument plus:

| Property | Type | Description |
|----------|------|-------------|
| PTC_PART_NUMBER | String | PTC part number |
| PTC_SYNC_DATA | String | PTC sync data |

**Query Operations:**
```
GET /CADDocumentMgmt/CADDocuments?$filter=ObjectType eq 'wt.epm.EPMDocument' and Category/Value eq 'PTC_PROXY'
```

---

### CADDocumentReference

**Endpoint:** Navigation property from CADDocument
**Operations:** `READ`

**Properties:**
| Property | Type | Description |
|----------|------|-------------|
| ID | String | Object identifier (OID) |
| DepType | DepTypeInfo | Dependency type |
| ECADHookEnabled | Collection(Boolean) | ECAD hook enabled |
| MergeContent | Collection(Boolean) | Merge content |
| MergeRefDes | Collection(Boolean) | Merge reference designators |
| ObjectType | String | Object type (ReadOnly) |
| PartNumberRule | Collection(Int64) | Part number rule |
| ReferenceInfo | CADDocumentDependencyMaster | Reference info |
| Required | Boolean | Is required |
| RetrieveVariants | Collection(Boolean) | Retrieve variants |
| ReviewUndefined | Collection(Boolean) | Review undefined |

**Navigation Properties:**
- CADDocument - Referenced CAD document

**Query Operations:**
```
GET /CADDocumentMgmt/CADDocuments('{id}')/References
GET /CADDocumentMgmt/CADDocuments('{id}')/References?$expand=CADDocument
```

---

### CADDocumentUse

**Endpoint:** Navigation property from CADDocument
**Operations:** `READ`

**Properties:**
| Property | Type | Description |
|----------|------|-------------|
| ID | String | Object identifier (OID) |
| ComponentName | String | Component name |
| DepType | DepTypeInfo | Dependency type |
| FeatureID | Int32 | Feature ID |
| FeatureNumber | Int32 | Feature number |
| HasFixedConstraint | Boolean | Has fixed constraint |
| LNO | Int64 | Line number |
| LayerID | Int32 | Layer ID |
| Location | TransformLocation | Transform location |
| ObjectType | String | Object type (ReadOnly) |
| Placed | Boolean | Is placed |
| Quantity | Double | Quantity |
| Required | Boolean | Is required |
| Suppressed | Boolean | Is suppressed |
| Unit | EnumType | Unit |
| UseInfo | CADDocumentDependencyMaster | Use info |

**Query Operations:**
```
GET /CADDocumentMgmt/CADDocuments('{id}')/Uses
GET /CADDocumentMgmt/CADDocuments('{id}')/Uses?$expand=CADDocument
GET /CADDocumentMgmt/CADDocuments('{id}')/Uses?$filter=Suppressed eq false
```

---

### DerivedSource

**Endpoint:** Navigation property from CADDocument
**Operations:** `READ`

**Properties:**
| Property | Type | Description |
|----------|------|-------------|
| ID | String | Object identifier (OID) |
| ObjectType | String | Object type (ReadOnly) |
| SourceCADDocument | CADDocument | Source CAD document |

**Query Operations:**
```
GET /CADDocumentMgmt/CADDocuments('{id}')/DerivedSources
GET /CADDocumentMgmt/CADDocuments('{id}')/DerivedSources?$expand=SourceCADDocument
```

---

### PartDocAssociation

**Endpoint:** Navigation property from CADDocument
**Operations:** `READ`

**Properties:**
| Property | Type | Description |
|----------|------|-------------|
| ID | String | Object identifier (OID) |
| CADDocument | CADDocument | Associated CAD document |
| CADDocumentName | String | CAD document name |
| CADDocumentNumber | String | CAD document number |
| CADDocumentFileName | String | CAD document file name |
| CADDocumentID | String | CAD document ID |
| CADDocumentMasterID | String | CAD document master ID |
| CADDocumentIdentity | String | CAD document identity |
| CADDocumentState | Object | CAD document state |
| CADDocumentLatest | Boolean | CAD document latest |
| CADDocumentVersion | String | CAD document version |
| CADDocumentRevision | String | CAD document revision |
| CADDocumentCategory | Object | CAD document category |
| CADDocumentAuthoringApplication | Object | CAD document authoring application |
| CADDocumentOwnerApplication | Object | CAD document owner application |
| Part | Part | Associated Part |
| PartName | String | Part name |
| PartNumber | String | Part number |
| PartID | String | Part ID |
| PartMasterID | String | Part master ID |
| PartIdentity | String | Part identity |
| PartState | Object | Part state |
| PartLatest | Boolean | Part latest |
| PartVersion | String | Part version |
| PartRevision | String | Part revision |
| PartUnit | Object | Part unit |
| PartDefaultUnit | Object | Part default unit |
| PartFamilyTableStatus | Int32 | Part family table status |
| ObjectType | String | Object type (ReadOnly) |
| CreatedBy | String | Created by |
| CreatedOn | DateTime | Created timestamp |

**Query Operations:**
```
GET /CADDocumentMgmt/CADDocuments('{id}')/PartDocAssociations
GET /CADDocumentMgmt/CADDocuments('{id}')/PartDocAssociations?$expand=Part,CADDocument
```

---

### CADStructure

**Endpoint:** Navigation property for CAD structure
**Operations:** `READ`

CAD structure hierarchy linking CAD documents together.

**Query Operations:**
```
GET /CADDocumentMgmt/CADDocuments('{id}')/CADStructure
```

---

### MovePartDocAssociation

**Endpoint:** Navigation property for move part-doc association wrapper
**Operations:** `READ`

Move part-doc association wrapper entity.

**Query Operations:**
```
GET /CADDocumentMgmt/CADDocuments('{id}')/MovePartDocAssociation
```

---

### CADDocumentsListReportItem

**Endpoint:** Navigation property for parts list report items
**Operations:** `READ`

Parts list report items for CAD documents.

---

## Complex Types

### DepTypeInfo

Dependency type information.

### CADDocumentDependencyMaster

CAD document dependency master information.

### TransformLocation

Transform location information for CAD document uses.

### Icon

Icon type for status indicators.

### QuantityOfMeasureType

Quantity with unit of measure.

### WorkInProgressType

Work in progress state type.

---

## Common Query Examples

### Filter CAD Documents by Category
```
GET /CADDocumentMgmt/CADDocuments?$filter=Category/Value eq 'ASSEMBLY'
GET /CADDocumentMgmt/CADDocuments?$filter=Category/Value eq 'PART'
GET /CADDocumentMgmt/CADDocuments?$filter=Category/Value eq 'DRAWING'
```

### Filter CAD Documents by State
```
GET /CADDocumentMgmt/CADDocuments?$filter=State/Value eq 'RELEASED'
GET /CADDocumentMgmt/CADDocuments?$filter=State/Value eq 'WORKING'
```

### Get Latest CAD Documents Only
```
GET /CADDocumentMgmt/CADDocuments?$filter=Latest eq true
```

### Search CAD Documents
```
GET /CADDocumentMgmt/CADDocuments?$filter=contains(Number, '123')
GET /CADDocumentMgmt/CADDocuments?$filter=contains(Name, 'Assembly')
GET /CADDocumentMgmt/CADDocuments?$filter=contains(Description, 'motor')
```

### Get CAD Document with Full Details
```
GET /CADDocumentMgmt/CADDocuments('{id}')?$expand=Context,Folder,Organization,Creator,Modifier,Uses,References,PartDocAssociations,Drawings,Representations
```

### Get CAD Document Structure
```
GET /CADDocumentMgmt/CADDocuments('{id}')/Uses?$expand=CADDocument($expand=Uses)
```

### Get CAD Document by Authoring Application
```
GET /CADDocumentMgmt/CADDocuments?$filter=AuthoringApplication/Value eq 'PROE'
```