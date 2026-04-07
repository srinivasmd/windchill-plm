# UDI (Unique Device Identification) Domain Reference

This domain provides access to Windchill UDI (Unique Device Identification) entities for medical device regulatory compliance, including UDI supersets, subjects, FDA codes, and device characteristics.

## UDI API Endpoint

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/UDI/
```

## Metadata

OData metadata is available at:
```
GET /UDI/$metadata
```

## OData Version

The UDI domain uses OData v6.

## UDI Domain Entities

The UDI domain includes the following main entity types:

| Entity | Description | Operations |
|--------|-------------|------------|
| **UDISuperSets** | UDI supersets (main UDI records) | READ |
| **UDISuperSets2** | Extended UDI supersets (newer version) | READ |
| **UDISubjects** | UDI subjects (parts linked to UDI) | READ |
| **SubjectLink** | Links between UDI supersets and subjects | READ |
| **DeviceContact** | Device contact information | READ |
| **FDAProductCode** | FDA product codes | READ |
| **PackagingConfiguration** | Packaging configurations | READ |
| **UDISuperSetDetail** | Base detail class for UDI details | READ |
| **FDAPremarketAuthorizationNumber** | FDA premarket authorization numbers | READ |
| **FDAListingNumber** | FDA listing numbers | READ |
| **SterilizationMethod** | Sterilization methods | READ |
| **DeviceSizeCharacteristic** | Device size characteristics | READ |
| **GMDNTermCode** | GMDN term codes | READ |
| **StorageAndHandlingRequirement** | Storage and handling requirements | READ |
| **UDISubject** | UDI subject (individual part linked to UDI) | READ |
| **Detail** | Base detail class | READ |
| **AlternateIdentifier** | Alternate device identifiers | READ |

## Entity Collections

| Collection | Entity Type |
|------------|-------------|
| UDISuperSets | PTC.UDI.UDISuperSet |
| UDISuperSets2 | PTC.UDI.UDISuperSet2 |
| UDISubjects | PTC.UDI.UDISubject |

## Actions

| Action | Target | Description |
|--------|--------|-------------|
| Revise | UDISuperSet | Revise UDI superset |
| ReviseUDISuperSets2 | UDISuperSet2 | Revise UDI superset 2 |
| SetState | UDISuperSet | Set lifecycle state |
| SetStateUDISuperSets2 | UDISuperSet2 | Set lifecycle state for UDISuperSet2 |
| SetState | UDISuperSet | Set lifecycle state |
| SetStateUDISuperSets | UDISuperSet | Set lifecycle state for UDISuperSet |

## Functions

| Function | Return | Description |
|----------|--------|-------------|
| GetValidStateTransitions | Collection | Get valid state transitions |
| GetLifeCycleTemplate | LifecycleTemplate | Get lifecycle template |
| GetLifeCycleTemplate | LifecycleTemplate | Get lifecycle template |
| GetValidStateTransitions | Collection | Get valid state transitions |

## Entity Details

### UDISuperSet2

Main UDI superset record (extended version with multiple subject support).

**Common Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Number** | String | UDI record number |
| **Name** | String | UDI record name |
| **Version** | String | Version |
| **Identity** | String | Display identity string |
| **DeviceIdentifier** | String | Device identifier (DI) |
| **DeviceIdentifierIssuingAgency** | EnumType | Issuing agency (FDA, etc.) |
| **DirectPartMarkingDeviceIdentifier** | String | DPM device identifier |
| **BrandName** | String | Brand name |
| **BrandNamePartofDeviceFamily** | Boolean | Whether brand name is part of device family |
| **CatalogNumber** | String | Catalog number |
| **DeviceDescription** | String | Device description |
| **DeviceCount** | Int16 | Number of devices in kit |
| **KitProduct** | Boolean | Is a kit product |
| **CombinationProduct** | Boolean | Is a combination product |
| **ExpirationDateControlled** | Boolean | Has expiration date control |
| **ContainsHumanTissue** | Boolean | Contains human tissue |
| **ContainsLatex** | Boolean | Contains latex |
| **ByDonationIdentificationNumber** | Boolean | Has donation identification number |
| **DiscontinuedDate** | DateTimeOffset | Discontinuation date |
| **FolderLocation** | String | Folder location path |
| **FolderName** | String | Folder name |
| **CabinetName** | String | Cabinet name |
| **CreatedBy** | String | Creator username |
| **ModifiedBy** | String | Last modifier username |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |
| **State** | EnumType | Lifecycle state |
| **MasterID** | String | Master object ID |

**Navigation Properties:**
- **Template** → PTC.UDI.UDISuperSet2 (Template used)
- **Subjects** → Collection(PTC.UDI.SubjectLink) (Linked subjects/parts)
- **Details** → Collection(PTC.UDI.Detail) (Detail records)
- **PackagingConfigurations** → Collection(PTC.UDI.PackagingConfiguration) (Packaging info)
- **Context** → PTC.DataAdmin.Container (Container context)
- **Versions** → Collection(PTC.UDI.UDISuperSet2) (Version history)
- **Revisions** → Collection(PTC.UDI.UDISuperSet2) (Revision history)
- **Creator** → PTC.PrincipalMgmt.User (User who created)
- **Modifier** → PTC.PrincipalMgmt.User (User who last modified)
- **Folder** → PTC.DataAdmin.Folder (Folder)

### UDISuperSet

Legacy UDI superset record (single subject support).

**Common Properties:**

Similar to UDISuperSet2 but without multi-subject support.

**Navigation Properties:**
- **Template** → PTC.UDI.UDISuperSet (Template used)
- **Subject** → PTC.UDI.UDISubject (Linked subject/part)
- **Details** → Collection(PTC.UDI.Detail) (Detail records)
- **PackagingConfigurations** → Collection(PTC.UDI.PackagingConfiguration) (Packaging info)
- **Context** → PTC.DataAdmin.Container (Container context)
- **Creator** → PTC.PrincipalMgmt.User (User who created)
- **Modifier** → PTC.PrincipalMgmt.User (User who last modified)

### UDISubject

Subject (part) linked to UDI superset.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **Number** | String | Part number |
| **Name** | String | Part name |
| **Identity** | String | Display identity string |
| **Version** | String | Version |
| **View** | String | View (Design, Manufacturing) |
| **OrganizationID** | String | Organization ID |
| **MasterID** | String | Master object ID |
| **CreatedBy** | String | Creator username |
| **ModifiedBy** | String | Last modifier username |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- **Context** → PTC.DataAdmin.Container (Container context)
- **Creator** → PTC.PrincipalMgmt.User (User who created)
- **Modifier** → PTC.PrincipalMgmt.User (User who last modified)

### SubjectLink

Link between UDISuperSet2 and UDISubject (for multi-subject UDI records).

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- **Subject** → PTC.UDI.UDISubject (Linked subject)

### PackagingConfiguration

Packaging information for UDI records.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **ID** | String | Object identifier (OID) (Key, ReadOnly) |
| **PackageDeviceIdentifier** | String | Package device identifier |
| **Quantity** | String | Quantity |
| **Description** | String | Description |
| **DiscontinuedDate** | DateTimeOffset | Discontinuation date |
| **ObjectType** | String | Object type |
| **CreatedOn** | DateTimeOffset | Creation timestamp (ReadOnly) |
| **LastModified** | DateTimeOffset | Last modification timestamp (ReadOnly) |

**Navigation Properties:**
- **Contains** → PTC.UDI.PackagingConfiguration (Nested packages)

### Detail Types (inherit from Detail or UDISuperSetDetail)

#### DeviceContact

Device contact information.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **PhoneNumber** | String | Phone number |
| **PhoneExtension** | String | Phone extension |
| **EmailAddress** | String | Email address |

#### FDAProductCode

FDA product code information.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **Udiss_fdaProductCode** | String | FDA product code |

#### FDAPremarketAuthorizationNumber

FDA premarket authorization information.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **Udiss_fdaPremarketAuthorizationNumber** | String | FDA PMA number |
| **Udiss_fdaSupplementNumber** | String | FDA supplement number |

#### FDAListingNumber

FDA listing number information.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **Udiss_fdaListingNumber** | String | FDA listing number |

#### SterilizationMethod

Sterilization method information.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **SterilizationMethod** | EnumType | Sterilization method type |

#### DeviceSizeCharacteristic

Device size characteristics.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **Value** | String | Size value |
| **SizeType** | EnumType | Size type |
| **UnitOfMeasure** | EnumType | Unit of measure |
| **Description** | String | Description |

#### GMDNTermCode

GMDN (Global Medical Device Nomenclature) term code.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **GMDNTermCode** | String | GMDN term code |

#### StorageAndHandlingRequirement

Storage and handling requirements.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **Description** | String | Description |
| **LowValue** | Double | Low temperature/value |
| **HighValue** | Double | High temperature/value |
| **StorageType** | EnumType | Storage type |
| **UnitOfMeasure** | EnumType | Unit of measure |

#### AlternateIdentifier

Alternate device identifier.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| **IdentifierType** | String | Type of identifier |
| **IdentifierValue** | String | Identifier value |

## Common Query Patterns

### Get All UDI Supersets

```bash
GET /UDI/UDISuperSets
```

### Get All UDI Supersets2

```bash
GET /UDI/UDISuperSets2
```

### Get All UDI Subjects

```bash
GET /UDI/UDISubjects
```

### Get UDI Superset2 by ID

```bash
GET /UDI/UDISuperSets2('OR:wt.udi.UDISuperSet2:12345')
```

### Get UDI Superset by ID

```bash
GET /UDI/UDISuperSets('OR:wt.udi.UDISuperSet:12345')
```

### Get UDI Subject by ID

```bash
GET /UDI/UDISubjects('OR:wt.part.WTPart:12345')
```

### Filter UDI Supersets by Device Identifier

```bash
GET /UDI/UDISuperSets2?$filter=DeviceIdentifier eq '12345678901234'
```

### Filter UDI Supersets by Brand Name

```bash
GET /UDI/UDISuperSets2?$filter=contains(BrandName, 'Med')
```

### Filter UDI Supersets by Catalog Number

```bash
GET /UDI/UDISuperSets2?$filter=CatalogNumber eq 'CAT-001'
```

### Get Active UDI Supersets (not discontinued)

```bash
GET /UDI/UDISuperSets2?$filter=DiscontinuedDate eq null
```

### Get Discontinued UDI Supersets

```bash
GET /UDI/UDISuperSets2?$filter=DiscontinuedDate ne null
```

### Filter UDI Subjects by Number

```bash
GET /UDI/UDISubjects?$filter=Number eq '12345'
```

### Filter UDI Subjects by Name

```bash
GET /UDI/UDISubjects?$filter=contains(Name, 'Device')
```

### Get UDI Superset with Expanded Details

```bash
GET /UDI/UDISuperSets2('OR:wt.udi.UDISuperSet2:12345')?$expand=Subjects,Details,PackagingConfigurations
```

### Get UDI Superset with Full Expansion

```bash
GET /UDI/UDISuperSets2('OR:wt.udi.UDISuperSet2:12345')?$expand=Subjects($expand=Subject),Details,PackagingConfigurations,Creator,Modifier,Context
```

### Get Subjects for a UDI Superset2

```bash
GET /UDI/UDISuperSets2('OR:wt.udi.UDISuperSet2:12345')/Subjects
```

### Get Subjects with Full Subject Details

```bash
GET /UDI/UDISuperSets2('OR:wt.udi.UDISuperSet2:12345')/Subjects?$expand=Subject
```

### Get Details for a UDI Superset2

```bash
GET /UDI/UDISuperSets2('OR:wt.udi.UDISuperSet2:12345')/Details
```

### Get Packaging Configurations

```bash
GET /UDI/UDISuperSets2('OR:wt.udi.UDISuperSet2:12345')/PackagingConfigurations
```

### Select Specific Properties

```bash
GET /UDI/UDISuperSets2?$select=ID,DeviceIdentifier,BrandName,CatalogNumber,State
```

### Order UDI Supersets

```bash
GET /UDI/UDISuperSets2?$orderby=CreatedOn desc
GET /UDI/UDISuperSets2?$orderby=BrandName
```

### Top N UDI Supersets

```bash
GET /UDI/UDISuperSets2?$top=20
```

### Count UDI Supersets

```bash
GET /UDI/UDISuperSets2/$count
```

### Count Active UDI Supersets

```bash
GET /UDI/UDISuperSets2/$count?$filter=DiscontinuedDate eq null
```

### Get UDI Superset by Subject

```bash
# Get UDI supersets linked to a specific subject
GET /UDI/UDISuperSets2?$filter=Subjects/any(s: s/Subject/Number eq '12345')
```

### FDA-Specific Queries

Get UDI supersets with FDA product code:
```bash
GET /UDI/UDISuperSets2?$filter=Details/any(d: UDISuperSet2/DeviceIdentifier ne null)
```

### Complex Filters

Multiple conditions:
```bash
GET /UDI/UDISuperSets2?$filter=(
  DeviceIdentifier ne null and
  DiscontinuedDate eq null and
  KitProduct eq false
) or (
  CatalogNumber eq 'CAT-001'
)
```

String filters:
```bash
GET /UDI/UDISuperSets2?$filter=startswith(BrandName, 'Acme')
GET /UDI/UDISubjects?$filter=contains(Name, 'Surgical')
```

## Actions

### Revise UDI Superset

```bash
POST /UDI/UDISuperSets('OR:wt.udi.UDISuperSet:12345')/PTC.UDI.Revise
```

### Revise UDI Superset2

```bash
POST /UDI/UDISuperSets2('OR:wt.udi.UDISuperSet2:12345')/PTC.UDI.ReviseUDISuperSets2
```

### Set State

```bash
POST /UDI/UDISuperSets('OR:wt.udi.UDISuperSet:12345')/PTC.UDI.SetState
Content-Type: application/json

{
  "State": "APPROVED"
}
```

```bash
POST /UDI/UDISuperSets2('OR:wt.udi.UDISuperSet2:12345')/PTC.UDI.SetStateUDISuperSets2
Content-Type: application/json

{
  "State": "APPROVED"
}
```

## Functions

### Get Valid State Transitions

```bash
GET /UDI/UDISuperSets2('OR:wt.udi.UDISuperSet2:12345')/PTC.UDI.GetValidStateTransitions
```

### Get Lifecycle Template

```bash
GET /UDI/UDISuperSets2('OR:wt.udi.UDISuperSet2:12345')/PTC.UDI.GetLifeCycleTemplate
```

## UDI Device Identifier Issuing Agencies

Common issuing agencies (EnumType):
- **FDA** - U.S. Food and Drug Administration
- **GS1** - GS1 Standards
- **HIBCC** - Health Industry Bar Code Council
- **ICCBBA** - International Council for Commonality in Blood Banking Automation

## Device Size Types

Common size types (EnumType):
- **LENGTH**
- **WIDTH**
- **HEIGHT**
- **DIAMETER**
- **THICKNESS**
- **VOLUME**
- **WEIGHT**

## Storage Types

Common storage types (EnumType):
- **TEMPERATURE**
- **HUMIDITY**
- **LIGHT**
- **PRESSURE**

## Sterilization Methods

Common sterilization methods (EnumType):
- **AUTOCLAVE**
- **ETHYLENE_OXIDE**
- **GAMMA_IRRADIATION**
- **E-BEAM**
- **DRY_HEAT**
- **STERILE_FILTER**

## Example Use Cases

### Example 1: Get All Active UDI Supersets

```bash
GET /UDI/UDISuperSets2?$filter=DiscontinuedDate eq null&$expand=Subjects,Details&$orderby=BrandName
```

### Example 2: Find UDI by Device Identifier

```bash
GET /UDI/UDISuperSets2?$filter=DeviceIdentifier eq '12345678901234'&$expand=Subjects,Details,PackagingConfigurations
```

### Example 3: Get All Devices with Latex

```bash
GET /UDI/UDISuperSets2?$filter=ContainsLatex eq true
```

### Example 4: Get All UDI Subjects for a PartNumber

```bash
GET /UDI/UDISubjects?$filter=Number eq '12345'
```

### Example 5: Get UDI Superset with All Related Data

```bash
GET /UDI/UDISuperSets2('OR:wt.udi.UDISuperSet2:12345')?$expand=Subjects($expand=Subject),Details,PackagingConfigurations,Creator,Modifier,Context,Folder
```

### Example 6: Get UDI Supersets Created in Date Range

```bash
GET /UDI/UDISuperSets2?$filter=CreatedOn ge 2024-01-01 and CreatedOn le 2024-12-31&$expand=Subjects
```

### Example 7: Find UDI Supersets Linked to Multiple Subjects

```bash
GET /UDI/UDISuperSets2?$filter=Subjects/$count gt 1&$expand=Subjects($expand=Subject)
```

### Example 8: Get UDI Supersets with Packaging Info

```bash
GET /UDI/UDISuperSets2?$filter=PackagingConfigurations/$count gt 0&$expand=PackagingConfigurations
```

### Example 9: Search by Catalog Number Pattern

```bash
GET /UDI/UDISuperSets2?$filter=contains(CatalogNumber, 'CAT-')&$expand=Subjects
```

### Example 10: Get Discontinued UDI Supersets with Details

```bash
GET /UDI/UDISuperSets2?$filter=DiscontinuedDate ne null&$expand=Subjects,Details&$orderby=DiscontinuedDate desc
```

## Navigation Between Entities

The UDI domain has several relationships to other domains:

| From Entity | Navigation | To Entity | Description |
|-------------|------------|-----------|-------------|
| UDISuperSet2 | Template | UDISuperSet2 | Template used for this UDI |
| UDISuperSet2 | Subjects | Collection(SubjectLink) | Linked subjects/parts |
| UDISuperSet2 | Details | Collection(Detail) | Detail records |
| UDISuperSet2 | PackagingConfigurations | Collection(PackagingConfiguration) | Packaging info |
| UDISuperSet2 | Context | DataAdmin.Container | Container context |
| UDISuperSet2 | Creator | PrincipalMgmt.User | User who created |
| UDISuperSet2 | Modifier | PrincipalMgmt.User | User who last modified |
| UDISuperSet2 | Folder | DataAdmin.Folder | Folder |
| SubjectLink | Subject | UDISubject | Linked subject/part |
| PackagingConfiguration | Contains | PackagingConfiguration | Nested packages |
| UDISuperSet | Subject | UDISubject | Linked subject/part |
| UDISuperSet | Context | DataAdmin.Container | Container context |
| UDISuperSet | Creator | PrincipalMgmt.User | User who created |
| UDISuperSet | Modifier | PrincipalMgmt.User | User who last modified |
| UDISubject | Context | DataAdmin.Container | Container context |
| UDISubject | Creator | PrincipalMgmt.User | User who created |
| UDISubject | Modifier | PrincipalMgmt.User | User who last modified |

## Pagination

Use `$top` and `$skip` for pagination:

```bash
GET /UDI/UDISuperSets2?$top=50&$skip=0
GET /UDI/UDISuperSets2?$top=50&$skip=50
```

## Filtering Options

Complex filters using `and`, `or`, `not`:

```bash
GET /UDI/UDISuperSets2?$filter=(
  DeviceIdentifier ne null and
  DiscontinuedDate eq null
) or (
  KitProduct eq true
)
```

String filters using `startswith`, `endswith`, `contains`:

```bash
GET /UDI/UDISuperSets2?$filter=startswith(BrandName, 'Acme')
GET /UDI/UDISuperSets2?$filter=contains(CatalogNumber, 'CAT-')
```

Date filters:

```bash
GET /UDI/UDISuperSets2?$filter=CreatedOn ge 2024-01-01 and CreatedOn le 2024-12-31
GET /UDI/UDISuperSets2?$filter=DiscontinuedDate lt 2024-01-01
```

## Notes

1. ** READ-ONLY Access** - The UDI domain is primarily read-only for querying. Actions like Revise and SetState are available but use the appropriate action endpoints.

2. **Two Superset Types** - There are two UDI superset versions:
   - **UDISuperSet** - Legacy version with single subject support
   - **UDISuperSet2** - Extended version with multi-subject support via SubjectLink

3. **Detail Classes** - Various detail classes inherit from `Detail` or `UDISuperSetDetail` and store additional UDI information such as FDA codes, sterilization methods, device characteristics, etc.

4. ** SubjectLink** - For UDISuperSet2, subjects are linked via the `SubjectLink` entity, which allows one UDI record to be associated with multiple parts/subjects.

5. ** Navigation Performance** - Expanding multiple navigation properties can impact performance. Only expand what you need.

6. ** OData Version** - The UDI domain uses OData v6.

7. ** Timezone** - All timestamps are in UTC. Use `@PTC.AppliedContainerContext.LocalTimeZone` for local timezone information.

8. ** Object Identifiers** - IDs are OIDs (Object Identifiers) in the format `OR:<ObjectType>:<NumericID>`. Always use these for dereferencing navigation properties.

9. ** Regulatory Compliance** - UDI domain is specifically designed for FDA UDI regulatory compliance tracking and reporting.

10. ** Multi-Support** - UDISuperSet2 supports linking to multiple subjects (parts) through the SubjectLink entity, while UDISuperSet only supports a single subject link.

## Relationship to Other Windchill Domains

| Domain | Relationship | Usage |
|--------|-------------|-------|
| **ProdMgmt** | UDISubject → WTPart | UDI subjects are parts stored in ProdMgmt |
| **DataAdmin** | UDISuperSet → Container | UDI records are stored in containers/folders |
| **PrincipalMgmt** | UDISuperSet → User | Creator/modifier tracking |
| **DataAdmin** | UDISuperSet → Folder | Folder organization |

## UDI Regulatory Information

### FDA UDI Requirements

The UDI domain supports FDA UDI requirements including:
- Device Identifier (DI)
- Production Identifier (PI) - expiration date, lot/batch, serial number
- Device description
- Brand name
- Catalog number
- Labeler information (brand owner)
- FDA product code
- FDA premarket authorization (PMA) number
- FDA listing number

### GMDN Support

Global Medical Device Nomenclature (GMDN) term codes are supported for international regulatory compliance.

### Sterilization and Packaging

Detailed tracking of:
- Sterilization methods
- Storage and handling requirements
- Packaging configurations
- Device characteristics (size, etc.)

### Multi-Subject Support

UDISuperSet2 supports association with multiple parts/subjects, allowing comprehensive UDI management of product families or kits.
