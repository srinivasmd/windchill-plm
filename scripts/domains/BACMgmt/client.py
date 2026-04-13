'''
Windchill PLM BACMgmt Domain Client

Baseline and Configuration Management domain client providing:
- Baseline management
- Association management
- State management for managed baselines
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


class BACMgmtClient(WindchillBaseClient):
    '''
    Client for Windchill BACMgmt OData domain.
    
    Provides baseline and configuration management operations.
    '''
    
    DOMAIN = 'BACMgmt'
    
    def __init__(self, **kwargs):
        '''Initialize BACMgmt client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Baseline Management
    # =========================================================================
    
    def get_baselines(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get baselines.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of baselines
        '''
        return self.query_entities('Baselines', filter_expr=filter_expr, top=top)
    
    def get_baseline_by_id(self, baseline_id: str) -> dict:
        '''
        Get baseline by ID.
        
        Args:
            baseline_id: Baseline ID
        
        Returns:
            Baseline dictionary
        '''
        return self.get_entity('Baselines', baseline_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Baseline Content Management
    # =========================================================================
    
    def add_to_baseline(self, baseline_id: str, object_ids: List[str]) -> dict:
        '''
        Add objects to a baseline.
        
        Args:
            baseline_id: Baseline ID
            object_ids: List of object IDs to add
        
        Returns:
            Add result
        '''
        return self.invoke_action(
            'AddToBaseline',
            parameters={'Objects': [{'ID': obj_id} for obj_id in object_ids]},
            entity_id=baseline_id,
            entity_type='Baseline'
        )
    
    def remove_from_baseline(self, baseline_id: str, object_ids: List[str]) -> dict:
        '''
        Remove objects from a baseline.
        
        Args:
            baseline_id: Baseline ID
            object_ids: List of object IDs to remove
        
        Returns:
            Remove result
        '''
        return self.invoke_action(
            'RemoveFromBaseline',
            parameters={'Objects': [{'ID': obj_id} for obj_id in object_ids]},
            entity_id=baseline_id,
            entity_type='Baseline'
        )
    
    # =========================================================================
    # Association Management
    # =========================================================================
    
    def create_associations(self, source_id: str, target_ids: List[str],
                            association_type: str = None) -> List[dict]:
        '''
        Create associations between objects.
        
        Args:
            source_id: Source object ID
            target_ids: List of target object IDs
            association_type: Association type (optional)
        
        Returns:
            List of created associations
        '''
        associations = []
        for target_id in target_ids:
            assoc_data = {'Source': {'ID': source_id}, 'Target': {'ID': target_id}}
            if association_type:
                assoc_data['AssociationType'] = association_type
            associations.append(assoc_data)
        
        return self.invoke_action(
            'CreateAssociations',
            parameters={'Associations': associations}
        )
    
    def delete_associations(self, association_ids: List[str]) -> bool:
        '''
        Delete associations.
        
        Args:
            association_ids: List of association IDs to delete
        
        Returns:
            True if successful
        '''
        return self.invoke_action(
            'DeleteAssociations',
            parameters={'IDs': association_ids}
        )
    
    def move_associations(self, association_ids: List[str], new_source_id: str) -> dict:
        '''
        Move associations to a new source.
        
        Args:
            association_ids: List of association IDs to move
            new_source_id: New source object ID
        
        Returns:
            Move result
        '''
        return self.invoke_action(
            'MoveAssociations',
            parameters={
                'AssociationIDs': association_ids,
                'NewSource': {'ID': new_source_id}
            }
        )
    
    # =========================================================================
    # State Management
    # =========================================================================
    
    def set_state_managed_baselines(self, baseline_id: str, state: str,
                                      comment: str = None) -> dict:
        '''
        Set state for managed baselines.
        
        Args:
            baseline_id: Baseline ID
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
            entity_id=baseline_id,
            entity_type='ManagedBaseline'
        )


def create_bacmgmt_client(config_path: str = None, base_url: str = None,
                           username: str = None, password: str = None) -> BACMgmtClient:
    '''
    Factory function to create a BACMgmt client.
    
    Args:
        config_path: Path to config.json
        base_url: Windchill server URL
        username: Username
        password: Password
    
    Returns:
        BACMgmtClient instance
    '''
    return BACMgmtClient(
        config_path=config_path,
        base_url=base_url,
        username=username,
        password=password
    )


def main():
    '''CLI entry point for BACMgmt client.'''
    import argparse
    
    parser = argparse.ArgumentParser(description='Windchill BACMgmt Client')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--baselines', action='store_true', help='List baselines')
    parser.add_argument('--baseline-id', help='Get baseline by ID')
    parser.add_argument('--add-to-baseline', nargs=2, metavar=('BASELINE_ID', 'OBJECT_IDS'), 
                        help='Add objects to baseline')
    parser.add_argument('--remove-from-baseline', nargs=2, metavar=('BASELINE_ID', 'OBJECT_IDS'),
                        help='Remove objects from baseline')
    
    args = parser.parse_args()
    
    client = create_bacmgmt_client(config_path=args.config)
    
    if args.baselines:
        result = client.get_baselines()
        print(json.dumps(result, indent=2))
    
    if args.baseline_id:
        result = client.get_baseline_by_id(args.baseline_id)
        print(json.dumps(result, indent=2))
    
    if args.add_to_baseline:
        baseline_id = args.add_to_baseline[0]
        object_ids = args.add_to_baseline[1].split(',')
        result = client.add_to_baseline(baseline_id, object_ids)
        print(json.dumps(result, indent=2))
    
    if args.remove_from_baseline:
        baseline_id = args.remove_from_baseline[0]
        object_ids = args.remove_from_baseline[1].split(',')
        result = client.remove_from_baseline(baseline_id, object_ids)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
