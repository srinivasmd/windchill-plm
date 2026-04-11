# ClfStructure Navigation Properties

This document describes navigation properties for entities in the PTC.ClfStructure namespace.

## Overview

ClfStructure domain defines **1 entities** with navigation properties.

---

## ClfNode

| Navigation Property | Type | Partner | Contains Target |
|---------------------|------|---------|-----------------|
| `ChildNodes` | `ClfNode` | - | No |
| `ParentNode` | `ClfNode` | - | No |
| `ClassifiedObjects` | `ClassifiedObject` | - | Yes |

**OData $expand Example:**
```
GET /ClfStructure/ClfNodes('{id}')?$expand=ChildNodes,ParentNode,ClassifiedObjects
```
