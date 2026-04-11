# RegMstr Actions

This document describes OData actions available in this domain.

## Unbound Actions

These actions can be called directly on the entity set.

| Action | Parameters | Return Type |
|--------|------------|-------------|
| ProcessAcknowledgement | SubmissionType, AcknowledgementName, AcknowledgementBody | ApplicationData |
| SetStateRegSubmission2 | RegSubmission2, State | RegSubmission2) |
| ReviseRegSubmission2 | RegSubmission2 | RegSubmission2) |
| CheckOutRegSubmission2 | Workables, CheckOutNote | RegSubmission2) |
| CheckInRegSubmission2 | Workables, CheckInNote | RegSubmission2) |
| UndoCheckOutRegSubmission2 | Workables | RegSubmission2) |
| SetStateRegulatorySubmissions | RegulatorySubmissions, State | RegulatorySubmission) |

## Bound Actions

These actions are bound to specific entity types.

| Action | Bound To | Parameters | Return Type |
|--------|----------|------------|-------------|
| UploadStage1Action | RegSubmission2 | NoOfFiles, DelegateName | CacheDescriptor) |
| UploadStage3Action | RegSubmission2 | ContentInfo | ApplicationData) |
| Reserve | RegSubmission2 | Duration | RegSubmission2 |
| UndoReservation | RegSubmission2 | - | RegSubmission2 |
| SetState | RegSubmission2 | State | RegSubmission2 |
| Revise | RegSubmission2 | VersionId | RegSubmission2 |
| CheckIn | RegSubmission2 | CheckInNote, CheckOutNote, KeepCheckedOut | RegSubmission2 |
| CheckOut | RegSubmission2 | CheckOutNote | RegSubmission2 |
| UndoCheckOut | RegSubmission2 | - | RegSubmission2 |
| UploadStage3Action | RegulatorySubmission | ContentInfo | ApplicationData) |
| CreateFollowup | RegulatorySubmission | - | RegulatorySubmission |
| UploadStage1Action | RegulatorySubmission | NoOfFiles, DelegateName | CacheDescriptor) |
| SetState | RegulatorySubmission | State | RegulatorySubmission |
| UndoReservation | RegulatorySubmission | - | RegulatorySubmission |
| Reserve | RegulatorySubmission | Duration | RegulatorySubmission |
