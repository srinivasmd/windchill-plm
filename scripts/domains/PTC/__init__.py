'''
Windchill PLM PTC Common Domain Client

PTC namespace provides shared entities used across all Windchill OData domains:
- Content management (ApplicationData, ContentItem)
- User references (UserRef)
- Cross-domain actions (DownloadContentAsZip)
- Base types (WindchillEntity, ObjectReferenceable)
'''

from .client import PTCClient, create_ptc_client

__all__ = ['PTCClient', 'create_ptc_client']
