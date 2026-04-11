# PartListMgmt Actions Reference

This document lists all OData actions for the PartListMgmt domain.

---

## PartList Actions

### CheckOut (Bound)

Check out a PartList for editing.

**Bound To:** `PartList`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| workable | PartList | No |
| CheckOutNote | String | Yes |

---

### CheckIn (Bound)

Check in a PartList.

**Bound To:** `PartList`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| workable | PartList | No |
| CheckInNote | String | Yes |
| CheckOutNote | String | Yes |
| KeepCheckedOut | Boolean | Yes |

---

### UndoCheckOut (Bound)

Undo check out for a PartList.

**Bound To:** `PartList`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| workable | PartList | No |

---

### Revise (Bound)

Revise a PartList.

**Bound To:** `PartList`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| versioned | PartList | No |
| VersionId | String | Yes |

---

### SetState (Bound)

Set lifecycle state for a PartList.

**Bound To:** `PartList`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| lifecycleManaged | PartList | No |
| State | String | No |

---

### UpdateCommonProperties (Bound)

Update common properties for a PartList.

**Bound To:** `PartList`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| PartList | PartList | No |
| Updates | Collection(CommonPropertyUpdate) | No |

---

## Bulk PartList Actions

### CheckOutPartLists (Unbound)

Check out multiple PartLists.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| Workables | Collection(String) | No |
| CheckOutNote | String | Yes |

---

### CheckInPartLists (Unbound)

Check in multiple PartLists.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| Workables | Collection(String) | No |
| CheckInNote | String | Yes |

---

### UndoCheckOutPartLists (Unbound)

Undo check out for multiple PartLists.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| Workables | Collection(String) | No |

---

### RevisePartLists (Unbound)

Revise multiple PartLists.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| PartLists | Collection(String) | No |

---

### SetStatePartLists (Unbound)

Set lifecycle state for multiple PartLists.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| PartLists | Collection(String) | No |
| State | String | No |

---

## PartListItem Actions

### CheckOut (Bound)

Check out a PartListItem for editing.

**Bound To:** `PartListItem`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| workable | PartListItem | No |
| CheckOutNote | String | Yes |

---

### CheckIn (Bound)

Check in a PartListItem.

**Bound To:** `PartListItem`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| workable | PartListItem | No |
| CheckInNote | String | Yes |
| CheckOutNote | String | Yes |
| KeepCheckedOut | Boolean | Yes |

---

### UndoCheckOut (Bound)

Undo check out for a PartListItem.

**Bound To:** `PartListItem`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| workable | PartListItem | No |

---

### Revise (Bound)

Revise a PartListItem.

**Bound To:** `PartListItem`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| versioned | PartListItem | No |
| VersionId | String | Yes |

---

### SetState (Bound)

Set lifecycle state for a PartListItem.

**Bound To:** `PartListItem`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| lifecycleManaged | PartListItem | No |
| State | String | No |

---

### UpdateCommonProperties (Bound)

Update common properties for a PartListItem.

**Bound To:** `PartListItem`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| PartListItem | PartListItem | No |
| Updates | Collection(CommonPropertyUpdate) | No |

---

## Illustration Actions

### UpdateCommonProperties (Bound)

Update common properties for an Illustration.

**Bound To:** `Illustration`

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| Illustration | Illustration | No |
| Updates | Collection(CommonPropertyUpdate) | No |

---

## PartListInformationElement Actions

### RevisePartListInformationElements (Unbound)

Revise multiple PartListInformationElements.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| PartListInformationElements | Collection(String) | No |

---

### SetStatePartListInformationElements (Unbound)

Set lifecycle state for multiple PartListInformationElements.

**Parameters:**

| Parameter | Type | Nullable |
|-----------|------|----------|
| PartListInformationElements | Collection(String) | No |
| State | String | No |

---

## Usage Examples

### Version Control for PartList

```python
from domains.PartListMgmt import PartListMgmtClient
client = PartListMgmtClient(config_path="config.json")

# Check out
client.check_out_partlist(partlist_id, check_out_note="Updating part list")

# Check in
client.check_in_partlist(partlist_id, check_in_note="Changes complete")

# Undo check out
client.undo_check_out_partlist(partlist_id)

# Revise
client.revise_partlist(partlist_id)
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

### Update Common Properties

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

### Bulk Version Control

```python
# Bulk check out
client.check_out_partlists_bulk([pl_id1, pl_id2], check_out_note="Bulk update")

# Bulk check in
client.check_in_partlists_bulk([pl_id1, pl_id2], check_in_note="Bulk complete")

# Bulk revise
client.revise_partlists_bulk([pl_id1, pl_id2])
```
