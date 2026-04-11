'''
Windchill PLM CADDocumentMgmt Domain Client

CAD Document Management domain including:
- CAD Documents
- Drawings
- CAD structure and references
'''

from .client import CADDocumentMgmtClient, create_cad_documentmgmt_client

__all__ = ['CADDocumentMgmtClient', 'create_cad_documentmgmt_client']
