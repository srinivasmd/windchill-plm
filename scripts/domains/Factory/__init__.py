'''
Windchill PLM Factory Domain Client

Factory management domain client for standard operations,
procedures, control characteristics, and resources.
'''

from .client import FactoryClient, create_factory_client

__all__ = ['FactoryClient', 'create_factory_client']
