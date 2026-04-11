'''
Windchill PLM RegMstr Domain Client

Regulatory Master domain including:
- Regulatory registrations
- Registrations management
- Compliance tracking
'''

from .client import RegMstrClient, create_regmstr_client

__all__ = ['RegMstrClient', 'create_regmstr_client']
