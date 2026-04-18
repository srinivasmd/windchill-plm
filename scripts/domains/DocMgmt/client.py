'''
Windchill PLM DocMgmt Domain Client

Document Management domain client providing:
- Document queries and CRUD
- Folder management
- Document attachments and content
- Document versions
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


class DocMgmtClient(WindchillBaseClient):
    '''
    Client for Windchill DocMgmt OData domain.
    
    Provides document management operations.
    '''
    
    DOMAIN = 'DocMgmt'
    
    def __init__(self, **kwargs):
        '''Initialize DocMgmt client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Document Queries
    # =========================================================================
    
    def get_document_by_number(self, number: str, expand: str = None) -> dict:
        '''
        Get document by number.
        
        Args:
            number: Document number
            expand: Navigation properties to expand
        
        Returns:
            Document dictionary
        '''
        docs = self.query_entities(
            'Documents',
            filter_expr=f"number eq '{number}'",
            expand=expand,
            top=1
        )
        if not docs:
            raise ODataError(404, f"Document with number '{number}' not found")
        return docs[0]
    
    def search_documents(self, search_term: str, top: int = 50) -> List[dict]:
        '''
        Search documents by term using Windchill full-text search.

        IMPORTANT: This uses $search (full-text search) which searches across ALL fields
        (Name, Number, Description, etc.) and matches substrings anywhere.

        For field-specific filtering, use query_entities() with filter_expr instead:

        Example - Search only Name field for 'manual':
            docs = client.query_entities('Documents', filter_expr="contains(Name, 'manual')")

        Example - Search only Number field:
            docs = client.query_entities('Documents', filter_expr="contains(Number, 'DOC')")

        Args:
            search_term: Search term (full-text search across all fields)
            top: Maximum results

        Returns:
            List of matching documents
        '''
        return self.search('Documents', search_term, domain=self.DOMAIN, top=top)

    def get_document_versions(self, document_id: str) -> List[dict]:
        '''
        Get all versions of a document.
        
        Args:
            document_id: Document ID
        
        Returns:
            List of document versions
        '''
        return self.get_navigation('Documents', document_id, 'Versions', domain=self.DOMAIN)
    
    # =========================================================================
    # Document Content and Attachments
    # =========================================================================
    
    def get_document_attachments(self, document_id: str) -> List[dict]:
        '''
        Get attachments for a document.
        
        Args:
            document_id: Document ID
        
        Returns:
            List of attachments
        '''
        return self.get_navigation('Documents', document_id, 'Attachments', domain=self.DOMAIN)
    
    def get_document_primary_content(self, document_id: str) -> dict:
        '''
        Get primary content of a document.
        
        Args:
            document_id: Document ID
        
        Returns:
            Primary content information
        '''
        return self.get_navigation('Documents', document_id, 'PrimaryContent', domain=self.DOMAIN)
    
    def get_document_thumbnails(self, document_id: str) -> List[dict]:
        '''
        Get thumbnails for a document.
        
        Args:
            document_id: Document ID
        
        Returns:
            List of thumbnails
        '''
        return self.get_navigation('Documents', document_id, 'Thumbnails', domain=self.DOMAIN)
    
    # =========================================================================
    # Folder Management
    # =========================================================================
    
    def get_folders(self, container_id: str = None) -> List[dict]:
        '''
        Get folders, optionally filtered by container.
        
        Args:
            container_id: Container ID (optional)
        
        Returns:
            List of folders
        '''
        if container_id:
            return self.query_entities('Folders', filter_expr=f"containerID eq '{container_id}'")
        return self.query_entities('Folders')
    
    def get_folder_by_id(self, folder_id: str) -> dict:
        '''
        Get folder by ID.
        
        Args:
            folder_id: Folder ID
        
        Returns:
            Folder dictionary
        '''
        return self.get_entity('Folders', folder_id, domain=self.DOMAIN)
    
    def get_folder_contents(self, folder_id: str, top: int = 100) -> List[dict]:
        '''
        Get contents of a folder.
        
        Args:
            folder_id: Folder ID
            top: Maximum results
        
        Returns:
            List of folder contents
        '''
        return self.get_navigation('Folders', folder_id, 'Contents', domain=self.DOMAIN)
    
    def create_folder(self, name: str, parent_id: str = None, 
                      container_id: str = None) -> dict:
        '''
        Create a new folder.
        
        Args:
            name: Folder name
            parent_id: Parent folder ID (optional)
            container_id: Container ID
        
        Returns:
            Created folder
        '''
        folder_data = {'name': name}
        if parent_id:
            folder_data['parentFolder'] = {'ID': parent_id}
        if container_id:
            folder_data['container'] = {'ID': container_id}
        
        return self.create_entity('Folders', folder_data, domain=self.DOMAIN)
    
    def update_folder(self, folder_id: str, folder_data: dict) -> dict:
        '''
        Update folder properties.
        
        Args:
            folder_id: Folder ID
            folder_data: Updated properties
        
        Returns:
            Updated folder
        '''
        return self.update_entity('Folders', folder_id, folder_data, domain=self.DOMAIN)
    
    def delete_folder(self, folder_id: str) -> bool:
        '''
        Delete a folder.
        
        Args:
            folder_id: Folder ID
        
        Returns:
            True if deleted
        '''
        return self.delete_entity('Folders', folder_id, domain=self.DOMAIN)


def create_docmgmt_client(config_path: str = None, base_url: str = None,
                           username: str = None, password: str = None) -> DocMgmtClient:
    '''
    Factory function to create a DocMgmt client.
    
    Args:
        config_path: Path to config.json
        base_url: Windchill server URL
        username: Username
        password: Password
    
    Returns:
        DocMgmtClient instance
    '''
    return DocMgmtClient(
        config_path=config_path,
        base_url=base_url,
        username=username,
        password=password
    )


def main():
    '''CLI entry point for DocMgmt client.'''
    import argparse
    
    parser = argparse.ArgumentParser(description='Windchill DocMgmt Client')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--doc-number', help='Get document by number')
    parser.add_argument('--doc-id', help='Get document by ID')
    parser.add_argument('--search', help='Search documents')
    parser.add_argument('--attachments', help='Get attachments for document ID')
    parser.add_argument('--folders', action='store_true', help='List folders')
    parser.add_argument('--folder-id', help='Get folder by ID')
    parser.add_argument('--folder-contents', help='Get folder contents')
    
    args = parser.parse_args()
    
    client = create_docmgmt_client(config_path=args.config)
    
    if args.doc_number:
        doc = client.get_document_by_number(args.doc_number)
        print(json.dumps(doc, indent=2))
    
    if args.doc_id:
        doc = client.get_entity('Documents', args.doc_id)
        print(json.dumps(doc, indent=2))
    
    if args.search:
        docs = client.search_documents(args.search)
        print(json.dumps(docs, indent=2))
    
    if args.attachments:
        attachments = client.get_document_attachments(args.attachments)
        print(json.dumps(attachments, indent=2))
    
    if args.folders:
        folders = client.get_folders()
        print(json.dumps(folders, indent=2))
    
    if args.folder_id:
        folder = client.get_folder_by_id(args.folder_id)
        print(json.dumps(folder, indent=2))
    
    if args.folder_contents:
        contents = client.get_folder_contents(args.folder_contents)
        print(json.dumps(contents, indent=2))


if __name__ == '__main__':
    main()
