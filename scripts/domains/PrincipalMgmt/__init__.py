'''
Windchill PLM PrincipalMgmt Domain Client

Principal Management domain including:
- Users
- Groups
- Roles
- Organizations
'''

from .client import PrincipalMgmtClient, create_principalmgmt_client

__all__ = ['PrincipalMgmtClient', 'create_principalmgmt_client']
