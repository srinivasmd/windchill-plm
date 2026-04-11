# Workflow Actions

This document describes OData actions available in this domain.

## Unbound Actions

These actions can be called directly on the entity set.

| Action | Parameters | Return Type |
|--------|------------|-------------|
| ReassignWorkItems | WorkItems, User, Comment, RestrictReassignToRole | WorkItem) |

## Bound Actions

These actions are bound to specific entity types.

| Action | Bound To | Parameters | Return Type |
|--------|----------|------------|-------------|
| CompleteWorkitem | WorkItem | UserEventList, WorkitemComment, VoteAction, AutomateFastTrack, Variables, SignatureToken, SubjectName, ActivityName | WorkItem |
| SaveWorkitem | WorkItem | UserEventList, WorkitemComment, VoteAction, AutomateFastTrack, Variables | WorkItem |
