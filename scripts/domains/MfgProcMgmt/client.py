'''
Windchill PLM MfgProcMgmt Domain Client

Manufacturing Process Management domain client providing:
- Process plan queries
- Operation management
- Work definition navigation
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


class MfgProcMgmtClient(WindchillBaseClient):
    '''
    Client for Windchill MfgProcMgmt OData domain.
    
    Provides manufacturing process management operations.
    '''
    
    DOMAIN = 'MfgProcMgmt'
    
    def __init__(self, **kwargs):
        '''Initialize MfgProcMgmt client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Process Plan Queries
    # =========================================================================
    
    def get_process_plan_by_number(self, number: str, expand: str = None) -> dict:
        '''
        Get process plan by number.
        
        Args:
            number: Process plan number
            expand: Navigation properties to expand
        
        Returns:
            Process plan dictionary
        '''
        plans = self.query_entities(
            'ProcessPlans',
            filter_expr=f"Number eq '{number}'",
            expand=expand,
            top=1
        )
        if not plans:
            raise ODataError(404, f"Process plan with number '{number}' not found")
        return plans[0]
    
    def query_process_plans(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Query process plans.

        Args:
            filter_expr: OData filter expression
            top: Maximum results

        Returns:
            List of process plans
        '''
        return self.query_entities('ProcessPlans', filter_expr=filter_expr, top=top)

    def search_process_plans(self, search_term: str, top: int = 50) -> List[dict]:
        '''
        Search process plans by term using Windchill full-text search.

        Args:
            search_term: Search term
            top: Maximum results

        Returns:
            List of matching process plans
        '''
        return self.search('ProcessPlans', search_term, domain=self.DOMAIN, top=top)

    # =========================================================================
    # Operations
    # =========================================================================
    
    def get_process_plan_operations(self, plan_id: str) -> List[dict]:
        '''
        Get operations for a process plan.
        
        Args:
            plan_id: Process plan ID
        
        Returns:
            List of operations
        '''
        return self.get_navigation('ProcessPlans', plan_id, 'Operations', domain=self.DOMAIN)
    
    def get_operation_parts(self, operation_id: str) -> List[dict]:
        '''
        Get parts associated with an operation.
        
        Args:
            operation_id: Operation ID
        
        Returns:
            List of parts
        '''
        return self.get_navigation('Operations', operation_id, 'Parts', domain=self.DOMAIN)


def create_mfgprocmgmt_client(config_path: str = None, base_url: str = None,
                               username: str = None, password: str = None) -> MfgProcMgmtClient:
    '''
    Factory function to create a MfgProcMgmt client.
    
    Args:
        config_path: Path to config.json
        base_url: Windchill server URL
        username: Username
        password: Password
    
    Returns:
        MfgProcMgmtClient instance
    '''
    return MfgProcMgmtClient(
        config_path=config_path,
        base_url=base_url,
        username=username,
        password=password
    )


def main():
    '''CLI entry point for MfgProcMgmt client.'''
    import argparse
    
    parser = argparse.ArgumentParser(description='Windchill MfgProcMgmt Client')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--plan-number', help='Get process plan by number')
    parser.add_argument('--plan-id', help='Get process plan by ID')
    parser.add_argument('--operations', help='Get operations for plan ID')
    
    args = parser.parse_args()
    
    client = create_mfgprocmgmt_client(config_path=args.config)
    
    if args.plan_number:
        plan = client.get_process_plan_by_number(args.plan_number)
        print(json.dumps(plan, indent=2))
    
    if args.plan_id:
        plan = client.get_entity('ProcessPlans', args.plan_id)
        print(json.dumps(plan, indent=2))
    
    if args.operations:
        ops = client.get_process_plan_operations(args.operations)
        print(json.dumps(ops, indent=2))


if __name__ == '__main__':
    main()
