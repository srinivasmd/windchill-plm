'''
Windchill PLM QMS Domain Client

Quality Management System domain including:
- CAPA (Corrective and Preventive Actions)
- NCR (Non-Conformance Reports)
- Quality Actions
- Audits
'''

from .client import QMSClient, create_qms_client

__all__ = ['QMSClient', 'create_qms_client']
