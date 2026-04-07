# Service Information Management Domain (ServiceInfoMgmt) Reference

This domain provides access to Windchill Service Information Management entities for creating, managing, and publishing service documentation including information structures, documents, graphical/textual elements, and publications.

## ServiceInfoMgmt API Endpoint

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/ServiceInfoMgmt/
```

## Metadata

OData metadata is available at:
```
GET /ServiceInfoMgmt/$metadata
```

## OData Version

The ServiceInfoMgmt domain uses OData v6.

## ServiceInfoMgmt Domain Entities

The ServiceInfoMgmt domain includes the following main entity types:

| Entity | Description | Operations |
|--------|-------------|------------|
| **SIMDocuments** | Service Information Management documents | READ |
| **InformationStructures** | Information structures (parts for structuring service info) | READ |
| **InformationGroups** | Information groups (organizational containers) | READ |
| **PublicationStructures** | Publication structures (managing publication output) | READ |
| **SIMDynamicDocuments** | SIM Dynamic Documents | READ |
| **TextualInformationElements** | Textual information elements (text content) | READ |
| **DocumentInformationElements** | Document information elements (linked to SIMDocuments) | READ |
| **GraphicalInformationElements** | Graphical information elements (images, graphics) | READ |
| **PublicationSections** | Publication sections (parts of publications) | READ |
| **Indexes** | Indexes (table of contents, cross-references) | READ |
| **GenericInformationElements** | Generic information elements | READ |
| **TableOfContents** | Table of contents | READ |
| **InformationBaseObject** | Base entity for SIM objects | READ |
| **InformationUsageLink** | Links between information objects | READ |
| **Structure** | Generic structure | READ |
| **PublicationStructure** | Publication structure | READ |
| **DynamicDocumentInformationElement** | Base for dynamic information elements | READ |

## Entity Collections

| Collection | Entity Type |
|------------|-------------|
| SIMDocuments | PTC.ServiceInfoMgmt.SIMDocument |
| InformationStructures | PTC.ServiceInfoMgmt.InformationStructure |
| InformationGroups | PTC.ServiceInfoMgmt.InformationGroup |
| PublicationStructures | PTC.ServiceInfoMgmt.PublicationStructure |
| SIMDynamicDocuments | PTC.ServiceInfoMgmt.SIMDynamicDocument |
| TextualInformationElements | PTC.ServiceInfoMgmt.TextualInformationElement |
| DocumentInformationElements | PTC.ServiceInfoMgmt.DocumentInformationElement |
| GraphicalInformationElements | PTC.ServiceInfoMgmt.GraphicalInformationElement |
| PublicationSections | PTC.ServiceInfoMgmt.PublicationSection |
| Indexes | PTC.ServiceInfoMgmt.Indexes |
| GenericInformationElements | PTC.ServiceInfoMgmt.GenericInformationElement |
| TableOfContents | PTC.ServiceInfoMgmt.TableOfContent |

## Actions (Summary)

The ServiceInfoMgmt domain has extensive action support (94+ actions) including:

| Action | Target | Description |
|--------|--------|-------------|
| UploadStage3Action | Various | Upload stage 3 content |
| UploadStage1Action | Various | Upload stage 1 content |
| GetDocStructure | SIMDocuments | Get document structure |
| Revise | Various | Revise entity |
| SetState | Various | Set lifecycle state |
| CheckIn | Various | Check in entity |
| CheckOut | Various | Check out entity |
| UndoCheckOut | Various | Undo check out |
| GetStructure | InformationStructures | Get structure |

## Entity Details

### SIMDocument

Service Information Management documents (extends WTDocument from DocMgmt).

**Common Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Number** | String | Document number |
| **Name** | String | Document name |
| **Description** | String | Document description |
| **State** | EnumType | Lifecycle state |
| **Revision** | String | Revision |
| **Version** | String | Version |
| **Identity** | String | Display identity |
| **DocTypeName** | String | Document type name |
| **FolderLocation** | String | Folder location path |
| **CreatedBy** | String | Creator username |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- **InformationElement** → Collection(DocumentInformationElement) (Linked information elements)

### InformationStructure

Information structures are parts used for organizing and structuring service information (extends WTPart).

**Common Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Number** | String | Information structure number |
| **Name** | String | Information structure name |
| **TranslationName** | String | Translated name |
| **Identity** | String | Display identity |
| **State** | EnumType | Lifecycle state |
| **Revision** | String | Revision |
| **Version** | String | Version |
| **View** | String | View (Service, Manufacturing) |
| **AuthoringLanguage** | EnumType | Authoring language |
| **ServiceDescription** | String | Service description |
| **EndItem** | Boolean | Is end item |
| **AssemblyMode** | EnumType | Assembly mode |
| **Source** | EnumType | Source (make/buy) |
| **DefaultContentLocation** | String | Default content location path |
| **HasRepresentation** | Boolean | Has representation |
| **IsPrimary** | Boolean | Is primary structure |
| **IsTemplate** | Boolean | Is template |
| **DefaultUnit** | EnumType | Default unit |
| **ExcludeContentFromOutput** | Boolean | Exclude content from output |
| **ExcludeTitleFromTableOfContents** | Boolean | Exclude title from TOC |

**Navigation Properties:**
- Inherits navigation from WTPart (PartUsages, etc.)

### InformationGroup

Information groups for organizing information elements.

**Common Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **DefaultContentLocation** | String | Default content location path |
| **HasRepresentation** | Boolean | Has representation |
| **Representation** | String | Representation |

### PublicationStructure

Publication structures for managing publication output.

**Common Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Number** | String | Publication structure number |
| **Name** | String | Publication structure name |
| **Identity** | String | Display identity |
| **State** | EnumType | Lifecycle state |
| **DefaultContentLocation** | String | Default content location path |
| **IsTemplate** | Boolean | Is template |
| **ApplyTitleFromContent** | Boolean | Apply title from content |

### InformationElement Types

#### TextualInformationElement

Textual information elements (text content for service documentation).

**Common Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **SisContentholderIterationInfoModifier** | String | Iteration info modifier |
| **SisContentholderTitleFromContent** | Boolean | Title from content flag |
| **SisContentholderType** | String | Content holder type |

**Navigation Properties:**
- **Content** → SIMDynamicDocument (Parent dynamic document)

#### DocumentInformationElement

Document information elements (references to SIMDocuments).

**Common Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **SisContentholderIterationInfoModifier** | String | Iteration info modifier |
| **SisContentholderTitleFromContent** | Boolean | Title from content flag |
| **SisContentholderType** | String | Content holder type |
| **Symptoms** | String | Associated symptoms |

**Navigation Properties:**
- **Content** → SIMDocument (Referenced document)

#### GraphicalInformationElement

Graphical information elements (images, graphics, diagrams).

**Common Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **SisContentholderIterationInfoModifier** | String | Iteration info modifier |
| **SisContentholderTitleFromContent** | Boolean | Title from content flag |
| **SisContentholderType** | String | Content holder type |

**Navigation Properties:**
- **Content** → SIMDynamicDocument (Parent dynamic document)

## Common Query Patterns

### Get All SIMDocuments

```bash
GET /ServiceInfoMgmt/SIMDocuments
```

### Get All InformationStructures

```bash
GET /ServiceInfoMgmt/InformationStructures
```

### Get All InformationGroups

```bash
GET /ServiceInfoMgmt/InformationGroups
```

### Get All PublicationStructures

```bash
GET /ServiceInfoMgmt/PublicationStructures
```

### Get SIMDocument by ID

```bash
GET /ServiceInfoMgmt/SIMDocuments('OR:wt.doc.WTDocument:12345')
```

### Get InformationStructure by ID

```bash
GET /ServiceInfoMgmt/InformationStructures('OR:wt.part.WTPart:12345')
```

### Filter SIMDocuments by State

```bash
GET /ServiceInfoMgmt/SIMDocuments?$filter=State/Value eq 'RELEASED'
```

### Filter InformationStructures by View

```bash
GET /ServiceInfoMgmt/InformationStructures?$filter=View eq 'Service'
```

### Filter SIMDocuments by Number

```bash
GET /ServiceInfoMgmt/SIMDocuments?$filter=Number eq '12345'
```

### Filter by Folder Location

```bash
GET /ServiceInfoMgmt/SIMDocuments?$filter=FolderLocation eq '/Technical Documentation'
```

### SIMDocuments with Expanded Information Elements

```bash
GET /ServiceInfoMgmt/SIMDocuments('OR:wt.doc.WTDocument:12345')?$expand=InformationElement
```

### Get Textual Information Elements

```bash
GET /ServiceInfoMgmt/TextualInformationElements
```

### Get Document Information Elements

```bash
GET /ServiceInfoMgmt/DocumentInformationElements
```

### Get Graphical Information Elements

```bash
GET /ServiceInfoMgmt/GraphicalInformationElements
```

### Get Dynamic Documents

```bash
GET /ServiceInfoMgmt/SIMDynamicDocuments
```

### Get Table of Contents

```bash
GET /ServiceInfoMgmt/TableOfContents
```

### Filter Information Elements by Content Type

```bash
GET /ServiceInfoMgmt/TextualInformationElements?$filter=SisContentholderType eq 'Procedure'
```

### Get Information Elements for a Dynamic Document

```bash
GET /ServiceInfoMgmt/SIMDynamicDocuments('OR:wt.doc.WTDocument:12345')/InformationElement
```

### Select Specific Properties

```bash
GET /ServiceInfoMgmt/SIMDocuments?$select=ID,Name,Number,State,Description
```

### Order SIMDocuments

```bash
GET /ServiceInfoMgmt/SIMDocuments?$orderby=CreatedOn desc
GET /ServiceInfoMgmt/InformationStructures?$orderby=Name
```

### Top N Records

```bash
GET /ServiceInfoMgmt/SIMDocuments?$top=20
```

### Count Records

```bash
GET /ServiceInfoMgmt/SIMDocuments/$count
```

### Complex Filters

Multiple conditions:
```bash
GET /ServiceInfoMgmt/SIMDocuments?$filter=State/Value eq 'RELEASED' and FolderLocation eq '/Technical Documentation'
```

String filters:
```bash
GET /ServiceInfoMgmt/SIMDocuments?$filter=contains(Name, 'Installation')
GET /ServiceInfoMgmt/InformationStructures?$filter=startswith(Name, 'Service')
```

## Actions

### Get Document Structure

```bash
POST /ServiceInfoMgmt/SIMDocuments('OR:wt.doc.WTDocument:12345')/PTC.ServiceInfoMgmt.GetDocStructure
Content-Type: application/json

{
  "structureName": "MyStructure"
}
```

### Check Out

```bash
POST /ServiceInfoMgmt/SIMDocuments('OR:wt.doc.WTDocument:12345')/PTC.ServiceInfoMgmt.CheckOut
```

### Check In

```bash
POST /ServiceInfoMgmt/SIMDocuments('OR:wt.doc.WTDocument:12345')/PTC.ServiceInfoMgmt.CheckIn
Content-Type: application/json

{
  "keepCheckedOut": false,
  "comment": "Check in comment"
}
```

### Undo Check Out

```bash
POST /ServiceInfoMgmt/SIMDocuments('OR:wt.doc.WTDocument:12345')/PTC.ServiceInfoMgmt.UndoCheckOut
```

### Set State

```bash
POST /ServiceInfoMgmt/SIMDocuments('OR:wt.doc.WTDocument:12345')/PTC.ServiceInfoMgmt.SetState
Content-Type: application/json

{
  "State": "RELEASED"
}
```

### Revise

```bash
POST /ServiceInfoMgmt/SIMDocuments('OR:wt.doc.WTDocument:12345')/PTC.ServiceInfoMgmt.Revise
Content-Type: application/json

{
  "minorVersion": true,
  "comment": "Revision comment"
}
```

## Lifecycle States

Common lifecycle states for SIM objects:
- **INWORK** / **In Work** - Work in progress
- **RELEASED** - Released
- **DESIGN** - Design phase
- **CHECKED_IN** - Checked in
- **CHECKED_OUT** - Checked out

## Views

Common views for Information Structures:
- **Service** - Service documentation view
- **Manufacturing** - Manufacturing documentation view
- **Design** - Design view

## Authoring Languages

Common authoring languages:
- **en-US** - English (United States)
- **fr-FR** - French
- **de-DE** - German
- **es-ES** - Spanish

## Navigation Between Entities

| From Entity | Navigation | To Entity | Description |
|-------------|------------|-----------|-------------|
| SIMDocument | InformationElement | Collection(DocumentInformationElement) | Linked info elements |
| SIMDynamicDocument | InformationElement | Collection(DynamicDocumentInformationElement) | Linked dynamic info elements |
| DocumentInformationElement | Content | SIMDocument | Referenced document |
| TextualInformationElement | Content | SIMDynamicDocument | Parent dynamic document |
| GraphicalInformationElement | Content | SIMDynamicDocument | Parent dynamic document |
| InformationStructure | PartUsages | Collection(PartUsage) | Child parts |
| InformationStructure | BOM | Collection | Bill of Materials |

## Example Use Cases

### Example 1: Get All Released SIMDocuments

```bash
GET /ServiceInfoMgmt/SIMDocuments?$filter=State/Value eq 'RELEASED'
```

### Example 2: Find SIMDocuments for Specific Part

```bash
GET /ServiceInfoMgmt/InformationStructures?$filter=Number eq '12345'&$expand=PartUsages($expand=Child)
```

### Example 3: Get Service Documentation Structures

```bash
GET /ServiceInfoMgmt/InformationStructures?$filter=View eq 'Service' and State/Value eq 'RELEASED'
```

### Example 4: Get SIMDocument with Associated Elements

```bash
GET /ServiceInfoMgmt/SIMDocuments('OR:wt.doc.WTDocument:12345')?$expand=InformationElement
```

### Example 5: Get Textual Elements by Content Type

```bash
GET /ServiceInfoMgmt/TextualInformationElements?$filter=SisContentholderType eq 'Procedure'
```

### Example 6: Get Documentation from Specific Folder

```bash
GET /ServiceInfoMgmt/SIMDocuments?$filter=startswith(FolderLocation, '/Technical Documentation')
```

### Example 7: Get Graphical Elements

```bash
GET /ServiceInfoMgmt/GraphicalInformationElements
```

### Example 8: Get Service Documentation by Language

```bash
GET /ServiceInfoMgmt/InformationStructures?$filter=AuthoringLanguage/Value eq 'en-US'
```

### Example 9: Find Documentation with Symptoms

```bash
GET /ServiceInfoMgmt/DocumentInformationElements?$filter=Symptoms ne null
```

### Example 10: Get Primary Information Structures

```bash
GET /ServiceInfoMgmt/InformationStructures?$filter=IsPrimary eq true
```

## Pagination

Use `$top` and `$skip` for pagination:

```bash
GET /ServiceInfoMgmt/SIMDocuments?$top=50&$skip=0
GET /ServiceInfoMgmt/InformationStructures?$top=50&$skip=50
```

## Notes

1. **READ-ONLY for Query** - While this domain has extensive action support (CheckIn, CheckOut, Revise, SetState), the primary use case is querying service information for documentation and publication purposes.

2. **Complex Domain** - ServiceInfoMgmt is a complex domain with relationships to DocMgmt, DynamicDocMgmt, and ProdMgmt domains.

3. **Document Types** - SIMDocuments extend WTDocument (from DocMgmt domain) and include all document properties plus SIM-specific properties.

4. **Information Structures as Parts** - InformationStructures are essentially parts (WTParts) with SIM-specific attributes for structuring service documentation.

5. **Content Model** - The domain supports multiple types of information elements (textual, document, graphical) that can be assembled into dynamic documents.

6. **Navigation Performance** - Expanding multiple navigation properties can impact performance. Only expand what you need.

7. ** OData Version** - The ServiceInfoMgmt domain uses OData v6.

8. ** Timezone** - All timestamps are in UTC. Use `@PTC.AppliedContainerContext.LocalTimeZone` for local timezone information.

9. ** Object Identifiers** - IDs are OIDs (Object Identifiers) in the format `OR:<ObjectType>:<NumericID>`.

10. ** Authoring Language Support** - Information Structures support multiple authoring languages for international service documentation.

11. ** Publication Management** - The domain supports complex publication structures with sections, table of contents, and indexes.

## Relationship to Other Windchill Domains

| Domain | Relationship | Usage |
|--------|-------------|-------|
| **DocMgmt** | SIMDocument → WTDocument | SIMDocuments are documents in DocMgmt |
| **DynamicDocMgmt** | SIMDynamicDocument → DynamicDocument | Dynamic documents |
| **ProdMgmt** | InformationStructure → WTPart | Information structures are parts |
| **DataAdmin** | All → Container/Folder | Storage organization |
| **PrincipalMgmt** | All → User | Creator/modifier tracking |

## Service Information Use Cases

The Service Information Management domain supports:

- **Service Manual Creation** - Creating structured service manuals and guides
- **Technical Documentation** - Managing technical documentation for products
- **Multi-language Support** - Authoring documentation in multiple languages
- **Publication Management** - Structured publication with sections and TOC
- **Content Reuse** - Reusing documentation elements across multiple documents
- **Dynamic Content Assembly** - Assembling dynamic documents from information elements
- **Multimedia Content** - Supporting textual, graphical, and document-based content
- **Versioning and Lifecycle** - Full version control and lifecycle management
- **Service Impact Tracking** - Tracking service impact events and subscribers
- **Traceability** - Linking documentation to specific parts and configurations
