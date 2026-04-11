# DataAdmin Navigation Properties

This document describes navigation properties for entities in this domain.

## ProductContainer

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| AssignedOptionSet | OptionSet |  | No |
| OptionPoolAliases | ExpressionAlias |  | No |
| OptionPool | OptionPoolItem |  | No |

## Container

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Folders | Folder |  | Yes |
| Creator | User |  | No |
| Organization | Organization |  | No |

## LibraryContainer

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| AssignedOptionSet | OptionSet |  | No |
| OptionPoolAliases | ExpressionAlias |  | No |
| OptionPool | OptionPoolItem |  | No |

## Folder

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Folders | Folder |  | Yes |
| Contents | FolderContent |  | Yes |
| FolderContents | WindchillEntity |  | Yes |

## Participant

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Principals | Principal |  | No |
