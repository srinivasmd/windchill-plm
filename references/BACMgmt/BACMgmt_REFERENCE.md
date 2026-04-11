---
Domain: BACMgmt
Client: `from domains.BACMgmt import BACMgmtClient`
---

> **Use the BACMgmtClient**: `from domains.BACMgmt import BACMgmtClient`
>
> This reference documents the entity types and properties. For programmatic access, use the domain client.

# Bulk Air Control Management (BACMgmt) Domain Reference

Complete reference documentation for the Windchill Bulk Air Control Management OData domain.

## Base URL

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/BACMgmt/
```

## Metadata URL

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/BACMgmt/$metadata
```

## Domain Overview

The Bulk Air Control (BAC) Management domain provides access to Windchill's bulk data import/export capabilities. This domain is used for:
- Managing received BAC deliveries (bulk data packages)
- Import mapping configurations
- Permission management for BAC operations

---

## Entity Types

### BACReceivedDelivery

A BAC Received Delivery represents a bulk data package that has been received into Windchill for processing.

**Endpoint:** `/BACMgmt/BACReceivedDeliveries`

**Operations:** `READ`

**Key Properties:**

| Property | Type | Nullable | Description |
|----------|------|----------|-------------|
| **ID** | String | No | Object identifier (OID) - Primary Key |
| **Name** | String | No | Delivery name |
| **FileName** | String | Yes | Original file name of the delivery |
| **Status** | String | Yes | Current processing status |
| **ReceivedDate** | DateTimeOffset | Yes | Date/time when delivery was received |
| **CreatedBy** | String | Yes | User who received the delivery |

**CRUD Operations:**

```bash
# Get all BAC received deliveries
GET /BACMgmt/BACReceivedDeliveries

# Get delivery by ID
GET /BACMgmt/BACReceivedDeliveries('{id}')

# Filter by status
GET /BACMgmt/BACReceivedDeliveries?$filter=Status eq 'RECEIVED'

# Filter by date range
GET /BACMgmt/BACReceivedDeliveries?$filter=ReceivedDate ge 2024-01-01T00:00:00Z

# Order by received date
GET /BACMgmt/BACReceivedDeliveries?$orderby=ReceivedDate desc

# Select specific properties
GET /BACMgmt/BACReceivedDeliveries?$select=ID,Name,Status,ReceivedDate
```

---

## Actions

### GetIXPermissions

Retrieves Information Exchange (IX) permissions for BAC operations.

**Action:** `GET /BACMgmt/GetIXPermissions`

**Parameters:** None

**Returns:** Permission information for the current user

**Usage:**

```bash
# Get IX permissions
POST /BACMgmt/GetIXPermissions
Content-Type: application/json
CSRF_NONCE: {token}

{}
```

---

### GetImportMappings

Retrieves available import mapping configurations for BAC operations.

**Action:** `GET /BACMgmt/GetImportMappings`

**Parameters:** None

**Returns:** Collection of import mapping configurations

**Usage:**

```bash
# Get import mappings
POST /BACMgmt/GetImportMappings
Content-Type: application/json
CSRF_NONCE: {token}

{}
```

---

## Common Query Examples

### Get Recent Deliveries

```bash
GET /BACMgmt/BACReceivedDeliveries?$orderby=ReceivedDate desc&$top=10
```

### Get Deliveries by Status

```bash
GET /BACMgmt/BACReceivedDeliveries?$filter=Status eq 'PROCESSING'
```

### Get Deliveries from Specific User

```bash
GET /BACMgmt/BACReceivedDeliveries?$filter=CreatedBy eq 'jsmith'
```

### Search Deliveries by Name

```bash
GET /BACMgmt/BACReceivedDeliveries?$filter=contains(Name, 'Project')
```

---

## Delivery Status Values

Common status values for BAC received deliveries:

| Status | Description |
|--------|-------------|
| **RECEIVED** | Delivery has been received, awaiting processing |
| **VALIDATING** | Delivery is being validated |
| **PROCESSING** | Delivery is being processed/imported |
| **COMPLETED** | Processing completed successfully |
| **FAILED** | Processing failed with errors |
| **CANCELLED** | Processing was cancelled |

---

## Notes

1. **Limited Operations**: BACMgmt domain primarily supports read operations and action calls.

2. **Bulk Operations**: This domain is designed for bulk data management. Individual entity operations may be limited.

3. **CSRF Token**: Required for all action calls (POST operations).

4. **Integration**: BACMgmt is typically used in integration scenarios for bulk data exchange between Windchill instances or external systems.

5. **Permissions**: Access to BAC operations requires appropriate Information Exchange permissions.

---

## Related Domains

- **ProdMgmt** - Parts and BOMs may be imported via BAC
- **DocMgmt** - Documents may be imported via BAC
- **Workflow** - Import workflows may be triggered by BAC operations

---

## Schema Version

Schema Version: Various (check metadata for version details)
