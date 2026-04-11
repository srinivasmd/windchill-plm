# Factory Navigation Properties

This document describes navigation properties for entities in this domain.

## Document

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `Context` | `Container` | - | No |
| `Versions` | `Document` | - | No |
| `Creator` | `User` | - | No |
| `Representations` | `Representation` | - | No |
| `Revisions` | `Document` | - | No |
| `Modifier` | `User` | - | No |

**OData $expand Example:**
```
GET /Factory/Documents('{id}')?$expand=Context,Versions,Creator
```

## StandardProcedureUsage

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `SPL` | `StandardProcedure` | - | No |

**OData $expand Example:**
```
GET /Factory/StandardProcedureUsages('{id}')?$expand=SPL
```

## SCCStandardProcedureUsage

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `SCCSPL` | `StandardProcedure` | - | No |

**OData $expand Example:**
```
GET /Factory/SCCStandardProcedureUsages('{id}')?$expand=SCCSPL
```

## Resource

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `Creator` | `User` | - | No |
| `Modifier` | `User` | - | No |

**OData $expand Example:**
```
GET /Factory/Resources('{id}')?$expand=Creator,Modifier
```

## StandardProcedure

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `Context` | `Container` | - | No |
| `Versions` | `StandardProcedure` | - | No |
| `Creator` | `User` | - | No |
| `Revisions` | `StandardProcedure` | - | No |
| `Modifier` | `User` | - | No |

**OData $expand Example:**
```
GET /Factory/StandardProcedures('{id}')?$expand=Context,Versions,Creator
```

## ResourceUsage

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `Tools` | `Resource` | - | No |

**OData $expand Example:**
```
GET /Factory/ResourceUsages('{id}')?$expand=Tools
```

## SCCResourceUsage

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `SCCTools` | `Resource` | - | No |

**OData $expand Example:**
```
GET /Factory/SCCResourceUsages('{id}')?$expand=SCCTools
```

## SCCReferenceDocument

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `SCCRefDocuments` | `Document` | - | No |

**OData $expand Example:**
```
GET /Factory/SCCReferenceDocuments('{id}')?$expand=SCCRefDocuments
```

## DescribedByDocument

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `DescribedBy` | `Document` | - | No |

**OData $expand Example:**
```
GET /Factory/DescribedByDocuments('{id}')?$expand=DescribedBy
```

## StandardControlCharacteristic

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `SCCDDLinks` | `SCCDescribedByDocument` | - | Yes |
| `SCCDRLinks` | `SCCReferenceDocument` | - | Yes |
| `SCCResourceLinks` | `SCCResourceUsage` | - | Yes |
| `SCCSPLinks` | `SCCStandardProcedureUsage` | - | Yes |
| `Context` | `Container` | - | No |
| `Versions` | `StandardControlCharacteristic` | - | No |
| `Creator` | `User` | - | No |
| `Revisions` | `StandardControlCharacteristic` | - | No |
| `Modifier` | `User` | - | No |

**OData $expand Example:**
```
GET /Factory/StandardControlCharacteristics('{id}')?$expand=SCCDDLinks,SCCDRLinks,SCCResourceLinks
```

## StandardOperation

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `SOPSCCLinks` | `SOPToSCCLink` | - | Yes |
| `Context` | `Container` | - | No |
| `Versions` | `StandardOperation` | - | No |
| `Creator` | `User` | - | No |
| `Revisions` | `StandardOperation` | - | No |
| `Modifier` | `User` | - | No |

**OData $expand Example:**
```
GET /Factory/StandardOperations('{id}')?$expand=SOPSCCLinks,Context,Versions
```

## SOPToSCCLink

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `StandardCCs` | `StandardControlCharacteristic` | - | No |
| `DDLinks` | `DescribedByDocument` | - | Yes |
| `DRLinks` | `ReferenceDocument` | - | No |
| `SPLinks` | `StandardProcedureUsage` | - | Yes |
| `ResourceLinks` | `ResourceUsage` | - | Yes |

**OData $expand Example:**
```
GET /Factory/SOPToSCCLinks('{id}')?$expand=StandardCCs,DDLinks,DRLinks
```

## ReferenceDocument

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `RefDocuments` | `Document` | - | No |

**OData $expand Example:**
```
GET /Factory/ReferenceDocuments('{id}')?$expand=RefDocuments
```

## SCCDescribedByDocument

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `SCCDocuments` | `Document` | - | No |

**OData $expand Example:**
```
GET /Factory/SCCDescribedByDocuments('{id}')?$expand=SCCDocuments
```
