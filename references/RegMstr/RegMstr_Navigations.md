# RegMstr Navigation Properties

This document describes navigation properties for entities in this domain.

## Subject

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Context | Container |  | No |

## RegulatorySubmission

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Subject | Subject |  | No |
| SubjectLink | SubjectLink |  | No |
| SubmittedTo | Place |  | No |
| DriverLinks | DriverLink |  | No |
| Drivers | Driver |  | No |
| TableData | TableData |  | No |
| AcknowledgementMessages | AcknowledgementMessage |  | No |
| RegulatoryContent | ContentItem |  | Yes |
| Context | Container |  | No |
| PrimaryContent | ContentItem |  | Yes |
| Thumbnails | ContentItem |  | Yes |
| Creator | User |  | No |
| SmallThumbnails | ContentItem |  | Yes |
| Attachments | ContentItem |  | Yes |
| Modifier | User |  | No |

## DriverLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Driver | Driver |  | No |

## SubjectLink

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Subject | Subject |  | No |

## RegSubmission2

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Subjects | Subject |  | No |
| SubjectLinks | SubjectLink |  | No |
| SubmittedTo | Place |  | No |
| DriverLinks | DriverLink |  | No |
| Drivers | Driver |  | No |
| TableData | TableData |  | No |
| AcknowledgementMessages | AcknowledgementMessage |  | No |
| SubmissionAssignee | User |  | No |
| RegulatoryContent | ContentItem |  | Yes |
| Context | Container |  | No |
| Versions | RegSubmission2 |  | No |
| PrimaryContent | ContentItem |  | Yes |
| Thumbnails | ContentItem |  | Yes |
| Creator | User |  | No |
| SmallThumbnails | ContentItem |  | Yes |
| Revisions | RegSubmission2 |  | No |
| Attachments | ContentItem |  | Yes |
| Modifier | User |  | No |
