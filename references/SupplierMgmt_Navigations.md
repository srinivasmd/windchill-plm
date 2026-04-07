# SupplierMgmt Domain - Entity Navigations

## Overview
This document describes the navigation properties between entities in the Supplier Management domain of Windchill PLM.

## Entity Navigation Map

### Supplier
Main supplier entity with comprehensive navigation to related objects.

| Navigation Property | Target Type | Description |
|-------------------|-------------|-------------|
| SupplierSites | Collection(SupplierSite) | Physical locations/facilities for the supplier |
| SupplierContacts | Collection(SupplierContact) | Contact persons associated with the supplier |
| SupplierProducts | Collection(SupplierProduct) | Products/parts supplied by this supplier |
| SupplierContracts | Collection(SupplierContract) | Contracts and agreements with the supplier |
| SupplierQualifications | Collection(SupplierQualification) | Qualification and certification records |
| SupplierEvaluations | Collection(SupplierEvaluation) | Performance evaluations |
| Context | Container | Container context |
| Organization | Organization | Organization details |
| Creator | User | User who created the record |
| Revisions | Collection(Supplier) | All revisions |
| Folder | Folder | Folder location |
| Versions | Collection(Supplier) | All versions |
| Modifier | User | User who last modified the record |

### SupplierSite
Physical locations for suppliers.

| Navigation Property | Target Type | Description |
|-------------------|-------------|-------------|
| Supplier | Supplier | Parent supplier |
| Contacts | Collection(SupplierContact) | Contacts at this site |

### SupplierContact
Contact persons associated with suppliers.

| Navigation Property | Target Type | Description |
|-------------------|-------------|-------------|
| Supplier | Supplier | Parent supplier |
| Site | SupplierSite | Associated supplier site |

### SupplierProduct
Products/parts supplied by suppliers.

| Navigation Property | Target Type | Description |
|-------------------|-------------|-------------|
| Supplier | Supplier | Parent supplier |
| Part | Part (ProdMgmt) | Associated part |

### SupplierContract
Contracts and agreements with suppliers.

| Navigation Property | Target Type | Description |
|-------------------|-------------|-------------|
| Supplier | Supplier | Parent supplier |
| ContractProducts | Collection(SupplierProduct) | Products covered by this contract |
| Documents | Collection(Document) | Related documents |

### SupplierQualification
Supplier qualification and certification records.

| Navigation Property | Target Type | Description |
|-------------------|-------------|-------------|
| Supplier | Supplier | Parent supplier |
| Documents | Collection(Document) | Certificate documents |

### SupplierEvaluation
Supplier performance evaluations.

| Navigation Property | Target Type | Description |
|-------------------|-------------|-------------|
| Supplier | Supplier | Parent supplier |
| EvaluationDetails | Collection(EvaluationDetail) | Evaluation detail records |

### EvaluationDetail
Detailed evaluation criteria and scores.

| Navigation Property | Target Type | Description |
|-------------------|-------------|-------------|
| Evaluation | SupplierEvaluation | Parent evaluation |

## OData Query Examples

### Get Supplier with Sites and Contacts
```
GET /Windchill/servlet/odata/SupplierMgmt/Supplier?$filter=Number eq 'SUP-001'
&$expand=SupplierSites,SupplierContacts
```

### Get Supplier with Products
```
GET /Windchill/servlet/odata/SupplierMgmt/Supplier?$filter=Number eq 'SUP-001'
&$expand=SupplierProducts($expand=Part)
```

### Get Supplier with Contracts
```
GET /Windchill/servlet/odata/SupplierMgmt/Supplier?$filter=Number eq 'SUP-001'
&$expand=SupplierContracts($expand=Documents)
```

### Get Supplier with Evaluations and Details
```
GET /Windchill/servlet/odata/SupplierMgmt/Supplier?$filter=Number eq 'SUP-001'
&$expand=SupplierEvaluations($expand=EvaluationDetails)
```

### Get Site with Contacts
```
GET /Windchill/servlet/odata/SupplierMgmt/SupplierSite?$filter=SupplierID eq 'OR:wt.org.Organization:12345'
&$expand=Contacts
```

### Get Product with Part
```
GET /Windchill/servlet/odata/SupplierMgmt/SupplierProduct?$filter=PartNumber eq 'PART-001'
&$expand=Supplier,Part
```

## Cross-Domain Navigations

The SupplierMgmt domain navigates to the following external domains:

| Domain | Entity | Navigation From |
|--------|--------|-----------------|
| ProdMgmt | Part | SupplierProduct.Part |
| DocMgmt | Document | SupplierContract.Documents, SupplierQualification.Documents |
| DataAdmin | Container | Supplier.Context, Organization.Context |
| DataAdmin | Folder | Supplier.Folder |
| PrincipalMgmt | Organization | Supplier.Organization |
| PrincipalMgmt | User | Supplier.Creator, Supplier.Modifier, Organization.Creator, Organization.Modifier |