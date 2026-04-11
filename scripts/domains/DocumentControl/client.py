'''
Windchill PLM DocumentControl Domain Client

Document Control domain client providing:
- Control Document queries and management
- Training Record queries and management
- Document lifecycle operations
'''

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class DocumentControlClient(WindchillBaseClient):
    '''
    Client for Windchill DocumentControl OData domain.
    
    Provides document control operations for controlled documents
    and training records.
    '''
    
    DOMAIN = 'DocumentControl'
    
    def __init__(self, **kwargs):
        '''Initialize DocumentControl client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Control Document Queries
    # =========================================================================
    
    def get_control_documents(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Control Document records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Control Document records
        '''
        return self.query_entities('ControlDocuments', filter_expr=filter_expr, top=top)
    
    def get_control_document_by_id(self, doc_id: str, expand: List[str] = None) -> dict:
        '''
        Get Control Document by ID.
        
        Args:
            doc_id: Document ID (OID format)
            expand: Navigation properties to expand
        
        Returns:
            Control Document dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('ControlDocuments', doc_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_control_document_by_number(self, number: str) -> dict:
        '''
        Get Control Document by number.
        
        Args:
            number: Document number
        
        Returns:
            Control Document dictionary
        '''
        docs = self.query_entities(
            'ControlDocuments',
            filter_expr=f"Number eq '{number}'",
            top=1
        )
        return docs[0] if docs else None
    
    def get_control_documents_by_state(self, state: str, top: int = 50) -> List[dict]:
        '''
        Get Control Documents by lifecycle state.
        
        Args:
            state: Lifecycle state value
            top: Maximum results
        
        Returns:
            List of Control Documents in specified state
        '''
        return self.query_entities(
            'ControlDocuments',
            filter_expr=f"State/Value eq '{state}'",
            top=top
        )
    
    def search_control_documents(self, search_term: str, top: int = 20) -> List[dict]:
        '''
        Search Control Documents by name or number.
        
        Args:
            search_term: Search string
            top: Maximum results
        
        Returns:
            List of matching Control Documents
        '''
        return self.query_entities(
            'ControlDocuments',
            filter_expr=f"contains(Name, '{search_term}') or contains(Number, '{search_term}')",
            top=top
        )
    
    # =========================================================================
    # Control Document Navigation Properties
    # =========================================================================
    
    def get_document_creator(self, doc_id: str) -> dict:
        '''
        Get Control Document creator.
        
        Args:
            doc_id: Document ID
        
        Returns:
            Creator (User) dictionary
        '''
        return self.get_navigation('ControlDocuments', doc_id, 'Creator', domain=self.DOMAIN)
    
    def get_document_modifier(self, doc_id: str) -> dict:
        '''
        Get Control Document modifier.
        
        Args:
            doc_id: Document ID
        
        Returns:
            Modifier (User) dictionary
        '''
        return self.get_navigation('ControlDocuments', doc_id, 'Modifier', domain=self.DOMAIN)
    
    def get_document_folder(self, doc_id: str) -> dict:
        '''
        Get Control Document folder.
        
        Args:
            doc_id: Document ID
        
        Returns:
            Folder dictionary
        '''
        return self.get_navigation('ControlDocuments', doc_id, 'Folder', domain=self.DOMAIN)
    
    def get_document_master(self, doc_id: str) -> dict:
        '''
        Get Control Document master.
        
        Args:
            doc_id: Document ID
        
        Returns:
            Master dictionary
        '''
        return self.get_navigation('ControlDocuments', doc_id, 'Master', domain=self.DOMAIN)
    
    def get_document_training_records(self, doc_id: str, top: int = 50) -> List[dict]:
        '''
        Get Training Records for a Control Document.
        
        Args:
            doc_id: Document ID
            top: Maximum results
        
        Returns:
            List of Training Records
        '''
        return self.get_navigation('ControlDocuments', doc_id, 'TrainingRecords', domain=self.DOMAIN, top=top)
    
    def get_document_attachments(self, doc_id: str, top: int = 50) -> List[dict]:
        '''
        Get Control Document attachments.
        
        Args:
            doc_id: Document ID
            top: Maximum results
        
        Returns:
            List of attachments
        '''
        return self.get_navigation('ControlDocuments', doc_id, 'Attachments', domain=self.DOMAIN, top=top)
    
    # =========================================================================
    # Training Record Queries
    # =========================================================================
    
    def get_training_records(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Training Record entries.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Training Records
        '''
        return self.query_entities('TrainingRecords', filter_expr=filter_expr, top=top)
    
    def get_training_record_by_id(self, record_id: str, expand: List[str] = None) -> dict:
        '''
        Get Training Record by ID.
        
        Args:
            record_id: Training Record ID
            expand: Navigation properties to expand
        
        Returns:
            Training Record dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('TrainingRecords', record_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_training_records_by_user(self, user_id: str, top: int = 50) -> List[dict]:
        '''
        Get Training Records for a specific user.
        
        Args:
            user_id: User ID
            top: Maximum results
        
        Returns:
            List of Training Records
        '''
        return self.query_entities(
            'TrainingRecords',
            filter_expr=f"Trainee/ID eq '{user_id}'",
            top=top
        )
    
    def get_training_records_by_status(self, status: str, top: int = 50) -> List[dict]:
        '''
        Get Training Records by status.
        
        Args:
            status: Training status value
            top: Maximum results
        
        Returns:
            List of Training Records
        '''
        return self.query_entities(
            'TrainingRecords',
            filter_expr=f"Status/Value eq '{status}'",
            top=top
        )
    
    # =========================================================================
    # Training Record Navigation Properties
    # =========================================================================
    
    def get_training_record_trainee(self, record_id: str) -> dict:
        '''
        Get Training Record trainee.
        
        Args:
            record_id: Training Record ID
        
        Returns:
            Trainee (User) dictionary
        '''
        return self.get_navigation('TrainingRecords', record_id, 'Trainee', domain=self.DOMAIN)
    
    def get_training_record_document(self, record_id: str) -> dict:
        '''
        Get Control Document for a Training Record.
        
        Args:
            record_id: Training Record ID
        
        Returns:
            Control Document dictionary
        '''
        return self.get_navigation('TrainingRecords', record_id, 'ControlDocument', domain=self.DOMAIN)
    
    # =========================================================================
    # State Management Actions
    # =========================================================================
    
    def set_document_state(self, doc_id: str, state: str) -> dict:
        '''
        Set Control Document lifecycle state.
        
        Args:
            doc_id: Document ID
            state: Target state value
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/ControlDocuments('{doc_id}')/PTC.DocumentControl.SetState"
        
        payload = {"State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def set_training_records_state_bulk(self, record_ids: List[str], state: str) -> dict:
        '''
        Set lifecycle state for multiple Training Records.
        
        Args:
            record_ids: List of Training Record IDs
            state: Target state value
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/TrainingRecords/PTC.DocumentControl.SetStateTrainingRecords"
        
        payload = {
            "TrainingRecords": record_ids,
            "State": state
        }
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}


def create_document_control_client(config_path: str = None, **kwargs) -> DocumentControlClient:
    '''
    Factory function to create DocumentControl client.
    
    Args:
        config_path: Path to config.json
        **kwargs: Additional client options
    
    Returns:
        DocumentControlClient instance
    '''
    if config_path:
        with open(config_path, 'r') as f:
            config = json.load(f)
        kwargs.update(config)
    
    return DocumentControlClient(**kwargs)
