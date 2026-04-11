# Workflow Navigation Properties

This document describes navigation properties for entities in this domain.

## VotingEventAudit

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Assignee | User |  | No |

## WfEventAudit

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| CompletedBy | User |  | No |

## WorkItem

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Owner | User |  | No |
| Activity | Activity |  | No |
| Subject | Subject |  | No |
| OriginalOwner | User |  | No |
| ProcessTemplate | WorkItemProcessTemplate |  | No |
| CompletedBy | User |  | No |

## Activity

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| WorkItems | WorkItem |  | No |
| VotingEventAudits | VotingEventAudit |  | Yes |
| Context | Container |  | No |

## WorkItemProcessTemplate

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Creator | User |  | No |
| Modifier | User |  | No |
