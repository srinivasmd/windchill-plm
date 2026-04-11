'''
NC Domain - Nonconformance Management

Provides client for Windchill NC OData domain.
'''

from .client import NCClient, create_nc_client

__all__ = ['NCClient', 'create_nc_client']
