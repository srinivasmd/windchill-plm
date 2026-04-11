# QMS Navigation Properties

This document describes navigation properties for entities in this domain.

## Relationship

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Related | PersonPlace |  | No |

## MPMProcessPlan

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Context | Container |  | No |

## Subject

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Creator | User |  | No |
| Modifier | User |  | No |

## PersonPlace

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| AdditionalAddresses | Address |  | Yes |
| PrimaryAddress | Address |  | Yes |
| AdditionalEmails | Email |  | Yes |
| PrimaryEmail | Email |  | Yes |
| AdditionalPhoneNumbers | PhoneNumber |  | Yes |
| PrimaryPhoneNumber | PhoneNumber |  | Yes |
| XReferences | XReference |  | Yes |
| Relationships | Relationship |  | Yes |
| RelatedSubjects | RelatedSubject |  | Yes |
| Context | Container |  | No |

## PartInstance

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Context | Container |  | No |

## MPMOperation

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Context | Container |  | No |

## Part

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Context | Container |  | No |

## MPMResource

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Context | Container |  | No |

## EPMDocument

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Context | Container |  | No |

## RelatedSubject

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Related | Subject |  | No |

## Document

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Context | Container |  | No |

## QualityContact

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Contact | PersonPlace |  | No |
