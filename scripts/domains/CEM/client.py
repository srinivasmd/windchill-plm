'''
Windchill PLM CEM Domain Client

Customer Experience Management domain client providing:
- Customer experience CRUD
- Attachment management
- State transitions
'''

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class CEMClient(WindchillBaseClient):
    '''
    Client for Windchill CEM OData domain.
    
    Provides customer experience management operations.
    '''
    
    DOMAIN = 'CEM'
    
    def __init__(self, **kwargs):
        '''Initialize CEM client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Customer Experience Queries
    # =========================================================================
    
    def get_customer_experiences(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get customer experiences.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of customer experiences
        '''
        return self.query_entities('CustomerExperiences', filter_expr=filter_expr, top=top)
    
    def get_customer_experience_by_id(self, experience_id: str, expand: str = None) -> dict:
        '''
        Get customer experience by ID.
        
        Args:
            experience_id: Customer experience ID
            expand: Navigation properties to expand
        
        Returns:
            Customer experience dictionary
        '''
        return self.get_entity('CustomerExperiences', experience_id, domain=self.DOMAIN, expand=expand)
    
    # =========================================================================
    # CRUD Operations
    # =========================================================================
    
    def create_customer_experience(self, experience_data: dict) -> dict:
        '''
        Create a new customer experience.
        
        Args:
            experience_data: Customer experience properties
        
        Returns:
            Created customer experience
        '''
        return self.create_entity('CustomerExperiences', experience_data, domain=self.DOMAIN)
    
    def update_customer_experience(self, experience_id: str, experience_data: dict) -> dict:
        '''
        Update a customer experience.
        
        Args:
            experience_id: Customer experience ID
            experience_data: Updated properties
        
        Returns:
            Updated customer experience
        '''
        return self.update_entity('CustomerExperiences', experience_id, experience_data, domain=self.DOMAIN)
    
    # =========================================================================
    # Attachments
    # =========================================================================
    
    def get_customer_experience_attachments(self, experience_id: str) -> List[dict]:
        '''
        Get attachments for a customer experience.
        
        Args:
            experience_id: Customer experience ID
        
        Returns:
            List of attachments
        '''
        return self.get_navigation('CustomerExperiences', experience_id, 'Attachments', domain=self.DOMAIN)
    
    # =========================================================================
    # State Management
    # =========================================================================
    
    def set_customer_experience_state(self, experience_id: str, state: str, 
                                       comment: str = None) -> dict:
        '''
        Set lifecycle state of a customer experience.
        
        Args:
            experience_id: Customer experience ID
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
            entity_id=experience_id,
            entity_type='CustomerExperience'
        )
    
    def set_customer_experiences_state(self, experience_ids: List[str], state: str,
                                        comment: str = None) -> List[dict]:
        '''
        Set state for multiple customer experiences.
        
        Args:
            experience_ids: List of customer experience IDs
            state: Target state
            comment: State change comment
        
        Returns:
            List of state change results
        '''
        results = []
        for exp_id in experience_ids:
            result = self.set_customer_experience_state(exp_id, state, comment)
            results.append(result)
        return results


def create_cem_client(config_path: str = None, base_url: str = None,
                       username: str = None, password: str = None) -> CEMClient:
    '''
    Factory function to create a CEM client.
    
    Args:
        config_path: Path to config.json
        base_url: Windchill server URL
        username: Username
        password: Password
    
    Returns:
        CEMClient instance
    '''
    return CEMClient(
        config_path=config_path,
        base_url=base_url,
        username=username,
        password=password
    )


def main():
    '''CLI entry point for CEM client.'''
    import argparse
    
    parser = argparse.ArgumentParser(description='Windchill CEM Client')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--list', action='store_true', help='List customer experiences')
    parser.add_argument('--id', help='Get customer experience by ID')
    parser.add_argument('--attachments', help='Get attachments for experience ID')
    parser.add_argument('--state', nargs=2, metavar=('ID', 'STATE'), help='Set state')
    
    args = parser.parse_args()
    
    client = create_cem_client(config_path=args.config)
    
    if args.list:
        result = client.get_customer_experiences()
        print(json.dumps(result, indent=2))
    
    if args.id:
        result = client.get_customer_experience_by_id(args.id)
        print(json.dumps(result, indent=2))
    
    if args.attachments:
        result = client.get_customer_experience_attachments(args.attachments)
        print(json.dumps(result, indent=2))
    
    if args.state:
        result = client.set_customer_experience_state(args.state[0], args.state[1])
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
