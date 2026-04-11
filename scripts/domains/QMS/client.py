'''
Windchill PLM QMS Domain Client

Quality Management System domain client providing:
- CAPA queries and management
- NCR queries and management
- Quality Actions
- Audit record access
'''

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class QMSClient(WindchillBaseClient):
    '''
    Client for Windchill QMS OData domain.
    
    Provides quality management operations.
    '''
    
    DOMAIN = 'QMS'
    
    def __init__(self, **kwargs):
        '''Initialize QMS client with default domain.'''
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
    
    def get_capa_by_id(self, capa_id: str, expand: str = None) -> dict:
        '''
        Get CAPA by ID.
        
        Args:
            capa_id: CAPA ID
            expand: Navigation properties to expand
        
        Returns:
            CAPA dictionary
        '''
        return self.get_entity('CAPAs', capa_id, domain=self.DOMAIN, expand=expand)
    
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
            filter_expr=f"number eq '{number}'",
            top=1
        )
        if not capas:
            raise ODataError(404, f"CAPA with number '{number}' not found")
        return capas[0]
    
    def get_open_capas(self) -> List[dict]:
        '''
        Get all open CAPA records.
        
        Returns:
            List of open CAPA records
        '''
        return self.query_entities(
            'CAPAs',
            filter_expr="lifeCycleState ne 'Closed'"
        )
    
    # =========================================================================
    # NCR Queries
    # =========================================================================
    
    def get_ncrs(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get NCR (Non-Conformance Report) records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of NCR records
        '''
        return self.query_entities('NCRs', filter_expr=filter_expr, top=top)
    
    def get_ncr_by_id(self, ncr_id: str) -> dict:
        '''
        Get NCR by ID.
        
        Args:
            ncr_id: NCR ID
        
        Returns:
            NCR dictionary
        '''
        return self.get_entity('NCRs', ncr_id, domain=self.DOMAIN)
    
    def get_open_ncrs(self) -> List[dict]:
        '''
        Get all open NCR records.
        
        Returns:
            List of open NCR records
        '''
        return self.query_entities(
            'NCRs',
            filter_expr="lifeCycleState ne 'Closed'"
        )
    
    # =========================================================================
    # Quality Actions
    # =========================================================================
    
    def get_quality_actions(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get quality actions.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of quality actions
        '''
        return self.query_entities('QualityActions', filter_expr=filter_expr, top=top)
    
    def get_quality_action_by_id(self, action_id: str) -> dict:
        '''
        Get quality action by ID.
        
        Args:
            action_id: Quality action ID
        
        Returns:
            Quality action dictionary
        '''
        return self.get_entity('QualityActions', action_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Navigation Properties
    # =========================================================================
    
    def get_capa_actions(self, capa_id: str) -> List[dict]:
        '''
        Get quality actions associated with a CAPA.
        
        Args:
            capa_id: CAPA ID
        
        Returns:
            List of quality actions
        '''
        return self.get_navigation('CAPAs', capa_id, 'Actions', domain=self.DOMAIN)
    
    def get_capa_affected_objects(self, capa_id: str) -> List[dict]:
        '''
        Get affected objects for a CAPA.
        
        Args:
            capa_id: CAPA ID
        
        Returns:
            List of affected objects
        '''
        return self.get_navigation('CAPAs', capa_id, 'AffectedObjects', domain=self.DOMAIN)
    
    def get_ncr_actions(self, ncr_id: str) -> List[dict]:
        '''
        Get quality actions associated with an NCR.
        
        Args:
            ncr_id: NCR ID
        
        Returns:
            List of quality actions
        '''
        return self.get_navigation('NCRs', ncr_id, 'Actions', domain=self.DOMAIN)
    
    # =========================================================================
    # State Management
    # =========================================================================
    
    def set_capa_state(self, capa_id: str, state: str,
                        comment: str = None) -> dict:
        '''
        Set lifecycle state of a CAPA.
        
        Args:
            capa_id: CAPA ID
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
            entity_id=capa_id,
            entity_type='CAPA'
        )
    
    def set_ncr_state(self, ncr_id: str, state: str,
                       comment: str = None) -> dict:
        '''
        Set lifecycle state of an NCR.
        
        Args:
            ncr_id: NCR ID
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
            entity_id=ncr_id,
            entity_type='NCR'
        )


def create_qms_client(config_path: str = None, base_url: str = None,
                       username: str = None, password: str = None) -> QMSClient:
    '''
    Factory function to create a QMS client.
    
    Args:
        config_path: Path to config.json
        base_url: Windchill server URL
        username: Username
        password: Password
    
    Returns:
        QMSClient instance
    '''
    return QMSClient(
        config_path=config_path,
        base_url=base_url,
        username=username,
        password=password
    )


def main():
    '''CLI entry point for QMS client.'''
    import argparse
    
    parser = argparse.ArgumentParser(description='Windchill QMS Client')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--capas', action='store_true', help='List CAPAs')
    parser.add_argument('--capa-id', help='Get CAPA by ID')
    parser.add_argument('--open-capas', action='store_true', help='List open CAPAs')
    parser.add_argument('--ncrs', action='store_true', help='List NCRs')
    parser.add_argument('--ncr-id', help='Get NCR by ID')
    parser.add_argument('--open-ncrs', action='store_true', help='List open NCRs')
    parser.add_argument('--actions', action='store_true', help='List quality actions')
    parser.add_argument('--capa-actions', help='Get actions for CAPA ID')
    
    args = parser.parse_args()
    
    client = create_qms_client(config_path=args.config)
    
    if args.capas:
        result = client.get_capas()
        print(json.dumps(result, indent=2))
    
    if args.capa_id:
        result = client.get_capa_by_id(args.capa_id)
        print(json.dumps(result, indent=2))
    
    if args.open_capas:
        result = client.get_open_capas()
        print(json.dumps(result, indent=2))
    
    if args.ncrs:
        result = client.get_ncrs()
        print(json.dumps(result, indent=2))
    
    if args.ncr_id:
        result = client.get_ncr_by_id(args.ncr_id)
        print(json.dumps(result, indent=2))
    
    if args.open_ncrs:
        result = client.get_open_ncrs()
        print(json.dumps(result, indent=2))
    
    if args.actions:
        result = client.get_quality_actions()
        print(json.dumps(result, indent=2))
    
    if args.capa_actions:
        result = client.get_capa_actions(args.capa_actions)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
