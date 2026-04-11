# CADDocumentMgmt Actions

This document describes OData actions available in this domain.

## Unbound Actions

These actions can be called directly on the entity set.

| Action | Parameters | Return Type |
|--------|------------|-------------|
| SetStateCADDocuments | CADDocuments, State | CADDocument) |
| EditCADDocumentsSecurityLabels | CADDocuments | CADDocument) |

## Bound Actions

These actions are bound to specific entity types.

| Action | Bound To | Parameters | Return Type |
|--------|----------|------------|-------------|
| GetStructure | CADDocument | BOMMembersOnly, NavigationCriteria, PathFilterWithSiblings | CADStructure |
| GetMultiLevelComponentsReport | CADDocument | NavigationCriteria, BOMMembersOnly, ShowSingleLevelReport | CADDocumentsListReportItem) |
| SetState | CADDocument | State | CADDocument |
