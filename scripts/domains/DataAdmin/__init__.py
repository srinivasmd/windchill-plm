'''
Windchill PLM DataAdmin Domain Client

Data Administration domain including:
- Containers (Products, Projects, Libraries)
- Organizations
- Sites
'''

from .client import DataAdminClient, create_dataadmin_client

__all__ = ['DataAdminClient', 'create_dataadmin_client']
