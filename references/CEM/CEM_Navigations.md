# CEM Navigation Properties

This document describes navigation properties for entities in this domain.

## CustomerExperience

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| AdditionalRelatedProducts | RelatedProduct |  | Yes |
| PrimaryRelatedProduct | RelatedProduct |  | Yes |
| EntryLocation | Place |  | No |
| Context | Container |  | No |
| PrimaryRelatedPersonOrLocation | QualityContact |  | No |
| Creator | User |  | No |
| Modifier | User |  | No |
| AdditionalRelatedPersonnelOrLocations | QualityContact |  | No |

## RelatedProduct

| Navigation | Type | Partner | Contains Target |
|------------|------|---------|-----------------|
| Subject | Subject |  | No |
| ManufacturingLocation | Place |  | No |
