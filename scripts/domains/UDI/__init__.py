'''
Windchill PLM UDI Domain Client

Unique Device Identification domain including:
- UDI compliance
- Device identification records
- Label management
'''

from .client import UDIClient, create_udi_client

__all__ = ['UDIClient', 'create_udi_client']
