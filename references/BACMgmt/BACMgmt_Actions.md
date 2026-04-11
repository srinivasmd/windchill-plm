# BACMgmt Actions

This document describes OData actions available in this domain.

## Unbound Actions

These actions can be called directly on the entity set.

| Action | Parameters | Return Type |
|--------|------------|-------------|
| GetBACHistoryRecord | types, startDate, endDate, contextOID | BACHistoryData) |
| Preview | types, startDate, endDate | Delta) |
| Export | name, description, types, objects, startDate, endDate, isAutoCollectAllDependentsRequest | String |
| ImportStage1Action | - | CacheDescriptor) |
| ImportStage3Action | ContentInfo, UseBundledMappings, UseBundledResolutions | ImportResponse |
| SaveImportMappings | ImportMappings | Boolean |
| DeleteBACReceivedDeliveries | BACReceivedDeliveries | - |
