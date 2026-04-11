# CEM Actions

This document describes OData actions available in this domain.

## Unbound Actions

These actions can be called directly on the entity set.

| Action | Parameters | Return Type |
|--------|------------|-------------|
| SetStateCustomerExperiences | CustomerExperiences, State | CustomerExperience) |
| EditCustomerExperiencesSecurityLabels | CustomerExperiences | CustomerExperience) |

## Bound Actions

These actions are bound to specific entity types.

| Action | Bound To | Parameters | Return Type |
|--------|----------|------------|-------------|
| SetState | CustomerExperience | State | CustomerExperience |
