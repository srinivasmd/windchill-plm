'''
Windchill PLM UDI Domain Client

Unique Device Identification domain client providing:
- UDI record queries
- Device identification management
- Label compliance operations
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


class UDIClient(WindchillBaseClient):
    '''
    Client for Windchill UDI OData domain.
    
    Provides UDI compliance operations.
    '''
    
    DOMAIN = 'UDI'
    
    def __init__(self, **kwargs):
        '''Initialize UDI client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # UDI Record Queries
    # =========================================================================
    
    def get_udi_records(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get UDI records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of UDI records
        '''
        return self.query_entities('UDIRecords', filter_expr=filter_expr, top=top)
    
    def get_udi_record_by_id(self, udi_id: str, expand: str = None) -> dict:
        '''
        Get UDI record by ID.
        
        Args:
            udi_id: UDI record ID
            expand: Navigation properties to expand
        
        Returns:
            UDI record dictionary
        '''
        return self.get_entity('UDIRecords', udi_id, domain=self.DOMAIN, expand=expand)
    
    def get_udi_record_by_di(self, di: str) -> dict:
        '''
        Get UDI record by Device Identifier (DI).
        
        Args:
            di: Device Identifier
        
        Returns:
            UDI record dictionary
        '''
        records = self.query_entities(
            'UDIRecords',
            filter_expr=f"DeviceIdentifier eq '{di}'",
            top=1
        )
        if not records:
            raise ODataError(404, f"UDI record with DI '{di}' not found")
        return records[0]
    
    # =========================================================================
    # Device Identification
    # =========================================================================
    
    def get_device_identifiers(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get device identifiers.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of device identifiers
        '''
        return self.query_entities('DeviceIdentifiers', filter_expr=filter_expr, top=top)
    
    def search_by_udid(self, udi_di: str) -> List[dict]:
        '''
        Search UDI records by UDI-DI.
        
        Args:
            udi_di: UDI Device Identifier
        
        Returns:
            List of matching UDI records
        '''
        return self.query_entities(
            'UDIRecords',
            filter_expr=f"contains(udiDI, '{udi_di}')"
        )
    
    # =========================================================================
    # Label Management
    # =========================================================================
    
    def get_udi_labels(self, udi_id: str) -> List[dict]:
        '''
        Get labels for a UDI record.
        
        Args:
            udi_id: UDI record ID
        
        Returns:
            List of labels
        '''
        return self.get_navigation('UDIRecords', udi_id, 'Labels', domain=self.DOMAIN)
    
    # =========================================================================
    # Compliance Operations
    # =========================================================================
    
    def validate_udi_compliance(self, udi_id: str) -> dict:
        '''
        Validate UDI compliance for a record.
        
        Args:
            udi_id: UDI record ID
        
        Returns:
            Validation result
        '''
        return self.invoke_action(
            'ValidateCompliance',
            entity_id=udi_id,
            entity_type='UDIRecord'
        )
    
    def submit_to_gudid(self, udi_id: str) -> dict:
        '''
        Submit UDI record to GUDID (Global UDI Database).
        
        Args:
            udi_id: UDI record ID
        
        Returns:
            Submission result
        '''
        return self.invoke_action(
            'SubmitToGUDID',
            entity_id=udi_id,
            entity_type='UDIRecord'
        )
    
    # =========================================================================
    # State Management
    # =========================================================================
    
    def set_udi_record_state(self, udi_id: str, state: str,
                              comment: str = None) -> dict:
        '''
        Set lifecycle state of a UDI record.
        
        Args:
            udi_id: UDI record ID
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
            entity_id=udi_id,
            entity_type='UDIRecord'
        )


def create_udi_client(config_path: str = None, base_url: str = None,
                       username: str = None, password: str = None) -> UDIClient:
    '''
    Factory function to create a UDI client.
    
    Args:
        config_path: Path to config.json
        base_url: Windchill server URL
        username: Username
        password: Password
    
    Returns:
        UDIClient instance
    '''
    return UDIClient(
        config_path=config_path,
        base_url=base_url,
        username=username,
        password=password
    )


def main():
    '''CLI entry point for UDI client.'''
    import argparse
    
    parser = argparse.ArgumentParser(description='Windchill UDI Client')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--records', action='store_true', help='List UDI records')
    parser.add_argument('--record-id', help='Get UDI record by ID')
    parser.add_argument('--di', help='Get UDI record by Device Identifier')
    parser.add_argument('--search', help='Search by UDI-DI')
    parser.add_argument('--labels', help='Get labels for UDI record ID')
    parser.add_argument('--validate', help='Validate compliance for UDI record ID')
    
    args = parser.parse_args()
    
    client = create_udi_client(config_path=args.config)
    
    if args.records:
        result = client.get_udi_records()
        print(json.dumps(result, indent=2))
    
    if args.record_id:
        result = client.get_udi_record_by_id(args.record_id)
        print(json.dumps(result, indent=2))
    
    if args.di:
        result = client.get_udi_record_by_di(args.di)
        print(json.dumps(result, indent=2))
    
    if args.search:
        result = client.search_by_udid(args.search)
        print(json.dumps(result, indent=2))
    
    if args.labels:
        result = client.get_udi_labels(args.labels)
        print(json.dumps(result, indent=2))
    
    if args.validate:
        result = client.validate_udi_compliance(args.validate)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
