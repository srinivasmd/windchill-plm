# ProdMgmt Actions

This document describes OData actions available in this domain.

## Unbound Actions

These actions can be called directly on the entity set.

| Action | Parameters | Return Type |
|--------|------------|-------------|
| GetExtendedDatasForPartsWithInlineNavCriteria | parts, NavigationCriteria | ExtendedDataListItem) |
| GetExtendedDatasForParts | parts, navigationCriteriaId | ExtendedDataListItem) |
| GetExtendedDatas | ExtendedDatas | ExtendedData) |
| GetDepartmentDatasForPartsWithInlineNavCriteria | parts, NavigationCriteria, departmentDataTypes, supplyChains, locations, categories, views | DepartmentDataListItem) |
| GetDepartmentDatasForParts | parts, navigationCriteriaId | DepartmentDataListItem) |
| GetDepartmentDatasFromPlantWithInlineNavCriteria | plants, NavigationCriteria, departmentDataTypes, supplyChains, locations, categories | DepartmentDataForPlantListItem) |
| GetDepartmentDatas | DepartmentDatas | DepartmentData) |
| GetDepartmentDatasFromPlant | plants, navigationCriteriaId | DepartmentDataForPlantListItem) |
| GetEquivalenceNetworkForParts | parts | EquivalenceNetworkListItem) |
| AssignPlant | parts, plants, changeOid | ExtendedDataListItem) |
| CreateDepartmentData | parts, departmentData, NavigationCriteria, changeOid, view | DepartmentDataListItem) |
| CreateDepartmentDataForPlantData | plantData, departmentData, changeOid | DepartmentDataForPlantListItem) |
| GetRawMaterialsForParts | parts, navigationCriteriaId | RawMaterialListItem) |
| GetRawMaterialsForPartsWithInlineNavCriteria | parts, NavigationCriteria | RawMaterialListItem) |
| RemovePlantDataAssociations | PartPlantDataAssociations | - |
| RemoveDepartmentDataAssociations | PlantDataDepartmentDataAssociations, ChangeOid | - |
| UpdateCommonPropertiesForDepartmentDatas | DepartmentData | DepartmentData) |
| UpdateCommonPropertiesForExtendedDatas | ExtendedData | ExtendedData) |
| GetMadeFromSetForParts | Parts, navigationCriteriaId | MadeFromSetListItem) |
| GetMadeFromSetForPartsWithInlineNavCriteria | Parts, NavigationCriteria | MadeFromSetListItem) |
| CreateCoproduce | Coproduces, navigationCriteriaId | Coproduce) |
| CreateCoproduceWithInlineNavCriteria | Coproduces, NavigationCriteria | Coproduce) |
| GetMadeFromSetData | MadeFromSets, navigationCriteriaId | MadeFromSet) |
| GetMadeFromSetDataWithInlineNavCriteria | MadeFromSets, NavigationCriteria | MadeFromSet) |
| CreateMadeFromSets | MadeFromSets, ChangeOid | MadeFromSet) |
| AddCoproduceMembers | CoproduceSecondaryMembersAssociations, navigationCriteriaId, ChangeOid | Coproduce) |
| AddCoproduceMembersWithInlineNavCriteria | CoproduceSecondaryMembersAssociations, NavigationCriteria, ChangeOid | Coproduce) |
| AddScrapMembers | CoproduceSecondaryMembersAssociations, ChangeOid | Coproduce) |
| RemoveCoproduceMembers | CoproduceSecondaryMembersAssociations, navigationCriteriaId, ChangeOid | - |
| RemoveCoproduceMembersWithInlineNavCriteria | CoproduceSecondaryMembersAssociations, NavigationCriteria, ChangeOid | - |
| AddCoproduceUsages | CoproduceUsageMembersAssociations, ChangeOid | Coproduce) |
| RemoveCoproduceUsages | CoproduceUsageMembersAssociations, ChangeOid | - |
| InsertMadeFrom | MadeFromAssociations, ChangeOid | MadeFromAssociation) |
| UpdateCoproduceStructure | Coproduces, navigationCriteriaId | Coproduce) |
| UpdateCoproduceStructureWithInlineNavCriteria | Coproduces, NavigationCriteria | Coproduce) |
| GetCoproduceData | Coproduces, navigationCriteriaId | Coproduce) |
| GetCoproduceDataWithInlineNavCriteria | Coproduces, NavigationCriteria | Coproduce) |
| GetCoproduceForParts | Parts, navigationCriteriaId | CoproduceListItem) |
| GetCoproduceForPartsWithInlineNavCriteria | Parts, NavigationCriteria | CoproduceListItem) |
| RemoveMadeFromAssociations | MadeFromAssociations, ChangeOid | - |
| RemoveMadeFromSetAssociations | MadeFromSetAssociations, ChangeOid | - |
| ReplaceMadeFroms | ReplaceMadeFromAssociations, ChangeOid | ReplaceMadeFromAssociation) |
| RemovePrimaryCoproduceAssociations | PrimaryCoproduceAssociations, ChangeOid | - |
| GetExistingDownstreamObjects | DownstreamBranchAttributes, ExistingDownstreamObjectQueryParams, TransformationActionType, DownstreamPathId, DownstreamRoot, UpstreamRoot, UpstreamNavigationCriteria, DownstreamNavigationCriteria | ExistingDownstreamObjectsListItem) |
| SubcontractToPlants | DiscrepancyContext, Views, ChangeOid | EquivalentUsageAssociation) |
| Assemble | DiscrepancyContext, NewObjectIdentifications, NewAlternates, CheckInDownstreamObject, ChangeOid | EquivalentUsageAssociation) |
| UpdateToCurrentUpstreamEquivalents | DownstreamParts, UpstreamNavigationCriteria, DownstreamNavigationCriteria, DoCopyOver, ChangeOid | ExistingDownstreamAssociation) |
| SplitAssemble | DiscrepancyContext, NewObjectIdentifications, NewSplitAlternates, ReplaceAllUsage, CheckInDownstreamObject, ChangeOid | EquivalentUsageAssociation) |
| CreateEquivalenceUsageLinks | EquivalenceUsageAssociation, UpstreamNavigationCriteria, DownstreamNavigationCriteria | EquivalenceUsageAssociation) |
| PasteAsNewBranch | TargetPath, SourceRoot, TargetRoot, TransformationDefinitions, UpstreamNavigationCriteria, DownstreamNavigationCriteria, ChangeOid | ExistingDownstreamAssociation) |
| PasteAsNewPart | TargetPath, SourceRoot, TargetRoot, TransformationDefinitions, UpstreamNavigationCriteria, DownstreamNavigationCriteria, ChangeOid | ExistingDownstreamAssociation) |
| DetectAndResolveDiscrepancies | DiscrepancyContext, CheckInDownstreamObject, ChangeOid | DiscrepancyItem) |
| DetectDiscrepancies | DiscrepancyContext | DiscrepancyItem) |
| NewDownstreamBranch | UpstreamNavigationCriteria, DownstreamNavigationCriteria, TransformationDefinitions, ChangeOid | ExistingDownstreamAssociation) |
| ResolveDiscrepancies | DiscrepancyItems, DiscrepancyContext, CheckInDownstreamObject, ChangeOid | DiscrepancyItem) |
| NewDownstreamPart | UpstreamNavigationCriteria, DownstreamNavigationCriteria, TransformationDefinitions, ChangeOid | ExistingDownstreamAssociation) |
| NewDownstreamAlternate | UpstreamNavigationCriteria, DownstreamNavigationCriteria, TransformationDefinitions, ChangeOid | ExistingDownstreamAssociation) |
| PasteAsIs | TargetPath, SourceRoot, TargetRoot, TransformationDefinitions, UpstreamNavigationCriteria, DownstreamNavigationCriteria | ExistingDownstreamAssociation) |
| CreateEquivalenceLinks | EquivalenceLinkAssociations, UpstreamNavigationCriteria, DownstreamNavigationCriteria, ChangeOid | EquivalenceLinkAssociation) |
| RemoveEquivalenceLinks | EquivalenceLinkAssociations, ChangeOid | - |
| GenerateDownstreamStructure | DiscrepancyContext, ChangeOid | EquivalentUsageAssociation) |
| GenerateDownstreamStructureFromTemplate | GDSFromTemplateContext, ChangeOid | EquivalentUsageAssociation) |
| PasteSpecial | DiscrepancyContext, ChangeOid | EquivalentUsageAssociation) |
| SetStateDepartmentDatas | DepartmentDatas, State | DepartmentData) |
| ReviseDepartmentDatas | DepartmentDatas | DepartmentData) |
| CheckOutDepartmentDatas | Workables, CheckOutNote | DepartmentData) |
| CheckInDepartmentDatas | Workables, CheckInNote | DepartmentData) |
| UndoCheckOutDepartmentDatas | Workables | DepartmentData) |
| UpdateDepartmentDatas | DepartmentDatas | DepartmentData) |
| SetStateCoproduces | Coproduces, State | Coproduce) |
| ReviseCoproduces | Coproduces | Coproduce) |
| CheckOutCoproduces | Workables, CheckOutNote | Coproduce) |
| CheckInCoproduces | Workables, CheckInNote | Coproduce) |
| UndoCheckOutCoproduces | Workables | Coproduce) |
| EditCoproducesSecurityLabels | Coproduces | Coproduce) |
| DeleteCoproduces | Coproduces | - |
| UpdateCoproduces | Coproduces | Coproduce) |
| SetStateMadeFromSets | MadeFromSets, State | MadeFromSet) |
| ReviseMadeFromSets | MadeFromSets | MadeFromSet) |
| CheckOutMadeFromSets | Workables, CheckOutNote | MadeFromSet) |
| CheckInMadeFromSets | Workables, CheckInNote | MadeFromSet) |
| UndoCheckOutMadeFromSets | Workables | MadeFromSet) |
| EditMadeFromSetsSecurityLabels | MadeFromSets | MadeFromSet) |
| DeleteMadeFromSets | MadeFromSets | - |
| UpdateMadeFromSets | MadeFromSets | MadeFromSet) |
| SetStateExtendedDatas | ExtendedDatas, State | ExtendedData) |
| ReviseExtendedDatas | ExtendedDatas | ExtendedData) |
| CheckOutExtendedDatas | Workables, CheckOutNote | ExtendedData) |
| CheckInExtendedDatas | Workables, CheckInNote | ExtendedData) |
| UndoCheckOutExtendedDatas | Workables | ExtendedData) |
| UpdateExtendedDatas | ExtendedDatas | ExtendedData) |

## Bound Actions

These actions are bound to specific entity types.

| Action | Bound To | Parameters | Return Type |
|--------|----------|------------|-------------|
| GetManufacturingBOM | XBOMPart | NavigationCriteria, RelatedItems | TreeStructureItem |
| SetState | DepartmentData | State | DepartmentData |
| RemoveEffectivities | DepartmentData | Effectivities | - |
| ModifyEffectivities | DepartmentData | Effectivities | Effectivity) |
| Revise | DepartmentData | VersionId | DepartmentData |
| CheckIn | DepartmentData | CheckInNote, CheckOutNote, KeepCheckedOut | DepartmentData |
| CheckOut | DepartmentData | CheckOutNote | DepartmentData |
| UndoCheckOut | DepartmentData | - | DepartmentData |
| SetState | Coproduce | State | Coproduce |
| RemoveEffectivities | Coproduce | Effectivities | - |
| ModifyEffectivities | Coproduce | Effectivities | Effectivity) |
| Revise | Coproduce | VersionId | Coproduce |
| CheckIn | Coproduce | CheckInNote, CheckOutNote, KeepCheckedOut | Coproduce |
| CheckOut | Coproduce | CheckOutNote | Coproduce |
| UndoCheckOut | Coproduce | - | Coproduce |
| UpdateSecondaryCoproduceLinks | Coproduce | SecondaryCoproduceLinks, NavigationCriteria | SecondaryCoproduceLink) |
| GetExtendedDatasWithInlineNavCriteria | Part | NavigationCriteria | ExtendedData) |
| UpdateCoProduceUsageLinks | Coproduce | CoProduceUsageLinks | CoProduceUsageLink) |
| RemoveEffectivities | MadeFromSet | Effectivities | - |
| ModifyEffectivities | MadeFromSet | Effectivities | Effectivity) |
| SetState | MadeFromSet | State | MadeFromSet |
| Revise | MadeFromSet | VersionId | MadeFromSet |
| CheckIn | MadeFromSet | CheckInNote, CheckOutNote, KeepCheckedOut | MadeFromSet |
| CheckOut | MadeFromSet | CheckOutNote | MadeFromSet |
| UndoCheckOut | MadeFromSet | - | MadeFromSet |
| UpdateRawMaterialLinks | MadeFromSet | RawMaterialLinks, ChangeOid | RawMaterialLink) |
| GetExtendedDatasWithInlineNavCriteria | Part | NavigationCriteria | ExtendedData) |
| SetState | ExtendedData | State | ExtendedData |
| RemoveEffectivities | ExtendedData | Effectivities | - |
| ModifyEffectivities | ExtendedData | Effectivities | Effectivity) |
| Revise | ExtendedData | VersionId | ExtendedData |
| CheckIn | ExtendedData | CheckInNote, CheckOutNote, KeepCheckedOut | ExtendedData |
| CheckOut | ExtendedData | CheckOutNote | ExtendedData |
| UndoCheckOut | ExtendedData | - | ExtendedData |
