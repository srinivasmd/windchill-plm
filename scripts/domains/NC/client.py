'''
Windchill PLM NC (Nonconformance) Domain Client

Nonconformance management domain client providing:
- Nonconformance tracking and management
- Affected objects handling
- Immediate actions management
- Other items tracking
- Lifecycle state management
- Reservation (checkout) operations
- File attachment uploads

This domain integrates with QMS for quality management workflows.
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
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class NCClient(WindchillBaseClient):
    '''
    Client for Windchill NC (Nonconformance) OData domain.
    
    Provides nonconformance management operations including
    tracking, affected objects, immediate actions, and lifecycle.
    '''
    
    DOMAIN = 'NC'
    
    # Priority constants
    PRIORITY_LOW = 'LOW'
    PRIORITY_MEDIUM = 'MEDIUM'
    PRIORITY_HIGH = 'HIGH'
    PRIORITY_CRITICAL = 'CRITICAL'
    
    # Severity constants
    SEVERITY_MINOR = 'MINOR'
    SEVERITY_MAJOR = 'MAJOR'
    SEVERITY_CRITICAL = 'CRITICAL'
    
    # Impact constants
    IMPACT_LOW = 'LOW'
    IMPACT_MEDIUM = 'MEDIUM'
    IMPACT_HIGH = 'HIGH'
    
    # State constants
    STATE_OPEN = 'OPEN'
    STATE_IN_REVIEW = 'IN_REVIEW'
    STATE_IN_PROGRESS = 'IN_PROGRESS'
    STATE_PENDING_DISPOSITION = 'PENDING_DISPOSITION'
    STATE_CLOSED = 'CLOSED'
    
    def __init__(self, **kwargs):
        '''Initialize NC client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Nonconformance Queries
    # =========================================================================
    
    def get_nonconformances(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Nonconformance records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Nonconformances
        '''
        return self.query_entities('Nonconformances', filter_expr=filter_expr, top=top)
    
    def get_nonconformance_by_id(self, nc_id: str, expand: List[str] = None) -> dict:
        '''
        Get Nonconformance by ID.
        
        Args:
            nc_id: Nonconformance ID (OID format)
            expand: Navigation properties to expand
        
        Returns:
            Nonconformance dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('Nonconformances', nc_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_nonconformance_by_number(self, number: str) -> dict:
        '''
        Get Nonconformance by number.
        
        Args:
            number: NC number
        
        Returns:
            Nonconformance dictionary
        '''
        ncs = self.query_entities(
            'Nonconformances',
            filter_expr=f"NCNumber eq '{number}'",
            top=1
        )
        return ncs[0] if ncs else None
    
    def get_nonconformances_by_state(self, state: str, top: int = 50) -> List[dict]:
        '''
        Get Nonconformances by lifecycle state.
        
        Args:
            state: Lifecycle state value
            top: Maximum results
        
        Returns:
            List of Nonconformances in specified state
        '''
        return self.query_entities(
            'Nonconformances',
            filter_expr=f"State/Value eq '{state}'",
            top=top
        )
    
    def get_nonconformances_by_priority(self, priority: str, top: int = 50) -> List[dict]:
        '''
        Get Nonconformances by priority.
        
        Args:
            priority: Priority level (LOW, MEDIUM, HIGH, CRITICAL)
            top: Maximum results
        
        Returns:
            List of Nonconformances with specified priority
        '''
        return self.query_entities(
            'Nonconformances',
            filter_expr=f"Priority/Value eq '{priority}'",
            top=top
        )
    
    def get_nonconformances_by_severity(self, severity: str, top: int = 50) -> List[dict]:
        '''
        Get Nonconformances by severity.
        
        Args:
            severity: Severity level (MINOR, MAJOR, CRITICAL)
            top: Maximum results
        
        Returns:
            List of Nonconformances with specified severity
        '''
        return self.query_entities(
            'Nonconformances',
            filter_expr=f"Severity/Value eq '{severity}'",
            top=top
        )
    
    def get_nonconformances_by_assignee(self, assignee_id: str, top: int = 50) -> List[dict]:
        '''
        Get Nonconformances assigned to a specific user.
        
        Args:
            assignee_id: User OID
            top: Maximum results
        
        Returns:
            List of Nonconformances assigned to the user
        '''
        return self.query_entities(
            'Nonconformances',
            filter_expr=f"AssignedTo eq '{assignee_id}'",
            top=top
        )
    
    def get_open_nonconformances(self, top: int = 50) -> List[dict]:
        '''
        Get all open nonconformances.
        
        Args:
            top: Maximum results
        
        Returns:
            List of open Nonconformances
        '''
        return self.query_entities(
            'Nonconformances',
            filter_expr="State/Value ne 'CLOSED'",
            top=top
        )
    
    # =========================================================================
    # Nonconformance Navigation Properties
    # =========================================================================
    
    def get_affected_objects(self, nc_id: str, top: int = 50) -> List[dict]:
        '''
        Get affected objects for a nonconformance.
        
        Args:
            nc_id: Nonconformance ID
            top: Maximum results
        
        Returns:
            List of AffectedObjects
        '''
        return self.get_navigation('Nonconformances', nc_id, 'AffectedObjects', domain=self.DOMAIN, top=top)
    
    def get_immediate_actions(self, nc_id: str, top: int = 50) -> List[dict]:
        '''
        Get immediate actions for a nonconformance.
        
        Args:
            nc_id: Nonconformance ID
            top: Maximum results
        
        Returns:
            List of ImmediateActions
        '''
        return self.get_navigation('Nonconformances', nc_id, 'ImmediateActions', domain=self.DOMAIN, top=top)
    
    def get_other_items(self, nc_id: str, top: int = 50) -> List[dict]:
        '''
        Get other items for a nonconformance.
        
        Args:
            nc_id: Nonconformance ID
            top: Maximum results
        
        Returns:
            List of OtherItems
        '''
        return self.get_navigation('Nonconformances', nc_id, 'OtherItems', domain=self.DOMAIN, top=top)
    
    def get_nc_creator(self, nc_id: str) -> dict:
        '''Get Nonconformance creator.'''
        return self.get_navigation('Nonconformances', nc_id, 'Creator', domain=self.DOMAIN)
    
    def get_nc_owner(self, nc_id: str) -> dict:
        '''Get Nonconformance owner.'''
        return self.get_navigation('Nonconformances', nc_id, 'Owner', domain=self.DOMAIN)
    
    def get_nc_assignee(self, nc_id: str) -> dict:
        '''Get Nonconformance assignee.'''
        return self.get_navigation('Nonconformances', nc_id, 'Assignee', domain=self.DOMAIN)
    
    def get_nc_container(self, nc_id: str) -> dict:
        '''Get Nonconformance container.'''
        return self.get_navigation('Nonconformances', nc_id, 'Container', domain=self.DOMAIN)
    
    def get_nc_folder(self, nc_id: str) -> dict:
        '''Get Nonconformance folder.'''
        return self.get_navigation('Nonconformances', nc_id, 'Folder', domain=self.DOMAIN)
    
    # =========================================================================
    # Affected Object Operations
    # =========================================================================
    
    def get_affected_object_by_id(self, affected_id: str) -> dict:
        '''
        Get Affected Object by ID.
        
        Args:
            affected_id: AffectedObject ID
        
        Returns:
            AffectedObject dictionary
        '''
        # AffectedObjects are contained in Nonconformance
        # Need to query through navigation
        results = self.query_entities(
            'Nonconformances',
            filter_expr=f"AffectedObjects/ID eq '{affected_id}'",
            expand='AffectedObjects',
            top=1
        )
        if results:
            for obj in results[0].get('AffectedObjects', []):
                if obj.get('ID') == affected_id:
                    return obj
        return None
    
    def add_affected_object(
        self,
        nc_id: str,
        name: str,
        number: str,
        description: str,
        quantity: float = None,
        part_number: str = None,
        serial_number: str = None,
        revision: str = None,
        disposition: str = None,
        comments: str = None
    ) -> dict:
        '''
        Add an affected object to a nonconformance.
        
        Args:
            nc_id: Nonconformance ID
            name: Object name
            number: Object number
            description: Object description
            quantity: Quantity affected
            part_number: Part number
            serial_number: Serial number
            revision: Revision
            disposition: Disposition
            comments: Additional comments
        
        Returns:
            Created AffectedObject
        '''
        payload = {
            'Name': name,
            'Number': number,
            'Description': description
        }
        
        if quantity is not None:
            payload['Quantity'] = quantity
        if part_number:
            payload['PartNumber'] = part_number
        if serial_number:
            payload['SerialNumber'] = serial_number
        if revision:
            payload['Revision'] = revision
        if disposition:
            payload['Disposition'] = disposition
        if comments:
            payload['Comments'] = comments
        
        # Create via contained navigation
        url = f"{self._get_base_url()}/Nonconformances('{nc_id}')/AffectedObjects"
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    # =========================================================================
    # Immediate Action Operations
    # =========================================================================
    
    def get_immediate_action_by_id(self, action_id: str) -> dict:
        '''
        Get Immediate Action by ID.
        
        Args:
            action_id: ImmediateAction ID
        
        Returns:
            ImmediateAction dictionary
        '''
        results = self.query_entities(
            'Nonconformances',
            filter_expr=f"ImmediateActions/ID eq '{action_id}'",
            expand='ImmediateActions',
            top=1
        )
        if results:
            for action in results[0].get('ImmediateActions', []):
                if action.get('ID') == action_id:
                    return action
        return None
    
    def add_immediate_action(
        self,
        nc_id: str,
        description: str,
        action_type: str = None,
        action_date: str = None,
        comments: str = None
    ) -> dict:
        '''
        Add an immediate action to a nonconformance.
        
        Args:
            nc_id: Nonconformance ID
            description: Action description
            action_type: Type of action
            action_date: Date of action (ISO 8601)
            comments: Additional comments
        
        Returns:
            Created ImmediateAction
        '''
        payload = {
            'Description': description
        }
        
        if action_type:
            payload['ActionType'] = action_type
        if action_date:
            payload['ActionDate'] = action_date
        if comments:
            payload['Comments'] = comments
        
        url = f"{self._get_base_url()}/Nonconformances('{nc_id}')/ImmediateActions"
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    # =========================================================================
    # Other Item Operations
    # =========================================================================
    
    def add_other_item(
        self,
        nc_id: str,
        description: str,
        item_id: str,
        quantity: float,
        unit: str,
        item_type: str = None,
        purchase_order_number: str = None,
        comments: str = None
    ) -> dict:
        '''
        Add an other item to a nonconformance.
        
        Args:
            nc_id: Nonconformance ID
            description: Item description
            item_id: Item identifier
            quantity: Quantity
            unit: Unit of measure
            item_type: Item type
            purchase_order_number: PO number
            comments: Additional comments
        
        Returns:
            Created OtherItem
        '''
        payload = {
            'Description': description,
            'ItemID': item_id,
            'Quantity': quantity,
            'Unit': unit
        }
        
        if item_type:
            payload['ItemType'] = item_type
        if purchase_order_number:
            payload['PurchaseOrderNumber'] = purchase_order_number
        if comments:
            payload['Comments'] = comments
        
        url = f"{self._get_base_url()}/Nonconformances('{nc_id}')/OtherItems"
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    # =========================================================================
    # Nonconformance CRUD Operations
    # =========================================================================
    
    def create_nonconformance(
        self,
        description: str,
        identified_date: str = None,
        source: str = None,
        origin: str = None,
        priority: str = None,
        severity: str = None,
        impact: str = None,
        location: str = None,
        assigned_to: str = None,
        customer_name: str = None,
        cost_impact: float = None,
        comments: str = None
    ) -> dict:
        '''
        Create a new nonconformance.
        
        Args:
            description: Description of the nonconformance
            identified_date: Date identified (ISO 8601)
            source: Source of the NC report
            origin: Origin of the nonconformance
            priority: Priority level
            severity: Severity level
            impact: Impact level
            location: Location where NC occurred
            assigned_to: User OID to assign
            customer_name: Customer name if applicable
            cost_impact: Financial impact
            comments: Additional comments
        
        Returns:
            Created Nonconformance
        '''
        payload = {
            'Description': description
        }
        
        if identified_date:
            payload['IdentifiedDate'] = identified_date
        if source:
            payload['Source'] = source
        if origin:
            payload['Origin'] = origin
        if priority:
            payload['Priority'] = priority
        if severity:
            payload['Severity'] = severity
        if impact:
            payload['Impact'] = impact
        if location:
            payload['Location'] = location
        if assigned_to:
            payload['AssignedTo'] = assigned_to
        if customer_name:
            payload['CustomerName'] = customer_name
        if cost_impact is not None:
            payload['CostImpact'] = cost_impact
        if comments:
            payload['Comments'] = comments
        
        return self.create_entity('Nonconformances', payload, domain=self.DOMAIN)
    
    def update_nonconformance(
        self,
        nc_id: str,
        description: str = None,
        disposition: str = None,
        priority: str = None,
        severity: str = None,
        assigned_to: str = None,
        location: str = None,
        cost_impact: float = None,
        comments: str = None,
        completion_date: str = None
    ) -> dict:
        '''
        Update a nonconformance.
        
        Args:
            nc_id: Nonconformance ID
            description: Updated description
            disposition: Disposition decision
            priority: Updated priority
            severity: Updated severity
            assigned_to: Updated assignee
            location: Updated location
            cost_impact: Updated cost impact
            comments: Updated comments
            completion_date: Completion date
        
        Returns:
            Updated Nonconformance
        '''
        payload = {}
        
        if description is not None:
            payload['Description'] = description
        if disposition is not None:
            payload['Disposition'] = disposition
        if priority is not None:
            payload['Priority'] = priority
        if severity is not None:
            payload['Severity'] = severity
        if assigned_to is not None:
            payload['AssignedTo'] = assigned_to
        if location is not None:
            payload['Location'] = location
        if cost_impact is not None:
            payload['CostImpact'] = cost_impact
        if comments is not None:
            payload['Comments'] = comments
        if completion_date is not None:
            payload['CompletionDate'] = completion_date
        
        return self.update_entity('Nonconformances', nc_id, payload, domain=self.DOMAIN)
    
    def delete_nonconformance(self, nc_id: str) -> bool:
        '''
        Delete a nonconformance.
        
        Args:
            nc_id: Nonconformance ID
        
        Returns:
            True if successful
        '''
        return self.delete_entity('Nonconformances', nc_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Lifecycle Actions
    # =========================================================================
    
    def set_nonconformance_state(self, nc_id: str, state: str) -> dict:
        '''
        Set the lifecycle state of a nonconformance.
        
        Args:
            nc_id: Nonconformance ID
            state: Target state value
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/Nonconformances('{nc_id}')/PTC.NC.SetState"
        
        payload = {"State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def set_nonconformances_state_bulk(self, nc_ids: List[str], state: str) -> dict:
        '''
        Set lifecycle state for multiple nonconformances.
        
        Args:
            nc_ids: List of Nonconformance IDs
            state: Target state value
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/Nonconformances/PTC.NC.SetStateNonconformances"
        
        payload = {"Nonconformances": nc_ids, "State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    # =========================================================================
    # Reservation (Check Out) Actions
    # =========================================================================
    
    def reserve_nonconformance(self, nc_id: str, reservation_note: str = None) -> dict:
        '''
        Reserve (check out) a nonconformance for editing.
        
        Args:
            nc_id: Nonconformance ID
            reservation_note: Optional note about the reservation
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/Nonconformances('{nc_id}')/PTC.NC.Reserve"
        
        payload = {"ReservationNote": reservation_note or ""}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def undo_reservation_nonconformance(self, nc_id: str) -> dict:
        '''
        Undo reservation (undo check out) for a nonconformance.
        
        Args:
            nc_id: Nonconformance ID
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/Nonconformances('{nc_id}')/PTC.NC.UndoReservation"
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    # =========================================================================
    # File Attachment Actions
    # =========================================================================
    
    def upload_attachment(
        self,
        nc_id: str,
        file_name: str,
        file_path: str = None,
        file_content: bytes = None,
        content_type: str = 'application/octet-stream'
    ) -> dict:
        '''
        Upload a file attachment to a nonconformance.
        
        Args:
            nc_id: Nonconformance ID
            file_name: Name of the file
            file_path: Path to the file (if reading from disk)
            file_content: File content as bytes (if provided directly)
            content_type: MIME type of the file
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        # Read file content if path provided
        if file_path and not file_content:
            with open(file_path, 'rb') as f:
                file_content = f.read()
        
        if not file_content:
            raise ValueError("Either file_path or file_content must be provided")
        
        # Stage 1: Initialize upload
        import uuid
        content_id = str(uuid.uuid4())
        
        stage1_url = f"{self._get_base_url()}/Nonconformances('{nc_id}')/PTC.NC.UploadStage1Action"
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        stage1_payload = {
            "ContentID": content_id,
            "FileName": file_name,
            "FileContent": file_content
        }
        
        response = self.session.post(stage1_url, json=stage1_payload, headers=headers)
        response.raise_for_status()
        
        # Stage 3: Complete upload
        stage3_url = f"{self._get_base_url()}/Nonconformances('{nc_id}')/PTC.NC.UploadStage3Action"
        
        stage3_payload = {
            "ContentID": content_id,
            "FileName": file_name
        }
        
        response = self.session.post(stage3_url, json=stage3_payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True, 'ContentID': content_id}
    
    # =========================================================================
    # Security Labels
    # =========================================================================
    
    def edit_security_labels(self, nc_ids: List[str], security_labels: List[dict]) -> dict:
        '''
        Edit security labels for nonconformances.
        
        Args:
            nc_ids: List of Nonconformance IDs
            security_labels: List of security label objects
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/Nonconformances/PTC.NC.EditNonconformancesSecurityLabels"
        
        payload = {
            "Nonconformances": nc_ids,
            "SecurityLabels": security_labels
        }
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}


def create_nc_client(config_path: str = None, **kwargs) -> NCClient:
    '''
    Factory function to create NC client.
    
    Args:
        config_path: Path to config.json
        **kwargs: Additional client options
    
    Returns:
        NCClient instance
    '''
    if config_path:
        with open(config_path, 'r') as f:
            config = json.load(f)
        kwargs.update(config)
    
    return NCClient(**kwargs)
