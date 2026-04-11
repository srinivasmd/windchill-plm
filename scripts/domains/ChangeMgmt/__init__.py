'''
Windchill PLM ChangeMgmt Domain Client

Change Management domain including:
- Change Notices (CN)
- Change Requests (CR)
- Change Tasks
- Affected/resulting objects
'''

from .client import ChangeMgmtClient, create_changemgmt_client

__all__ = ['ChangeMgmtClient', 'create_changemgmt_client']
