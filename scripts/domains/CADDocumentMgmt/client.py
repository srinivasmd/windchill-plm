'''
Windchill PLM CADDocumentMgmt Domain Client

CAD Document Management domain client providing:
- CAD document queries
- CAD structure navigation
- Drawing and reference management
- Part associations
'''

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class CADDocumentMgmtClient(WindchillBaseClient):
    '''
    Client for Windchill CADDocumentMgmt OData domain.
    
    Provides CAD document management operations.
    '''
    
    DOMAIN = 'CADDocumentMgmt'
    
    def __init__(self, **kwargs):
        '''Initialize CADDocumentMgmt client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # CAD Document Queries
    # =========================================================================
    
    def get_cad_document_by_number(self, number: str, expand: str = None) -> dict:
        '''
        Get CAD document by number.
        
        Args:
            number: CAD document number
            expand: Navigation properties to expand
        
        Returns:
            CAD document dictionary
        '''
        docs = self.query_entities(
            'CADDocuments',
            filter_expr=f"number eq '{number}'",
            expand=expand,
            top=1
        )
        if not docs:
            raise ODataError(404, f"CAD document with number '{number}' not found")
        return docs[0]
    
    def query_cad_documents(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Query CAD documents.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of CAD documents
        '''
        return self.query_entities('CADDocuments', filter_expr=filter_expr, top=top)
    
    # =========================================================================
    # CAD Structure Navigation
    # =========================================================================
    
    def get_cad_document_structure(self, document_id: str) -> List[dict]:
        '''
        Get CAD document structure (assembly structure).
        
        Args:
            document_id: CAD document ID
        
        Returns:
            List of structure elements
        '''
        return self.get_navigation('CADDocuments', document_id, 'Structure', domain=self.DOMAIN)
    
    def get_cad_document_uses(self, document_id: str) -> List[dict]:
        '''
        Get CAD document uses (where used in assemblies).
        
        Args:
            document_id: CAD document ID
        
        Returns:
            List of usages
        '''
        return self.get_navigation('CADDocuments', document_id, 'Uses', domain=self.DOMAIN)
    
    def get_cad_document_references(self, document_id: str) -> List[dict]:
        '''
        Get CAD document references (referenced documents).
        
        Args:
            document_id: CAD document ID
        
        Returns:
            List of referenced documents
        '''
        return self.get_navigation('CADDocuments', document_id, 'References', domain=self.DOMAIN)
    
    def get_cad_document_related_parts(self, document_id: str) -> List[dict]:
        '''
        Get parts associated with a CAD document.
        
        Args:
            document_id: CAD document ID
        
        Returns:
            List of related parts
        '''
        return self.get_navigation('CADDocuments', document_id, 'RelatedParts', domain=self.DOMAIN)
    
    def get_cad_document_drawings(self, document_id: str) -> List[dict]:
        '''
        Get drawings associated with a CAD document.
        
        Args:
            document_id: CAD document ID
        
        Returns:
            List of drawings
        '''
        return self.get_navigation('CADDocuments', document_id, 'Drawings', domain=self.DOMAIN)


def create_cad_documentmgmt_client(config_path: str = None, base_url: str = None,
                                    username: str = None, password: str = None) -> CADDocumentMgmtClient:
    '''
    Factory function to create a CADDocumentMgmt client.
    
    Args:
        config_path: Path to config.json
        base_url: Windchill server URL
        username: Username
        password: Password
    
    Returns:
        CADDocumentMgmtClient instance
    '''
    return CADDocumentMgmtClient(
        config_path=config_path,
        base_url=base_url,
        username=username,
        password=password
    )


def main():
    '''CLI entry point for CADDocumentMgmt client.'''
    import argparse
    
    parser = argparse.ArgumentParser(description='Windchill CADDocumentMgmt Client')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--doc-number', help='Get CAD document by number')
    parser.add_argument('--doc-id', help='Get CAD document by ID')
    parser.add_argument('--structure', help='Get structure for document ID')
    parser.add_argument('--uses', help='Get uses for document ID')
    parser.add_argument('--references', help='Get references for document ID')
    parser.add_argument('--parts', help='Get related parts for document ID')
    parser.add_argument('--drawings', help='Get drawings for document ID')
    
    args = parser.parse_args()
    
    client = create_cad_documentmgmt_client(config_path=args.config)
    
    if args.doc_number:
        doc = client.get_cad_document_by_number(args.doc_number)
        print(json.dumps(doc, indent=2))
    
    if args.doc_id:
        doc = client.get_entity('CADDocuments', args.doc_id)
        print(json.dumps(doc, indent=2))
    
    if args.structure:
        result = client.get_cad_document_structure(args.structure)
        print(json.dumps(result, indent=2))
    
    if args.uses:
        result = client.get_cad_document_uses(args.uses)
        print(json.dumps(result, indent=2))
    
    if args.references:
        result = client.get_cad_document_references(args.references)
        print(json.dumps(result, indent=2))
    
    if args.parts:
        result = client.get_cad_document_related_parts(args.parts)
        print(json.dumps(result, indent=2))
    
    if args.drawings:
        result = client.get_cad_document_drawings(args.drawings)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
