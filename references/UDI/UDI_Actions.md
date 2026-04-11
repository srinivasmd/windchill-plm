# UDI Actions

This document describes OData actions available in this domain.

## Unbound Actions

These actions can be called directly on the entity set.

| Action | Parameters | Return Type |
|--------|------------|-------------|
| ReviseUDISuperSets2 | UDISuperSets2 | UDISuperSet2) |
| SetStateUDISuperSets2 | UDISuperSets2, State | UDISuperSet2) |
| SetStateUDISuperSets | UDISuperSets, State | UDISuperSet) |

## Bound Actions

These actions are bound to specific entity types.

| Action | Bound To | Parameters | Return Type |
|--------|----------|------------|-------------|
| Revise | UDISuperSet2 | VersionId | UDISuperSet2 |
| SetState | UDISuperSet2 | State | UDISuperSet2 |
| SetState | UDISuperSet | State | UDISuperSet |
