# Audit Actions

This document describes OData actions available in this domain.

## Unbound Actions

These actions can be called directly on the entity set.

| Action | Parameters | Return Type |
|--------|------------|-------------|
| SetStateAudits | Audits, State | Audit) |

## Bound Actions

These actions are bound to specific entity types.

| Action | Bound To | Parameters | Return Type |
|--------|----------|------------|-------------|
| UndoReservation | Audit | - | Audit |
| Reserve | Audit | Duration | Audit |
| SetState | Audit | State | Audit |
| UploadStage1Action | Audit | NoOfFiles, DelegateName | CacheDescriptor) |
| UploadStage3Action | Audit | ContentInfo | ApplicationData) |
