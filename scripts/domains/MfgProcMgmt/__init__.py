'''
Windchill PLM MfgProcMgmt Domain Client

Manufacturing Process Management domain including:
- Process Plans
- Operations
- Work definitions
'''

from .client import MfgProcMgmtClient, create_mfgprocmgmt_client

__all__ = ['MfgProcMgmtClient', 'create_mfgprocmgmt_client']
