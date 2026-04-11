'''
Windchill PLM DynamicDocMgmt Domain Client

Dynamic Document Management domain client providing:
- Dynamic Document queries and management
- Document versioning and lifecycle
- File upload operations
- Burst configuration management
'''

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class DynamicDocMgmtClient(WindchillBaseClient):
    '''
    Client for Windchill DynamicDocMgmt OData domain.
    
    Provides dynamic document management operations.
    '''
    
    DOMAIN = 'DynamicDocMgmt'
    
    def __init__(self, **kwargs):
        '''Initialize DynamicDocMgmt client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Dynamic Document Queries
    # =========================================================================
    
    def get_dynamic_documents(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Dynamic Document records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Dynamic Documents
        '''
        return self.query_entities('DynamicDocuments', filter_expr=filter_expr, top=top)
    
    def get_dynamic_document_by_id(self, doc_id: str, expand: List[str] = None) -> dict:
        '''
        Get Dynamic Document by ID.
        
        Args:
            doc_id: Document ID (OID format)
            expand: Navigation properties to expand
        
        Returns:
            Dynamic Document dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('DynamicDocuments', doc_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_dynamic_document_by_number(self, number: str) -> dict:
        '''
        Get Dynamic Document by number.
        
        Args:
            number: Document number
        
        Returns:
            Dynamic Document dictionary
        '''
        docs = self.query_entities(
            'DynamicDocuments',
            filter_expr=f"Number eq '{number}'",
            top=1
        )
        return docs[0] if docs else None
    
    def get_dynamic_documents_by_state(self, state: str, top: int = 50) -> List[dict]:
        '''
        Get Dynamic Documents by lifecycle state.
        
        Args:
            state: Lifecycle state value
            top: Maximum results
        
        Returns:
            List of Dynamic Documents in specified state
        '''
        return self.query_entities(
            'DynamicDocuments',
            filter_expr=f"State/Value eq '{state}'",
            top=top
        )
    
    def search_dynamic_documents(self, search_term: str, top: int = 20) -> List[dict]:
        '''
        Search Dynamic Documents by name or number.
        
        Args:
            search_term: Search string
            top: Maximum results
        
        Returns:
            List of matching Dynamic Documents
        '''
        return self.query_entities(
            'DynamicDocuments',
            filter_expr=f"contains(Name, '{search_term}') or contains(Number, '{search_term}')",
            top=top
        )
    
    # =========================================================================
    # Dynamic Document Navigation Properties
    # =========================================================================
    
    def get_document_creator(self, doc_id: str) -> dict:
        '''Get Dynamic Document creator.'''
        return self.get_navigation('DynamicDocuments', doc_id, 'Creator', domain=self.DOMAIN)
    
    def get_document_modifier(self, doc_id: str) -> dict:
        '''Get Dynamic Document modifier.'''
        return self.get_navigation('DynamicDocuments', doc_id, 'Modifier', domain=self.DOMAIN)
    
    def get_document_folder(self, doc_id: str) -> dict:
        '''Get Dynamic Document folder.'''
        return self.get_navigation('DynamicDocuments', doc_id, 'Folder', domain=self.DOMAIN)
    
    def get_document_master(self, doc_id: str) -> dict:
        '''Get Dynamic Document master.'''
        return self.get_navigation('DynamicDocuments', doc_id, 'Master', domain=self.DOMAIN)
    
    def get_document_versions(self, doc_id: str, top: int = 50) -> List[dict]:
        '''Get all versions of a Dynamic Document.'''
        return self.get_navigation('DynamicDocuments', doc_id, 'Versions', domain=self.DOMAIN, top=top)
    
    def get_document_attachments(self, doc_id: str, top: int = 50) -> List[dict]:
        '''Get Dynamic Document attachments.'''
        return self.get_navigation('DynamicDocuments', doc_id, 'Attachments', domain=self.DOMAIN, top=top)
    
    def get_document_members(self, doc_id: str, top: int = 50) -> List[dict]:
        '''Get Dynamic Document members.'''
        return self.get_navigation('DynamicDocuments', doc_id, 'Members', domain=self.DOMAIN, top=top)
    
    def get_document_references(self, doc_id: str, top: int = 50) -> List[dict]:
        '''Get Dynamic Document references.'''
        return self.get_navigation('DynamicDocuments', doc_id, 'References', domain=self.DOMAIN, top=top)
    
    def get_document_thumbnails(self, doc_id: str, top: int = 50) -> List[dict]:
        '''Get Dynamic Document thumbnails.'''
        return self.get_navigation('DynamicDocuments', doc_id, 'Thumbnails', domain=self.DOMAIN, top=top)
    
    # =========================================================================
    # Burst Configuration Queries
    # =========================================================================
    
    def get_burst_configurations(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Burst Configuration records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Burst Configurations
        '''
        return self.query_entities('BurstConfigurations', filter_expr=filter_expr, top=top)
    
    def get_burst_configuration_by_id(self, config_id: str) -> dict:
        '''
        Get Burst Configuration by ID.
        
        Args:
            config_id: Configuration ID
        
        Returns:
            Burst Configuration dictionary
        '''
        return self.get_entity('BurstConfigurations', config_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Note Queries
    # =========================================================================
    
    def get_notes(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Note records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Notes
        '''
        return self.query_entities('Notes', filter_expr=filter_expr, top=top)
    
    def get_note_by_id(self, note_id: str) -> dict:
        '''
        Get Note by ID.
        
        Args:
            note_id: Note ID
        
        Returns:
            Note dictionary
        '''
        return self.get_entity('Notes', note_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Document Member Operations
    # =========================================================================
    
    def get_document_member_by_id(self, member_id: str) -> dict:
        '''Get Dynamic Document Member by ID.'''
        return self.get_entity('DynamicDocumentMembers', member_id, domain=self.DOMAIN)
    
    def get_member_document(self, member_id: str) -> dict:
        '''Get the Dynamic Document for a member.'''
        return self.get_navigation('DynamicDocumentMembers', member_id, 'DynamicDocument', domain=self.DOMAIN)
    
    # =========================================================================
    # Document Reference Operations
    # =========================================================================
    
    def get_document_reference_by_id(self, ref_id: str) -> dict:
        '''Get Dynamic Document Reference by ID.'''
        return self.get_entity('DynamicDocumentReferences', ref_id, domain=self.DOMAIN)
    
    def get_reference_document(self, ref_id: str) -> dict:
        '''Get the referenced Dynamic Document.'''
        return self.get_navigation('DynamicDocumentReferences', ref_id, 'DynamicDocument', domain=self.DOMAIN)
    
    # =========================================================================
    # Lifecycle State Actions
    # =========================================================================
    
    def set_document_state(self, doc_id: str, state: str) -> dict:
        '''
        Set Dynamic Document lifecycle state.
        
        Args:
            doc_id: Document ID
            state: Target state value
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/DynamicDocuments('{doc_id}')/PTC.DynamicDocMgmt.SetState"
        
        payload = {"State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def set_documents_state_bulk(self, doc_ids: List[str], state: str) -> dict:
        '''
        Set lifecycle state for multiple Dynamic Documents.
        
        Args:
            doc_ids: List of Document IDs
            state: Target state value
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/DynamicDocuments/PTC.DynamicDocMgmt.SetStateDynamicDocuments"
        
        payload = {
            "DynamicDocuments": doc_ids,
            "State": state
        }
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    # =========================================================================
    # Version Control Actions
    # =========================================================================
    
    def revise_document(self, doc_id: str, version_id: str = None) -> dict:
        '''
        Revise a Dynamic Document.
        
        Args:
            doc_id: Document ID
            version_id: Optional version ID
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/DynamicDocuments('{doc_id}')/PTC.DynamicDocMgmt.Revise"
        
        payload = {"VersionId": version_id} if version_id else {}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def check_out_document(self, doc_id: str) -> dict:
        '''
        Check out a Dynamic Document.
        
        Args:
            doc_id: Document ID
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/DynamicDocuments('{doc_id}')/PTC.DynamicDocMgmt.CheckOut"
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def undo_check_out_document(self, doc_id: str) -> dict:
        '''
        Undo check out for a Dynamic Document.
        
        Args:
            doc_id: Document ID
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/DynamicDocuments('{doc_id}')/PTC.DynamicDocMgmt.UndoCheckOut"
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def check_in_document(self, doc_id: str, check_in_note: str = None, keep_checked_out: bool = False) -> dict:
        '''
        Check in a Dynamic Document.
        
        Args:
            doc_id: Document ID
            check_in_note: Optional check-in note
            keep_checked_out: Whether to keep document checked out
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/DynamicDocuments('{doc_id}')/PTC.DynamicDocMgmt.CheckIn"
        
        payload = {
            "CheckInNote": check_in_note or "",
            "KeepCheckedOut": keep_checked_out
        }
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    # =========================================================================
    # File Upload Actions
    # =========================================================================
    
    def upload_stage1(self, doc_id: str, no_of_files: int, delegate_name: str = None) -> dict:
        '''
        Stage 1 of file upload process.
        
        Args:
            doc_id: Document ID
            no_of_files: Number of files to upload
            delegate_name: Optional delegate name
        
        Returns:
            Upload session info
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/DynamicDocuments('{doc_id}')/PTC.DynamicDocMgmt.UploadStage1Action"
        
        payload = {
            "NoOfFiles": no_of_files,
            "DelegateName": delegate_name or ""
        }
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def upload_stage3(self, doc_id: str, content_info: dict) -> dict:
        '''
        Stage 3 of file upload process - finalizes the upload.
        
        Args:
            doc_id: Document ID
            content_info: Content metadata
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/DynamicDocuments('{doc_id}')/PTC.DynamicDocMgmt.UploadStage3Action"
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json={"ContentInfo": content_info}, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    # =========================================================================
    # Create and Update Actions
    # =========================================================================
    
    def create_dynamic_documents(self, documents: List[dict]) -> dict:
        '''
        Create multiple Dynamic Documents.
        
        Args:
            documents: List of document definitions
        
        Returns:
            Creation result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/DynamicDocuments/PTC.DynamicDocMgmt.CreateDynamicDocuments"
        
        payload = {"DynamicDocuments": documents}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def update_dynamic_documents(self, documents: List[dict]) -> dict:
        '''
        Update multiple Dynamic Documents.
        
        Args:
            documents: List of document updates
        
        Returns:
            Update result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/DynamicDocuments/PTC.DynamicDocMgmt.UpdateDynamicDocuments"
        
        payload = {"DynamicDocuments": documents}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def update_common_properties(self, doc_id: str, updates: dict) -> dict:
        '''
        Update common properties of a Dynamic Document.
        
        Args:
            doc_id: Document ID
            updates: Property updates
        
        Returns:
            Update result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/DynamicDocuments('{doc_id}')/PTC.DynamicDocMgmt.UpdateCommonProperties"
        
        payload = {"Updates": updates}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def edit_security_labels(self, doc_ids: List[str]) -> dict:
        '''
        Edit security labels for Dynamic Documents.
        
        Args:
            doc_ids: List of Document IDs
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/DynamicDocuments/PTC.DynamicDocMgmt.EditDynamicDocumentsSecurityLabels"
        
        payload = {"DynamicDocuments": doc_ids}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}


def create_dynamic_doc_mgmt_client(config_path: str = None, **kwargs) -> DynamicDocMgmtClient:
    '''
    Factory function to create DynamicDocMgmt client.
    
    Args:
        config_path: Path to config.json
        **kwargs: Additional client options
    
    Returns:
        DynamicDocMgmtClient instance
    '''
    if config_path:
        with open(config_path, 'r') as f:
            config = json.load(f)
        kwargs.update(config)
    
    return DynamicDocMgmtClient(**kwargs)
