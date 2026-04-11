'''
Windchill PLM CAPA Domain Client

Corrective and Preventive Action (CAPA) domain client providing:
- CAPA queries and management
- CAPA Action Plan operations
- CAPA Site management
- Affected Object tracking
'''

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class CAPAClient(WindchillBaseClient):
    '''
    Client for Windchill CAPA OData domain.
    
    Provides corrective and preventive action operations.
    '''
    
    DOMAIN = 'CAPA'
    
    def __init__(self, **kwargs):
        '''Initialize CAPA client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # CAPA Queries
    # =========================================================================
    
    def get_capas(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get CAPA records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of CAPA records
        '''
        return self.query_entities('CAPAs', filter_expr=filter_expr, top=top)
    
    def get_capa_by_id(self, capa_id: str, expand: List[str] = None) -> dict:
        '''
        Get CAPA by ID.
        
        Args:
            capa_id: CAPA ID (OID format)
            expand: Navigation properties to expand
        
        Returns:
            CAPA dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('CAPAs', capa_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_capa_by_number(self, number: str) -> dict:
        '''
        Get CAPA by number.
        
        Args:
            number: CAPA number
        
        Returns:
            CAPA dictionary
        '''
        capas = self.query_entities(
            'CAPAs',
            filter_expr=f"Number eq '{number}'",
            top=1
        )
        return capas[0] if capas else None
    
    def get_open_capas(self, top: int = 50) -> List[dict]:
        '''
        Get open CAPAs (not in closed state).
        
        Args:
            top: Maximum results
        
        Returns:
            List of open CAPAs
        '''
        return self.query_entities(
            'CAPAs',
            filter_expr="State/Value ne 'CLOSED'",
            top=top
        )
    
    def get_capas_by_state(self, state: str, top: int = 50) -> List[dict]:
        '''
        Get CAPAs by lifecycle state.
        
        Args:
            state: Lifecycle state value
            top: Maximum results
        
        Returns:
            List of CAPAs in specified state
        '''
        return self.query_entities(
            'CAPAs',
            filter_expr=f"State/Value eq '{state}'",
            top=top
        )
    
    def search_capas(self, search_term: str, top: int = 20) -> List[dict]:
        '''
        Search CAPAs by name or number.
        
        Args:
            search_term: Search string
            top: Maximum results
        
        Returns:
            List of matching CAPAs
        '''
        return self.query_entities(
            'CAPAs',
            filter_expr=f"contains(Name, '{search_term}') or contains(Number, '{search_term}')",
            top=top
        )
    
    # =========================================================================
    # CAPA Navigation Properties
    # =========================================================================
    
    def get_capa_primary_site(self, capa_id: str) -> dict:
        '''
        Get CAPA primary site.
        
        Args:
            capa_id: CAPA ID
        
        Returns:
            Primary site dictionary
        '''
        return self.get_navigation('CAPAs', capa_id, 'PrimarySite', domain=self.DOMAIN)
    
    def get_capa_additional_sites(self, capa_id: str, top: int = 50) -> List[dict]:
        '''
        Get CAPA additional sites.
        
        Args:
            capa_id: CAPA ID
            top: Maximum results
        
        Returns:
            List of additional sites
        '''
        return self.get_navigation('CAPAs', capa_id, 'AdditionalSites', domain=self.DOMAIN, top=top)
    
    def get_capa_affected_objects(self, capa_id: str, top: int = 50) -> List[dict]:
        '''
        Get objects affected by CAPA.
        
        Args:
            capa_id: CAPA ID
            top: Maximum results
        
        Returns:
            List of affected objects
        '''
        return self.get_navigation('CAPAs', capa_id, 'AffectedObjects', domain=self.DOMAIN, top=top)
    
    def get_capa_plan(self, capa_id: str) -> dict:
        '''
        Get CAPA action plan.
        
        Args:
            capa_id: CAPA ID
        
        Returns:
            Action plan dictionary
        '''
        return self.get_navigation('CAPAs', capa_id, 'Plan', domain=self.DOMAIN)
    
    def get_capa_attachments(self, capa_id: str, top: int = 50) -> List[dict]:
        '''
        Get CAPA attachments.
        
        Args:
            capa_id: CAPA ID
            top: Maximum results
        
        Returns:
            List of attachments
        '''
        return self.get_navigation('CAPAs', capa_id, 'Attachments', domain=self.DOMAIN, top=top)
    
    # =========================================================================
    # CAPA Action Plan Operations
    # =========================================================================
    
    def get_action_plan_by_id(self, plan_id: str, expand: List[str] = None) -> dict:
        '''
        Get CAPA Action Plan by ID.
        
        Args:
            plan_id: Action Plan ID
            expand: Navigation properties to expand
        
        Returns:
            Action plan dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('CAPAActionPlans', plan_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_action_plan_actions(self, plan_id: str, top: int = 50) -> List[dict]:
        '''
        Get actions in a CAPA Action Plan.
        
        Args:
            plan_id: Action Plan ID
            top: Maximum results
        
        Returns:
            List of actions
        '''
        return self.get_navigation('CAPAActionPlans', plan_id, 'Actions', domain=self.DOMAIN, top=top)
    
    # =========================================================================
    # Action Operations
    # =========================================================================
    
    def get_action_by_id(self, action_id: str) -> dict:
        '''
        Get CAPA Action by ID.
        
        Args:
            action_id: Action ID
        
        Returns:
            Action dictionary
        '''
        return self.get_entity('Actions', action_id, domain=self.DOMAIN)
    
    def get_action_subjects(self, action_id: str, top: int = 50) -> List[dict]:
        '''
        Get subjects for a CAPA Action.
        
        Args:
            action_id: Action ID
            top: Maximum results
        
        Returns:
            List of action subjects
        '''
        return self.get_navigation('Actions', action_id, 'ActionSubjects', domain=self.DOMAIN, top=top)
    
    # =========================================================================
    # CAPA Site Operations
    # =========================================================================
    
    def get_capa_sites(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get CAPA sites.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of CAPA sites
        '''
        return self.query_entities('CAPASites', filter_expr=filter_expr, top=top)
    
    # =========================================================================
    # Affected Object Operations
    # =========================================================================
    
    def get_affected_objects(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get affected objects.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of affected objects
        '''
        return self.query_entities('AffectedObjects', filter_expr=filter_expr, top=top)
    
    # =========================================================================
    # State Management Actions
    # =========================================================================
    
    def set_capa_state(self, capa_id: str, state: str) -> dict:
        '''
        Set CAPA lifecycle state.
        
        Args:
            capa_id: CAPA ID
            state: Target state value
        
        Returns:
            Action result
        '''
        # Get CSRF token if needed
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/CAPAs('{capa_id}')/PTC.CAPA.SetState"
        
        payload = {
            "State": state
        }
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def set_capas_state_bulk(self, capa_ids: List[str], state: str) -> dict:
        '''
        Set lifecycle state for multiple CAPAs.
        
        Args:
            capa_ids: List of CAPA IDs
            state: Target state value
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/CAPAs/PTC.CAPA.SetStateCAPAs"
        
        payload = {
            "CAPAs": capa_ids,
            "State": state
        }
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}


def create_capa_client(config_path: str = None, **kwargs) -> CAPAClient:
    '''
    Factory function to create CAPA client.
    
    Args:
        config_path: Path to config.json
        **kwargs: Additional client options
    
    Returns:
        CAPAClient instance
    '''
    if config_path:
        with open(config_path, 'r') as f:
            config = json.load(f)
        kwargs.update(config)
    
    return CAPAClient(**kwargs)
