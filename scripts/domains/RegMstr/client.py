'''
Windchill PLM RegMstr Domain Client

Regulatory Master domain client providing:
- Registration queries
- Regulatory compliance operations
- Market tracking
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


class RegMstrClient(WindchillBaseClient):
    '''
    Client for Windchill RegMstr OData domain.
    
    Provides regulatory registration operations.
    '''
    
    DOMAIN = 'RegMstr'
    
    def __init__(self, **kwargs):
        '''Initialize RegMstr client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Registration Queries
    # =========================================================================
    
    def get_registrations(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get registrations.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of registrations
        '''
        return self.query_entities('Registrations', filter_expr=filter_expr, top=top)
    
    def get_registration_by_id(self, registration_id: str, expand: str = None) -> dict:
        '''
        Get registration by ID.
        
        Args:
            registration_id: Registration ID
            expand: Navigation properties to expand
        
        Returns:
            Registration dictionary
        '''
        return self.get_entity('Registrations', registration_id, domain=self.DOMAIN, expand=expand)
    
    def get_registration_by_number(self, number: str) -> dict:
        '''
        Get registration by number.
        
        Args:
            number: Registration number
        
        Returns:
            Registration dictionary
        '''
        regs = self.query_entities(
            'Registrations',
            filter_expr=f"Number eq '{number}'",
            top=1
        )
        if not regs:
            raise ODataError(404, f"Registration with number '{number}' not found")
        return regs[0]
    
    # =========================================================================
    # Market Queries
    # =========================================================================
    
    def get_registrations_by_market(self, market: str) -> List[dict]:
        '''
        Get registrations for a specific market/country.
        
        Args:
            market: Market/country code
        
        Returns:
            List of registrations for the market
        '''
        return self.query_entities(
            'Registrations',
            filter_expr=f"Market eq '{market}'"
        )
    
    def get_registration_markets(self, registration_id: str) -> List[dict]:
        '''
        Get markets for a registration.
        
        Args:
            registration_id: Registration ID
        
        Returns:
            List of markets
        '''
        return self.get_navigation('Registrations', registration_id, 'Markets', domain=self.DOMAIN)
    
    # =========================================================================
    # Product Association
    # =========================================================================
    
    def get_registration_products(self, registration_id: str) -> List[dict]:
        '''
        Get products associated with a registration.
        
        Args:
            registration_id: Registration ID
        
        Returns:
            List of products
        '''
        return self.get_navigation('Registrations', registration_id, 'Products', domain=self.DOMAIN)
    
    # =========================================================================
    # Compliance Operations
    # =========================================================================
    
    def get_compliance_status(self, registration_id: str) -> dict:
        '''
        Get compliance status for a registration.
        
        Args:
            registration_id: Registration ID
        
        Returns:
            Compliance status dictionary
        '''
        return self.invoke_action(
            'GetComplianceStatus',
            entity_id=registration_id,
            entity_type='Registration'
        )
    
    # =========================================================================
    # State Management
    # =========================================================================
    
    def set_registration_state(self, registration_id: str, state: str,
                                comment: str = None) -> dict:
        '''
        Set lifecycle state of a registration.
        
        Args:
            registration_id: Registration ID
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
            entity_id=registration_id,
            entity_type='Registration'
        )


def create_regmstr_client(config_path: str = None, base_url: str = None,
                           username: str = None, password: str = None) -> RegMstrClient:
    '''
    Factory function to create a RegMstr client.
    
    Args:
        config_path: Path to config.json
        base_url: Windchill server URL
        username: Username
        password: Password
    
    Returns:
        RegMstrClient instance
    '''
    return RegMstrClient(
        config_path=config_path,
        base_url=base_url,
        username=username,
        password=password
    )


def main():
    '''CLI entry point for RegMstr client.'''
    import argparse
    
    parser = argparse.ArgumentParser(description='Windchill RegMstr Client')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--registrations', action='store_true', help='List registrations')
    parser.add_argument('--registration-id', help='Get registration by ID')
    parser.add_argument('--registration-number', help='Get registration by number')
    parser.add_argument('--market', help='Get registrations by market')
    parser.add_argument('--products', help='Get products for registration ID')
    parser.add_argument('--compliance', help='Get compliance status for registration ID')
    
    args = parser.parse_args()
    
    client = create_regmstr_client(config_path=args.config)
    
    if args.registrations:
        result = client.get_registrations()
        print(json.dumps(result, indent=2))
    
    if args.registration_id:
        result = client.get_registration_by_id(args.registration_id)
        print(json.dumps(result, indent=2))
    
    if args.registration_number:
        result = client.get_registration_by_number(args.registration_number)
        print(json.dumps(result, indent=2))
    
    if args.market:
        result = client.get_registrations_by_market(args.market)
        print(json.dumps(result, indent=2))
    
    if args.products:
        result = client.get_registration_products(args.products)
        print(json.dumps(result, indent=2))
    
    if args.compliance:
        result = client.get_compliance_status(args.compliance)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
