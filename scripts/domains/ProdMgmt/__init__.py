'''
Windchill PLM ProdMgmt Domain Client

Product Management domain including:
- Parts (WTPart)
- BOM structures
- Supplier parts
- Part lifecycle management
'''

from .client import ProdMgmtClient, create_prodmgmt_client

__all__ = ['ProdMgmtClient', 'create_prodmgmt_client']
