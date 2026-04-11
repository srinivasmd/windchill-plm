# PartListMgmt Navigation Properties

This document lists all navigation properties for PartListMgmt domain entities.

---

## PartList

Primary entity for Part Lists (Illustrated Parts Lists).

| Navigation | Type | Description |
|------------|------|-------------|
| `Creator` | User | User who created the PartList |
| `Modifier` | User | User who last modified the PartList |
| `Folder` | Folder | Folder location |
| `Context` | Container | Container context |
| `Organization` | Organization | Organization |
| `Versions` | Collection(PartList) | Version history |
| `Revisions` | Collection(PartList) | Revision history |
| `Uses` | Collection(PartListItem) | Part list items (BOM items) |
| `DescribedBy` | Collection(Illustration) | Illustrations describing this PartList |
| `InformationElement` | Collection(PartListInformationElement) | Information elements |
| `Representations` | Collection(Representation) | Visualization representations |

---

## PartListItem

Individual item in a Part List.

| Navigation | Type | Description |
|------------|------|-------------|
| `UsedBy` | PartList | Parent PartList |
| `Uses` | Part | Referenced Part |
| `Substitutes` | Collection(Substitute) | Substitute parts |
| `Supplements` | Collection(Supplement) | Supplement parts |

---

## Illustration

Illustration associated with Part Lists.

| Navigation | Type | Description |
|------------|------|-------------|
| `Describes` | PartList | PartList described by this Illustration |
| `DescribedBy` | DynamicDocument | DynamicDocument source |

---

## Substitute

Substitute part for a PartListItem.

| Navigation | Type | Description |
|------------|------|-------------|
| `SubstituteFor` | PartListItem | PartListItem this substitutes |
| `Substitutes` | Part | The substitute Part |

---

## Supplement

Supplement part for a PartListItem.

| Navigation | Type | Description |
|------------|------|-------------|
| `SupplementedBy` | PartListItem | PartListItem this supplements |
| `Supplements` | Part | The supplement Part |

---

## PartListInformationElement

Information element for PartList.

| Navigation | Type | Description |
|------------|------|-------------|
| `Content` | PartList | Associated PartList |

---

## Usage Examples

### Get PartList with Items

```python
from domains.PartListMgmt import PartListMgmtClient
client = PartListMgmtClient(config_path="config.json")

# Get PartList with expanded navigation
partlist = client.get_partlist_by_id(partlist_id, expand=[
    "Uses",
    "Creator",
    "Organization",
    "Versions"
])

# Get items in PartList
items = client.get_partlist_items_for_partlist(partlist_id)

# Get illustrations
illustrations = client.get_illustrations_for_partlist(partlist_id)
```

### Get PartListItem with Substitutes

```python
# Get PartListItem with navigation
item = client.get_partlist_item_by_id(item_id, expand=[
    "Uses",
    "UsedBy",
    "Substitutes",
    "Supplements"
])

# Get substitutes
substitutes = client.get_substitutes_for_item(item_id)

# Get supplements
supplements = client.get_supplements_for_item(item_id)
```

### Get Illustration Details

```python
# Get illustration
illustration = client.get_illustration_by_id(ill_id, expand=[
    "Describes",
    "DescribedBy"
])

# Get PartList for illustration
partlist = client.get_partlist_for_illustration(ill_id)
```
