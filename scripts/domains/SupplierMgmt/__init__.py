'''
Windchill PLM SupplierMgmt Domain Client

Supplier Management domain including:
- Suppliers
- Manufacturer Parts
- Vendor Parts
'''

from .client import SupplierMgmtClient, create_suppliermgmt_client

__all__ = ['SupplierMgmtClient', 'create_suppliermgmt_client']
