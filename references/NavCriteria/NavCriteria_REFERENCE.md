# NavCriteria Domain Reference

Navigation Criteria management in PTC Windchill PLM. This domain handles configuration specifications and filters for navigating product structures.

## Overview

| Property | Value |
|----------|-------|
| Namespace | PTC.NavCriteria |
| Entity Sets | 2 |
| Entity Types | 2 |
| Actions | 0 |
| Complex Types | 41 |

---

## Entity Sets

- **NavigationCriterias**: NavigationCriteria
- **CachedNavigationCriterias**: CachedNavigationCriteria

---

## Entity Types

### NavigationCriteria

Primary entity for defining navigation criteria with configuration specifications and filters.

**Key:** `ID`

**Properties (13):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `ApplicableType` | String | No | Type this criteria applies to |
| `ApplicationName` | String | Yes | Application name (NonFilterable) |
| `ApplyToTopLevelObject` | Boolean | Yes | Apply to top-level objects |
| `Centricity` | Boolean | Yes | Centricity flag |
| `ConfigSpecs` | Collection(ConfigSpec) | Yes | Configuration specifications (NonFilterable) |
| `CreatedOn` | DateTimeOffset | Yes | Creation timestamp (ReadOnly) |
| `Filters` | Collection(Filter) | Yes | Filters collection (NonFilterable) |
| `HideUnresolvedDependents` | Boolean | Yes | Hide unresolved dependents |
| `ID` | String | Yes | Unique identifier (ReadOnly) |
| `LastModified` | DateTimeOffset | Yes | Last modified timestamp (ReadOnly) |
| `Name` | String | Yes | Criteria name |
| `SharedToAll` | Boolean | Yes | Shared to all users |
| `UseDefaultForUnresolved` | Boolean | Yes | Use default for unresolved |

**Operations:** READ

---

### CachedNavigationCriteria

Cached version of navigation criteria for performance optimization.

**Key:** `ID`

**Properties (11):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `ApplicableType` | String | No | Type this criteria applies to |
| `ApplicationName` | String | Yes | Application name |
| `ApplyToTopLevelObject` | Boolean | Yes | Apply to top-level objects |
| `Centricity` | Boolean | Yes | Centricity flag |
| `CreatedOn` | DateTimeOffset | Yes | Creation timestamp |
| `HideUnresolvedDependents` | Boolean | Yes | Hide unresolved dependents |
| `ID` | String | Yes | Unique identifier |
| `LastModified` | DateTimeOffset | Yes | Last modified timestamp |
| `Name` | String | Yes | Criteria name |
| `SharedToAll` | Boolean | Yes | Shared to all users |
| `UseDefaultForUnresolved` | Boolean | Yes | Use default for unresolved |

---

## Complex Types (41)

NavCriteria domain provides extensive complex types for configuration specifications and filters.

### Configuration Specification Types

| Complex Type | Purpose |
|--------------|---------|
| `ConfigSpec` | Base configuration specification |
| `BaselineConfigSpec` | Baseline-based configuration |
| `ChangeConfigSpec` | Change-based configuration |
| `StandardConfigSpec` | Standard/latest configuration |
| `AsStoredConfigSpec` | As-stored configuration |
| `AsMaturedConfigSpec` | As-matured configuration |
| `PromotionNoticeConfigSpec` | Promotion notice configuration |
| `EffectivityConfigSpec` | Effectivity-based configuration |

### Part Configuration Specs

| Complex Type | Purpose |
|--------------|---------|
| `WTPartStandardConfigSpec` | Windchill Part standard config |
| `WTPartBaselineConfigSpec` | Windchill Part baseline config |
| `WTPartChangeConfigSpec` | Windchill Part change config |
| `WTPartAsMaturedConfigSpec` | Windchill Part as-matured config |
| `WTPartEffectivityDateConfigSpec` | Part effectivity by date |
| `WTPartEffectivityUnitConfigSpec` | Part effectivity by unit |
| `WTPartPromotionNoticeConfigSpec` | Part promotion notice config |

### EPMDocument Configuration Specs

| Complex Type | Purpose |
|--------------|---------|
| `EPMDocStandardConfigSpec` | EPMDocument standard config |
| `EPMDocBaselineConfigSpec` | EPMDocument baseline config |
| `EPMDocChangeConfigSpec` | EPMDocument change config |
| `EPMDocAsStoredConfigSpec` | EPMDocument as-stored config |
| `EPMDocPromotionNoticeConfigSpec` | EPMDoc promotion notice config |

### Plant Configuration Specs

| Complex Type | Purpose |
|--------------|---------|
| `PlantStandardConfigSpec` | Plant standard configuration |
| `PlantEffectivityDateConfigSpec` | Plant effectivity by date |
| `PlantEffectivityUnitConfigSpec` | Plant effectivity by unit |

### Filter Types

| Complex Type | Purpose |
|--------------|---------|
| `Filter` | Base filter type |
| `AttributeFilter` | Attribute-based filtering |
| `PathFilter` | Path-based filtering |
| `SpatialFilter` | Spatial/geometric filtering |
| `OptionFilter` | Option-based filtering |
| `PlantFilter` | Plant-based filtering |
| `PartTagFilter` | Part tag filtering |

### Path Filter Types

| Complex Type | Purpose |
|--------------|---------|
| `OccurrencePathFilter` | Filter by occurrence path |
| `UsesPathFilter` | Filter by uses path |
| `UsagePathFilter` | Filter by usage path |

### Spatial Filter Types

| Complex Type | Purpose |
|--------------|---------|
| `BoxSpatialFilter` | Box-shaped spatial filter |
| `SphereSpatialFilter` | Sphere-shaped spatial filter |
| `ProximitySpatialFilter` | Proximity-based spatial filter |

### Attribute Filter Types

| Complex Type | Purpose |
|--------------|---------|
| `AttributeStructFilterRule` | Attribute structure filter rule |
| `AttributeStructFilterRuleExpression` | Attribute filter expression |
| `PlantAttributeStructFilterRule` | Plant attribute filter rule |
| `PlantAttributeStructFilterRuleExpression` | Plant attribute filter expression |

### Option Filter Types

| Complex Type | Purpose |
|--------------|---------|
| `OptionFilterConfigSpec` | Option filter configuration |
| `OptionFilterMode` | Option filter mode settings |
| `SelectedChoice` | Selected option choice |

### Supporting Types

| Complex Type | Purpose |
|--------------|---------|
| `PathFilterTableRowItem` | Path filter table row |
| `PathReference` | Path reference |
| `ObjectTagFilterItem` | Object tag filter item |

---

## Usage Examples

### Query Navigation Criteria

```python
from domains.NavCriteria import NavCriteriaClient

client = NavCriteriaClient(config_path="config.json")

# Get all navigation criteria
criteria = client.get_navigation_criteria(top=50)

# Get by name
criteria = client.get_navigation_criteria_by_name("MyConfig")

# Get cached criteria
cached = client.get_cached_navigation_criteria(top=50)
```

### Create Navigation Criteria with ConfigSpec

```python
# Create with standard config spec
criteria = client.create_navigation_criteria(
    name="StandardView",
    applicable_type="WTPart",
    config_specs=[{
        "@odata.type": "PTC.NavCriteria.WTPartStandardConfigSpec",
        "View": "Manufacturing"
    }],
    apply_to_top_level_object=True
)
```

### Create with Baseline ConfigSpec

```python
criteria = client.create_navigation_criteria(
    name="BaselineView",
    applicable_type="WTPart",
    config_specs=[{
        "@odata.type": "PTC.NavCriteria.WTPartBaselineConfigSpec",
        "BaselineOID": "OR:wt.proj.Baseline:12345"
    }]
)
```

### Create with Effectivity ConfigSpec

```python
criteria = client.create_navigation_criteria(
    name="EffectivityView",
    applicable_type="WTPart",
    config_specs=[{
        "@odata.type": "PTC.NavCriteria.WTPartEffectivityDateConfigSpec",
        "StartDate": "2024-01-01T00:00:00Z",
        "EndDate": "2024-12-31T23:59:59Z"
    }]
)
```

### Create with Filters

```python
criteria = client.create_navigation_criteria(
    name="FilteredView",
    applicable_type="WTPart",
    filters=[{
        "@odata.type": "PTC.NavCriteria.AttributeFilter",
        "Attribute": "Material",
        "Operator": "Equals",
        "Value": "Steel"
    }],
    hide_unresolved_dependents=True
)
```

### Spatial Filter Example

```python
# Box spatial filter for CAD geometry
criteria = client.create_navigation_criteria(
    name="SpatialView",
    applicable_type="EPMDocument",
    filters=[{
        "@odata.type": "PTC.NavCriteria.BoxSpatialFilter",
        "MinX": 0.0,
        "MinY": 0.0,
        "MinZ": 0.0,
        "MaxX": 100.0,
        "MaxY": 100.0,
        "MaxZ": 100.0
    }]
)
```

---

## Related Files

| File | Description |
|------|-------------|
| NavCriteria_Entities.json | Machine-readable entity definitions |
| NavCriteria_Navigations.md | Navigation properties reference |
| NavCriteria_Actions.md | OData actions reference |
| NavCriteria_Metadata.xml | Raw OData metadata |
