# Audit Navigation Properties

This document describes navigation properties for entities in this domain.

## AuditDetail

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| ChangeItem | ChangeItem |  | No |

## Audit

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| AuditDetails | AuditDetail |  | Yes |
| Auditor | User |  | No |
| Context | Container |  | No |
| Thumbnails | ContentItem |  | Yes |
| Creator | User |  | No |
| SmallThumbnails | ContentItem |  | Yes |
| Attachments | ContentItem |  | Yes |
| Modifier | User |  | No |
