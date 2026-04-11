# ChangeMgmt Navigation Properties

This document describes navigation properties for entities in this domain.

## ReportedAgainstLinkItem

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Changeable | Changeable |  | No |
| VarianceSubstituteLinks | VarianceSubstituteLinkItem |  | No |
| AffectedObjects | Changeable |  | No |

## ChangeItem

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ReferenceObjects | ChangeItem |  | Yes |
| Versions | ChangeItem |  | No |
| Organization | Organization |  | No |
| AffectedObjects | Changeable |  | No |
| AffectsLinks | AffectsLinkItem |  | Yes |
| Revisions | ChangeItem |  | No |
| ProcessObjects | ChangeItem |  | Yes |

## PendingEffectivity

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| EffectivityContext | PartEffectivityContext |  | No |

## ChangeRequest

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ChangeAdministratorI | Principal |  | No |
| Context | Container |  | No |
| CRAffectLinks | RelevantRequestDataLinkItem |  | Yes |
| Folder | Folder |  | No |
| Attachments | ContentItem |  | Yes |

## VarianceSubstituteLinkItem

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ReplacedWith | ReplacementPart |  | No |
| ReplacementFor | PartUse |  | Yes |
| AffectedObjectLink | ReportedAgainstLinkItem |  | No |

## ProcessLinkItem

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ProcessObjects | ChangeItem |  | Yes |

## GenericChangeRequest

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ProcessLinks | ProcessLinkItem |  | Yes |
| ReferenceLinks | ReferenceLinkItem |  | Yes |
| Creator | User |  | No |
| Modifier | User |  | No |

## ChangeOrder

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ProcessLinks | ProcessLinkItem |  | Yes |
| ResultingObjects | Changeable |  | No |
| UnincorporatedLinks | UnincorporatedLinkItem |  | Yes |
| ReferenceLinks | ReferenceLinkItem |  | Yes |
| Creator | User |  | No |
| CNAffectLinks | AffectedActivityDataLinkItem |  | Yes |
| ResultingLinks | ResultingLinkItem |  | Yes |
| Modifier | User |  | No |

## ChangeIssue

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ProcessLinks | ProcessLinkItem |  | Yes |
| CIAffectLinks | ReportedAgainstLinkItem |  | Yes |
| ReferenceLinks | ReferenceLinkItem |  | Yes |
| Creator | User |  | No |
| Modifier | User |  | No |

## AffectedActivityDataLinkItem

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Changeable | Changeable |  | No |
| AffectedObjects | Changeable |  | No |

## Changeable

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Context | Container |  | No |
| Organization | Organization |  | No |
| UnincorporatedByObjects | ChangeItem |  | Yes |
| UnincorporatedByChangeObjects | ChangeItem |  | Yes |
| AffectedByObjects | ChangeItem |  | Yes |
| ResultingByLinks | ResultingLinkItem |  | Yes |
| Creator | User |  | No |
| Revisions | Changeable |  | No |
| AffectedByLinks | AffectsLinkItem |  | Yes |
| ResultedByObjects | ChangeItem |  | Yes |
| Versions | Changeable |  | No |
| AffectedByTasks | ChangeItem |  | Yes |
| ResultedByChangeObjects | ChangeItem |  | Yes |
| UnincorporatedByLinks | UnincorporatedLinkItem |  | Yes |
| Modifier | User |  | No |
| AffectedByChangeObjects | ChangeItem |  | Yes |

## ReferenceLinkItem

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ReferenceObjects | ChangeItem |  | Yes |

## RelevantRequestDataLinkItem

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Changeable | Changeable |  | No |
| AffectedObjects | Changeable |  | No |

## AffectsLinkItem

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| AffectedByObjects | ChangeItem |  | Yes |
| AffectedObjects | Changeable |  | No |
| AffectedByChangeObjects | ChangeItem |  | Yes |

## ResultingLinkItem

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Changeable | Changeable |  | No |
| PendingEffectivities | PendingEffectivity |  | Yes |
| ResultedByObjects | ChangeItem |  | Yes |
| ResultingObjects | Changeable |  | No |
| ResultedByChangeObjects | ChangeItem |  | Yes |

## UnincorporatedLinkItem

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ResultedByObjects | ChangeItem |  | Yes |
| ResultingObjects | Changeable |  | No |
| UnincorporatedByObjects | ChangeItem |  | Yes |
| UnincorporatedByChangeObjects | ChangeItem |  | Yes |

## ChangeNotice

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ChangeAdministratorI | Principal |  | No |
| ChangeAdministratorII | Principal |  | No |
| ImplementationPlan | ChangeTask |  | No |
| Context | Container |  | No |
| Folder | Folder |  | No |
| Attachments | ContentItem |  | Yes |

## Variance

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| VarianceOwners | User |  | No |
| ChangeAdministratorI | Principal |  | No |
| Context | Container |  | No |
| Folder | Folder |  | No |
| Attachments | ContentItem |  | Yes |

## ProblemReport

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ChangeAdministratorI | Principal |  | No |
| Context | Container |  | No |
| Folder | Folder |  | No |
| Attachments | ContentItem |  | Yes |

## ChangeTask

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ChangeNotice | ChangeNotice |  | No |
| Assignee | User |  | No |
| Reviewer | User |  | No |
| Context | Container |  | No |
| ResultingObjects | Changeable |  | No |
| UnincorporatedLinks | UnincorporatedLinkItem |  | Yes |
| Creator | User |  | No |
| CNAffectLinks | AffectedActivityDataLinkItem |  | Yes |
| ResultingLinks | ResultingLinkItem |  | Yes |
| Attachments | ContentItem |  | Yes |
| Modifier | User |  | No |
