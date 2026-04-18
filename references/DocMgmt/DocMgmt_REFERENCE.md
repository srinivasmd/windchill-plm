---
Domain: DocMgmt
Client: `from domains.DocMgmt import DocMgmtClient`
---

> **Use the DocMgmtClient**: `from domains.DocMgmt import DocMgmtClient`
>
> This reference documents the entity types and properties. For programmatic access, use the domain client.

# Document Management Domain - Complete Reference

## Base URL
```
https://windchill.example.com/Windchill/servlet/odata/DocMgmt/
```

## Entity Set
- **Documents** - Main entity set for all document types

---

## Document Types & CRUD Operations

### Base Type: Document (PTC.DocMgmt.Document)

| Entity | Operations | Capabilities |
|--------|------------|--------------|
| Document | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| General | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| Agenda | READ, UPDATE, DELETE | Notifiable, Workable |
| ApprovedRecord | READ, UPDATE, DELETE | Notifiable, Workable |
| GarrettTRL | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| InterCommData | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| Minutes | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| Msds | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| Plan | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| Presentation | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| PublishedContent | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| QMSDocument | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| QualityProductReport | READ, UPDATE, DELETE | Notifiable, Workable |
| ReferenceDocument | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| Record | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| TranslationDocument | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| WorkRecord | READ, UPDATE, DELETE | Notifiable, Workable |

### Base Type: ControlledDocument (PTC.DocMgmt.ControlledDocument)

| Entity | Operations | Capabilities |
|--------|------------|--------------|
| ControlledDocument | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| GovernanceDocument | READ, UPDATE, DELETE | Notifiable, Workable |
| Quality | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| StandardOperatingProcedure | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| WorkInstruction | READ, UPDATE, DELETE | Notifiable, Workable |

### Base Type: ApprovedRecord (PTC.DocMgmt.ApprovedRecord)

| Entity | Operations | Capabilities |
|--------|------------|--------------|
| Specification | READ, UPDATE, DELETE | Notifiable, Workable |
| Training | READ, UPDATE, DELETE | Notifiable, Workable |

### Base Type: Record (PTC.DocMgmt.Record)

| Entity | Operations | Capabilities |
|--------|------------|--------------|
| Audit | READ, UPDATE, DELETE | Notifiable, Workable |
| Equipment | READ, UPDATE, DELETE | Notifiable, Workable |
| FacilityRecordsAndCertificates | READ, UPDATE, DELETE | Notifiable, Workable |
| Manual | READ, UPDATE, DELETE | Notifiable, Workable |
| MasterManufacturingRecord | READ, UPDATE, DELETE | Notifiable, Workable |
| MaterialRecordsAndCertificates | READ, UPDATE, DELETE | Notifiable, Workable |
| Method | READ, UPDATE, DELETE | Notifiable, Workable |
| PackagingAndLabeling | READ, UPDATE, DELETE | Notifiable, Workable |
| ProductRecordsAndCertificates | READ, UPDATE, DELETE | Notifiable, Workable |
| SupplierQuality | READ, UPDATE, DELETE | Notifiable, Workable |
| SupportingDocument | READ, UPDATE, DELETE | Notifiable, Workable |
| TestDocument | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |

### Software Documents

| Entity | Operations | Capabilities |
|--------|------------|--------------|
| SoftwareDocument | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| SoftwareBuild | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |
| SoftwareConfigurationData | READ, CREATE, UPDATE, DELETE | Notifiable, Workable |

### Special Entities

| Entity | Operations | Description |
|--------|------------|-------------|
| DocumentUsageLink | READ | Document usage link |
| ContentInfo | READ | Content info for stage 3 upload |
| DocStructure | READ | Document structure |
| DocumentUse | READ | Document usage link |

---

## Common Properties (Document Entity)

| Property | Type | Description |
|----------|------|-------------|
| CabinetName | String | Cabinet name |
| ChangeStatus | Icon | Change status |
| CheckOutStatus | String | Check out status |
| CheckoutState | String | Check out state |
| Classification | ClassificationInfo | Classification info |
| Comments | String | Comments |
| CreatedBy | String | Created by user |
| Description | String | Description |
| DocTypeName | String | Document type name |
| FolderLocation | String | Folder location |
| FolderName | String | Folder name |
| GeneralStatus | Icon | General status |
| Identity | String | Identity |
| Latest | Boolean | Is latest version |
| LifeCycleTemplateName | String | Lifecycle template name |
| MasterID | String | Master ID |
| ModifiedBy | String | Modified by user |
| Name | String | Name |
| Number | String | Document number |
| ObjectType | String | Object type |
| OrganizationName | String | Organization name |
| Revision | String | Revision |
| ShareStatus | Icon | Share status |
| State | EnumType | Lifecycle state |
| Title | String | Title |
| TypeIcon | Icon | Type icon |
| USE_GOOGLE_EDITOR | Boolean | Use Google editor flag |
| Version | String | Version |
| VersionID | String | Version ID |
| WorkInProgressState | WorkInProgressType | Work in progress state |

---

## Common Properties (ControlledDocument)

| Property | Type | Description |
|----------|------|-------------|
| Applicable_Departments | String | Applicable departments |
| Applicable_Roles | String | Applicable roles |
| Business_Owner | String | Business owner |
| Computer_System_Identifier | String | Computer system ID |
| DHFCategory | Collection(EnumType) | DHF category |
| Date_Obsolete | Date | Obsolescence date |
| DocumentClassification | String | Document classification |
| Effective_Date | Date | Effective date |
| Equipment_Name | String | Equipment name |
| Equipment_Number | String | Equipment number |
| Expiration_Date | Date | Expiration date |
| Facility_Site | String | Facility site |
| Language | String | Language |
| Last_Periodic_Review_Date | DateTimeOffset | Last periodic review date |
| Legacy_Document_Number | String | Legacy document number |
| Legacy_Document_Source | String | Legacy document source |
| LinkToTraining | String | Link to training |
| Manufacturer | String | Manufacturer |
| Manufacturing_Process | String | Manufacturing process |
| Next_Periodic_Review_Date | DateTimeOffset | Next periodic review date |
| Product_Family | String | Product family |
| Product_Line | String | Product line |
| Product_Model | String | Product model |
| Quality_System_Reference_Number | String | Quality system reference number |
| Reason_for_Withdrawal | String | Reason for withdrawal |
| TrainingDeadline | String | Training deadline |
| TrainingInterval | Int64 | Training interval |
| TrainingIntervalLeadTime | Int64 | Training interval lead time |
| TrainingOnRelease | Boolean | Training on release flag |
| Training_Required | Boolean | Training required flag |
| Translated_Document_Name | String | Translated document name |

---

## Software Build Properties

| Property | Type | Description |
|----------|------|-------------|
| ComPtcIesAdapterName | String | IES adapter name |
| ComPtcIesBuildDate | DateTimeOffset | Build date |
| ComPtcIesBuildDescription | String | Build description |
| ComPtcIesBuildLabel | String | Build label |
| ComPtcIesBuildStatus | String | Build status |
| ComPtcIesBuildVersion | String | Build version |
| ComPtcIesFileActivity | String | File activity |
| ComPtcIesLinesOfCode | String | Lines of code |
| ComPtcIesRevisionHolder | String | Revision holder |
| ComPtcIesSourceCodeArea | String | Source code area |

---

## API Endpoints

### Query Documents
```
GET /DocMgmt/Documents
GET /DocMgmt/Documents?$filter=Name eq 'MyDocument'
GET /DocMgmt/Documents?$select=Number,Name,State
GET /DocMgmt/Documents?$top=10&$orderby=Name
```

### Get Document by ID
```
GET /DocMgmt/Documents('{id}')
GET /DocMgmt/Documents('{id}')?$expand=DocStructure
```

### Create Document
```
POST /DocMgmt/Documents
Content-Type: application/json

{
  "Name": "My Document",
  "Number": "DOC-001",
  "Description": "Test document"
}
```

### Update Document
```
PATCH /DocMgmt/Documents('{id}')
Content-Type: application/json

{
  "Description": "Updated description"
}
```

### Delete Document
```
DELETE /DocMgmt/Documents('{id}')
```

---

## OData Query Options

| Option | Description | Example |
|--------|-------------|---------|
| $filter | Filter results | `$filter=Name eq 'Test'` |
| $select | Select properties | `$select=Number,Name,State` |
| $top | Limit results | `$top=10` |
| $skip | Skip results | `$skip=20` |
| $orderby | Sort results | `$orderby=Name asc` |
| $expand | Expand navigation properties | `$expand=DocStructure` |

---

## Common Filter Operators

| Operator | Description | Example |
|----------|-------------|---------|
| eq | Equal | `Name eq 'Test'` |
| ne | Not equal | `State ne 'CANCELED'` |
| gt | Greater than | `Version gt '1.0'` |
| ge | Greater or equal | `Version ge '1.0'` |
| lt | Less than | `Version lt '2.0'` |
| le | Less or equal | `Version le '2.0'` |
| and | Logical AND | `Name eq 'Test' and State eq 'APPROVED'` |
| or | Logical OR | `State eq 'APPROVED' or State eq 'RELEASED'` |
| contains | Contains substring | `contains(Name, 'Test')` |
| startswith | Starts with | `startswith(Name, 'DOC-')` |

---

## Authentication
Use Basic Authentication with:
- **Username:** pat
- **Password:** ptc

---

## Files Generated
- `DocMgmt_Metadata.xml` - Full OData metadata
- `DocMgmt_Entities.json` - Parsed entity data