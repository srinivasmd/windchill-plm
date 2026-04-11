# ProdPlatformMgmt Domain Reference

Product Platform Management in PTC Windchill PLM. This domain handles product variants, options, choices, and variant specifications for configurable product platforms.

## Overview

| Property | Value |
|----------|-------|
| Namespace | PTC.ProdPlatformMgmt |
| Entity Sets | 4 |
| Entity Types | 14 |
| Actions | 19 |
| Complex Types | 4 |

---

## Entity Sets

- **Options**: Option
- **OptionSets**: OptionSet
- **Choices**: Choice
- **VariantSpecifications**: VariantSpecification

---

## Entity Types

### VariantSpecification

Primary entity for defining product variant specifications.

**Key:** `ID`

**Properties (19):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `CreatedBy` | String | Yes | Creator (ReadOnly) |
| `CreatedOn` | DateTimeOffset | Yes | Creation timestamp (ReadOnly) |
| `Description` | String | Yes | Description |
| `Effectivity` | String | Yes | Effectivity information |
| `ID` | String | Yes | Unique identifier (ReadOnly) |
| `Identity` | String | Yes | Identity |
| `ItemType` | PTC.EnumType | Yes | Item type |
| `LastModified` | DateTimeOffset | Yes | Last modified (ReadOnly) |
| `LifecycleState` | PTC.EnumType | Yes | Lifecycle state |
| `LifecycleTemplate` | String | Yes | Lifecycle template |
| `ModifiedBy` | String | Yes | Modifier (ReadOnly) |
| `Name` | String | No | Variant specification name |
| `Number` | String | Yes | Variant specification number |
| `Organization` | String | Yes | Organization |
| `Owner` | String | Yes | Owner (ReadOnly) |
| `State` | PTC.EnumType | Yes | State |
| `Team` | String | Yes | Team |
| `Type` | String | Yes | Type |
| `Version` | String | Yes | Version |

**Navigation Properties (10):**

| Navigation | Type | Description |
|------------|------|-------------|
| `Creator` | User | User who created |
| `Modifier` | User | User who last modified |
| `Owner` | User | Owner of specification |
| `Container` | Container | Container context |
| `Folder` | Folder | Folder location |
| `Master` | Master | Master reference |
| `Options` | Collection(Option) | Options for this specification |
| `OptionSets` | Collection(OptionSet) | Option sets for this specification |
| `ModuleVariantInformationLinks` | Collection(ModuleVariantInformationLink) | Module variant links |
| `IndependentAssignedExpressions` | Collection(IndependentAssignedExpression) | Assigned expressions |

---

### OptionSet

Defines a set of options for product configuration.

**Key:** `ID`

**Properties (20):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `CreatedBy` | String | Yes | Creator (ReadOnly) |
| `CreatedOn` | DateTimeOffset | Yes | Creation timestamp (ReadOnly) |
| `Description` | String | Yes | Description |
| `Expression` | String | Yes | Expression |
| `ID` | String | Yes | Unique identifier (ReadOnly) |
| `Identity` | String | Yes | Identity |
| `IsActive` | Boolean | Yes | Active status |
| `ItemType` | PTC.EnumType | Yes | Item type |
| `LastModified` | DateTimeOffset | Yes | Last modified (ReadOnly) |
| `LifecycleState` | PTC.EnumType | Yes | Lifecycle state |
| `LifecycleTemplate` | String | Yes | Lifecycle template |
| `ModifiedBy` | String | Yes | Modifier (ReadOnly) |
| `Name` | String | No | Option set name |
| `Number` | String | Yes | Option set number |
| `Organization` | String | Yes | Organization |
| `Owner` | String | Yes | Owner (ReadOnly) |
| `State` | PTC.EnumType | Yes | State |
| `Team` | String | Yes | Team |
| `Type` | String | Yes | Type |
| `Version` | String | Yes | Version |

**Navigation Properties (6):**

| Navigation | Type | Description |
|------------|------|-------------|
| `Creator` | User | User who created |
| `Modifier` | User | User who last modified |
| `Owner` | User | Owner of option set |
| `Container` | Container | Container context |
| `Options` | Collection(Option) | Options in this set |
| `ExpressionAliases` | Collection(ExpressionAlias) | Expression aliases |

---

### Option

Represents a configurable option within a product platform.

**Key:** `ID`

**Properties (7):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `ID` | String | Yes | Unique identifier (ReadOnly) |
| `Identity` | String | Yes | Identity |
| `Name` | String | No | Option name |
| `Number` | String | Yes | Option number |
| `State` | PTC.EnumType | Yes | State |
| `Type` | String | Yes | Type |
| `Version` | String | Yes | Version |

**Navigation Properties (4):**

| Navigation | Type | Description |
|------------|------|-------------|
| `DesignChoices` | Collection(DesignChoice) | Design choices for this option |
| `SalesChoices` | Collection(SalesChoice) | Sales choices for this option |
| `OptionGroup` | OptionGroup | Parent option group |
| `VariantSpecification` | VariantSpecification | Parent variant specification |

---

### Choice (Base Type)

Base entity for DesignChoice and SalesChoice.

**Key:** `ID`

**Properties (12):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `CreatedBy` | String | Yes | Creator (ReadOnly) |
| `CreatedOn` | DateTimeOffset | Yes | Creation timestamp (ReadOnly) |
| `Description` | String | Yes | Description |
| `ID` | String | Yes | Unique identifier (ReadOnly) |
| `Identity` | String | Yes | Identity |
| `LastModified` | DateTimeOffset | Yes | Last modified (ReadOnly) |
| `ModifiedBy` | String | Yes | Modifier (ReadOnly) |
| `Name` | String | Yes | Choice name |
| `Number` | String | Yes | Choice number |
| `State` | PTC.EnumType | Yes | State |
| `Type` | String | Yes | Type |
| `Version` | String | Yes | Version |

**Navigation Properties (4):**

| Navigation | Type | Description |
|------------|------|-------------|
| `Creator` | User | User who created |
| `Modifier` | User | User who last modified |
| `Owner` | User | Owner of choice |
| `Container` | Container | Container context |

---

### DesignChoice

Represents a design choice for an option. Extends Choice.

**Navigation Properties (1):**

| Navigation | Type | Description |
|------------|------|-------------|
| `DesignOption` | DesignOption | Parent design option |

---

### SalesChoice

Represents a sales choice for an option. Extends Choice.

**Navigation Properties (1):**

| Navigation | Type | Description |
|------------|------|-------------|
| `SalesOption` | SalesOption | Parent sales option |

---

### DesignOption

Represents a design option in the product platform.

**Navigation Properties (1):**

| Navigation | Type | Description |
|------------|------|-------------|
| `Choices` | Collection(DesignChoice) | Design choices for this option |

---

### SalesOption

Represents a sales option in the product platform.

**Navigation Properties (1):**

| Navigation | Type | Description |
|------------|------|-------------|
| `Choices` | Collection(SalesChoice) | Sales choices for this option |

---

### OptionGroup

A group of options for organization.

**Key:** `ID`

**Properties (1):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `Name` | String | No | Group name |

**Navigation Properties (1):**

| Navigation | Type | Description |
|------------|------|-------------|
| `Options` | Collection(Option) | Options in this group |

---

### ExpressionAlias

Defines an alias for an expression.

**Key:** `ID`

**Properties (15):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `Alias` | String | Yes | Alias name |
| `CreatedBy` | String | Yes | Creator (ReadOnly) |
| `CreatedOn` | DateTimeOffset | Yes | Creation timestamp (ReadOnly) |
| `Description` | String | Yes | Description |
| `Expression` | String | Yes | Expression value |
| `ID` | String | Yes | Unique identifier (ReadOnly) |
| `Identity` | String | Yes | Identity |
| `LastModified` | DateTimeOffset | Yes | Last modified (ReadOnly) |
| `ModifiedBy` | String | Yes | Modifier (ReadOnly) |
| `Name` | String | Yes | Name |
| `Number` | String | Yes | Number |
| `State` | PTC.EnumType | Yes | State |
| `Type` | String | Yes | Type |
| `Version` | String | Yes | Version |
| `OptionSet` | String | Yes | Parent option set |

**Navigation Properties (7):**

| Navigation | Type | Description |
|------------|------|-------------|
| `Creator` | User | User who created |
| `Modifier` | User | User who last modified |
| `Owner` | User | Owner |
| `Container` | Container | Container context |
| `OptionSet` | OptionSet | Parent option set |
| `IndependentAssignedExpressions` | Collection(IndependentAssignedExpression) | Assigned expressions |
| `OptionSetAssignableEntities` | Collection(OptionSetAssignableEntity) | Assignable entities |

---

### IndependentAssignedExpression

An expression assigned independently.

**Key:** `ID`

**Properties (19):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `AssignedExpression` | String | Yes | Assigned expression |
| `CreatedBy` | String | Yes | Creator (ReadOnly) |
| `CreatedOn` | DateTimeOffset | Yes | Creation timestamp (ReadOnly) |
| `Description` | String | Yes | Description |
| `ID` | String | Yes | Unique identifier (ReadOnly) |
| `Identity` | String | Yes | Identity |
| `ItemType` | PTC.EnumType | Yes | Item type |
| `LastModified` | DateTimeOffset | Yes | Last modified (ReadOnly) |
| `LifecycleState` | PTC.EnumType | Yes | Lifecycle state |
| `ModifiedBy` | String | Yes | Modifier (ReadOnly) |
| `Name` | String | Yes | Name |
| `Number` | String | Yes | Number |
| `Organization` | String | Yes | Organization |
| `Owner` | String | Yes | Owner (ReadOnly) |
| `State` | PTC.EnumType | Yes | State |
| `Team` | String | Yes | Team |
| `Type` | String | Yes | Type |
| `VariantSpecification` | String | Yes | Parent variant specification |
| `Version` | String | Yes | Version |

**Navigation Properties (6):**

| Navigation | Type | Description |
|------------|------|-------------|
| `Creator` | User | User who created |
| `Modifier` | User | User who last modified |
| `Owner` | User | Owner |
| `Container` | Container | Container context |
| `VariantSpecification` | VariantSpecification | Parent variant specification |
| `ExpressionAlias` | ExpressionAlias | Expression alias |

---

### ModuleVariantInformationLink

Links module variant information to variant specifications.

**Key:** `ID`

**Properties (1):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `ID` | String | Yes | Unique identifier (ReadOnly) |

**Navigation Properties (2):**

| Navigation | Type | Description |
|------------|------|-------------|
| `VariantSpecification` | VariantSpecification | Parent variant specification |
| `Module` | Part | Linked module part |

---

### OptionSetAssignableEntity

Entity that can be assigned to an option set.

**Key:** `ID`

**Properties (4):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `AssignableEntity` | String | Yes | Assignable entity reference |
| `ID` | String | Yes | Unique identifier (ReadOnly) |
| `OptionSet` | String | Yes | Parent option set |
| `Type` | String | Yes | Entity type |

**Navigation Properties (1):**

| Navigation | Type | Description |
|------------|------|-------------|
| `ExpressionAlias` | ExpressionAlias | Expression alias |

---

### OptionPoolItem (Base Type)

Base entity for OptionGroup.

**Key:** `ID`

**Properties (5):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `ID` | String | Yes | Unique identifier (ReadOnly) |
| `Identity` | String | Yes | Identity |
| `Name` | String | Yes | Name |
| `Number` | String | Yes | Number |
| `State` | PTC.EnumType | Yes | State |

**Navigation Properties (1):**

| Navigation | Type | Description |
|------------|------|-------------|
| `Container` | Container | Container context |

---

## Actions (19)

### Unbound Actions

#### GetAssignedExpressions

Get assigned expressions for an entity.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `EntityID` | String | No |

---

#### GetVariantSpecificationsLinkedFromMVIL

Get variant specifications linked from module variant information links.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `MVILID` | String | No |

---

#### GetAssignedOptionSets

Get assigned option sets for an entity.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `EntityID` | String | No |

---

#### SetStateChoices

Set state for multiple choices.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Choices` | Collection(String) | No |
| `State` | String | No |

---

#### SetStateVariantSpecifications

Set state for multiple variant specifications.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `VariantSpecifications` | Collection(String) | No |
| `State` | String | No |

---

#### ReviseVariantSpecifications

Revise multiple variant specifications.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `VariantSpecifications` | Collection(String) | No |

---

#### CheckOutVariantSpecifications

Check out multiple variant specifications.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `VariantSpecifications` | Collection(String) | No |
| `CheckOutNote` | String | Yes |

---

#### CheckInVariantSpecifications

Check in multiple variant specifications.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `VariantSpecifications` | Collection(String) | No |
| `CheckInNote` | String | Yes |

---

#### UndoCheckOutVariantSpecifications

Undo check out for multiple variant specifications.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `VariantSpecifications` | Collection(String) | No |

---

#### SetStateOptionSets

Set state for multiple option sets.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `OptionSets` | Collection(String) | No |
| `State` | String | No |

---

#### ReviseOptionSets

Revise multiple option sets.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `OptionSets` | Collection(String) | No |

---

### Bound Actions

#### SetState (Bound to Choice)

Set lifecycle state of a choice.

**Bound To:** `Choice`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `State` | String | No |

---

#### SetState (Bound to VariantSpecification)

Set lifecycle state of a variant specification.

**Bound To:** `VariantSpecification`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `State` | String | No |

---

#### Revise (Bound to VariantSpecification)

Revise a variant specification.

**Bound To:** `VariantSpecification`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Description` | String | Yes |
| `Option` | String | Yes |

---

#### CheckIn (Bound to VariantSpecification)

Check in a variant specification.

**Bound To:** `VariantSpecification`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `CheckInNote` | String | Yes |
| `Description` | String | Yes |
| `KeepCheckedOut` | Boolean | Yes |
| `Version` | String | Yes |

---

#### CheckOut (Bound to VariantSpecification)

Check out a variant specification.

**Bound To:** `VariantSpecification`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `CheckOutNote` | String | Yes |
| `Description` | String | Yes |

---

#### UndoCheckOut (Bound to VariantSpecification)

Undo check out for a variant specification.

**Bound To:** `VariantSpecification`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `VariantSpecification` | VariantSpecification | No |

---

#### SetState (Bound to OptionSet)

Set lifecycle state of an option set.

**Bound To:** `OptionSet`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `State` | String | No |

---

#### Revise (Bound to OptionSet)

Revise an option set.

**Bound To:** `OptionSet`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| `Description` | String | Yes |
| `Option` | String | Yes |

---

## Complex Types (4)

### OptionSetAssignableListItem

List item for option set assignable entities.

### PartsToVariantSpecificationsListItem

List item for parts to variant specifications mapping.

### AssignedExpression

Assigned expression structure.

### AssignedExpressionItem

Individual assigned expression item.

---

## Usage Examples

### Query Variant Specifications

```python
from domains.ProdPlatformMgmt import ProdPlatformMgmtClient
client = ProdPlatformMgmtClient(config_path="config.json")

# Get all variant specifications
specs = client.get_variant_specifications(top=50)

# Get by number
spec = client.get_variant_specification_by_number("VS-2024-001")

# Get by state
released = client.get_variant_specifications_by_state("RELEASED")

# Get with expanded navigation
spec = client.get_variant_specification_by_id(spec_id, expand=[
    "Options",
    "OptionSets",
    "Creator",
    "Owner"
])
```

### Query Options and Option Sets

```python
# Get all options
options = client.get_options(top=50)
option = client.get_option_by_number("OPT-001")

# Get all option sets
option_sets = client.get_option_sets(top=50)
option_set = client.get_option_set_by_number("OS-001")

# Get options for a variant specification
options = client.get_options_for_variant_spec(spec_id)

# Get option sets for a variant specification
option_sets = client.get_option_sets_for_variant_spec(spec_id)
```

### Manage Choices

```python
# Get choices
choices = client.get_choices(top=50)
choice = client.get_choice_by_number("CH-001")

# Get design choices for an option
design_choices = client.get_design_choices_for_option(option_id)

# Get sales choices for an option
sales_choices = client.get_sales_choices_for_option(option_id)
```

### Version Control Operations

```python
# Check out
client.check_out_variant_specification(spec_id, check_out_note="Updating specification")

# Check in
client.check_in_variant_specification(
    spec_id,
    check_in_note="Changes complete",
    keep_checked_out=False
)

# Undo check out
client.undo_check_out_variant_specification(spec_id)

# Revise
client.revise_variant_specification(spec_id, description="New revision")
```

### Lifecycle State Management

```python
# Set state for single entity
client.set_variant_specification_state(spec_id, "RELEASED")
client.set_option_set_state(option_set_id, "RELEASED")
client.set_choice_state(choice_id, "RELEASED")

# Set state for multiple entities
client.set_variant_specifications_state_bulk([spec_id1, spec_id2], "INWORK")
client.set_option_sets_state_bulk([os_id1, os_id2], "RELEASED")
client.set_choices_state_bulk([ch_id1, ch_id2], "RELEASED")
```

### Expression Management

```python
# Get assigned expressions
expressions = client.get_assigned_expressions(spec_id)

# Get expression aliases
aliases = client.get_expression_aliases(option_set_id)

# Create expression alias
alias = client.create_expression_alias(
    option_set_id=option_set_id,
    alias="ColorRed",
    expression="Color = 'Red'"
)
```

---

## Related Files

| File | Description |
|------|-------------|
| ProdPlatformMgmt_Entities.json | Machine-readable entity definitions |
| ProdPlatformMgmt_Navigations.md | Navigation properties reference |
| ProdPlatformMgmt_Actions.md | OData actions reference |
| ProdPlatformMgmt_Metadata.xml | Raw OData metadata |
