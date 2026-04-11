# ChangeMgmt Actions

This document describes OData actions available in this domain.

## Unbound Actions

These actions can be called directly on the entity set.

| Action | Parameters | Return Type |
|--------|------------|-------------|
| CreateChangeNoticeHierarchy | ChangeNotice, ChangeTask | ChangeNotice |
| SetPendingEffectivities | ResultingLinkItem, PendingEffectivities | PendingEffectivityManagedListItem) |
| SetStateChangeNotices | ChangeNotices, State | ChangeNotice) |
| EditChangeNoticesSecurityLabels | ChangeNotices | ChangeNotice) |
| SetStateChangeables | Changeables, State | Changeable) |
| SetStateProblemReports | ProblemReports, State | ProblemReport) |
| EditProblemReportsSecurityLabels | ProblemReports | ProblemReport) |
| SetStateVariances | Variances, State | Variance) |
| EditVariancesSecurityLabels | Variances | Variance) |
| SetStateChangeRequests | ChangeRequests, State | ChangeRequest) |
| EditChangeRequestsSecurityLabels | ChangeRequests | ChangeRequest) |
| SetStateChangeTasks | ChangeTasks, State | ChangeTask) |
| EditChangeTasksSecurityLabels | ChangeTasks | ChangeTask) |
| DeleteChangeTasks | ChangeTasks | - |

## Bound Actions

These actions are bound to specific entity types.

| Action | Bound To | Parameters | Return Type |
|--------|----------|------------|-------------|
| ReviseChangeNoticeWithChangeTasks | ChangeNotice | ChangeTaskImpact | ChangeNotice |
| Submit | ChangeNotice | - | ChangeNotice |
| Reserve | ChangeNotice | Duration | ChangeNotice |
| UndoReservation | ChangeNotice | - | ChangeNotice |
| SetState | ChangeNotice | State | ChangeNotice |
| UploadStage1Action | ChangeNotice | NoOfFiles, DelegateName | CacheDescriptor) |
| UploadStage3Action | ChangeNotice | ContentInfo | ApplicationData) |
| ModifyPendingEffectivities | ResultingLinkItem | PendingEffectivities | PendingEffectivity) |
| RemovePendingEffectivities | ResultingLinkItem | PendingEffectivities | - |
| ReviseChangeIssue | ChangeIssue | - | ChangeIssue |
| SetState | Changeable | State | Changeable |
| ReviseChangeIssue | ProblemReport | - | ChangeIssue |
| Reserve | ProblemReport | Duration | ProblemReport |
| UndoReservation | ProblemReport | - | ProblemReport |
| Submit | ProblemReport | - | ProblemReport |
| SetState | ProblemReport | State | ProblemReport |
| UploadStage1Action | ProblemReport | NoOfFiles, DelegateName | CacheDescriptor) |
| UploadStage3Action | ProblemReport | ContentInfo | ApplicationData) |
| ReviseChangeIssue | Variance | - | ChangeIssue |
| SetState | Variance | State | Variance |
| Submit | Variance | - | Variance |
| Reserve | Variance | Duration | Variance |
| UndoReservation | Variance | - | Variance |
| UploadStage1Action | Variance | NoOfFiles, DelegateName | CacheDescriptor) |
| UploadStage3Action | Variance | ContentInfo | ApplicationData) |
| ReviseChangeRequest | ChangeRequest | - | ChangeRequest |
| Submit | ChangeRequest | - | ChangeRequest |
| UndoReservation | ChangeRequest | - | ChangeRequest |
| Reserve | ChangeRequest | Duration | ChangeRequest |
| SetState | ChangeRequest | State | ChangeRequest |
| UploadStage1Action | ChangeRequest | NoOfFiles, DelegateName | CacheDescriptor) |
| UploadStage3Action | ChangeRequest | ContentInfo | ApplicationData) |
| UndoReservation | ChangeTask | - | ChangeTask |
| Reserve | ChangeTask | Duration | ChangeTask |
| SetState | ChangeTask | State | ChangeTask |
| UploadStage1Action | ChangeTask | NoOfFiles, DelegateName | CacheDescriptor) |
| UploadStage3Action | ChangeTask | ContentInfo | ApplicationData) |
