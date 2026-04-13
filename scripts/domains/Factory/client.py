'''
Windchill PLM Factory Domain Client

Factory management domain client providing:
- Standard Operations and Procedures management
- Standard Control Characteristics (SCC)
- Resources and Resource Usage tracking
- Document management within factory context
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


class FactoryClient(WindchillBaseClient):
    '''
    Client for Windchill Factory OData domain.
    
    Provides factory management operations including standard operations,
    procedures, control characteristics, and resources.
    '''
    
    DOMAIN = 'Factory'
    
    def __init__(self, **kwargs):
        '''Initialize Factory client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Document Queries
    # =========================================================================
    
    def get_documents(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Document records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Documents
        '''
        return self.query_entities('Documents', filter_expr=filter_expr, top=top)
    
    def get_document_by_id(self, doc_id: str, expand: List[str] = None) -> dict:
        '''
        Get Document by ID.
        
        Args:
            doc_id: Document ID (OID format)
            expand: Navigation properties to expand
        
        Returns:
            Document dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('Documents', doc_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_document_by_number(self, number: str) -> dict:
        '''
        Get Document by number.
        
        Args:
            number: Document number
        
        Returns:
            Document dictionary
        '''
        docs = self.query_entities(
            'Documents',
            filter_expr=f"Number eq '{number}'",
            top=1
        )
        return docs[0] if docs else None
    
    def get_documents_by_state(self, state: str, top: int = 50) -> List[dict]:
        '''
        Get Documents by lifecycle state.
        
        Args:
            state: Lifecycle state value
            top: Maximum results
        
        Returns:
            List of Documents in specified state
        '''
        return self.query_entities(
            'Documents',
            filter_expr=f"State/Value eq '{state}'",
            top=top
        )
    
    # =========================================================================
    # Document Navigation Properties
    # =========================================================================
    
    def get_document_folder(self, doc_id: str) -> dict:
        '''Get Document folder.'''
        return self.get_navigation('Documents', doc_id, 'Folder', domain=self.DOMAIN)
    
    def get_document_creator(self, doc_id: str) -> dict:
        '''Get Document creator.'''
        return self.get_navigation('Documents', doc_id, 'Creator', domain=self.DOMAIN)
    
    def get_document_modifier(self, doc_id: str) -> dict:
        '''Get Document modifier.'''
        return self.get_navigation('Documents', doc_id, 'Modifier', domain=self.DOMAIN)
    
    def get_document_master(self, doc_id: str) -> dict:
        '''Get Document master.'''
        return self.get_navigation('Documents', doc_id, 'Master', domain=self.DOMAIN)
    
    def get_document_versions(self, doc_id: str, top: int = 50) -> List[dict]:
        '''Get all versions of a Document.'''
        return self.get_navigation('Documents', doc_id, 'Versions', domain=self.DOMAIN, top=top)
    
    # =========================================================================
    # Standard Operation Queries
    # =========================================================================
    
    def get_standard_operations(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Standard Operation records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Standard Operations
        '''
        return self.query_entities('StandardOperations', filter_expr=filter_expr, top=top)
    
    def get_standard_operation_by_id(self, op_id: str, expand: List[str] = None) -> dict:
        '''
        Get Standard Operation by ID.
        
        Args:
            op_id: Operation ID (OID format)
            expand: Navigation properties to expand
        
        Returns:
            Standard Operation dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('StandardOperations', op_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_standard_operation_by_number(self, number: str) -> dict:
        '''
        Get Standard Operation by number.
        
        Args:
            number: Operation number
        
        Returns:
            Standard Operation dictionary
        '''
        ops = self.query_entities(
            'StandardOperations',
            filter_expr=f"Number eq '{number}'",
            top=1
        )
        return ops[0] if ops else None
    
    def get_standard_operations_by_state(self, state: str, top: int = 50) -> List[dict]:
        '''
        Get Standard Operations by lifecycle state.
        
        Args:
            state: Lifecycle state value
            top: Maximum results
        
        Returns:
            List of Standard Operations in specified state
        '''
        return self.query_entities(
            'StandardOperations',
            filter_expr=f"State/Value eq '{state}'",
            top=top
        )
    
    # =========================================================================
    # Standard Operation Navigation Properties
    # =========================================================================
    
    def get_operation_folder(self, op_id: str) -> dict:
        '''Get Standard Operation folder.'''
        return self.get_navigation('StandardOperations', op_id, 'Folder', domain=self.DOMAIN)
    
    def get_operation_creator(self, op_id: str) -> dict:
        '''Get Standard Operation creator.'''
        return self.get_navigation('StandardOperations', op_id, 'Creator', domain=self.DOMAIN)
    
    def get_operation_master(self, op_id: str) -> dict:
        '''Get Standard Operation master.'''
        return self.get_navigation('StandardOperations', op_id, 'Master', domain=self.DOMAIN)
    
    def get_operation_versions(self, op_id: str, top: int = 50) -> List[dict]:
        '''Get all versions of a Standard Operation.'''
        return self.get_navigation('StandardOperations', op_id, 'Versions', domain=self.DOMAIN, top=top)
    
    def get_operation_procedure_usages(self, op_id: str, top: int = 50) -> List[dict]:
        '''Get Standard Procedure Usages for a Standard Operation.'''
        return self.get_navigation('StandardOperations', op_id, 'StandardProcedureUsages', domain=self.DOMAIN, top=top)
    
    # =========================================================================
    # Standard Procedure Queries
    # =========================================================================
    
    def get_standard_procedures(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Standard Procedure records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Standard Procedures
        '''
        return self.query_entities('StandardProcedures', filter_expr=filter_expr, top=top)
    
    def get_standard_procedure_by_id(self, proc_id: str, expand: List[str] = None) -> dict:
        '''
        Get Standard Procedure by ID.
        
        Args:
            proc_id: Procedure ID (OID format)
            expand: Navigation properties to expand
        
        Returns:
            Standard Procedure dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('StandardProcedures', proc_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_standard_procedure_by_number(self, number: str) -> dict:
        '''
        Get Standard Procedure by number.
        
        Args:
            number: Procedure number
        
        Returns:
            Standard Procedure dictionary
        '''
        procs = self.query_entities(
            'StandardProcedures',
            filter_expr=f"Number eq '{number}'",
            top=1
        )
        return procs[0] if procs else None
    
    # =========================================================================
    # Standard Procedure Navigation Properties
    # =========================================================================
    
    def get_procedure_folder(self, proc_id: str) -> dict:
        '''Get Standard Procedure folder.'''
        return self.get_navigation('StandardProcedures', proc_id, 'Folder', domain=self.DOMAIN)
    
    def get_procedure_creator(self, proc_id: str) -> dict:
        '''Get Standard Procedure creator.'''
        return self.get_navigation('StandardProcedures', proc_id, 'Creator', domain=self.DOMAIN)
    
    def get_procedure_master(self, proc_id: str) -> dict:
        '''Get Standard Procedure master.'''
        return self.get_navigation('StandardProcedures', proc_id, 'Master', domain=self.DOMAIN)
    
    def get_procedure_versions(self, proc_id: str, top: int = 50) -> List[dict]:
        '''Get all versions of a Standard Procedure.'''
        return self.get_navigation('StandardProcedures', proc_id, 'Versions', domain=self.DOMAIN, top=top)
    
    # =========================================================================
    # Standard Control Characteristic Queries
    # =========================================================================
    
    def get_standard_control_characteristics(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Standard Control Characteristic records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Standard Control Characteristics
        '''
        return self.query_entities('StandardControlCharacteristics', filter_expr=filter_expr, top=top)
    
    def get_scc_by_id(self, scc_id: str, expand: List[str] = None) -> dict:
        '''
        Get Standard Control Characteristic by ID.
        
        Args:
            scc_id: SCC ID (OID format)
            expand: Navigation properties to expand
        
        Returns:
            Standard Control Characteristic dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('StandardControlCharacteristics', scc_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_scc_by_number(self, number: str) -> dict:
        '''
        Get Standard Control Characteristic by number.
        
        Args:
            number: SCC number
        
        Returns:
            Standard Control Characteristic dictionary
        '''
        sccs = self.query_entities(
            'StandardControlCharacteristics',
            filter_expr=f"Number eq '{number}'",
            top=1
        )
        return sccs[0] if sccs else None
    
    def get_sccs_by_state(self, state: str, top: int = 50) -> List[dict]:
        '''
        Get Standard Control Characteristics by lifecycle state.
        
        Args:
            state: Lifecycle state value
            top: Maximum results
        
        Returns:
            List of SCCs in specified state
        '''
        return self.query_entities(
            'StandardControlCharacteristics',
            filter_expr=f"State/Value eq '{state}'",
            top=top
        )
    
    # =========================================================================
    # SCC Navigation Properties
    # =========================================================================
    
    def get_scc_folder(self, scc_id: str) -> dict:
        '''Get SCC folder.'''
        return self.get_navigation('StandardControlCharacteristics', scc_id, 'Folder', domain=self.DOMAIN)
    
    def get_scc_creator(self, scc_id: str) -> dict:
        '''Get SCC creator.'''
        return self.get_navigation('StandardControlCharacteristics', scc_id, 'Creator', domain=self.DOMAIN)
    
    def get_scc_master(self, scc_id: str) -> dict:
        '''Get SCC master.'''
        return self.get_navigation('StandardControlCharacteristics', scc_id, 'Master', domain=self.DOMAIN)
    
    def get_scc_versions(self, scc_id: str, top: int = 50) -> List[dict]:
        '''Get all versions of a Standard Control Characteristic.'''
        return self.get_navigation('StandardControlCharacteristics', scc_id, 'Versions', domain=self.DOMAIN, top=top)
    
    def get_scc_resource_usages(self, scc_id: str, top: int = 50) -> List[dict]:
        '''Get Resource Usages for a SCC.'''
        return self.get_navigation('StandardControlCharacteristics', scc_id, 'ResourceUsages', domain=self.DOMAIN, top=top)
    
    def get_scc_procedure_usages(self, scc_id: str, top: int = 50) -> List[dict]:
        '''Get Standard Procedure Usages for a SCC.'''
        return self.get_navigation('StandardControlCharacteristics', scc_id, 'StandardProcedureUsages', domain=self.DOMAIN, top=top)
    
    # =========================================================================
    # Resource Queries
    # =========================================================================
    
    def get_resources(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Resource records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Resources
        '''
        return self.query_entities('Resources', filter_expr=filter_expr, top=top)
    
    def get_resource_by_id(self, resource_id: str, expand: List[str] = None) -> dict:
        '''
        Get Resource by ID.
        
        Args:
            resource_id: Resource ID (OID format)
            expand: Navigation properties to expand
        
        Returns:
            Resource dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('Resources', resource_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_resource_by_number(self, number: str) -> dict:
        '''
        Get Resource by number.
        
        Args:
            number: Resource number
        
        Returns:
            Resource dictionary
        '''
        resources = self.query_entities(
            'Resources',
            filter_expr=f"Number eq '{number}'",
            top=1
        )
        return resources[0] if resources else None
    
    # =========================================================================
    # Resource Navigation Properties
    # =========================================================================
    
    def get_resource_folder(self, resource_id: str) -> dict:
        '''Get Resource folder.'''
        return self.get_navigation('Resources', resource_id, 'Folder', domain=self.DOMAIN)
    
    def get_resource_usages(self, resource_id: str, top: int = 50) -> List[dict]:
        '''Get Resource Usages for a Resource.'''
        return self.get_navigation('Resources', resource_id, 'ResourceUsages', domain=self.DOMAIN, top=top)
    
    # =========================================================================
    # Reference Document Queries
    # =========================================================================
    
    def get_reference_documents(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Reference Document records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Reference Documents
        '''
        return self.query_entities('ReferenceDocuments', filter_expr=filter_expr, top=top)
    
    def get_reference_document_by_id(self, ref_id: str) -> dict:
        '''
        Get Reference Document by ID.
        
        Args:
            ref_id: Reference Document ID
        
        Returns:
            Reference Document dictionary
        '''
        return self.get_entity('ReferenceDocuments', ref_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Document Lifecycle Actions
    # =========================================================================
    
    def set_document_state(self, doc_id: str, state: str) -> dict:
        '''
        Set Document lifecycle state.
        
        Args:
            doc_id: Document ID
            state: Target state value
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/Documents('{doc_id}')/PTC.Factory.SetState"
        
        payload = {"State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def set_documents_state_bulk(self, doc_ids: List[str], state: str) -> dict:
        '''
        Set lifecycle state for multiple Documents.
        
        Args:
            doc_ids: List of Document IDs
            state: Target state value
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/Documents/PTC.Factory.SetStateDocuments"
        
        payload = {"Documents": doc_ids, "State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def revise_document(self, doc_id: str, version_id: str = None) -> dict:
        '''
        Revise a Document.
        
        Args:
            doc_id: Document ID
            version_id: Optional version ID
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/Documents('{doc_id}')/PTC.Factory.Revise"
        
        payload = {"VersionId": version_id} if version_id else {}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def check_out_document(self, doc_id: str, check_out_note: str = None) -> dict:
        '''
        Check out a Document.
        
        Args:
            doc_id: Document ID
            check_out_note: Optional check-out note
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/Documents('{doc_id}')/PTC.Factory.CheckOut"
        
        payload = {"CheckOutNote": check_out_note or ""}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def undo_check_out_document(self, doc_id: str) -> dict:
        '''
        Undo check out for a Document.
        
        Args:
            doc_id: Document ID
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/Documents('{doc_id}')/PTC.Factory.UndoCheckOut"
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def check_in_document(self, doc_id: str, check_in_note: str = None, keep_checked_out: bool = False) -> dict:
        '''
        Check in a Document.
        
        Args:
            doc_id: Document ID
            check_in_note: Optional check-in note
            keep_checked_out: Whether to keep document checked out
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/Documents('{doc_id}')/PTC.Factory.CheckIn"
        
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
    # Standard Operation Actions
    # =========================================================================
    
    def set_operation_state(self, op_id: str, state: str) -> dict:
        '''
        Set Standard Operation lifecycle state.
        
        Args:
            op_id: Operation ID
            state: Target state value
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/StandardOperations('{op_id}')/PTC.Factory.SetState"
        
        payload = {"State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def set_operations_state_bulk(self, op_ids: List[str], state: str) -> dict:
        '''
        Set lifecycle state for multiple Standard Operations.
        
        Args:
            op_ids: List of Operation IDs
            state: Target state value
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/StandardOperations/PTC.Factory.SetStateStandardOperations"
        
        payload = {"StandardOperations": op_ids, "State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def revise_operation(self, op_id: str, version_id: str = None) -> dict:
        '''
        Revise a Standard Operation.
        
        Args:
            op_id: Operation ID
            version_id: Optional version ID
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/StandardOperations('{op_id}')/PTC.Factory.Revise"
        
        payload = {"VersionId": version_id} if version_id else {}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def check_out_operation(self, op_id: str, check_out_note: str = None) -> dict:
        '''
        Check out a Standard Operation.
        
        Args:
            op_id: Operation ID
            check_out_note: Optional check-out note
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/StandardOperations('{op_id}')/PTC.Factory.CheckOut"
        
        payload = {"CheckOutNote": check_out_note or ""}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def check_in_operation(self, op_id: str, check_in_note: str = None, keep_checked_out: bool = False) -> dict:
        '''
        Check in a Standard Operation.
        
        Args:
            op_id: Operation ID
            check_in_note: Optional check-in note
            keep_checked_out: Whether to keep operation checked out
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/StandardOperations('{op_id}')/PTC.Factory.CheckIn"
        
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
    
    def update_sop_related_links(self, op_id: str, test_run: str = None, update_requests: List[dict] = None) -> dict:
        '''
        Update SOP related links for a Standard Operation.
        
        Args:
            op_id: Operation ID
            test_run: Test run ID
            update_requests: List of update request objects
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/StandardOperations('{op_id}')/PTC.Factory.updateSOPRelatedLinks"
        
        payload = {
            "TestRun": test_run,
            "UpdateRequests": update_requests or []
        }
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    # =========================================================================
    # Standard Control Characteristic Actions
    # =========================================================================
    
    def set_scc_state(self, scc_id: str, state: str) -> dict:
        '''
        Set Standard Control Characteristic lifecycle state.
        
        Args:
            scc_id: SCC ID
            state: Target state value
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/StandardControlCharacteristics('{scc_id}')/PTC.Factory.SetState"
        
        payload = {"State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def set_sccs_state_bulk(self, scc_ids: List[str], state: str) -> dict:
        '''
        Set lifecycle state for multiple Standard Control Characteristics.
        
        Args:
            scc_ids: List of SCC IDs
            state: Target state value
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/StandardControlCharacteristics/PTC.Factory.SetStateStandardControlCharacteristics"
        
        payload = {"StandardControlCharacteristics": scc_ids, "State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def revise_scc(self, scc_id: str, version_id: str = None) -> dict:
        '''
        Revise a Standard Control Characteristic.
        
        Args:
            scc_id: SCC ID
            version_id: Optional version ID
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/StandardControlCharacteristics('{scc_id}')/PTC.Factory.Revise"
        
        payload = {"VersionId": version_id} if version_id else {}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def check_out_scc(self, scc_id: str, check_out_note: str = None) -> dict:
        '''
        Check out a Standard Control Characteristic.
        
        Args:
            scc_id: SCC ID
            check_out_note: Optional check-out note
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/StandardControlCharacteristics('{scc_id}')/PTC.Factory.CheckOut"
        
        payload = {"CheckOutNote": check_out_note or ""}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def check_in_scc(self, scc_id: str, check_in_note: str = None, keep_checked_out: bool = False) -> dict:
        '''
        Check in a Standard Control Characteristic.
        
        Args:
            scc_id: SCC ID
            check_in_note: Optional check-in note
            keep_checked_out: Whether to keep SCC checked out
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/StandardControlCharacteristics('{scc_id}')/PTC.Factory.CheckIn"
        
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
    
    def update_scc_related_links(self, scc_id: str, test_run: str = None, update_requests: List[dict] = None) -> dict:
        '''
        Update SCC related links for a Standard Control Characteristic.
        
        Args:
            scc_id: SCC ID
            test_run: Test run ID
            update_requests: List of update request objects
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/StandardControlCharacteristics('{scc_id}')/PTC.Factory.updateSCCRelatedLinks"
        
        payload = {
            "TestRun": test_run,
            "UpdateRequests": update_requests or []
        }
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    # =========================================================================
    # Standard Procedure Actions
    # =========================================================================
    
    def set_procedure_state(self, proc_id: str, state: str) -> dict:
        '''
        Set Standard Procedure lifecycle state.
        
        Args:
            proc_id: Procedure ID
            state: Target state value
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/StandardProcedures('{proc_id}')/PTC.Factory.SetState"
        
        payload = {"State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def revise_procedure(self, proc_id: str, version_id: str = None) -> dict:
        '''
        Revise a Standard Procedure.
        
        Args:
            proc_id: Procedure ID
            version_id: Optional version ID
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/StandardProcedures('{proc_id}')/PTC.Factory.Revise"
        
        payload = {"VersionId": version_id} if version_id else {}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}


def create_factory_client(config_path: str = None, **kwargs) -> FactoryClient:
    '''
    Factory function to create Factory client.
    
    Args:
        config_path: Path to config.json
        **kwargs: Additional client options
    
    Returns:
        FactoryClient instance
    '''
    if config_path:
        with open(config_path, 'r') as f:
            config = json.load(f)
        kwargs.update(config)
    
    return FactoryClient(**kwargs)
