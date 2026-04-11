'''
Windchill PLM CEM Domain Client

Customer Experience Management domain including:
- Customer Experiences
- Attachments
- State management
'''

from .client import CEMClient, create_cem_client

__all__ = ['CEMClient', 'create_cem_client']
