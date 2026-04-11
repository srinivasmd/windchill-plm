# ProdMgmt Navigation Properties

This document describes navigation properties for entities in this domain.

## TreeStructureItem

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Object | WindchillEntity |  | No |
| Link | WindchillEntity |  | Yes |
| Occurrence | UsageOccurrence |  | Yes |
| Components | TreeStructureItem |  | Yes |

## SecondaryCoproduceLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Secondary | Part |  | No |
| CoProduce | Coproduce |  | No |
| AlternateSetMaster | ObjectReferenceable |  | No |
| ResultedByObjects | ChangeItem |  | Yes |

## EquivalenceNetworkNode

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| AllParts | EquivalenceNetworkNode |  | No |
| Downstream | EquivalenceNetworkNode |  | No |
| Upstream | EquivalenceNetworkNode |  | No |
| Part | WindchillEntity |  | No |
| EquivalenceLink | EquivalenceLink |  | No |

## PrimaryCoproduceLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Primary | Part |  | No |
| CoProduce | Coproduce |  | No |
| AlternateSetMaster | ObjectReferenceable |  | No |
| ResultedByObjects | ChangeItem |  | Yes |

## EquivalentUsageAssociation

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| UpstreamPart | Part |  | No |
| DownstreamPart | Part |  | No |
| EquivalenceLink | EquivalenceLink |  | No |
| UsageLink | PartUse |  | No |

## PrimaryCoproduceAssociation

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Primary | Part |  | No |
| CoProduce | Coproduce |  | No |

## GDSFromTemplateContext

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| SourceRoot | Part |  | No |
| TargetRoot | Part |  | No |
| UpstreamNavigationCriteria | NavigationCriteria |  | No |
| DownstreamNavigationCriteria | NavigationCriteria |  | No |

## RawMaterialAlternateLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Alternates | MadeFromSet |  | No |
| AlternateFor | Part |  | No |

## PasteAsNewPartDefinition

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| TransformationEntity | Part |  | No |

## MadeFromSet

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| AlternateMadeFromLinkToParent | RawMaterialAlternateLink |  | No |
| AlternateFor | Part |  | No |
| Context | Container |  | No |
| PPlan_LinkNav | ObjectReferenceable |  | No |
| Organization | Organization |  | No |
| ExtendedData | ExtendedData |  | No |
| Creator | User |  | No |
| Revisions | MadeFromSet |  | No |
| Folder | Folder |  | No |
| ResultedByObjects | ChangeItem |  | Yes |
| Versions | MadeFromSet |  | No |
| MadeFromLink | RawMaterialLink |  | No |
| Effectivities | Effectivity |  | Yes |
| PartMadeFrom | Part |  | No |
| Modifier | User |  | No |

## EquivalenceLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Upstream | WindchillEntity |  | No |
| Downstream | WindchillEntity |  | No |

## CoproduceUsageMembersAssociation

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Coproduce | Coproduce |  | No |
| UsageMembers | Part |  | No |

## AbstractExtendedData

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Creator | User |  | No |
| Modifier | User |  | No |

## NewDownstreamPartDefinition

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| TransformationEntity | Part |  | No |

## RawMaterialLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Makes | Part |  | No |
| MadeFrom | Part |  | No |
| PendingEffectivities | PendingLinkEffectivity |  | Yes |
| Effectivities | Effectivity |  | Yes |

## NewDownstreamBranchDefinition

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| TransformationEntity | TransformationEntity |  | No |

## TransformationDefinition

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| SourcePart | Part |  | No |
| ExistingDownstreamAssociations | ExistingDownstreamAssociation |  | No |

## XBOMPart

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Creator | User |  | No |
| Modifier | User |  | No |

## StandardCC

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Creator | User |  | No |
| Modifier | User |  | No |

## ExtendedData

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| DepartmentData | DepartmentData |  | No |
| Context | Container |  | No |
| ResultedByObjects | ChangeItem |  | Yes |
| Versions | ExtendedData |  | No |
| Organization | Organization |  | No |
| Effectivities | Effectivity |  | Yes |
| Revisions | ExtendedData |  | No |
| Folder | Folder |  | No |

## NewDownstreamAlternateDefinition

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| SourcePart | Part |  | No |
| TransformationEntity | TransformationEntity |  | No |

## PlantDataDepartmentDataAssociation

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Plant | ExtendedData |  | No |
| DepartmentData | DepartmentData |  | No |

## NewAlternate

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Folder | Folder |  | No |

## DepartmentData

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Context | Container |  | No |
| ResultedByObjects | ChangeItem |  | Yes |
| Versions | DepartmentData |  | No |
| Organization | Organization |  | No |
| Effectivities | Effectivity |  | Yes |
| Revisions | DepartmentData |  | No |

## MadeFromAssociation

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Makes | Part |  | No |
| MadeFrom | Part |  | No |
| RawMaterialLink | RawMaterialLink |  | No |

## CoproduceSecondaryMembersAssociation

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Coproduce | Coproduce |  | No |
| SecondaryMembers | Part |  | No |

## EquivalenceLinkAssociation

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| EquivalenceLink | EquivalenceLink |  | No |
| UpstreamRoot | Part |  | No |
| DownstreamRoot | Part |  | No |
| UpstreamPart | Part |  | No |
| DownstreamPart | Part |  | No |

## TransformationEntity

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Context | Container |  | No |
| Folder | Folder |  | No |

## EquivalenceUsageAssociation

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| UpstreamRoot | Part |  | No |
| DownstreamRoot | Part |  | No |
| UpstreamPart | Part |  | No |
| DownstreamPart | Part |  | No |
| EquivalenceUsageLink | EquivalenceUsageLink |  | No |

## CoProduceUsageLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| CoProduceUsedBy | Part |  | No |
| CoProduceUses | Part |  | No |
| ResultedByObjects | ChangeItem |  | Yes |

## MadeFromSetAssociation

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Makes | Part |  | No |
| MadeFromSet | MadeFromSet |  | No |
| RawMaterialAlternateLink | RawMaterialAlternateLink |  | No |

## ExistingDownstreamAssociation

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| UpstreamPart | Part |  | No |
| DownstreamPart | Part |  | No |
| EquivalenceLink | EquivalenceLink |  | No |

## PartPlantDataAssociation

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Part | Part |  | No |
| Plants | ExtendedData |  | No |

## ReplaceMadeFromAssociation

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Makes | Part |  | No |
| MadeFrom | Part |  | No |
| RawMaterialLink | RawMaterialLink |  | No |
| RootPart | Part |  | No |
| NavigationCriteria | NavigationCriteria |  | No |

## PasteAsNewBranchDefinition

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| TransformationEntity | TransformationEntity |  | No |

## Coproduce

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| PrimaryPart | Part |  | No |
| SecondaryMembers | Part |  | No |
| PrimaryCoproduceLink | PrimaryCoproduceLink |  | No |
| SecondaryCoproduceLinks | SecondaryCoproduceLink |  | No |
| CoProduceUsageLinks | CoProduceUsageLink |  | No |
| CoProduceUsages | Part |  | No |
| Context | Container |  | No |
| PPlan_LinkNav | ObjectReferenceable |  | No |
| ResultedByObjects | ChangeItem |  | Yes |
| Versions | Coproduce |  | No |
| Organization | Organization |  | No |
| ExtendedData | ExtendedData |  | No |
| Effectivities | Effectivity |  | Yes |
| Creator | User |  | No |
| Revisions | Coproduce |  | No |
| Folder | Folder |  | No |
| Modifier | User |  | No |

## DiscrepancyContext

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| SourceRoot | Part |  | No |
| TargetRoot | Part |  | No |
| TargetPart | Part |  | No |
| UpstreamNavigationCriteria | NavigationCriteria |  | No |
| DownstreamNavigationCriteria | NavigationCriteria |  | No |
