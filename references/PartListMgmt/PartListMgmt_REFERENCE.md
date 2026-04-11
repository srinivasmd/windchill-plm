# PartListMgmt Domain Reference

Part List Management in PTC Windchill PLM. This domain handles Illustrated Parts Lists (IPL), Part List Items, Illustrations, Substitutes, and Supplements for service information management.

## Overview

| Property | Value |
|----------|-------|
| Namespace | PTC.PartListMgmt |
| Entity Sets | 6 |
| Entity Types | 6 |
| Actions | 20 |
| Complex Types | 0 |

---

## Entity Sets

| Entity Set | Entity Type | Description |
|------------|-------------|-------------|
| PartLists | PartList | Illustrated Parts Lists |
| PartListItems | PartListItem | Items within Part Lists |
| Illustrations | Illustration | Illustrations for Part Lists |
| PartListInformationElements | PartListInformationElement | Information elements |
| Substitutes | Substitute | Substitute parts |
| Supplements | Supplement | Supplement parts |

---

## Entity Types

### PartList

Primary entity for Illustrated Parts Lists. Contains parts information with illustrations for service documentation.

**Key:** `ID`

**Base Type:** WindchillEntity

**Properties (39):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `Name` | String | No | Part List name (UpdateableViaAction) |
| `Number` | String | Yes | Part List number (UpdateableViaAction) |
| `Description` | String | Yes | Description |
| `Revision` | String | Yes | Revision |
| `Version` | String | Yes | Version (NonFilterable) |
| `VersionID` | String | Yes | Version ID (NonFilterable, NonSortable) |
| `Latest` | Boolean | Yes | Latest version flag |
| `MasterID` | String | Yes | Master ID |
| `State` | EnumType | Yes | Lifecycle state |
| `CheckOutStatus` | String | Yes | Check-out status (NonFilterable, NonSortable) |
| `CheckoutState` | String | Yes | Checkout state (NonFilterable) |
| `WorkInProgressState` | WorkInProgressType | Yes | WIP state (NonFilterable, NonSortable) |
| `LifeCycleTemplateName` | String | Yes | Lifecycle template (NonFilterable, NonSortable) |
| `Generated` | Boolean | Yes | Generated flag (UpdateableViaAction) |
| `UpdateRequired` | Boolean | Yes | Update required flag (UpdateableViaAction) |
| `RegenerateRequired` | Boolean | Yes | Regenerate required flag (UpdateableViaAction) |
| `AuthoringLanguage` | AuthoringLanguage | Yes | Authoring language (NonFilterable, NonSortable, UpdateableViaAction) |
| `InformationType` | String | Yes | Information type |
| `PartListItemType` | String | Yes | Part list item type |
| `View` | String | Yes | View |
| `Comments` | String | Yes | Comments |
| `FolderName` | String | Yes | Folder name |
| `FolderLocation` | String | Yes | Folder location (NonFilterable, NonSortable) |
| `CabinetName` | String | Yes | Cabinet name |
| `CreatedBy` | String | Yes | Creator |
| `ModifiedBy` | String | Yes | Modifier |
| `OrganizationName` | String | Yes | Organization name (NonFilterable, NonSortable) |
| `GeneralStatus` | Icon | Yes | Status icon (NonFilterable, NonSortable) |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| `Creator` | User | User who created |
| `Modifier` | User | User who last modified |
| `Folder` | Folder | Folder location |
| `Context` | Container | Container context |
| `Organization` | Organization | Organization (UpdateableViaAction) |
| `Versions` | Collection(PartList) | Version history |
| `Revisions` | Collection(PartList) | Revision history |
| `Uses` | Collection(PartListItem) | Part list items |
| `DescribedBy` | Collection(Illustration) | Illustrations |
| `InformationElement` | Collection(PartListInformationElement) | Information elements |
| `Representations` | Collection(Representation) | Visualizations |

---

### PartListItem

Individual item within a Part List. Represents a part reference with quantity and position.

**Key:** `ID`

**Base Type:** WindchillEntity

**Properties (21):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `Name` | String | No | Item name (NonFilterable, NonSortable, UpdateableViaAction) |
| `Number` | String | Yes | Item number (NonFilterable, NonSortable, UpdateableViaAction) |
| `LineNumber` | Int64 | Yes | Line number in list |
| `ItemNumber` | String | Yes | Item number |
| `ItemSequenceNumber` | Int64 | Yes | Sequence number (NonFilterable, NonSortable) |
| `Quantity` | String | Yes | Quantity |
| `DefaultUnit` | EnumType | No | Default unit (NonFilterable, NonSortable, UpdateableViaAction) |
| `Indenture` | Int64 | Yes | Indentation level |
| `GraphicRef` | String | Yes | Graphic reference |
| `Illustrated` | Boolean | Yes | Illustrated flag (NonFilterable, NonSortable) |
| `Serviceable` | Boolean | Yes | Serviceable flag (NonFilterable, NonSortable) |
| `ComponentIds` | String | Yes | Component IDs |
| `InstanceIds` | String | Yes | Instance IDs |
| `StructureId` | String | Yes | Structure ID |
| `Remarks` | String | Yes | Remarks |
| `AuthoringLanguage` | AuthoringLanguage | Yes | Language (NonFilterable, NonSortable, UpdateableViaAction) |
| `CopiedFromBom` | Boolean | Yes | Copied from BOM flag |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| `UsedBy` | PartList | Parent PartList |
| `Uses` | Part | Referenced Part |
| `Substitutes` | Collection(Substitute) | Substitute parts |
| `Supplements` | Collection(Supplement) | Supplement parts |

---

### Illustration

Illustration associated with Part Lists. Links Part Lists to visual representations.

**Key:** `ID`

**Base Type:** WindchillEntity

**Properties (9):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `AuthoringApplication` | String | Yes | Authoring application (UpdateableViaAction) |
| `AuthoringLanguage` | AuthoringLanguage | Yes | Language (NonFilterable, NonSortable, UpdateableViaAction) |
| `Format` | String | Yes | Illustration format |
| `GraphicRef` | String | Yes | Graphic reference |
| `NavCriteria` | String | Yes | Navigation criteria (NonFilterable, NonSortable) |
| `PrintOrder` | Int64 | Yes | Print order |
| `PrintView` | String | Yes | Print view |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| `Describes` | PartList | PartList described |
| `DescribedBy` | DynamicDocument | Source document |

---

### PartListInformationElement

Information element for Part List metadata.

**Key:** `ID`

**Base Type:** InformationBaseObject

**Properties (5):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `SisContentholderType` | String | Yes | Content holder type |
| `SisContentholderTitleFromContent` | Boolean | Yes | Title from content |
| `SisContentholderIterationInfoModifier` | String | Yes | Modifier |
| `Symptoms` | Collection(String) | Yes | Symptoms |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| `Content` | PartList | Associated PartList |

---

### Substitute

Substitute part for a PartListItem. Defines alternative parts that can be used.

**Key:** `ID`

**Base Type:** WindchillEntity

**Properties (4):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `ReplacementType` | EnumType | Yes | Type of replacement |
| `CopiedFromBom` | Boolean | Yes | Copied from BOM flag |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| `SubstituteFor` | PartListItem | Item this substitutes |
| `Substitutes` | Part | The substitute Part |

---

### Supplement

Supplement part for a PartListItem. Defines additional parts required.

**Key:** `ID`

**Base Type:** WindchillEntity

**Properties (3):**

| Property | Type | Nullable | Notes |
|----------|------|----------|-------|
| `CopiedFromBom` | Boolean | Yes | Copied from BOM flag |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| `SupplementedBy` | PartListItem | Item this supplements |
| `Supplements` | Part | The supplement Part |

---

## Actions (20)

### Version Control Actions

| Action | Bound | Parameters | Description |
|--------|-------|------------|-------------|
| CheckOut | Yes | workable, CheckOutNote | Check out PartList/PartListItem |
| CheckIn | Yes | workable, CheckInNote, CheckOutNote, KeepCheckedOut | Check in PartList/PartListItem |
| UndoCheckOut | Yes | workable | Undo check out |
| Revise | Yes | versioned, VersionId | Revise PartList/PartListItem |

### Bulk Version Control Actions

| Action | Bound | Parameters | Description |
|--------|-------|------------|-------------|
| CheckOutPartLists | No | Workables, CheckOutNote | Check out multiple PartLists |
| CheckInPartLists | No | Workables, CheckInNote | Check in multiple PartLists |
| UndoCheckOutPartLists | No | Workables | Undo check out for multiple |
| RevisePartLists | No | PartLists | Revise multiple PartLists |

### Lifecycle State Actions

| Action | Bound | Parameters | Description |
|--------|-------|------------|-------------|
| SetState | Yes | lifecycleManaged, State | Set state for PartList/PartListItem |
| SetStatePartLists | No | PartLists, State | Set state for multiple PartLists |
| SetStatePartListInformationElements | No | PartListInformationElements, State | Set state for InfoElements |

### Property Update Actions

| Action | Bound | Parameters | Description |
|--------|-------|------------|-------------|
| UpdateCommonProperties | Yes | PartList, Updates | Update PartList properties |
| UpdateCommonProperties | Yes | PartListItem, Updates | Update PartListItem properties |
| UpdateCommonProperties | Yes | Illustration, Updates | Update Illustration properties |

---

## Usage Examples

### Query Part Lists

```python
from domains.PartListMgmt import PartListMgmtClient
client = PartListMgmtClient(config_path="config.json")

# Get all Part Lists
partlists = client.get_partlists(top=50)

# Get by number
partlist = client.get_partlist_by_number("PL-001")

# Get by state
released = client.get_partlists_by_state("RELEASED")

# Get with expanded navigation
partlist = client.get_partlist_by_id(partlist_id, expand=[
    "Uses",
    "Creator",
    "Organization",
    "Versions"
])
```

### Query Part List Items

```python
# Get all Part List Items
items = client.get_partlist_items(top=50)

# Get by ID with navigation
item = client.get_partlist_item_by_id(item_id, expand=[
    "Uses",
    "UsedBy",
    "Substitutes",
    "Supplements"
])

# Get items for a Part List
items = client.get_partlist_items_for_partlist(partlist_id)

# Get Part referenced by item
part = client.get_part_for_item(item_id)
```

### Query Illustrations

```python
# Get all illustrations
illustrations = client.get_illustrations(top=50)

# Get by ID
illustration = client.get_illustration_by_id(ill_id)

# Get illustrations for a Part List
illustrations = client.get_illustrations_for_partlist(partlist_id)

# Get Part List for illustration
partlist = client.get_partlist_for_illustration(ill_id)
```

### Manage Substitutes and Supplements

```python
# Get substitutes for a Part List Item
substitutes = client.get_substitutes_for_item(item_id)

# Get supplements for a Part List Item
supplements = client.get_supplements_for_item(item_id)

# Get substitute by ID
substitute = client.get_substitute_by_id(sub_id)

# Get supplement by ID
supplement = client.get_supplement_by_id(sup_id)
```

### Version Control Operations

```python
# Check out
client.check_out_partlist(partlist_id, check_out_note="Updating part list")

# Check in
client.check_in_partlist(partlist_id, check_in_note="Changes complete")

# Undo check out
client.undo_check_out_partlist(partlist_id)

# Revise
client.revise_partlist(partlist_id)

# Bulk operations
client.check_out_partlists_bulk([pl_id1, pl_id2], check_out_note="Bulk update")
client.check_in_partlists_bulk([pl_id1, pl_id2], check_in_note="Bulk complete")
client.revise_partlists_bulk([pl_id1, pl_id2])
```

### Lifecycle State Management

```python
# Set state for single PartList
client.set_partlist_state(partlist_id, "RELEASED")

# Set state for multiple PartLists
client.set_partlists_state_bulk([pl_id1, pl_id2], "RELEASED")

# Set state for PartListInformationElements
client.set_partlist_information_elements_state_bulk([ie_id1, ie_id2], "INWORK")
```

### Update Properties

```python
# Update PartList properties
client.update_partlist_properties(partlist_id, updates=[
    {"Name": "New Part List Name"},
    {"Number": "PL-NEW-001"}
])

# Update PartListItem properties
client.update_partlist_item_properties(item_id, updates=[
    {"Name": "New Item Name"},
    {"Quantity": "10"}
])

# Update Illustration properties
client.update_illustration_properties(ill_id, updates=[
    {"PrintOrder": 1},
    {"Format": "SVG"}
])
```

---

## Related Files

| File | Description |
|------|-------------|
| PartListMgmt_Entities.json | Machine-readable entity definitions |
| PartListMgmt_Navigations.md | Navigation properties reference |
| PartListMgmt_Actions.md | OData actions reference |
| PartListMgmt_Metadata.xml | Raw OData metadata |
