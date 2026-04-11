# Reference Documentation

This folder contains detailed reference documentation organized by domain.

## Structure

```
references/
├── <Domain>/
│   ├── <Domain>_REFERENCE.md    # Usage guide and examples
│   ├── <Domain>_Navigations.md  # Navigation properties
│   ├── <Domain>_Entities.json   # Entity definitions
│   └── <Domain>_Metadata.xml    # Raw OData metadata
└── PTC/
    ├── PTC_REFERENCE.md         # Common PTC entities
    ├── actions.json             # All OData actions (39)
    ├── entities.json            # All entities (42 types)
    └── navigations.json         # All navigations (69)
```

## Domains (17)

| Domain | Description |
|--------|-------------|
| ProdMgmt | Parts, BOMs, product structures |
| DocMgmt | Documents, attachments |
| CADDocumentMgmt | CAD documents, drawings |
| ChangeMgmt | Change notices, requests, tasks |
| SupplierMgmt | Suppliers, vendor parts |
| MfgProcMgmt | Process plans, operations |
| CEM | Customer experiences |
| BACMgmt | Baselines, configurations |
| Workflow | Work items, activities |
| Audit | Audit records, compliance |
| DataAdmin | Containers, folders |
| ServiceInfoMgmt | Service documentation |
| UDI | Unique Device Identification |
| RegMstr | Regulatory Master |
| QMS | Quality Management (CAPA/NCR) |
| PrincipalMgmt | Users, groups, roles |
| PTC | Common entities, base types |

## How to Use

1. **Find your domain** - Identify which domain your entity belongs to
2. **Read REFERENCE.md** - Check the domain's reference file for usage
3. **Check Navigations.md** - Understand relationships between entities
4. **Use entities.json** - For programmatic access to entity definitions

## File Types

| Extension | Purpose |
|-----------|---------|
| `.md` | Human-readable documentation |
| `.json` | Machine-readable definitions |
| `.xml` | Raw OData $metadata |
