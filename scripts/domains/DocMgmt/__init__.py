'''
Windchill PLM DocMgmt Domain Client

Document Management domain including:
- Documents (WTDocument)
- Folders
- Document attachments and content
'''

from .client import DocMgmtClient, create_docmgmt_client

__all__ = ['DocMgmtClient', 'create_docmgmt_client']
