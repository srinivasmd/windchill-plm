'''
Windchill PLM Audit Domain Client

Audit domain including:
- Audit records
- Audit resolution
'''

from .client import AuditClient, create_audit_client

__all__ = ['AuditClient', 'create_audit_client']
