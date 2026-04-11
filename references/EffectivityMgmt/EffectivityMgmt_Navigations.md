# EffectivityMgmt Navigation Properties

This document describes navigation properties for entities in this domain.

## PartEffectivityContext

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `Context` | `Container` | - | No |
| `Organization` | `Organization` | - | No |

**OData $expand Example:**
```
GET /EffectivityMgmt/PartEffectivityContexts('{id}')?$expand=Context,Organization
```

## EffectivityManagedEntity

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `Effectivities` | `Effectivity` | - | Yes |
| `Creator` | `User` | - | No |
| `Modifier` | `User` | - | No |

**OData $expand Example:**
```
GET /EffectivityMgmt/EffectivityManagedEntitys('{id}')?$expand=Effectivities,Creator,Modifier
```

## Effectivity

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `EffectivityContext` | `PartEffectivityContext` | - | No |

**OData $expand Example:**
```
GET /EffectivityMgmt/Effectivitys('{id}')?$expand=EffectivityContext
```
