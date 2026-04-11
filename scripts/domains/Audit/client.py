'''
Windchill PLM Audit Domain Client

Audit domain client providing:
- Audit record queries
- Audit resolution
'''

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class AuditClient(WindchillBaseClient):
    '''
    Client for Windchill Audit OData domain.
    
    Provides audit management operations.
    '''
    
    DOMAIN = 'Audit'
    
    def __init__(self, **kwargs):
        '''Initialize Audit client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Audit Queries
    # =========================================================================
    
    def get_audits(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get audit records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of audit records
        '''
        return self.query_entities('Audits', filter_expr=filter_expr, top=top)
    
    def get_audit_by_id(self, audit_id: str) -> dict:
        '''
        Get audit record by ID.
        
        Args:
            audit_id: Audit record ID
        
        Returns:
            Audit record dictionary
        '''
        return self.get_entity('Audits', audit_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Audit Resolution
    # =========================================================================
    
    def resolve_audit(self, audit_id: str, resolution: str, 
                      comment: str = None) -> dict:
        '''
        Resolve an audit record.
        
        Args:
            audit_id: Audit record ID
            resolution: Resolution text
            comment: Additional comment
        
        Returns:
            Resolution result
        '''
        params = {'Resolution': resolution}
        if comment:
            params['Comment'] = comment
        
        return self.invoke_action(
            'Resolve',
            parameters=params,
            entity_id=audit_id,
            entity_type='Audit'
        )


def create_audit_client(config_path: str = None, base_url: str = None,
                         username: str = None, password: str = None) -> AuditClient:
    '''
    Factory function to create an Audit client.
    
    Args:
        config_path: Path to config.json
        base_url: Windchill server URL
        username: Username
        password: Password
    
    Returns:
        AuditClient instance
    '''
    return AuditClient(
        config_path=config_path,
        base_url=base_url,
        username=username,
        password=password
    )


def main():
    '''CLI entry point for Audit client.'''
    import argparse
    
    parser = argparse.ArgumentParser(description='Windchill Audit Client')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--audits', action='store_true', help='List audits')
    parser.add_argument('--audit-id', help='Get audit by ID')
    parser.add_argument('--resolve', nargs=2, metavar=('ID', 'RESOLUTION'), 
                        help='Resolve audit')
    
    args = parser.parse_args()
    
    client = create_audit_client(config_path=args.config)
    
    if args.audits:
        result = client.get_audits()
        print(json.dumps(result, indent=2))
    
    if args.audit_id:
        result = client.get_audit_by_id(args.audit_id)
        print(json.dumps(result, indent=2))
    
    if args.resolve:
        result = client.resolve_audit(args.resolve[0], args.resolve[1])
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
