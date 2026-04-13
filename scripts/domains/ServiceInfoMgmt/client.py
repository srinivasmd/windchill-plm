'''
Windchill PLM ServiceInfoMgmt Domain Client

Service Information Management domain client providing:
- Service document queries
- Service bulletin management
- Maintenance information tracking
'''
# Copyright 2025 Windchill PLM Client Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class ServiceInfoMgmtClient(WindchillBaseClient):
    '''
    Client for Windchill ServiceInfoMgmt OData domain.
    
    Provides service information management operations.
    '''
    
    DOMAIN = 'ServiceInfoMgmt'
    
    def __init__(self, **kwargs):
        '''Initialize ServiceInfoMgmt client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Service Document Queries
    # =========================================================================
    
    def get_service_documents(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get service documents.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of service documents
        '''
        return self.query_entities('ServiceDocuments', filter_expr=filter_expr, top=top)
    
    def get_service_document_by_id(self, document_id: str, expand: str = None) -> dict:
        '''
        Get service document by ID.
        
        Args:
            document_id: Service document ID
            expand: Navigation properties to expand
        
        Returns:
            Service document dictionary
        '''
        return self.get_entity('ServiceDocuments', document_id, domain=self.DOMAIN, expand=expand)
    
    def get_service_document_by_number(self, number: str, expand: str = None) -> dict:
        '''
        Get service document by number.
        
        Args:
            number: Service document number
            expand: Navigation properties to expand
        
        Returns:
            Service document dictionary
        '''
        docs = self.query_entities(
            'ServiceDocuments',
            filter_expr=f"number eq '{number}'",
            expand=expand,
            top=1
        )
        if not docs:
            raise ODataError(404, f"Service document with number '{number}' not found")
        return docs[0]
    
    # =========================================================================
    # Service Bulletins
    # =========================================================================
    
    def get_service_bulletins(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get service bulletins.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of service bulletins
        '''
        return self.query_entities('ServiceBulletins', filter_expr=filter_expr, top=top)
    
    def get_service_bulletin_by_id(self, bulletin_id: str) -> dict:
        '''
        Get service bulletin by ID.
        
        Args:
            bulletin_id: Service bulletin ID
        
        Returns:
            Service bulletin dictionary
        '''
        return self.get_entity('ServiceBulletins', bulletin_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Maintenance Information
    # =========================================================================
    
    def get_maintenance_info(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get maintenance information records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of maintenance information
        '''
        return self.query_entities('MaintenanceInfo', filter_expr=filter_expr, top=top)
    
    # =========================================================================
    # Navigation Properties
    # =========================================================================
    
    def get_service_document_attachments(self, document_id: str) -> List[dict]:
        '''
        Get attachments for a service document.
        
        Args:
            document_id: Service document ID
        
        Returns:
            List of attachments
        '''
        return self.get_navigation('ServiceDocuments', document_id, 'Attachments', domain=self.DOMAIN)
    
    def get_service_document_parts(self, document_id: str) -> List[dict]:
        '''
        Get parts associated with a service document.
        
        Args:
            document_id: Service document ID
        
        Returns:
            List of parts
        '''
        return self.get_navigation('ServiceDocuments', document_id, 'Parts', domain=self.DOMAIN)
    
    # =========================================================================
    # State Management
    # =========================================================================
    
    def set_service_document_state(self, document_id: str, state: str,
                                    comment: str = None) -> dict:
        '''
        Set lifecycle state of a service document.
        
        Args:
            document_id: Service document ID
            state: Target state
            comment: State change comment
        
        Returns:
            State change result
        '''
        params = {'State': state}
        if comment:
            params['Comment'] = comment
        
        return self.invoke_action(
            'SetState',
            parameters=params,
            entity_id=document_id,
            entity_type='ServiceDocument'
        )


def create_serviceinfomgmt_client(config_path: str = None, base_url: str = None,
                                    username: str = None, password: str = None) -> ServiceInfoMgmtClient:
    '''
    Factory function to create a ServiceInfoMgmt client.
    
    Args:
        config_path: Path to config.json
        base_url: Windchill server URL
        username: Username
        password: Password
    
    Returns:
        ServiceInfoMgmtClient instance
    '''
    return ServiceInfoMgmtClient(
        config_path=config_path,
        base_url=base_url,
        username=username,
        password=password
    )


def main():
    '''CLI entry point for ServiceInfoMgmt client.'''
    import argparse
    
    parser = argparse.ArgumentParser(description='Windchill ServiceInfoMgmt Client')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--documents', action='store_true', help='List service documents')
    parser.add_argument('--document-id', help='Get service document by ID')
    parser.add_argument('--document-number', help='Get service document by number')
    parser.add_argument('--bulletins', action='store_true', help='List service bulletins')
    parser.add_argument('--attachments', help='Get attachments for document ID')
    
    args = parser.parse_args()
    
    client = create_serviceinfomgmt_client(config_path=args.config)
    
    if args.documents:
        result = client.get_service_documents()
        print(json.dumps(result, indent=2))
    
    if args.document_id:
        result = client.get_service_document_by_id(args.document_id)
        print(json.dumps(result, indent=2))
    
    if args.document_number:
        result = client.get_service_document_by_number(args.document_number)
        print(json.dumps(result, indent=2))
    
    if args.bulletins:
        result = client.get_service_bulletins()
        print(json.dumps(result, indent=2))
    
    if args.attachments:
        result = client.get_service_document_attachments(args.attachments)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
