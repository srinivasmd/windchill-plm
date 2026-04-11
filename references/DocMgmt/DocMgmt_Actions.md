# DocMgmt Actions

This document describes OData actions available in this domain.

## Unbound Actions

These actions can be called directly on the entity set.

| Action | Parameters | Return Type |
|--------|------------|-------------|
| ReviseDocuments | Documents | Document) |
| SetStateDocuments | Documents, State | Document) |
| CheckOutDocuments | Workables, CheckOutNote | Document) |
| CheckInDocuments | Workables, CheckInNote | Document) |
| UndoCheckOutDocuments | Workables | Document) |
| EditDocumentsSecurityLabels | Documents | Document) |
| DeleteDocuments | Documents | - |
| CreateDocuments | Documents | Document) |
| UpdateDocuments | Documents | Document) |

## Bound Actions

These actions are bound to specific entity types.

| Action | Bound To | Parameters | Return Type |
|--------|----------|------------|-------------|
| GetDocStructure | Document | - | DocStructure |
| UploadStage1Action | Document | NoOfFiles, DelegateName | CacheDescriptor) |
| UploadStage3Action | Document | ContentInfo | ApplicationData) |
| Revise | Document | VersionId | Document |
| SetState | Document | State | Document |
| CheckIn | Document | CheckInNote, CheckOutNote, KeepCheckedOut | Document |
| CheckOut | Document | CheckOutNote | Document |
| UndoCheckOut | Document | - | Document |
| UpdateCommonProperties | Document | Updates | Document |
