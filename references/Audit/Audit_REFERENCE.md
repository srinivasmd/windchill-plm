---
Domain: Audit
Client: `from domains.Audit import AuditClient`
---

> **Use the AuditClient**: `from domains.Audit import AuditClient`
>
> This reference documents the entity types and properties. For programmatic access, use the domain client.

# Audit Domain Reference

Complete reference documentation for the Windchill Audit OData domain.

## Base URL

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/Audit/
```

## Metadata URL

```
https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/Audit/$metadata
```

## Domain Overview

The Audit domain provides access to Windchill's audit trail and compliance tracking capabilities. This domain is used for:
- Tracking user actions and system events
- Recording data changes for compliance
- Audit trail queries and reporting
- Change tracking for regulated environments

---

## Entity Types

### Audit

An Audit record represents a tracked event or action in Windchill. Audit records capture who did what, when, and to which objects.

**Endpoint:** `/Audit/Audits`

**Operations:** `READ`

**Key Properties:**

| Property | Type | Nullable | Description |
|----------|------|----------|-------------|
| **ID** | String | No | Object identifier (OID) - Primary Key |
| **Name** | String | Yes | Audit event name |
| **AuditType** | String | Yes | Type of audit event |
| **Action** | String | Yes | Action performed (CREATE, UPDATE, DELETE, etc.) |
| **ObjectName** | String | Yes | Name of the affected object |
| **ObjectType** | String | Yes | Type of the affected object |
| **ObjectID** | String | Yes | ID of the affected object |
| **Timestamp** | DateTimeOffset | Yes | When the event occurred |
| **UserName** | String | Yes | User who performed the action |
| **Details** | String | Yes | Additional event details |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **AuditDetails** | Collection(PTC.Audit.AuditDetail) | Detailed audit information |
| **Context** | PTC.DataAdmin.Container | Container context |
| **User** | PTC.PrincipalMgmt.User | User who performed the action |
| **SourceObject** | Object | The source object of the audit |
| **TargetObject** | Object | The target object of the audit |
| **RelatedObjects** | Collection | Related objects |
| **Session** | PTC.Audit.AuditSession | Session information |
| **Attachments** | Collection(PTC.ContentItem) | Attached documents |

**CRUD Operations:**

```bash
# Get all audit records
GET /Audit/Audits

# Get audit by ID
GET /Audit/Audits('{id}')

# Filter by action type
GET /Audit/Audits?$filter=Action eq 'CREATE'

# Filter by user
GET /Audit/Audits?$filter=UserName eq 'jsmith'

# Filter by object type
GET /Audit/Audits?$filter=ObjectType eq 'WTPart'

# Filter by date range
GET /Audit/Audits?$filter=Timestamp ge 2024-01-01T00:00:00Z and Timestamp le 2024-12-31T23:59:59Z

# Get audit with details
GET /Audit/Audits('{id}')?$expand=AuditDetails,User

# Order by timestamp
GET /Audit/Audits?$orderby=Timestamp desc

# Paginate results
GET /Audit/Audits?$skip=0&$top=100
```

---

### AuditDetail

AuditDetail provides granular information about a specific audit event, including field-level changes.

**Endpoint:** `/Audit/AuditDetails`

**Operations:** `READ`

**Key Properties:**

| Property | Type | Nullable | Description |
|----------|------|----------|-------------|
| **ID** | String | No | Object identifier (OID) - Primary Key |
| **FieldName** | String | Yes | Name of the changed field |
| **OldValue** | String | Yes | Value before the change |
| **NewValue** | String | Yes | Value after the change |
| **DataType** | String | Yes | Data type of the field |
| **ChangeType** | String | Yes | Type of change (UPDATE, ADD, REMOVE) |
| **Timestamp** | DateTimeOffset | Yes | When the change occurred |
| **SequenceNumber** | Int32 | Yes | Order of the change within the audit |
| **PropertyName** | String | Yes | Internal property name |
| **Description** | String | Yes | Human-readable description |
| **CreatedOn** | DateTimeOffset | Yes | Record creation timestamp |
| **ModifiedOn** | DateTimeOffset | Yes | Record modification timestamp |

**Navigation Properties:**

| Navigation | Type | Description |
|------------|------|-------------|
| **Audit** | PTC.Audit.Audit | Parent audit record |

**CRUD Operations:**

```bash
# Get all audit details
GET /Audit/AuditDetails

# Get details for specific audit
GET /Audit/AuditDetails?$filter=Audit/ID eq '{audit_id}'

# Get details by field name
GET /Audit/AuditDetails?$filter=FieldName eq 'State'

# Filter by change type
GET /Audit/AuditDetails?$filter=ChangeType eq 'UPDATE'
```

---

### ChangeItem

ChangeItem represents a specific item that was changed in an audit event.

**Endpoint:** `/Audit/ChangeItems`

**Operations:** `READ`

**Key Properties:**

| Property | Type | Nullable | Description |
|----------|------|----------|-------------|
| **ID** | String | No | Object identifier (OID) - Primary Key |
| **Name** | String | Yes | Change item name |
| **Type** | String | Yes | Type of the changed item |
| **Value** | String | Yes | Value of the change item |
| **Description** | String | Yes | Description of the change |
| **Sequence** | Int32 | Yes | Sequence order |

**CRUD Operations:**

```bash
# Get all change items
GET /Audit/ChangeItems

# Filter by type
GET /Audit/ChangeItems?$filter=Type eq 'Attribute'
```

---

## Actions

### Resolve

Resolves an audit record, marking it as reviewed or addressed.

**Action:** `POST /Audit/Audits('{id}')/PTC.Audit.Resolve`

**Parameters:** None

**Returns:** Updated audit record

**Usage:**

```bash
# Resolve an audit
POST /Audit/Audits('{id}')/PTC.Audit.Resolve
Content-Type: application/json
CSRF_NONCE: {token}

{}
```

---

## Common Query Examples

### Get Recent Audit Records

```bash
GET /Audit/Audits?$orderby=Timestamp desc&$top=50
```

### Get Audits by User

```bash
GET /Audit/Audits?$filter=UserName eq 'jsmith'&$expand=AuditDetails
```

### Get Audits for Specific Object

```bash
GET /Audit/Audits?$filter=ObjectID eq 'OR:wt.part.WTPart:123456'
```

### Get CREATE Actions in Date Range

```bash
GET /Audit/Audits?$filter=Action eq 'CREATE' and Timestamp ge 2024-01-01T00:00:00Z and Timestamp le 2024-01-31T23:59:59Z
```

### Get Audits by Object Type

```bash
GET /Audit/Audits?$filter=ObjectType eq 'WTPart'&$orderby=Timestamp desc
```

### Get Field-Level Changes

```bash
GET /Audit/AuditDetails?$filter=Audit/ID eq '{audit_id}'&$orderby=SequenceNumber asc
```

### Get State Changes

```bash
GET /Audit/AuditDetails?$filter=FieldName eq 'State' and ChangeType eq 'UPDATE'&$expand=Audit
```

### Count Audits by Action Type

```bash
GET /Audit/Audits?$filter=Timestamp ge 2024-01-01T00:00:00Z&$apply=groupby(Action,aggregate($count as Count))
```

---

## Audit Action Types

Common action types recorded in audits:

| Action | Description |
|--------|-------------|
| **CREATE** | Object was created |
| **UPDATE** | Object was modified |
| **DELETE** | Object was deleted |
| **CHECKOUT** | Object was checked out |
| **CHECKIN** | Object was checked in |
| **UNDHECKOUT** | Checkout was undone |
| **REVISE** | Object was revised |
| **STATE_CHANGE** | Lifecycle state changed |
| **MOVE** | Object was moved |
| **COPY** | Object was copied |
| **LOCK** | Object was locked |
| **UNLOCK** | Object was unlocked |
| **PERMISSION_CHANGE** | Permissions were modified |
| **SHARE** | Object was shared |
| **UNSHARE** | Object sharing was removed |

---

## Audit Configuration

Windchill audit can be configured to track:

1. **Object-Level Auditing**: Track CREATE, UPDATE, DELETE operations
2. **Attribute-Level Auditing**: Track changes to specific attributes
3. **Relationship Auditing**: Track relationship changes
4. **State Auditing**: Track lifecycle state transitions
5. **Security Auditing**: Track permission and access changes

---

## Notes

1. **Read-Only**: Audit records are typically read-only and cannot be modified or deleted through the OData API.

2. **Performance**: Large audit queries can impact performance. Use pagination and filters.

3. **Retention**: Audit records may be subject to retention policies. Check your Windchill configuration.

4. **Compliance**: Audit trails are critical for regulatory compliance (FDA, ISO, etc.). Ensure audit is properly configured.

5. **CSRF Token**: Required for action calls like Resolve.

---

## Related Domains

- **PrincipalMgmt** - User information for audit records
- **DataAdmin** - Container and organization context
- **Workflow** - Workflow-related audit events
- **ChangeMgmt** - Change object audit events

---

## Schema Version

Schema Version: Various (check metadata for version details)