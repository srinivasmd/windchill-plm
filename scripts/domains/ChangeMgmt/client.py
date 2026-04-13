'''
Windchill PLM ChangeMgmt Domain Client

Change Management domain client providing:
- Change notice, request, and task queries
- Affected and resulting object navigation
- Change object lifecycle
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


class ChangeMgmtClient(WindchillBaseClient):
    '''
    Client for Windchill ChangeMgmt OData domain.
    
    Provides change management operations.
    '''
    
    DOMAIN = 'ChangeMgmt'
    
    def __init__(self, **kwargs):
        '''Initialize ChangeMgmt client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Change Notice
    # =========================================================================
    
    def get_change_notice_by_number(self, number: str, expand: str = None) -> dict:
        '''
        Get change notice by number.
        
        Args:
            number: Change notice number
            expand: Navigation properties to expand
        
        Returns:
            Change notice dictionary
        '''
        notices = self.query_entities(
            'ChangeNotices',
            filter_expr=f"number eq '{number}'",
            expand=expand,
            top=1
        )
        if not notices:
            raise ODataError(404, f"Change notice with number '{number}' not found")
        return notices[0]
    
    def query_change_notices(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Query change notices.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of change notices
        '''
        return self.query_entities('ChangeNotices', filter_expr=filter_expr, top=top)
    
    # =========================================================================
    # Change Request
    # =========================================================================
    
    def get_change_request_by_number(self, number: str, expand: str = None) -> dict:
        '''
        Get change request by number.
        
        Args:
            number: Change request number
            expand: Navigation properties to expand
        
        Returns:
            Change request dictionary
        '''
        requests = self.query_entities(
            'ChangeRequests',
            filter_expr=f"number eq '{number}'",
            expand=expand,
            top=1
        )
        if not requests:
            raise ODataError(404, f"Change request with number '{number}' not found")
        return requests[0]
    
    def query_change_requests(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Query change requests.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of change requests
        '''
        return self.query_entities('ChangeRequests', filter_expr=filter_expr, top=top)
    
    # =========================================================================
    # Change Task
    # =========================================================================
    
    def get_change_task_by_number(self, number: str, expand: str = None) -> dict:
        '''
        Get change task by number.
        
        Args:
            number: Change task number
            expand: Navigation properties to expand
        
        Returns:
            Change task dictionary
        '''
        tasks = self.query_entities(
            'ChangeTasks',
            filter_expr=f"number eq '{number}'",
            expand=expand,
            top=1
        )
        if not tasks:
            raise ODataError(404, f"Change task with number '{number}' not found")
        return tasks[0]
    
    # =========================================================================
    # Affected and Resulting Objects
    # =========================================================================
    
    def get_change_affected_objects(self, change_id: str) -> List[dict]:
        '''
        Get objects affected by a change.
        
        Args:
            change_id: Change notice/request/task ID
        
        Returns:
            List of affected objects
        '''
        return self.get_navigation('ChangeNotices', change_id, 'AffectedObjects', domain=self.DOMAIN)
    
    def get_change_resulting_objects(self, change_id: str) -> List[dict]:
        '''
        Get objects resulting from a change.
        
        Args:
            change_id: Change notice/request/task ID
        
        Returns:
            List of resulting objects
        '''
        return self.get_navigation('ChangeNotices', change_id, 'ResultingObjects', domain=self.DOMAIN)


def create_changemgmt_client(config_path: str = None, base_url: str = None,
                              username: str = None, password: str = None) -> ChangeMgmtClient:
    '''
    Factory function to create a ChangeMgmt client.
    
    Args:
        config_path: Path to config.json
        base_url: Windchill server URL
        username: Username
        password: Password
    
    Returns:
        ChangeMgmtClient instance
    '''
    return ChangeMgmtClient(
        config_path=config_path,
        base_url=base_url,
        username=username,
        password=password
    )


def main():
    '''CLI entry point for ChangeMgmt client.'''
    import argparse
    
    parser = argparse.ArgumentParser(description='Windchill ChangeMgmt Client')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--cn-number', help='Get change notice by number')
    parser.add_argument('--cr-number', help='Get change request by number')
    parser.add_argument('--ct-number', help='Get change task by number')
    parser.add_argument('--affected', help='Get affected objects for change ID')
    parser.add_argument('--resulting', help='Get resulting objects for change ID')
    
    args = parser.parse_args()
    
    client = create_changemgmt_client(config_path=args.config)
    
    if args.cn_number:
        cn = client.get_change_notice_by_number(args.cn_number)
        print(json.dumps(cn, indent=2))
    
    if args.cr_number:
        cr = client.get_change_request_by_number(args.cr_number)
        print(json.dumps(cr, indent=2))
    
    if args.ct_number:
        ct = client.get_change_task_by_number(args.ct_number)
        print(json.dumps(ct, indent=2))
    
    if args.affected:
        result = client.get_change_affected_objects(args.affected)
        print(json.dumps(result, indent=2))
    
    if args.resulting:
        result = client.get_change_resulting_objects(args.resulting)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
