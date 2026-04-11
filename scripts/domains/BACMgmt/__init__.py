'''
Windchill PLM BACMgmt Domain Client

Baseline and Configuration Management domain including:
- Baselines
- Associations
- Managed Baselines
'''

from .client import BACMgmtClient, create_bacmgmt_client

__all__ = ['BACMgmtClient', 'create_bacmgmt_client']
