# ServiceInfoMgmt Actions

This document describes OData actions available in this domain.

## Unbound Actions

These actions can be called directly on the entity set.

| Action | Parameters | Return Type |
|--------|------------|-------------|
| ReviseSIMDocuments | SIMDocuments | SIMDocument) |
| SetStateSIMDocuments | SIMDocuments, State | SIMDocument) |
| SetStatePublicationStructures | PublicationStructures, State | PublicationStructure) |
| RevisePublicationStructures | PublicationStructures | PublicationStructure) |
| ReviseTableOfContents | TableOfContents | TableOfContent) |
| SetStateTableOfContents | TableOfContents, State | TableOfContent) |
| SetStateSIMDynamicDocuments | SIMDynamicDocuments, State | SIMDynamicDocument) |
| ReviseSIMDynamicDocuments | SIMDynamicDocuments | SIMDynamicDocument) |
| ReviseGraphicalInformationElements | GraphicalInformationElements | GraphicalInformationElement) |
| SetStateGraphicalInformationElements | GraphicalInformationElements, State | GraphicalInformationElement) |
| SetStateInformationGroups | InformationGroups, State | InformationGroup) |
| ReviseInformationGroups | InformationGroups | InformationGroup) |
| RevisePublicationSections | PublicationSections | PublicationSection) |
| SetStatePublicationSections | PublicationSections, State | PublicationSection) |
| SetStateInformationStructures | InformationStructures, State | InformationStructure) |
| ReviseInformationStructures | InformationStructures | InformationStructure) |
| ReviseTextualInformationElements | TextualInformationElements | TextualInformationElement) |
| SetStateTextualInformationElements | TextualInformationElements, State | TextualInformationElement) |
| ReviseGenericInformationElements | GenericInformationElements | GenericInformationElement) |
| SetStateGenericInformationElements | GenericInformationElements, State | GenericInformationElement) |
| ReviseIndexes | Indexes | Indexes) |
| SetStateIndexes | Indexes, State | Indexes) |
| SetStateDocumentInformationElements | DocumentInformationElements, State | DocumentInformationElement) |
| ReviseDocumentInformationElements | DocumentInformationElements | DocumentInformationElement) |

## Bound Actions

These actions are bound to specific entity types.

| Action | Bound To | Parameters | Return Type |
|--------|----------|------------|-------------|
| UploadStage3Action | SIMDocument | ContentInfo | ApplicationData) |
| UploadStage1Action | SIMDocument | NoOfFiles, DelegateName | CacheDescriptor) |
| GetDocStructure | SIMDocument | - | DocStructure |
| Revise | SIMDocument | VersionId | SIMDocument |
| SetState | SIMDocument | State | SIMDocument |
| CheckIn | SIMDocument | CheckInNote, CheckOutNote, KeepCheckedOut | SIMDocument |
| CheckOut | SIMDocument | CheckOutNote | SIMDocument |
| UndoCheckOut | SIMDocument | - | SIMDocument |
| SetState | PublicationStructure | State | PublicationStructure |
| Revise | PublicationStructure | VersionId | PublicationStructure |
| CheckIn | PublicationStructure | CheckInNote, CheckOutNote, KeepCheckedOut | PublicationStructure |
| CheckOut | PublicationStructure | CheckOutNote | PublicationStructure |
| UndoCheckOut | PublicationStructure | - | PublicationStructure |
| GetStructure | PublicationStructure | NavigationCriteriaId | Structure |
| Revise | TableOfContent | VersionId | TableOfContent |
| SetState | TableOfContent | State | TableOfContent |
| CheckIn | TableOfContent | CheckInNote, CheckOutNote, KeepCheckedOut | TableOfContent |
| CheckOut | TableOfContent | CheckOutNote | TableOfContent |
| UndoCheckOut | TableOfContent | - | TableOfContent |
| UploadStage3Action | SIMDynamicDocument | ContentInfo | ApplicationData) |
| UploadStage1Action | SIMDynamicDocument | NoOfFiles, DelegateName | CacheDescriptor) |
| SetState | SIMDynamicDocument | State | SIMDynamicDocument |
| Revise | SIMDynamicDocument | VersionId | SIMDynamicDocument |
| CheckOut | SIMDynamicDocument | - | SIMDynamicDocument) |
| UndoCheckOut | SIMDynamicDocument | - | SIMDynamicDocument) |
| CheckIn | SIMDynamicDocument | CheckInNote, KeepCheckedOut | SIMDynamicDocument) |
| Revise | GraphicalInformationElement | VersionId | GraphicalInformationElement |
| SetState | GraphicalInformationElement | State | GraphicalInformationElement |
| CheckIn | GraphicalInformationElement | CheckInNote, CheckOutNote, KeepCheckedOut | GraphicalInformationElement |
| CheckOut | GraphicalInformationElement | CheckOutNote | GraphicalInformationElement |
| UndoCheckOut | GraphicalInformationElement | - | GraphicalInformationElement |
| SetState | InformationGroup | State | InformationGroup |
| Revise | InformationGroup | VersionId | InformationGroup |
| CheckIn | InformationGroup | CheckInNote, CheckOutNote, KeepCheckedOut | InformationGroup |
| CheckOut | InformationGroup | CheckOutNote | InformationGroup |
| UndoCheckOut | InformationGroup | - | InformationGroup |
| GetStructure | InformationGroup | NavigationCriteriaId | Structure |
| Revise | PublicationSection | VersionId | PublicationSection |
| SetState | PublicationSection | State | PublicationSection |
| CheckIn | PublicationSection | CheckInNote, CheckOutNote, KeepCheckedOut | PublicationSection |
| CheckOut | PublicationSection | CheckOutNote | PublicationSection |
| UndoCheckOut | PublicationSection | - | PublicationSection |
| GetStructure | PublicationSection | NavigationCriteriaId | Structure |
| SetState | InformationStructure | State | InformationStructure |
| Revise | InformationStructure | VersionId | InformationStructure |
| CheckIn | InformationStructure | CheckInNote, CheckOutNote, KeepCheckedOut | InformationStructure |
| CheckOut | InformationStructure | CheckOutNote | InformationStructure |
| UndoCheckOut | InformationStructure | - | InformationStructure |
| GetStructure | InformationStructure | NavigationCriteriaId | Structure |
| Revise | TextualInformationElement | VersionId | TextualInformationElement |
| SetState | TextualInformationElement | State | TextualInformationElement |
| CheckIn | TextualInformationElement | CheckInNote, CheckOutNote, KeepCheckedOut | TextualInformationElement |
| CheckOut | TextualInformationElement | CheckOutNote | TextualInformationElement |
| UndoCheckOut | TextualInformationElement | - | TextualInformationElement |
| Revise | GenericInformationElement | VersionId | GenericInformationElement |
| SetState | GenericInformationElement | State | GenericInformationElement |
| CheckIn | GenericInformationElement | CheckInNote, CheckOutNote, KeepCheckedOut | GenericInformationElement |
| CheckOut | GenericInformationElement | CheckOutNote | GenericInformationElement |
| UndoCheckOut | GenericInformationElement | - | GenericInformationElement |
| GetStructure | GenericInformationElement | NavigationCriteriaId | Structure |
| Revise | Indexes | VersionId | Indexes |
| SetState | Indexes | State | Indexes |
| CheckIn | Indexes | CheckInNote, CheckOutNote, KeepCheckedOut | Indexes |
| CheckOut | Indexes | CheckOutNote | Indexes |
| UndoCheckOut | Indexes | - | Indexes |
| SetState | DocumentInformationElement | State | DocumentInformationElement |
| Revise | DocumentInformationElement | VersionId | DocumentInformationElement |
| CheckIn | DocumentInformationElement | CheckInNote, CheckOutNote, KeepCheckedOut | DocumentInformationElement |
| CheckOut | DocumentInformationElement | CheckOutNote | DocumentInformationElement |
| UndoCheckOut | DocumentInformationElement | - | DocumentInformationElement |
