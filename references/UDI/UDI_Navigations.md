# UDI Navigation Properties

This document describes navigation properties for entities in this domain.

## UDISuperSet2

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Template | UDISuperSet2 |  | No |
| Subjects | SubjectLink |  | No |
| Details | Detail |  | Yes |
| PackagingConfigurations | PackagingConfiguration |  | Yes |
| Context | Container |  | No |
| Versions | UDISuperSet2 |  | No |
| Creator | User |  | No |
| Folder | Folder |  | No |
| Revisions | UDISuperSet2 |  | No |
| Modifier | User |  | No |

## SubjectLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Subject | UDISubject |  | No |

## PackagingConfiguration

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Contains | PackagingConfiguration |  | Yes |

## UDISuperSet

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Template | UDISuperSet |  | No |
| Subject | UDISubject |  | No |
| Details | Detail |  | Yes |
| PackagingConfigurations | PackagingConfiguration |  | Yes |
| Context | Container |  | No |
| Creator | User |  | No |
| Modifier | User |  | No |

## UDISubject

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Context | Container |  | No |
| Creator | User |  | No |
| Modifier | User |  | No |

## UDISuperSetDetail

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Context | Container |  | No |
