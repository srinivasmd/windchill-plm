'''
Windchill PLM ServiceInfoMgmt Domain Client

Service Information Management domain including:
- Service documents
- Service bulletins
- Maintenance information
'''

from .client import ServiceInfoMgmtClient, create_serviceinfomgmt_client

__all__ = ['ServiceInfoMgmtClient', 'create_serviceinfomgmt_client']
