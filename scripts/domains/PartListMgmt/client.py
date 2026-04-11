'''
Windchill PLM PartListMgmt (Part List Management) Domain Client

Part List Management domain client providing:
- Illustrated Parts Lists (IPL) management
- Part List Items handling
- Illustrations and graphics
- Substitutes and Supplements
- Version control (check-in/check-out/revise)
- Lifecycle state management

This domain handles service information and parts documentation.
'''

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class PartListMgmtClient(WindchillBaseClient):
    '''
    Client for Windchill PartListMgmt OData domain.
    
    Provides part list management operations including
    part lists, items, illustrations, substitutes, and supplements.
    '''
    
    DOMAIN = 'PartListMgmt'
    
    def __init__(self, **kwargs):
        '''Initialize PartListMgmt client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # PartList Queries
    # =========================================================================
    
    def get_partlists(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get PartList records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of PartLists
        '''
        return self.query_entities('PartLists', filter_expr=filter_expr, top=top)
    
    def get_partlist_by_id(self, partlist_id: str, expand: List[str] = None) -> dict:
        '''
        Get PartList by ID.
        
        Args:
            partlist_id: PartList ID (OID format)
            expand: Navigation properties to expand
        
        Returns:
            PartList dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('PartLists', partlist_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_partlist_by_number(self, number: str) -> dict:
        '''
        Get PartList by number.
        
        Args:
            number: Part List number
        
        Returns:
            PartList dictionary
        '''
        partlists = self.query_entities(
            'PartLists',
            filter_expr=f"Number eq '{number}'",
            top=1
        )
        return partlists[0] if partlists else None
    
    def get_partlists_by_state(self, state: str, top: int = 50) -> List[dict]:
        '''
        Get PartLists by lifecycle state.
        
        Args:
            state: Lifecycle state value
            top: Maximum results
        
        Returns:
            List of PartLists in specified state
        '''
        return self.query_entities(
            'PartLists',
            filter_expr=f"State/Value eq '{state}'",
            top=top
        )
    
    def get_partlists_by_name(self, name: str, top: int = 50) -> List[dict]:
        '''
        Get PartLists by name.
        
        Args:
            name: Part List name
            top: Maximum results
        
        Returns:
            List of matching PartLists
        '''
        return self.query_entities(
            'PartLists',
            filter_expr=f"Name eq '{name}'",
            top=top
        )
    
    # =========================================================================
    # PartListItem Queries
    # =========================================================================
    
    def get_partlist_items(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get PartListItem records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of PartListItems
        '''
        return self.query_entities('PartListItems', filter_expr=filter_expr, top=top)
    
    def get_partlist_item_by_id(self, item_id: str, expand: List[str] = None) -> dict:
        '''
        Get PartListItem by ID.
        
        Args:
            item_id: PartListItem ID (OID format)
            expand: Navigation properties to expand
        
        Returns:
            PartListItem dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('PartListItems', item_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_partlist_item_by_number(self, number: str) -> dict:
        '''
        Get PartListItem by number.
        
        Args:
            number: Item number
        
        Returns:
            PartListItem dictionary
        '''
        items = self.query_entities(
            'PartListItems',
            filter_expr=f"Number eq '{number}'",
            top=1
        )
        return items[0] if items else None
    
    def get_partlist_items_for_partlist(self, partlist_id: str) -> List[dict]:
        '''
        Get PartListItems for a PartList.
        
        Args:
            partlist_id: PartList ID
        
        Returns:
            List of PartListItems
        '''
        return self.get_navigation('PartLists', partlist_id, 'Uses', domain=self.DOMAIN)
    
    # =========================================================================
    # Illustration Queries
    # =========================================================================
    
    def get_illustrations(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Illustration records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Illustrations
        '''
        return self.query_entities('Illustrations', filter_expr=filter_expr, top=top)
    
    def get_illustration_by_id(self, illustration_id: str, expand: List[str] = None) -> dict:
        '''
        Get Illustration by ID.
        
        Args:
            illustration_id: Illustration ID (OID format)
            expand: Navigation properties to expand
        
        Returns:
            Illustration dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('Illustrations', illustration_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_illustrations_for_partlist(self, partlist_id: str) -> List[dict]:
        '''
        Get Illustrations for a PartList.
        
        Args:
            partlist_id: PartList ID
        
        Returns:
            List of Illustrations
        '''
        return self.get_navigation('PartLists', partlist_id, 'DescribedBy', domain=self.DOMAIN)
    
    def get_partlist_for_illustration(self, illustration_id: str) -> dict:
        '''
        Get PartList for an Illustration.
        
        Args:
            illustration_id: Illustration ID
        
        Returns:
            PartList dictionary
        '''
        return self.get_navigation('Illustrations', illustration_id, 'Describes', domain=self.DOMAIN)
    
    # =========================================================================
    # PartListInformationElement Queries
    # =========================================================================
    
    def get_partlist_information_elements(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get PartListInformationElement records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of PartListInformationElements
        '''
        return self.query_entities('PartListInformationElements', filter_expr=filter_expr, top=top)
    
    def get_partlist_information_element_by_id(self, element_id: str) -> dict:
        '''
        Get PartListInformationElement by ID.
        
        Args:
            element_id: Element ID (OID format)
        
        Returns:
            PartListInformationElement dictionary
        '''
        return self.get_entity('PartListInformationElements', element_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Substitute Queries
    # =========================================================================
    
    def get_substitutes(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Substitute records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Substitutes
        '''
        return self.query_entities('Substitutes', filter_expr=filter_expr, top=top)
    
    def get_substitute_by_id(self, substitute_id: str) -> dict:
        '''
        Get Substitute by ID.
        
        Args:
            substitute_id: Substitute ID (OID format)
        
        Returns:
            Substitute dictionary
        '''
        return self.get_entity('Substitutes', substitute_id, domain=self.DOMAIN)
    
    def get_substitutes_for_item(self, item_id: str) -> List[dict]:
        '''
        Get Substitutes for a PartListItem.
        
        Args:
            item_id: PartListItem ID
        
        Returns:
            List of Substitutes
        '''
        return self.get_navigation('PartListItems', item_id, 'Substitutes', domain=self.DOMAIN)
    
    # =========================================================================
    # Supplement Queries
    # =========================================================================
    
    def get_supplements(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Supplement records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Supplements
        '''
        return self.query_entities('Supplements', filter_expr=filter_expr, top=top)
    
    def get_supplement_by_id(self, supplement_id: str) -> dict:
        '''
        Get Supplement by ID.
        
        Args:
            supplement_id: Supplement ID (OID format)
        
        Returns:
            Supplement dictionary
        '''
        return self.get_entity('Supplements', supplement_id, domain=self.DOMAIN)
    
    def get_supplements_for_item(self, item_id: str) -> List[dict]:
        '''
        Get Supplements for a PartListItem.
        
        Args:
            item_id: PartListItem ID
        
        Returns:
            List of Supplements
        '''
        return self.get_navigation('PartListItems', item_id, 'Supplements', domain=self.DOMAIN)
    
    # =========================================================================
    # Navigation Properties - PartList
    # =========================================================================
    
    def get_partlist_creator(self, partlist_id: str) -> dict:
        '''Get PartList creator.'''
        return self.get_navigation('PartLists', partlist_id, 'Creator', domain=self.DOMAIN)
    
    def get_partlist_modifier(self, partlist_id: str) -> dict:
        '''Get PartList modifier.'''
        return self.get_navigation('PartLists', partlist_id, 'Modifier', domain=self.DOMAIN)
    
    def get_partlist_folder(self, partlist_id: str) -> dict:
        '''Get PartList folder.'''
        return self.get_navigation('PartLists', partlist_id, 'Folder', domain=self.DOMAIN)
    
    def get_partlist_organization(self, partlist_id: str) -> dict:
        '''Get PartList organization.'''
        return self.get_navigation('PartLists', partlist_id, 'Organization', domain=self.DOMAIN)
    
    def get_partlist_versions(self, partlist_id: str) -> List[dict]:
        '''Get PartList versions.'''
        return self.get_navigation('PartLists', partlist_id, 'Versions', domain=self.DOMAIN)
    
    def get_partlist_information_elements(self, partlist_id: str) -> List[dict]:
        '''Get PartList information elements.'''
        return self.get_navigation('PartLists', partlist_id, 'InformationElement', domain=self.DOMAIN)
    
    # =========================================================================
    # Navigation Properties - PartListItem
    # =========================================================================
    
    def get_partlist_for_item(self, item_id: str) -> dict:
        '''Get PartList for a PartListItem.'''
        return self.get_navigation('PartListItems', item_id, 'UsedBy', domain=self.DOMAIN)
    
    def get_part_for_item(self, item_id: str) -> dict:
        '''Get Part referenced by a PartListItem.'''
        return self.get_navigation('PartListItems', item_id, 'Uses', domain=self.DOMAIN)
    
    # =========================================================================
    # PartList CRUD Operations
    # =========================================================================
    
    def create_partlist(
        self,
        name: str,
        number: str = None,
        description: str = None,
        comments: str = None,
        information_type: str = None,
        view: str = None
    ) -> dict:
        '''
        Create a new PartList.
        
        Args:
            name: Part List name
            number: Part List number
            description: Description
            comments: Comments
            information_type: Information type
            view: View
        
        Returns:
            Created PartList
        '''
        payload = {'Name': name}
        
        if number:
            payload['Number'] = number
        if description:
            payload['Description'] = description
        if comments:
            payload['Comments'] = comments
        if information_type:
            payload['InformationType'] = information_type
        if view:
            payload['View'] = view
        
        return self.create_entity('PartLists', payload, domain=self.DOMAIN)
    
    def update_partlist(
        self,
        partlist_id: str,
        name: str = None,
        description: str = None,
        comments: str = None
    ) -> dict:
        '''
        Update a PartList.
        
        Args:
            partlist_id: PartList ID
            name: Updated name
            description: Updated description
            comments: Updated comments
        
        Returns:
            Updated PartList
        '''
        payload = {}
        
        if name is not None:
            payload['Name'] = name
        if description is not None:
            payload['Description'] = description
        if comments is not None:
            payload['Comments'] = comments
        
        return self.update_entity('PartLists', partlist_id, payload, domain=self.DOMAIN)
    
    def delete_partlist(self, partlist_id: str) -> bool:
        '''
        Delete a PartList.
        
        Args:
            partlist_id: PartList ID
        
        Returns:
            True if successful
        '''
        return self.delete_entity('PartLists', partlist_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Version Control Actions - PartList
    # =========================================================================
    
    def check_out_partlist(self, partlist_id: str, check_out_note: str = None) -> dict:
        '''
        Check out a PartList for editing.
        
        Args:
            partlist_id: PartList ID
            check_out_note: Optional check out note
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/PartLists('{partlist_id}')/PTC.PartListMgmt.CheckOut"
        
        payload = {"CheckOutNote": check_out_note or ""}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def check_in_partlist(
        self,
        partlist_id: str,
        check_in_note: str = None,
        keep_checked_out: bool = False
    ) -> dict:
        '''
        Check in a PartList.
        
        Args:
            partlist_id: PartList ID
            check_in_note: Optional check in note
            keep_checked_out: Keep checked out after check in
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/PartLists('{partlist_id}')/PTC.PartListMgmt.CheckIn"
        
        payload = {
            "CheckInNote": check_in_note or "",
            "CheckOutNote": "",
            "KeepCheckedOut": keep_checked_out
        }
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def undo_check_out_partlist(self, partlist_id: str) -> dict:
        '''
        Undo check out for a PartList.
        
        Args:
            partlist_id: PartList ID
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/PartLists('{partlist_id}')/PTC.PartListMgmt.UndoCheckOut"
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def revise_partlist(self, partlist_id: str, version_id: str = None) -> dict:
        '''
        Revise a PartList.
        
        Args:
            partlist_id: PartList ID
            version_id: Optional version ID
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/PartLists('{partlist_id}')/PTC.PartListMgmt.Revise"
        
        payload = {"VersionId": version_id or ""}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    # =========================================================================
    # Bulk Version Control Actions - PartList
    # =========================================================================
    
    def check_out_partlists_bulk(self, partlist_ids: List[str], check_out_note: str = None) -> dict:
        '''
        Check out multiple PartLists.
        
        Args:
            partlist_ids: List of PartList IDs
            check_out_note: Optional check out note
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/PartLists/PTC.PartListMgmt.CheckOutPartLists"
        
        payload = {"Workables": partlist_ids, "CheckOutNote": check_out_note or ""}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def check_in_partlists_bulk(self, partlist_ids: List[str], check_in_note: str = None) -> dict:
        '''
        Check in multiple PartLists.
        
        Args:
            partlist_ids: List of PartList IDs
            check_in_note: Optional check in note
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/PartLists/PTC.PartListMgmt.CheckInPartLists"
        
        payload = {"Workables": partlist_ids, "CheckInNote": check_in_note or ""}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def undo_check_out_partlists_bulk(self, partlist_ids: List[str]) -> dict:
        '''
        Undo check out for multiple PartLists.
        
        Args:
            partlist_ids: List of PartList IDs
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/PartLists/PTC.PartListMgmt.UndoCheckOutPartLists"
        
        payload = {"Workables": partlist_ids}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def revise_partlists_bulk(self, partlist_ids: List[str]) -> dict:
        '''
        Revise multiple PartLists.
        
        Args:
            partlist_ids: List of PartList IDs
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/PartLists/PTC.PartListMgmt.RevisePartLists"
        
        payload = {"PartLists": partlist_ids}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    # =========================================================================
    # Lifecycle State Actions
    # =========================================================================
    
    def set_partlist_state(self, partlist_id: str, state: str) -> dict:
        '''
        Set lifecycle state for a PartList.
        
        Args:
            partlist_id: PartList ID
            state: Target state
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/PartLists('{partlist_id}')/PTC.PartListMgmt.SetState"
        
        payload = {"State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def set_partlists_state_bulk(self, partlist_ids: List[str], state: str) -> dict:
        '''
        Set lifecycle state for multiple PartLists.
        
        Args:
            partlist_ids: List of PartList IDs
            state: Target state
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/PartLists/PTC.PartListMgmt.SetStatePartLists"
        
        payload = {"PartLists": partlist_ids, "State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def set_partlist_information_elements_state_bulk(self, element_ids: List[str], state: str) -> dict:
        '''
        Set lifecycle state for multiple PartListInformationElements.
        
        Args:
            element_ids: List of PartListInformationElement IDs
            state: Target state
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/PartListInformationElements/PTC.PartListMgmt.SetStatePartListInformationElements"
        
        payload = {"PartListInformationElements": element_ids, "State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    # =========================================================================
    # Update Properties Actions
    # =========================================================================
    
    def update_partlist_properties(self, partlist_id: str, updates: List[dict]) -> dict:
        '''
        Update common properties for a PartList.
        
        Args:
            partlist_id: PartList ID
            updates: List of property updates [{"Name": "value"}, ...]
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/PartLists('{partlist_id}')/PTC.PartListMgmt.UpdateCommonProperties"
        
        payload = {"PartList": partlist_id, "Updates": updates}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def update_partlist_item_properties(self, item_id: str, updates: List[dict]) -> dict:
        '''
        Update common properties for a PartListItem.
        
        Args:
            item_id: PartListItem ID
            updates: List of property updates [{"Name": "value"}, ...]
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/PartListItems('{item_id}')/PTC.PartListMgmt.UpdateCommonProperties"
        
        payload = {"PartListItem": item_id, "Updates": updates}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def update_illustration_properties(self, illustration_id: str, updates: List[dict]) -> dict:
        '''
        Update common properties for an Illustration.
        
        Args:
            illustration_id: Illustration ID
            updates: List of property updates [{"Name": "value"}, ...]
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/Illustrations('{illustration_id}')/PTC.PartListMgmt.UpdateCommonProperties"
        
        payload = {"Illustration": illustration_id, "Updates": updates}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}


def create_partlist_mgmt_client(config_path: str = None, **kwargs) -> PartListMgmtClient:
    '''
    Factory function to create PartListMgmt client.
    
    Args:
        config_path: Path to config.json
        **kwargs: Additional client options
    
    Returns:
        PartListMgmtClient instance
    '''
    if config_path:
        with open(config_path, 'r') as f:
            config = json.load(f)
        kwargs.update(config)
    
    return PartListMgmtClient(**kwargs)
