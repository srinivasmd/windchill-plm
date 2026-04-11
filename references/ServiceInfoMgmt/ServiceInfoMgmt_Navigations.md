# ServiceInfoMgmt Navigation Properties

This document describes navigation properties for entities in this domain.

## GraphicalInformationElement

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Content | SIMDynamicDocument |  | No |

## SIMDocument

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| InformationElement | DocumentInformationElement |  | No |

## InformationBaseObject

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Uses | InformationUsageLink |  | Yes |
| UsedBy | InformationBaseObject |  | No |
| Context | Container |  | No |
| PPlan_LinkNav | ObjectReferenceable |  | No |
| Versions | InformationBaseObject |  | No |
| Organization | Organization |  | No |
| Creator | User |  | No |
| Representations | Representation |  | No |
| Revisions | InformationBaseObject |  | No |
| Folder | Folder |  | No |
| Modifier | User |  | No |

## DocumentInformationElement

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Content | SIMDocument |  | No |

## SIMDynamicDocument

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| InformationElement | DynamicDocumentInformationElement |  | Yes |

## TextualInformationElement

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Content | SIMDynamicDocument |  | No |

## InformationUsageLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Uses | InformationBaseObject |  | No |
| UsedBy | InformationBaseObject |  | No |

## Structure

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ServiceObject | InformationBaseObject |  | No |
| ServiceObjectUse | InformationUsageLink |  | No |
| Children | Structure |  | Yes |
