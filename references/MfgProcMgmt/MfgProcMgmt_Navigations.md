# MfgProcMgmt Navigation Properties

This document describes navigation properties for entities in this domain.

## ConsumedPart

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Part | Part |  | No |
| OperationToPartLink | OperationToPartLink |  | No |
| PartPathOccurrenceLinks | PartPathOccurrenceLink |  | No |

## StandardCC

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| StandardCCToProcessPlanLinks | StandardCCToProcessPlanLink |  | No |
| StandardCCToResourceLinks | StandardCCToResourceLink |  | No |
| Context | Container |  | No |
| ResultedByObjects | ChangeItem |  | Yes |
| Organization | Organization |  | No |
| Versions | StandardCC |  | No |
| Revisions | StandardCC |  | No |
| Folder | Folder |  | No |

## AssociativeToStandardCCLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| SCC | StandardCC |  | No |

## MPMDescribedByDocument

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| DocumentDescribeLink | DocumentDescribeLink |  | No |
| DescribedBy | Document |  | No |

## RoutingAssignmentLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| RoutingPlan | RoutingPlan |  | No |
| Routable | Routable |  | No |
| NavigationCriteria | NavigationCriteria |  | No |

## ProcessMaterial

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Context | Container |  | No |
| PPlan_LinkNav | ObjectReferenceable |  | No |
| ResultedByObjects | ChangeItem |  | Yes |
| Organization | Organization |  | No |
| Versions | ProcessMaterial |  | No |
| Effectivities | Effectivity |  | Yes |
| AssignedOptionSet | OptionSet |  | No |
| Revisions | ProcessMaterial |  | No |
| Folder | Folder |  | No |

## ConsumedProcessMaterial

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| OperationToConsumableLink | OperationToConsumableLink |  | No |
| ProcessMaterial | ProcessMaterial |  | No |

## OperationToOperatedPartLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| operation | Operation |  | No |
| Part | Part |  | No |

## OperationUsageLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| OperationHolder | OperationHolder |  | No |
| Operation | Operation |  | No |

## RoutingArtifactLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ProcessPlan | ProcessPlan |  | No |
| Part | Part |  | No |
| Resource | Resource |  | No |
| RoutingPrecedenceLink | RoutingPrecedenceLink |  | No |

## DocumentReferenceLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| References | Document |  | No |

## OperationToPartLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| OperationHolder | OperationHolder |  | No |
| Part | Part |  | No |

## OperationToWorkCenterLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ReferencedBy | Operation |  | No |
| WorkCenter | WorkCenter |  | No |

## OperationToStandardCCLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| StandardCC | StandardCC |  | No |
| Resources | Resource |  | No |
| MPMStandardCCsUsageToResourceLink | StandardCCUsageToResourceLink |  | Yes |
| StandardProcedures | StandardProcedure |  | No |
| MPMStdCCUsageToProcessPlanLink | StandardCCUsageToProcessPlanLink |  | Yes |
| PartReference | Material |  | No |
| DescribedByDocument | Document |  | No |
| MPMStandardCCUsageToDDLink | StandardCCUsageToDDLink |  | No |
| References | Document |  | No |
| MPMStandardCCUsageToDRLink | StandardCCUsageToDRLink |  | No |

## StandardCCUsageToResourceLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Resource | Resource |  | No |

## ConsumedStandardCC

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| OperationToStandardCCLink | OperationToStandardCCLink |  | No |
| StandardCC | StandardCC |  | No |

## Sequence

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| StandardProcedureLink | StandardProcedureLink |  | Yes |
| StandardCCLinks | OperationToStandardCCLink |  | Yes |
| Context | Container |  | No |
| ResultedByObjects | ChangeItem |  | Yes |
| Versions | Sequence |  | No |
| Effectivities | Effectivity |  | Yes |
| AssignedOptionSet | OptionSet |  | No |
| Revisions | Sequence |  | No |

## MPMReferenceDocument

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| DocumentReferenceLink | DocumentReferenceLink |  | No |
| References | Document |  | No |

## DocumentManageable

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| DocumentDescribeLinks | DocumentDescribeLink |  | No |
| DocumentReferenceLinks | DocumentReferenceLink |  | No |
| Creator | User |  | No |
| Modifier | User |  | No |

## MpmEpmDocumentDescribeLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| DescribedBy | CADDocument |  | No |

## RoutingMilestoneGroup

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Line | WorkCenter |  | No |

## RoutingMilestone

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| RoutingMilestoneLink | RoutingMilestoneLink |  | No |
| RoutingPrecedenceLink | RoutingPrecedenceLink |  | No |
| RoutingOperation | RoutingOperation |  | No |
| RouteHolder | RouteHolder |  | No |
| RoutingArtifactLink | RoutingArtifactLink |  | No |

## RoutingMilestoneLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| RoutingPlan | RoutingPlan |  | No |
| RoutingMilestone | RoutingMilestone |  | No |
| RoutingMilestoneGroup | RoutingMilestoneGroup |  | No |
| RoutingMilestoneContainer | RoutingMilestoneContainer |  | No |

## StandardCCToProcessPlanLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| StandardProcedure | StandardProcedure |  | No |

## Tooling

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Context | Container |  | No |
| PPlan_LinkNav | ObjectReferenceable |  | No |
| ResultedByObjects | ChangeItem |  | Yes |
| Versions | Tooling |  | No |
| Organization | Organization |  | No |
| Effectivities | Effectivity |  | Yes |
| AssignedOptionSet | OptionSet |  | No |
| Revisions | Tooling |  | No |
| Folder | Folder |  | No |

## RouteHolder

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| MPMCompatibilityLinks | MPMCompatibilityLink |  | Yes |

## Material

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| PartToProcessPlanLinks | PartToProcessPlanLink |  | No |
| AssociativeToSCCLinks | AssociativeToStandardCCLink |  | No |
| Context | Container |  | No |
| Versions | Material |  | No |
| Organization | Organization |  | No |
| Creator | User |  | No |
| Representations | Representation |  | No |
| Revisions | Material |  | No |
| Folder | Folder |  | No |
| Modifier | User |  | No |

## OperationHolder

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| OperationUsageLinks | OperationUsageLink |  | No |
| OperationHolderUsageLink | OperationHolderUsageLink |  | Yes |

## ConsumedTooling

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| OperationToConsumableLink | OperationToConsumableLink |  | No |
| Tooling | Tooling |  | No |

## SequenceHolder

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| SequenceUsageLink | SequenceUsageLink |  | No |

## StandardProcedureLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| OperationHolder | OperationHolder |  | No |
| ProcessPlan | ProcessPlan |  | No |

## WorkCenter

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Context | Container |  | No |
| PPlan_LinkNav | ObjectReferenceable |  | No |
| ResultedByObjects | ChangeItem |  | Yes |
| Organization | Organization |  | No |
| Versions | WorkCenter |  | No |
| Effectivities | Effectivity |  | Yes |
| AssignedOptionSet | OptionSet |  | No |
| Revisions | WorkCenter |  | No |
| Folder | Folder |  | No |

## DocumentDescribeLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| DescribedBy | Document |  | No |

## RoutingMilestoneContainer

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| RoutingPlan | RoutingPlan |  | No |
| RoutingMilestoneGroup | RoutingMilestoneGroup |  | No |

## Resource

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| DescribedBy | ResourceDescribeLink |  | Yes |
| References | ResourceReferenceLink |  | Yes |
| Uses | PartUse |  | Yes |
| MPMCompatibilityLinks | MPMCompatibilityLink |  | Yes |
| PartDocAssociations | PartDocAssociation |  | Yes |
| Creator | User |  | No |
| Modifier | User |  | No |

## ProcessPlan

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| StandardProcedureLink | StandardProcedureLink |  | Yes |
| StandardCCLinks | OperationToStandardCCLink |  | Yes |
| Context | Container |  | No |
| ResultedByObjects | ChangeItem |  | Yes |
| Versions | ProcessPlan |  | No |
| Organization | Organization |  | No |
| Effectivities | Effectivity |  | Yes |
| AssignedOptionSet | OptionSet |  | No |
| RoutingAssignmentLink | RoutingAssignmentLink |  | No |
| Folder | Folder |  | No |
| Revisions | ProcessPlan |  | No |

## StandardCCUsageToDDLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| DescribedBy | Document |  | No |

## ConsumedSkill

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| OperationToConsumableLink | OperationToConsumableLink |  | No |
| Skill | Skill |  | No |

## DocumentedObject

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| DescribedByDocuments | MPMDescribedByDocument |  | No |
| ReferenceDocuments | MPMReferenceDocument |  | No |

## Plant

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| PPlan_LinkNav | ObjectReferenceable |  | No |
| Versions | Plant |  | No |
| OrganizationReferenceNav | ObjectReferenceable |  | No |
| Effectivities | Effectivity |  | Yes |
| Revisions | Plant |  | No |
| Folder | Folder |  | No |

## BOP

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| OperationHolder | OperationHolder |  | No |
| OperationHolderUsageLink | OperationHolderUsageLink |  | No |
| Components | BOP |  | Yes |
| RelatedParts | PartToProcessPlanLink |  | No |
| ConsumedOperatedOnParts | ConsumedOperatedOnPart |  | No |
| ConsumedParts | ConsumedPart |  | No |
| ConsumedProcessMaterials | ConsumedProcessMaterial |  | No |
| ConsumedSkills | ConsumedSkill |  | No |
| ConsumedStandardCCs | ConsumedStandardCC |  | No |
| ConsumedToolings | ConsumedTooling |  | No |
| ConsumedWorkCenters | ConsumedWorkCenter |  | No |
| DescribedByDocuments | MPMDescribedByDocument |  | No |
| ReferenceDocuments | MPMReferenceDocument |  | No |
| DownloadUrls | DownloadUrl |  | No |
| Representations | Representation |  | No |

## PartToProcessPlanLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ProcessPlan | ProcessPlan |  | No |
| Part | Part |  | No |
| ProducedParts | Part |  | No |

## Operation

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| StandardCCLinks | OperationToStandardCCLink |  | Yes |
| OperationToConsumableLinks | OperationToConsumableLink |  | Yes |
| OperationToWorkCenterLinks | OperationToWorkCenterLink |  | Yes |
| StandardProcedureLink | StandardProcedureLink |  | Yes |
| OperationToOperatedPartLink | OperationToOperatedPartLink |  | Yes |
| OperationToPartLink | OperationToPartLink |  | Yes |
| Context | Container |  | No |
| ResultedByObjects | ChangeItem |  | Yes |
| Organization | Organization |  | No |
| Versions | Operation |  | No |
| Effectivities | Effectivity |  | Yes |
| AssignedOptionSet | OptionSet |  | No |
| Representations | Representation |  | No |
| Folder | Folder |  | No |
| Revisions | Operation |  | No |

## MPMCompatibilityLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ReferencedBy | Resource |  | No |
| References | Resource |  | No |

## OperationToConsumableLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ReferencedBy | Operation |  | No |
| ConsumableResource | ConsumableResource |  | No |

## Routable

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ProcessPlan | ProcessPlan |  | No |
| Part | Part |  | No |

## EPMDocumentManageable

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| EPMDocumentDescribeLinks | MpmEpmDocumentDescribeLink |  | No |
| Creator | User |  | No |
| Modifier | User |  | No |

## ConsumedWorkCenter

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| OperationToWorkCenterLink | OperationToWorkCenterLink |  | No |
| WorkCenter | WorkCenter |  | No |

## SequenceUsageLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| SequenceHolder | SequenceHolder |  | No |
| Sequence | Sequence |  | No |

## Skill

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Context | Container |  | No |
| PPlan_LinkNav | ObjectReferenceable |  | No |
| ResultedByObjects | ChangeItem |  | Yes |
| Versions | Skill |  | No |
| Organization | Organization |  | No |
| Effectivities | Effectivity |  | Yes |
| AssignedOptionSet | OptionSet |  | No |
| Folder | Folder |  | No |
| Revisions | Skill |  | No |

## ResourceReferenceLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ReferencedBy | Resource |  | No |
| References | Document |  | No |

## ConsumedOperatedOnPart

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Part | Part |  | No |
| OperationToOperatedPartLink | OperationToOperatedPartLink |  | No |

## ConsumingOperation

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ConsumedOperatedOnParts | ConsumedOperatedOnPart |  | No |
| ConsumedParts | ConsumedPart |  | No |
| ConsumedProcessMaterials | ConsumedProcessMaterial |  | No |
| ConsumedSkills | ConsumedSkill |  | No |
| ConsumedStandardCCs | ConsumedStandardCC |  | No |
| ConsumedToolings | ConsumedTooling |  | No |
| ConsumedWorkCenters | ConsumedWorkCenter |  | No |

## StandardCCUsageToProcessPlanLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| StandardProcedure | StandardProcedure |  | No |

## RoutingPlan

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| RoutingAssignmentLink | RoutingAssignmentLink |  | No |
| NavigationCriteria | NavigationCriteria |  | No |
| Plant | Plant |  | No |
| StartMilestone | RoutingMilestone |  | No |
| EndMilestone | RoutingMilestone |  | No |
| RoutingMilestone | RoutingMilestone |  | No |
| RoutingMilestoneLink | RoutingMilestoneLink |  | No |
| RoutingPrecedenceLink | RoutingPrecedenceLink |  | No |
| RoutingLine | WorkCenter |  | No |
| Context | Container |  | No |
| Versions | RoutingPlan |  | No |
| Organization | Organization |  | No |
| Effectivities | Effectivity |  | Yes |
| Creator | User |  | No |
| Revisions | RoutingPlan |  | No |
| Folder | Folder |  | No |
| Modifier | User |  | No |

## ResourceDescribeLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Describes | Resource |  | No |
| DescribedBy | Document |  | No |

## RoutableToNavigationCriteriaItem

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Routable | Routable |  | No |
| NavigationCriteria | NavigationCriteria |  | No |

## StandardCCToResourceLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Resource | Resource |  | No |

## RoutingPrecedenceLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| RoutingMilestone | RoutingMilestone |  | No |
| RoutingArtifactLink | RoutingArtifactLink |  | No |
