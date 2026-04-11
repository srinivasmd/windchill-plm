# ProdPlatformMgmt Navigation Properties

This document describes navigation properties for entities in this domain.

## DesignChoice

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `DesignOption` | `DesignOption` | - | No |

**OData $expand Example:**
```
GET /ProdPlatformMgmt/VariantSpecifications('{id}')?$expand=DesignOption
```

## OptionGroup

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `Options` | `Option` | - | No |

**OData $expand Example:**
```
GET /ProdPlatformMgmt/VariantSpecifications('{id}')?$expand=Options
```

## SalesChoice

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `SalesOption` | `SalesOption` | - | No |

**OData $expand Example:**
```
GET /ProdPlatformMgmt/VariantSpecifications('{id}')?$expand=SalesOption
```

## Choice

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `Option` | `Option` | - | No |
| `Context` | `Container` | - | No |
| `Creator` | `User` | - | No |
| `Modifier` | `User` | - | No |

**OData $expand Example:**
```
GET /ProdPlatformMgmt/VariantSpecifications('{id}')?$expand=Option,Context,Creator
```

## ModuleVariantInformationLink

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `LinkedTo` | `VariantSpecification` | - | No |
| `LinkedFrom` | `Part` | - | No |

**OData $expand Example:**
```
GET /ProdPlatformMgmt/VariantSpecifications('{id}')?$expand=LinkedTo,LinkedFrom
```

## Option

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `OptionGroup` | `OptionGroup` | - | No |
| `Choices` | `Choice` | - | No |
| `Creator` | `User` | - | No |
| `Modifier` | `User` | - | No |

**OData $expand Example:**
```
GET /ProdPlatformMgmt/VariantSpecifications('{id}')?$expand=OptionGroup,Choices,Creator
```

## OptionPoolItem

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `Context` | `Container` | - | No |

**OData $expand Example:**
```
GET /ProdPlatformMgmt/VariantSpecifications('{id}')?$expand=Context
```

## VariantSpecification

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `NavigationCriteria` | `NavigationCriteria` | - | No |
| `ConfigurableModule` | `Part` | - | No |
| `OptionSet` | `OptionSet` | - | No |
| `Context` | `Container` | - | No |
| `ModuleVariantInformationLinks` | `ModuleVariantInformationLink` | - | No |
| `Versions` | `VariantSpecification` | - | No |
| `PrimaryContent` | `ContentItem` | - | Yes |
| `Creator` | `User` | - | No |
| `Revisions` | `VariantSpecification` | - | No |
| `Modifier` | `User` | - | No |

**OData $expand Example:**
```
GET /ProdPlatformMgmt/VariantSpecifications('{id}')?$expand=NavigationCriteria,ConfigurableModule,OptionSet
```

## OptionSetAssignableEntity

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `AssignedOptionSet` | `OptionSet` | - | No |

**OData $expand Example:**
```
GET /ProdPlatformMgmt/VariantSpecifications('{id}')?$expand=AssignedOptionSet
```

## ExpressionAlias

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `AssignedTo` | `WindchillEntity` | - | No |
| `UsedIn` | `ExpressionAlias` | - | No |
| `Context` | `Container` | - | No |
| `Versions` | `ExpressionAlias` | - | No |
| `Creator` | `User` | - | No |
| `Revisions` | `ExpressionAlias` | - | No |
| `Modifier` | `User` | - | No |

**OData $expand Example:**
```
GET /ProdPlatformMgmt/VariantSpecifications('{id}')?$expand=AssignedTo,UsedIn,Context
```

## OptionSet

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `Options` | `Option` | - | No |
| `Context` | `Container` | - | No |
| `Versions` | `OptionSet` | - | No |
| `Creator` | `User` | - | No |
| `Revisions` | `OptionSet` | - | No |
| `Modifier` | `User` | - | No |

**OData $expand Example:**
```
GET /ProdPlatformMgmt/VariantSpecifications('{id}')?$expand=Options,Context,Versions
```

## IndependentAssignedExpression

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `Context` | `Container` | - | No |
| `Versions` | `IndependentAssignedExpression` | - | No |
| `Effectivities` | `Effectivity` | - | Yes |
| `Creator` | `User` | - | No |
| `Revisions` | `IndependentAssignedExpression` | - | No |
| `Modifier` | `User` | - | No |

**OData $expand Example:**
```
GET /ProdPlatformMgmt/VariantSpecifications('{id}')?$expand=Context,Versions,Effectivities
```

## DesignOption

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `DesignChoices` | `DesignChoice` | - | No |

**OData $expand Example:**
```
GET /ProdPlatformMgmt/VariantSpecifications('{id}')?$expand=DesignChoices
```

## SalesOption

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `SalesChoices` | `SalesChoice` | - | No |

**OData $expand Example:**
```
GET /ProdPlatformMgmt/VariantSpecifications('{id}')?$expand=SalesChoices
```
