# MfgProcMgmt Actions

This document describes OData actions available in this domain.

## Unbound Actions

These actions can be called directly on the entity set.

| Action | Parameters | Return Type |
|--------|------------|-------------|
| CreateStandardCCUsageToResourceLink | OperationToStandardCCLinkId, StandardCCUsageToResourceLink | StandardCCUsageToResourceLink) |
| DeleteMPMStdCCUsageToProcessPlanLinks | RoleAObject, LinksOIDs | String) |
| ChangeOperationIdentity | identities | Operation) |
| ChangeProcessPlanIdentity | identities | ProcessPlan) |
| ChangeSequenceIdentity | identities | Sequence) |
| ChangeSkillIdentity | identities | Skill) |
| ChangeToolingIdentity | identities | Tooling) |
| ChangeProcessMaterialIdentity | identities | ProcessMaterial) |
| UpdateMPMStdCCUsageToProcessPlanLink | StandardCCUsageToProcessPlanLink | StandardCCUsageToProcessPlanLink) |
| DeleteAssociativeToSCCLinks | RoleAObject, LinksOIDs, ChangeOID | String) |
| CreateMPMStdCCUsageToProcessPlanLink | OperationToStandardCCLinkId, StandardCCUsageToProcessPlanLink | StandardCCUsageToProcessPlanLink) |
| UpdateMPMStdCCUsageToResourceLinks | StandardCCUsageToResourceLinks | StandardCCUsageToResourceLink) |
| DeleteMPMStdCCUsageToResourceLinks | RoleAObject, LinksOIDs, ChangeOID | String |
| CreateMPMStandardCCUsageToDDLinks | OperationToStandardCCLinkId, StandardCCUsageToDocumentDescribeLinks | StandardCCUsageToDDLink) |
| DeleteMPMStandardCCUsageToDDLinks | RoleAObject, LinksOIDs, ChangeOID | String |
| UpdateAssociativeToSCCLinks | associativeOID, associativeToStandardCCLinks | AssociativeToStandardCCLink) |
| GetUnallocatedSCCs | Operation, ProcessPlan, RelatedAssemblyNavigationCriteria, ProcessPlanNavigationCriteria | AssociativeToStandardCCLink) |
| CreateResourcesAssociations | PartDocAssociations | PartDocAssociation) |
| DeleteResourcesAssociations | RoleAObject, LinksOIDs, ChangeOID | String |
| CreateAssociativeToSCCLinks | associativeOID, associativeToStandardCCLinks | AssociativeToStandardCCLink) |
| CreatePartTags | taggableOID, taggerOIDs, relatedProcessPlanOID | PartTagLink) |
| DeletePartTags | taggableOID, taggerOIDs | String |
| DeleteMPMCompatibilityLinks | RoleAObject, LinksOIDs, ChangeOID | String |
| CreateWCRoutingPlans | routingPlanItemList | RoutingPlan) |
| GetRoutingPlansForRoutables | Routables | RoutableToRoutingPlanListItem) |
| GenerateProcessPlans | GeneratedProcessPlanItem | ProcessPlan) |
| SynchronizeGeneratedProcessPlans | GeneratedProcessPlans, autoCheckIn | ProcessPlanSynchronizationReport) |
| SetStateStandardDataCollectionOperations | StandardDataCollectionOperations, State | StandardDataCollectionOperation) |
| ReviseStandardDataCollectionOperations | StandardDataCollectionOperations | StandardDataCollectionOperation) |
| DeleteStandardDataCollectionOperations | StandardDataCollectionOperations | - |
| CreateStandardDataCollectionOperations | StandardDataCollectionOperations | StandardDataCollectionOperation) |
| UpdateStandardDataCollectionOperations | StandardDataCollectionOperations | StandardDataCollectionOperation) |
| SetStatePlants | Plants, State | Plant) |
| RevisePlants | Plants | Plant) |
| CheckOutPlants | Workables, CheckOutNote | Plant) |
| CheckInPlants | Workables, CheckInNote | Plant) |
| UndoCheckOutPlants | Workables | Plant) |
| ReviseMaterials | Materials | Material) |
| SetStateMaterials | Materials, State | Material) |
| CheckOutMaterials | Workables, CheckOutNote | Material) |
| CheckInMaterials | Workables, CheckInNote | Material) |
| UndoCheckOutMaterials | Workables | Material) |
| ReviseOperations | Operations | Operation) |
| SetStateOperations | Operations, State | Operation) |
| CheckOutOperations | Workables, CheckOutNote | Operation) |
| CheckInOperations | Workables, CheckInNote | Operation) |
| UndoCheckOutOperations | Workables | Operation) |
| EditOperationsSecurityLabels | Operations | Operation) |
| DeleteOperations | Operations | - |
| CreateOperations | Operations | Operation) |
| UpdateOperations | Operations | Operation) |
| ReviseStandardCCs | StandardCCs | StandardCC) |
| SetStateStandardCCs | StandardCCs, State | StandardCC) |
| CheckOutStandardCCs | Workables, CheckOutNote | StandardCC) |
| CheckInStandardCCs | Workables, CheckInNote | StandardCC) |
| UndoCheckOutStandardCCs | Workables | StandardCC) |
| EditStandardCCsSecurityLabels | StandardCCs | StandardCC) |
| DeleteStandardCCs | StandardCCs | - |
| CreateStandardCCs | StandardCCs | StandardCC) |
| UpdateStandardCCs | StandardCCs | StandardCC) |
| ReviseSkills | Skills | Skill) |
| SetStateSkills | Skills, State | Skill) |
| CheckOutSkills | Workables, CheckOutNote | Skill) |
| CheckInSkills | Workables, CheckInNote | Skill) |
| UndoCheckOutSkills | Workables | Skill) |
| EditSkillsSecurityLabels | Skills | Skill) |
| DeleteSkills | Skills | - |
| CreateSkills | Skills | Skill) |
| UpdateSkills | Skills | Skill) |
| ReviseProcessMaterials | ProcessMaterials | ProcessMaterial) |
| SetStateProcessMaterials | ProcessMaterials, State | ProcessMaterial) |
| CheckOutProcessMaterials | Workables, CheckOutNote | ProcessMaterial) |
| CheckInProcessMaterials | Workables, CheckInNote | ProcessMaterial) |
| UndoCheckOutProcessMaterials | Workables | ProcessMaterial) |
| EditProcessMaterialsSecurityLabels | ProcessMaterials | ProcessMaterial) |
| DeleteProcessMaterials | ProcessMaterials | - |
| CreateProcessMaterials | ProcessMaterials | ProcessMaterial) |
| UpdateProcessMaterials | ProcessMaterials | ProcessMaterial) |
| SetStateSequences | Sequences, State | Sequence) |
| ReviseSequences | Sequences | Sequence) |
| CheckOutSequences | Workables, CheckOutNote | Sequence) |
| CheckInSequences | Workables, CheckInNote | Sequence) |
| UndoCheckOutSequences | Workables | Sequence) |
| EditSequencesSecurityLabels | Sequences | Sequence) |
| CreateSequences | Sequences | Sequence) |
| UpdateSequences | Sequences | Sequence) |
| ReviseProcessPlans | ProcessPlans | ProcessPlan) |
| SetStateProcessPlans | ProcessPlans, State | ProcessPlan) |
| CheckOutProcessPlans | Workables, CheckOutNote | ProcessPlan) |
| CheckInProcessPlans | Workables, CheckInNote | ProcessPlan) |
| UndoCheckOutProcessPlans | Workables | ProcessPlan) |
| EditProcessPlansSecurityLabels | ProcessPlans | ProcessPlan) |
| DeleteProcessPlans | ProcessPlans | - |
| CreateProcessPlans | ProcessPlans | ProcessPlan) |
| UpdateProcessPlans | ProcessPlans | ProcessPlan) |
| ReviseStandardProcedures | StandardProcedures | StandardProcedure) |
| SetStateStandardProcedures | StandardProcedures, State | StandardProcedure) |
| SetStateRoutingPlans | RoutingPlans, State | RoutingPlan) |
| ReviseRoutingPlans | RoutingPlans | RoutingPlan) |
| CheckOutRoutingPlans | Workables, CheckOutNote | RoutingPlan) |
| CheckInRoutingPlans | Workables, CheckInNote | RoutingPlan) |
| UndoCheckOutRoutingPlans | Workables | RoutingPlan) |
| DeleteRoutingPlans | RoutingPlans | - |
| ReviseStandardBuyOffOperations | StandardBuyOffOperations | StandardBuyOffOperation) |
| SetStateStandardBuyOffOperations | StandardBuyOffOperations, State | StandardBuyOffOperation) |
| DeleteStandardBuyOffOperations | StandardBuyOffOperations | - |
| CreateStandardBuyOffOperations | StandardBuyOffOperations | StandardBuyOffOperation) |
| UpdateStandardBuyOffOperations | StandardBuyOffOperations | StandardBuyOffOperation) |
| ReviseWorkCenters | WorkCenters | WorkCenter) |
| SetStateWorkCenters | WorkCenters, State | WorkCenter) |
| CheckOutWorkCenters | Workables, CheckOutNote | WorkCenter) |
| CheckInWorkCenters | Workables, CheckInNote | WorkCenter) |
| UndoCheckOutWorkCenters | Workables | WorkCenter) |
| EditWorkCentersSecurityLabels | WorkCenters | WorkCenter) |
| DeleteWorkCenters | WorkCenters | - |
| CreateWorkCenters | WorkCenters | WorkCenter) |
| UpdateWorkCenters | WorkCenters | WorkCenter) |
| ReviseToolings | Toolings | Tooling) |
| SetStateToolings | Toolings, State | Tooling) |
| CheckOutToolings | Workables, CheckOutNote | Tooling) |
| CheckInToolings | Workables, CheckInNote | Tooling) |
| UndoCheckOutToolings | Workables | Tooling) |
| EditToolingsSecurityLabels | Toolings | Tooling) |
| DeleteToolings | Toolings | - |
| CreateToolings | Toolings | Tooling) |
| UpdateToolings | Toolings | Tooling) |

## Bound Actions

These actions are bound to specific entity types.

| Action | Bound To | Parameters | Return Type |
|--------|----------|------------|-------------|
| CreateMPMDocumentDescribeLinks | OperationHolder | DocumentDescribeLink | DocumentDescribeLink) |
| GetDocumentsWithInlineNavCriteria | OperationHolder | navigationCriteria | DocumentedObject |
| UpdateMPMStandardProcedureLinks | OperationHolder | StandardProcedureLink | StandardProcedureLink) |
| DeleteMPMDocumentDescribeLink | OperationHolder | LinksOIDs, ChangeOID | String |
| CreateMPMDocumentReferenceLinks | OperationHolder | DocumentReferenceLink | DocumentReferenceLink) |
| CreateMPMStandardProcedureLinks | OperationHolder | StandardProcedureLink | StandardProcedureLink) |
| CreateOperationInContextFromTemplate | OperationHolder | OperationOID, NavigationCriteriaOID | Operation) |
| AssociateStandardOperations | OperationHolder | OperationUsageLink | OperationUsageLink) |
| UpdateMPMOperationUsageLinks | OperationHolder | OperationUsageLink | OperationUsageLink) |
| CreateOperationsInContext | OperationHolder | Operations | Operation) |
| GetDocuments | OperationHolder | navigationCriteriaId | DocumentedObject |
| CreateOperationToStandardCCLink | StandardDataCollectionOperation | OperationToStandardCCLink | OperationToStandardCCLink) |
| AssociateWorkCenter | StandardDataCollectionOperation | OperationToWorkCenterLink, doCopyOverDefaultCostAndTime | OperationToWorkCenterLink |
| GetDocuments | StandardDataCollectionOperation | navigationCriteriaId | DocumentedObject |
| CreateMPMOperationToPartLinks | StandardDataCollectionOperation | consumablePaths, operationPath, processPlanId, relatedAssemblyId, processPlanNavigationCriteriaId, relatedAssemblyNavigationCriteriaId | OperationToPartLink) |
| UpdateConsumableLinks | StandardDataCollectionOperation | OperationToConsumableLink | OperationToConsumableLink) |
| DeleteOperationToConsumableLink | StandardDataCollectionOperation | LinksOIDs, ChangeOID | String |
| CreateOperationToOperatedPartLink | StandardDataCollectionOperation | Part | OperationToOperatedPartLink) |
| UpdateOperationToStandardCCLink | StandardDataCollectionOperation | OperationToStandardCCLink | OperationToStandardCCLink) |
| CreateOperationsInContext | StandardDataCollectionOperation | Operations | Operation) |
| InsertNewOperations | StandardDataCollectionOperation | Operations | Operation) |
| CreateMPMDocumentReferenceLinks | StandardDataCollectionOperation | DocumentReferenceLink | DocumentReferenceLink) |
| CreateMPMStandardProcedureLinks | StandardDataCollectionOperation | StandardProcedureLink | StandardProcedureLink) |
| AssignCCFromProduct | StandardDataCollectionOperation | AssociativeToSCCLinkOIDs | OperationToStandardCCLink) |
| GetDocumentsWithInlineNavCriteria | StandardDataCollectionOperation | navigationCriteria | DocumentedObject |
| AssociateConsumableResources | StandardDataCollectionOperation | OperationToConsumableLink | OperationToConsumableLink) |
| CreateOperationInContextFromTemplate | StandardDataCollectionOperation | OperationOID, NavigationCriteriaOID | Operation) |
| AssociateStandardOperations | StandardDataCollectionOperation | OperationUsageLink | OperationUsageLink) |
| DeleteMPMOperationToStandardCCLinks | StandardDataCollectionOperation | LinksOIDs, ChangeOID | String |
| DeleteMPMOperationToPartLinks | StandardDataCollectionOperation | LinksOIDs, ChangeOID | String |
| UpdateOperationToPartLink | StandardDataCollectionOperation | OperationToPartLink | OperationToPartLink) |
| GetConsumed | StandardDataCollectionOperation | processPlanNavigationCriteriaId, relatedAssemblyNavigationCriteriaId, operationPath | ConsumingOperation |
| GetConsumedWithInlineNavCriteria | StandardDataCollectionOperation | processPlanNavigationCriteria, relatedAssemblyNavigationCriteria, operationPath | ConsumingOperation |
| DeleteMPMDocumentDescribeLink | StandardDataCollectionOperation | LinksOIDs, ChangeOID | String |
| GetBOPWithInlineNavCriteria | StandardDataCollectionOperation | processPlanNavigationCriteria, relatedAssemblyNavigationCriteria, operationPath | BOP |
| UpdateMPMOperationUsageLinks | StandardDataCollectionOperation | OperationUsageLink | OperationUsageLink) |
| CreateMPMDocumentDescribeLinks | StandardDataCollectionOperation | DocumentDescribeLink | DocumentDescribeLink) |
| UpdateOperationToOperatedPartLink | StandardDataCollectionOperation | OperationToOperatedPartLink | OperationToOperatedPartLink) |
| UpdateMPMStandardProcedureLinks | StandardDataCollectionOperation | StandardProcedureLink | StandardProcedureLink) |
| CreateMPMOperationToPartLinksWithInLineNavCriteria | StandardDataCollectionOperation | consumablePaths, operationPath, ProcessPlan, Material, processPlanNavigationCriteria, relatedAssemblyNavigationCriteria | OperationToPartLink) |
| DeleteOperationToOperatedPartLinks | StandardDataCollectionOperation | LinksOIDs, ChangeOID | String) |
| GetBOP | StandardDataCollectionOperation | processPlanNavigationCriteriaId, relatedAssemblyNavigationCriteriaId, operationPath | BOP |
| ModifyEffectivities | StandardDataCollectionOperation | Effectivities | Effectivity) |
| RemoveEffectivities | StandardDataCollectionOperation | Effectivities | - |
| SetState | StandardDataCollectionOperation | State | StandardDataCollectionOperation |
| Revise | StandardDataCollectionOperation | VersionId | StandardDataCollectionOperation |
| CheckIn | StandardDataCollectionOperation | CheckInNote, CheckOutNote, KeepCheckedOut | StandardDataCollectionOperation |
| CheckOut | StandardDataCollectionOperation | CheckOutNote | StandardDataCollectionOperation |
| UndoCheckOut | StandardDataCollectionOperation | - | StandardDataCollectionOperation |
| CreateResourceDescribeDocumentLinks | Plant | ResourceDescribeLink | ResourceDescribeLink) |
| CreateMPMCompatibilityLinks | Plant | MPMCompatibilityLinks | MPMCompatibilityLink) |
| CreateResourceReferenceDocumentLinks | Plant | ResourceReferenceLink | ResourceReferenceLink) |
| GetPartStructure | Plant | NavigationCriteria | PartStructureItem |
| DeleteResourceReferenceLinks | Plant | LinksOIDs, ChangeOID | String) |
| CreateUses | Plant | ChangeOID, ResourceUses | PartUse) |
| DeleteResourceDescribeLinks | Plant | LinksOIDs, ChangeOID | String) |
| SetState | Plant | State | Plant |
| Revise | Plant | VersionId | Plant |
| RemoveEffectivities | Plant | Effectivities | - |
| ModifyEffectivities | Plant | Effectivities | Effectivity) |
| CheckIn | Plant | CheckInNote, CheckOutNote, KeepCheckedOut | Plant |
| CheckOut | Plant | CheckOutNote | Plant |
| UndoCheckOut | Plant | - | Plant |
| DeleteMPMPartToProcessPlanLinks | Material | LinksOIDs, ChangeOID | String |
| UpdateMPMPartToProcessPlanLinks | Material | PartToProcessPlanLink | PartToProcessPlanLink) |
| CreateMPMPartToProcessPlanLinks | Material | PartToProcessPlanLink | PartToProcessPlanLink) |
| Revise | Material | VersionId | Material |
| SetState | Material | State | Material |
| CheckIn | Material | CheckInNote, CheckOutNote, KeepCheckedOut | Material |
| CheckOut | Material | CheckOutNote | Material |
| UndoCheckOut | Material | - | Material |
| UpdateOperationToStandardCCLink | Operation | OperationToStandardCCLink | OperationToStandardCCLink) |
| DeleteMPMOperationToStandardCCLinks | Operation | LinksOIDs, ChangeOID | String |
| AssociateWorkCenter | Operation | OperationToWorkCenterLink, doCopyOverDefaultCostAndTime | OperationToWorkCenterLink |
| CreateOperationToOperatedPartLink | Operation | Part | OperationToOperatedPartLink) |
| UpdateOperationToOperatedPartLink | Operation | OperationToOperatedPartLink | OperationToOperatedPartLink) |
| UpdateConsumableLinks | Operation | OperationToConsumableLink | OperationToConsumableLink) |
| DeleteOperationToOperatedPartLinks | Operation | LinksOIDs, ChangeOID | String) |
| CreateOperationInContextFromTemplate | Operation | OperationOID, NavigationCriteriaOID | Operation) |
| GetDocuments | Operation | navigationCriteriaId | DocumentedObject |
| UpdateMPMOperationUsageLinks | Operation | OperationUsageLink | OperationUsageLink) |
| GetConsumed | Operation | processPlanNavigationCriteriaId, relatedAssemblyNavigationCriteriaId, operationPath | ConsumingOperation |
| AssociateStandardOperations | Operation | OperationUsageLink | OperationUsageLink) |
| GetConsumedWithInlineNavCriteria | Operation | processPlanNavigationCriteria, relatedAssemblyNavigationCriteria, operationPath | ConsumingOperation |
| GetBOPWithInlineNavCriteria | Operation | processPlanNavigationCriteria, relatedAssemblyNavigationCriteria, operationPath | BOP |
| UpdateOperationToPartLink | Operation | OperationToPartLink | OperationToPartLink) |
| InsertNewOperations | Operation | Operations | Operation) |
| CreateMPMDocumentDescribeLinks | Operation | DocumentDescribeLink | DocumentDescribeLink) |
| GetBOP | Operation | processPlanNavigationCriteriaId, relatedAssemblyNavigationCriteriaId, operationPath | BOP |
| CreateOperationToStandardCCLink | Operation | OperationToStandardCCLink | OperationToStandardCCLink) |
| DeleteMPMDocumentDescribeLink | Operation | LinksOIDs, ChangeOID | String |
| CreateMPMOperationToPartLinks | Operation | consumablePaths, operationPath, processPlanId, relatedAssemblyId, processPlanNavigationCriteriaId, relatedAssemblyNavigationCriteriaId | OperationToPartLink) |
| CreateOperationsInContext | Operation | Operations | Operation) |
| AssociateConsumableResources | Operation | OperationToConsumableLink | OperationToConsumableLink) |
| DeleteMPMOperationToPartLinks | Operation | LinksOIDs, ChangeOID | String |
| UpdateMPMStandardProcedureLinks | Operation | StandardProcedureLink | StandardProcedureLink) |
| DeleteOperationToConsumableLink | Operation | LinksOIDs, ChangeOID | String |
| CreateMPMStandardProcedureLinks | Operation | StandardProcedureLink | StandardProcedureLink) |
| CreateMPMDocumentReferenceLinks | Operation | DocumentReferenceLink | DocumentReferenceLink) |
| CreateMPMOperationToPartLinksWithInLineNavCriteria | Operation | consumablePaths, operationPath, ProcessPlan, Material, processPlanNavigationCriteria, relatedAssemblyNavigationCriteria | OperationToPartLink) |
| AssignCCFromProduct | Operation | AssociativeToSCCLinkOIDs | OperationToStandardCCLink) |
| GetDocumentsWithInlineNavCriteria | Operation | navigationCriteria | DocumentedObject |
| Revise | Operation | VersionId | Operation |
| ModifyEffectivities | Operation | Effectivities | Effectivity) |
| RemoveEffectivities | Operation | Effectivities | - |
| SetState | Operation | State | Operation |
| CheckIn | Operation | CheckInNote, CheckOutNote, KeepCheckedOut | Operation |
| CheckOut | Operation | CheckOutNote | Operation |
| UndoCheckOut | Operation | - | Operation |
| DeleteMPMStandardCCToProcessPlanLinks | StandardCC | LinksOIDs | String |
| CreateMPMDocumentDescribeLinks | StandardCC | DocumentDescribeLink | DocumentDescribeLink) |
| CreateMPMStandardCCToProcessPlanLinks | StandardCC | StandardCCToProcessPlanLink | StandardCCToProcessPlanLink) |
| GetDocuments | StandardCC | navigationCriteriaId | DocumentedObject |
| GetDocumentsWithInlineNavCriteria | StandardCC | navigationCriteria | DocumentedObject |
| UpdateMPMStandardCCToProcessPlanLinks | StandardCC | StandardCCToProcessPlanLink | StandardCCToProcessPlanLink) |
| UpdateMPMStandardCCToResourceLinks | StandardCC | StandardCCToResourceLink | StandardCCToResourceLink) |
| DeleteMPMStandardCCToResourceLinks | StandardCC | LinksOIDs, ChangeOID | String) |
| DeleteMPMDocumentDescribeLink | StandardCC | LinksOIDs, ChangeOID | String |
| CreateMPMStandardCCToResourceLinks | StandardCC | StandardCCToResourceLink | StandardCCToResourceLink) |
| Revise | StandardCC | VersionId | StandardCC |
| SetState | StandardCC | State | StandardCC |
| CheckIn | StandardCC | CheckInNote, CheckOutNote, KeepCheckedOut | StandardCC |
| CheckOut | StandardCC | CheckOutNote | StandardCC |
| UndoCheckOut | StandardCC | - | StandardCC |
| Revise | Skill | VersionId | Skill |
| SetState | Skill | State | Skill |
| RemoveEffectivities | Skill | Effectivities | - |
| ModifyEffectivities | Skill | Effectivities | Effectivity) |
| CheckIn | Skill | CheckInNote, CheckOutNote, KeepCheckedOut | Skill |
| CheckOut | Skill | CheckOutNote | Skill |
| UndoCheckOut | Skill | - | Skill |
| Revise | ProcessMaterial | VersionId | ProcessMaterial |
| RemoveEffectivities | ProcessMaterial | Effectivities | - |
| ModifyEffectivities | ProcessMaterial | Effectivities | Effectivity) |
| SetState | ProcessMaterial | State | ProcessMaterial |
| CheckIn | ProcessMaterial | CheckInNote, CheckOutNote, KeepCheckedOut | ProcessMaterial |
| CheckOut | ProcessMaterial | CheckOutNote | ProcessMaterial |
| UndoCheckOut | ProcessMaterial | - | ProcessMaterial |
| CreateMPMStandardProcedureLinks | Sequence | StandardProcedureLink | StandardProcedureLink) |
| DeleteMPMOperationToStandardCCLinks | Sequence | LinksOIDs, ChangeOID | String |
| UpdateOperationToStandardCCLink | Sequence | OperationToStandardCCLink | OperationToStandardCCLink) |
| GetDocuments | Sequence | navigationCriteriaId | DocumentedObject |
| CreateMPMDocumentReferenceLinks | Sequence | DocumentReferenceLink | DocumentReferenceLink) |
| GetBOP | Sequence | processPlanNavigationCriteriaId, relatedAssemblyNavigationCriteriaId | BOP |
| GetDocumentsWithInlineNavCriteria | Sequence | navigationCriteria | DocumentedObject |
| CreateOperationsInContext | Sequence | Operations | Operation) |
| UpdateMPMOperationUsageLinks | Sequence | OperationUsageLink | OperationUsageLink) |
| AssociateStandardOperations | Sequence | OperationUsageLink | OperationUsageLink) |
| CreateMPMDocumentDescribeLinks | Sequence | DocumentDescribeLink | DocumentDescribeLink) |
| CreateOperationInContextFromTemplate | Sequence | OperationOID, NavigationCriteriaOID | Operation) |
| GetBOPWithInlineNavCriteria | Sequence | processPlanNavigationCriteria, relatedAssemblyNavigationCriteria | BOP |
| DeleteMPMDocumentDescribeLink | Sequence | LinksOIDs, ChangeOID | String |
| UpdateMPMStandardProcedureLinks | Sequence | StandardProcedureLink | StandardProcedureLink) |
| CreateMPMSequencesInSequenceContext | Sequence | SequencesToCreate | Sequence) |
| CreateOperationToStandardCCLink | Sequence | OperationToStandardCCLink | OperationToStandardCCLink) |
| SetState | Sequence | State | Sequence |
| RemoveEffectivities | Sequence | Effectivities | - |
| ModifyEffectivities | Sequence | Effectivities | Effectivity) |
| Revise | Sequence | VersionId | Sequence |
| CheckIn | Sequence | CheckInNote, CheckOutNote, KeepCheckedOut | Sequence |
| CheckOut | Sequence | CheckOutNote | Sequence |
| UndoCheckOut | Sequence | - | Sequence |
| CreateMPMEPMDocumentDescribeLinks | EPMDocumentManageable | MpmEpmDocumentDescribeLink | MpmEpmDocumentDescribeLink) |
| DeleteMPMEPMDocumentDescribeLinks | EPMDocumentManageable | LinksOIDs, ChangeOID | String |
| GetMPMEPMDocumentDescribes | EPMDocumentManageable | NavigationCriteria | DescribedByEPMItem) |
| GetBOP | ProcessPlan | processPlanNavigationCriteriaId, relatedAssemblyNavigationCriteriaId | BOP |
| UpdateOperationToStandardCCLink | ProcessPlan | OperationToStandardCCLink | OperationToStandardCCLink) |
| CreateMPMStandardProcedureLinks | ProcessPlan | StandardProcedureLink | StandardProcedureLink) |
| GetDocumentsWithInlineNavCriteria | ProcessPlan | navigationCriteria | DocumentedObject |
| UpdateMPMOperationUsageLinks | ProcessPlan | OperationUsageLink | OperationUsageLink) |
| CreateOperationsInContext | ProcessPlan | Operations | Operation) |
| BOPAllocateAssembly | ProcessPlan | NewAssembly, ProcessPlanNavigationCriteria, NewAssemblyNavigationCriteria | BOPReconciliationResult) |
| DeleteMPMOperationToStandardCCLinks | ProcessPlan | LinksOIDs, ChangeOID | String |
| CreateMPMDocumentDescribeLinks | ProcessPlan | DocumentDescribeLink | DocumentDescribeLink) |
| GetDocuments | ProcessPlan | navigationCriteriaId | DocumentedObject |
| DeleteMPMDocumentDescribeLink | ProcessPlan | LinksOIDs, ChangeOID | String |
| CreateMPMPartToProcessPlanLinks | ProcessPlan | PartToProcessPlanLink | PartToProcessPlanLink) |
| CreateOperationInContextFromTemplate | ProcessPlan | OperationOID, NavigationCriteriaOID | Operation) |
| AssociateStandardOperations | ProcessPlan | OperationUsageLink | OperationUsageLink) |
| UpdateMPMStandardProcedureLinks | ProcessPlan | StandardProcedureLink | StandardProcedureLink) |
| GetBOPWithInlineNavCriteria | ProcessPlan | processPlanNavigationCriteria, relatedAssemblyNavigationCriteria | BOP |
| CreateMPMSequencesInProcessPlanContext | ProcessPlan | SequencesToCreate | Sequence) |
| CreateMPMDocumentReferenceLinks | ProcessPlan | DocumentReferenceLink | DocumentReferenceLink) |
| CreateOperationToStandardCCLink | ProcessPlan | OperationToStandardCCLink | OperationToStandardCCLink) |
| Revise | ProcessPlan | VersionId | ProcessPlan |
| RemoveEffectivities | ProcessPlan | Effectivities | - |
| ModifyEffectivities | ProcessPlan | Effectivities | Effectivity) |
| SetState | ProcessPlan | State | ProcessPlan |
| CheckIn | ProcessPlan | CheckInNote, CheckOutNote, KeepCheckedOut | ProcessPlan |
| CheckOut | ProcessPlan | CheckOutNote | ProcessPlan |
| UndoCheckOut | ProcessPlan | - | ProcessPlan |
| UpdateOperationToStandardCCLink | StandardProcedure | OperationToStandardCCLink | OperationToStandardCCLink) |
| CreateMPMStandardProcedureLinks | StandardProcedure | StandardProcedureLink | StandardProcedureLink) |
| DeleteMPMDocumentDescribeLink | StandardProcedure | LinksOIDs, ChangeOID | String |
| CreateMPMSequencesInProcessPlanContext | StandardProcedure | SequencesToCreate | Sequence) |
| BOPAllocateAssembly | StandardProcedure | NewAssembly, ProcessPlanNavigationCriteria, NewAssemblyNavigationCriteria | BOPReconciliationResult) |
| GetBOP | StandardProcedure | processPlanNavigationCriteriaId, relatedAssemblyNavigationCriteriaId | BOP |
| CreateMPMPartToProcessPlanLinks | StandardProcedure | PartToProcessPlanLink | PartToProcessPlanLink) |
| CreateOperationToStandardCCLink | StandardProcedure | OperationToStandardCCLink | OperationToStandardCCLink) |
| GetBOPWithInlineNavCriteria | StandardProcedure | processPlanNavigationCriteria, relatedAssemblyNavigationCriteria | BOP |
| CreateOperationsInContext | StandardProcedure | Operations | Operation) |
| CreateOperationInContextFromTemplate | StandardProcedure | OperationOID, NavigationCriteriaOID | Operation) |
| DeleteMPMOperationToStandardCCLinks | StandardProcedure | LinksOIDs, ChangeOID | String |
| GetDocuments | StandardProcedure | navigationCriteriaId | DocumentedObject |
| UpdateMPMOperationUsageLinks | StandardProcedure | OperationUsageLink | OperationUsageLink) |
| UpdateMPMStandardProcedureLinks | StandardProcedure | StandardProcedureLink | StandardProcedureLink) |
| AssociateStandardOperations | StandardProcedure | OperationUsageLink | OperationUsageLink) |
| GetDocumentsWithInlineNavCriteria | StandardProcedure | navigationCriteria | DocumentedObject |
| CreateMPMDocumentDescribeLinks | StandardProcedure | DocumentDescribeLink | DocumentDescribeLink) |
| CreateMPMDocumentReferenceLinks | StandardProcedure | DocumentReferenceLink | DocumentReferenceLink) |
| Revise | StandardProcedure | VersionId | StandardProcedure |
| RemoveEffectivities | StandardProcedure | Effectivities | - |
| ModifyEffectivities | StandardProcedure | Effectivities | Effectivity) |
| SetState | StandardProcedure | State | StandardProcedure |
| CheckIn | StandardProcedure | CheckInNote, CheckOutNote, KeepCheckedOut | StandardProcedure |
| CheckOut | StandardProcedure | CheckOutNote | StandardProcedure |
| UndoCheckOut | StandardProcedure | - | StandardProcedure |
| CreateMPMDocumentDescribeLinks | SequenceHolder | DocumentDescribeLink | DocumentDescribeLink) |
| GetDocuments | SequenceHolder | navigationCriteriaId | DocumentedObject |
| UpdateSequenceUsageLink | SequenceHolder | SequenceUsageLink | SequenceUsageLink) |
| DeleteMPMDocumentDescribeLink | SequenceHolder | LinksOIDs, ChangeOID | String |
| GetDocumentsWithInlineNavCriteria | SequenceHolder | navigationCriteria | DocumentedObject |
| RelocalizeOperations | RoutingPlan | sourceResource, targetResource, operations | RoutingPlan |
| GetRoutingOperations | RoutingPlan | RoutableToNavigationCriteriaItem | RoutingOperation) |
| LocalizeOperations | RoutingPlan | routeHolder, operationUsageLink | RoutingPlanLocalizationReport |
| ModifyEffectivities | RoutingPlan | Effectivities | Effectivity) |
| RemoveEffectivities | RoutingPlan | Effectivities | - |
| SetState | RoutingPlan | State | RoutingPlan |
| Revise | RoutingPlan | VersionId | RoutingPlan |
| CheckIn | RoutingPlan | CheckInNote, CheckOutNote, KeepCheckedOut | RoutingPlan |
| CheckOut | RoutingPlan | CheckOutNote | RoutingPlan |
| UndoCheckOut | RoutingPlan | - | RoutingPlan |
| CreateMPMOperationToPartLinks | StandardBuyOffOperation | consumablePaths, operationPath, processPlanId, relatedAssemblyId, processPlanNavigationCriteriaId, relatedAssemblyNavigationCriteriaId | OperationToPartLink) |
| AssociateConsumableResources | StandardBuyOffOperation | OperationToConsumableLink | OperationToConsumableLink) |
| CreateOperationsInContext | StandardBuyOffOperation | Operations | Operation) |
| CreateOperationToOperatedPartLink | StandardBuyOffOperation | Part | OperationToOperatedPartLink) |
| UpdateOperationToPartLink | StandardBuyOffOperation | OperationToPartLink | OperationToPartLink) |
| AssociateStandardOperations | StandardBuyOffOperation | OperationUsageLink | OperationUsageLink) |
| AssociateWorkCenter | StandardBuyOffOperation | OperationToWorkCenterLink, doCopyOverDefaultCostAndTime | OperationToWorkCenterLink |
| GetBOPWithInlineNavCriteria | StandardBuyOffOperation | processPlanNavigationCriteria, relatedAssemblyNavigationCriteria, operationPath | BOP |
| DeleteMPMDocumentDescribeLink | StandardBuyOffOperation | LinksOIDs, ChangeOID | String |
| CreateMPMOperationToPartLinksWithInLineNavCriteria | StandardBuyOffOperation | consumablePaths, operationPath, ProcessPlan, Material, processPlanNavigationCriteria, relatedAssemblyNavigationCriteria | OperationToPartLink) |
| CreateMPMDocumentDescribeLinks | StandardBuyOffOperation | DocumentDescribeLink | DocumentDescribeLink) |
| UpdateOperationToOperatedPartLink | StandardBuyOffOperation | OperationToOperatedPartLink | OperationToOperatedPartLink) |
| InsertNewOperations | StandardBuyOffOperation | Operations | Operation) |
| GetDocuments | StandardBuyOffOperation | navigationCriteriaId | DocumentedObject |
| CreateOperationToStandardCCLink | StandardBuyOffOperation | OperationToStandardCCLink | OperationToStandardCCLink) |
| AssignCCFromProduct | StandardBuyOffOperation | AssociativeToSCCLinkOIDs | OperationToStandardCCLink) |
| UpdateConsumableLinks | StandardBuyOffOperation | OperationToConsumableLink | OperationToConsumableLink) |
| GetBOP | StandardBuyOffOperation | processPlanNavigationCriteriaId, relatedAssemblyNavigationCriteriaId, operationPath | BOP |
| DeleteOperationToOperatedPartLinks | StandardBuyOffOperation | LinksOIDs, ChangeOID | String) |
| UpdateOperationToStandardCCLink | StandardBuyOffOperation | OperationToStandardCCLink | OperationToStandardCCLink) |
| DeleteOperationToConsumableLink | StandardBuyOffOperation | LinksOIDs, ChangeOID | String |
| DeleteMPMOperationToPartLinks | StandardBuyOffOperation | LinksOIDs, ChangeOID | String |
| GetConsumed | StandardBuyOffOperation | processPlanNavigationCriteriaId, relatedAssemblyNavigationCriteriaId, operationPath | ConsumingOperation |
| CreateMPMDocumentReferenceLinks | StandardBuyOffOperation | DocumentReferenceLink | DocumentReferenceLink) |
| CreateMPMStandardProcedureLinks | StandardBuyOffOperation | StandardProcedureLink | StandardProcedureLink) |
| GetDocumentsWithInlineNavCriteria | StandardBuyOffOperation | navigationCriteria | DocumentedObject |
| UpdateMPMStandardProcedureLinks | StandardBuyOffOperation | StandardProcedureLink | StandardProcedureLink) |
| UpdateMPMOperationUsageLinks | StandardBuyOffOperation | OperationUsageLink | OperationUsageLink) |
| DeleteMPMOperationToStandardCCLinks | StandardBuyOffOperation | LinksOIDs, ChangeOID | String |
| GetConsumedWithInlineNavCriteria | StandardBuyOffOperation | processPlanNavigationCriteria, relatedAssemblyNavigationCriteria, operationPath | ConsumingOperation |
| CreateOperationInContextFromTemplate | StandardBuyOffOperation | OperationOID, NavigationCriteriaOID | Operation) |
| ModifyEffectivities | StandardBuyOffOperation | Effectivities | Effectivity) |
| RemoveEffectivities | StandardBuyOffOperation | Effectivities | - |
| Revise | StandardBuyOffOperation | VersionId | StandardBuyOffOperation |
| SetState | StandardBuyOffOperation | State | StandardBuyOffOperation |
| CheckIn | StandardBuyOffOperation | CheckInNote, CheckOutNote, KeepCheckedOut | StandardBuyOffOperation |
| CheckOut | StandardBuyOffOperation | CheckOutNote | StandardBuyOffOperation |
| UndoCheckOut | StandardBuyOffOperation | - | StandardBuyOffOperation |
| DeleteResourceReferenceLinks | Resource | LinksOIDs, ChangeOID | String) |
| CreateResourceDescribeDocumentLinks | Resource | ResourceDescribeLink | ResourceDescribeLink) |
| CreateResourceReferenceDocumentLinks | Resource | ResourceReferenceLink | ResourceReferenceLink) |
| CreateMPMCompatibilityLinks | Resource | MPMCompatibilityLinks | MPMCompatibilityLink) |
| CreateUses | Resource | ChangeOID, ResourceUses | PartUse) |
| GetPartStructure | Resource | NavigationCriteria | PartStructureItem |
| DeleteResourceDescribeLinks | Resource | LinksOIDs, ChangeOID | String) |
| GetDocuments | DocumentManageable | navigationCriteriaId | DocumentedObject |
| GetDocumentsWithInlineNavCriteria | DocumentManageable | navigationCriteria | DocumentedObject |
| CreateMPMDocumentDescribeLinks | DocumentManageable | DocumentDescribeLink | DocumentDescribeLink) |
| DeleteMPMDocumentDescribeLink | DocumentManageable | LinksOIDs, ChangeOID | String |
| CreateMPMCompatibilityLinks | WorkCenter | MPMCompatibilityLinks | MPMCompatibilityLink) |
| DeleteResourceReferenceLinks | WorkCenter | LinksOIDs, ChangeOID | String) |
| CreateResourceReferenceDocumentLinks | WorkCenter | ResourceReferenceLink | ResourceReferenceLink) |
| GetPartStructure | WorkCenter | NavigationCriteria | PartStructureItem |
| CreateResourceDescribeDocumentLinks | WorkCenter | ResourceDescribeLink | ResourceDescribeLink) |
| DeleteResourceDescribeLinks | WorkCenter | LinksOIDs, ChangeOID | String) |
| CreateUses | WorkCenter | ChangeOID, ResourceUses | PartUse) |
| Revise | WorkCenter | VersionId | WorkCenter |
| RemoveEffectivities | WorkCenter | Effectivities | - |
| ModifyEffectivities | WorkCenter | Effectivities | Effectivity) |
| SetState | WorkCenter | State | WorkCenter |
| CheckIn | WorkCenter | CheckInNote, CheckOutNote, KeepCheckedOut | WorkCenter |
| CheckOut | WorkCenter | CheckOutNote | WorkCenter |
| UndoCheckOut | WorkCenter | - | WorkCenter |
| ModifyEffectivities | Tooling | Effectivities | Effectivity) |
| RemoveEffectivities | Tooling | Effectivities | - |
| Revise | Tooling | VersionId | Tooling |
| SetState | Tooling | State | Tooling |
| CheckIn | Tooling | CheckInNote, CheckOutNote, KeepCheckedOut | Tooling |
| CheckOut | Tooling | CheckOutNote | Tooling |
| UndoCheckOut | Tooling | - | Tooling |
