'''
Windchill PLM EffectivityMgmt Domain Client

Effectivity Management domain client providing:
- Effectivity context queries
- Part effectivity management
- Serial number, lot, date, and unit effectivity operations
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


class EffectivityMgmtClient(WindchillBaseClient):
    '''
    Client for Windchill EffectivityMgmt OData domain.
    
    Provides effectivity management operations for parts and configurations.
    '''
    
    DOMAIN = 'EffectivityMgmt'
    
    def __init__(self, **kwargs):
        '''Initialize EffectivityMgmt client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Part Effectivity Context Queries
    # =========================================================================
    
    def get_part_effectivity_contexts(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Part Effectivity Context records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Part Effectivity Contexts
        '''
        return self.query_entities('PartEffectivityContexts', filter_expr=filter_expr, top=top)
    
    def get_part_effectivity_context_by_id(self, context_id: str, expand: List[str] = None) -> dict:
        '''
        Get Part Effectivity Context by ID.
        
        Args:
            context_id: Context ID (OID format)
            expand: Navigation properties to expand
        
        Returns:
            Part Effectivity Context dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('PartEffectivityContexts', context_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_contexts_by_part(self, part_id: str, top: int = 50) -> List[dict]:
        '''
        Get Part Effectivity Contexts for a specific part.
        
        Args:
            part_id: Part ID
            top: Maximum results
        
        Returns:
            List of Part Effectivity Contexts
        '''
        return self.query_entities(
            'PartEffectivityContexts',
            filter_expr=f"Part/ID eq '{part_id}'",
            top=top
        )
    
    def get_contexts_by_effectivity(self, effectivity_id: str, top: int = 50) -> List[dict]:
        '''
        Get Part Effectivity Contexts for a specific effectivity.
        
        Args:
            effectivity_id: Effectivity ID
            top: Maximum results
        
        Returns:
            List of Part Effectivity Contexts
        '''
        return self.query_entities(
            'PartEffectivityContexts',
            filter_expr=f"Effectivity/ID eq '{effectivity_id}'",
            top=top
        )
    
    # =========================================================================
    # Part Effectivity Context Navigation Properties
    # =========================================================================
    
    def get_context_part(self, context_id: str) -> dict:
        '''
        Get the Part associated with a Part Effectivity Context.
        
        Args:
            context_id: Context ID
        
        Returns:
            Part dictionary
        '''
        return self.get_navigation('PartEffectivityContexts', context_id, 'Part', domain=self.DOMAIN)
    
    def get_context_effectivity(self, context_id: str) -> dict:
        '''
        Get the Effectivity associated with a Part Effectivity Context.
        
        Args:
            context_id: Context ID
        
        Returns:
            Effectivity dictionary
        '''
        return self.get_navigation('PartEffectivityContexts', context_id, 'Effectivity', domain=self.DOMAIN)
    
    # =========================================================================
    # Effectivity Managed Entity Operations
    # =========================================================================
    
    def get_effectivity_managed_entities(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Effectivity Managed Entity records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Effectivity Managed Entities
        '''
        return self.query_entities('EffectivityManagedEntities', filter_expr=filter_expr, top=top)
    
    def get_effectivity_managed_entity_by_id(self, entity_id: str, expand: List[str] = None) -> dict:
        '''
        Get Effectivity Managed Entity by ID.
        
        Args:
            entity_id: Entity ID
            expand: Navigation properties to expand
        
        Returns:
            Effectivity Managed Entity dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('EffectivityManagedEntities', entity_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_entity_effectivities(self, entity_id: str, top: int = 50) -> List[dict]:
        '''
        Get effectivities for an Effectivity Managed Entity.
        
        Args:
            entity_id: Entity ID
            top: Maximum results
        
        Returns:
            List of effectivities
        '''
        return self.get_navigation('EffectivityManagedEntities', entity_id, 'Effectivities', domain=self.DOMAIN, top=top)
    
    def get_entity_latest_effectivity(self, entity_id: str) -> dict:
        '''
        Get the latest effectivity for an Effectivity Managed Entity.
        
        Args:
            entity_id: Entity ID
        
        Returns:
            Latest effectivity dictionary
        '''
        return self.get_navigation('EffectivityManagedEntities', entity_id, 'LatestEffectivity', domain=self.DOMAIN)
    
    def get_entity_effectivity_context(self, entity_id: str) -> dict:
        '''
        Get the effectivity context for an Effectivity Managed Entity.
        
        Args:
            entity_id: Entity ID
        
        Returns:
            Effectivity context dictionary
        '''
        return self.get_navigation('EffectivityManagedEntities', entity_id, 'EffectivityContext', domain=self.DOMAIN)
    
    # =========================================================================
    # Effectivity Queries
    # =========================================================================
    
    def get_effectivities(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Effectivity records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Effectivities
        '''
        return self.query_entities('Effectivities', filter_expr=filter_expr, top=top)
    
    def get_effectivity_by_id(self, effectivity_id: str) -> dict:
        '''
        Get Effectivity by ID.
        
        Args:
            effectivity_id: Effectivity ID
        
        Returns:
            Effectivity dictionary
        '''
        return self.get_entity('Effectivities', effectivity_id, domain=self.DOMAIN)
    
    def get_effectivity_part_effectivity(self, effectivity_id: str) -> dict:
        '''
        Get the Part Effectivity for an Effectivity.
        
        Args:
            effectivity_id: Effectivity ID
        
        Returns:
            Part Effectivity dictionary
        '''
        return self.get_navigation('Effectivities', effectivity_id, 'PartEffectivity', domain=self.DOMAIN)
    
    # =========================================================================
    # Date Effectivity Queries
    # =========================================================================
    
    def get_date_effectivities(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Date Effectivity records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Date Effectivities
        '''
        return self.query_entities('DateEffectivities', filter_expr=filter_expr, top=top)
    
    def get_date_effectivity_by_id(self, effectivity_id: str) -> dict:
        '''
        Get Date Effectivity by ID.
        
        Args:
            effectivity_id: Effectivity ID
        
        Returns:
            Date Effectivity dictionary
        '''
        return self.get_entity('DateEffectivities', effectivity_id, domain=self.DOMAIN)
    
    def get_date_effectivities_by_range(self, start_date: str, end_date: str = None, top: int = 50) -> List[dict]:
        '''
        Get Date Effectivities within a date range.
        
        Args:
            start_date: Start date (ISO format)
            end_date: End date (ISO format, optional)
            top: Maximum results
        
        Returns:
            List of Date Effectivities
        '''
        if end_date:
            filter_expr = f"StartDate ge {start_date} and EndDate le {end_date}"
        else:
            filter_expr = f"StartDate ge {start_date}"
        
        return self.query_entities('DateEffectivities', filter_expr=filter_expr, top=top)
    
    # =========================================================================
    # Unit Effectivity Queries
    # =========================================================================
    
    def get_unit_effectivities(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Unit Effectivity records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Unit Effectivities
        '''
        return self.query_entities('UnitEffectivities', filter_expr=filter_expr, top=top)
    
    def get_unit_effectivity_by_id(self, effectivity_id: str) -> dict:
        '''
        Get Unit Effectivity by ID.
        
        Args:
            effectivity_id: Effectivity ID
        
        Returns:
            Unit Effectivity dictionary
        '''
        return self.get_entity('UnitEffectivities', effectivity_id, domain=self.DOMAIN)
    
    def get_unit_effectivities_by_range(self, start_unit: int, end_unit: int = None, top: int = 50) -> List[dict]:
        '''
        Get Unit Effectivities within a unit range.
        
        Args:
            start_unit: Starting unit number
            end_unit: Ending unit number (optional)
            top: Maximum results
        
        Returns:
            List of Unit Effectivities
        '''
        if end_unit:
            filter_expr = f"StartUnit ge {start_unit} and EndUnit le {end_unit}"
        else:
            filter_expr = f"StartUnit ge {start_unit}"
        
        return self.query_entities('UnitEffectivities', filter_expr=filter_expr, top=top)
    
    # =========================================================================
    # Serial Number Effectivity Queries
    # =========================================================================
    
    def get_serial_number_effectivities(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Serial Number Effectivity records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Serial Number Effectivities
        '''
        return self.query_entities('SerialNumberEffectivities', filter_expr=filter_expr, top=top)
    
    def get_serial_number_effectivity_by_id(self, effectivity_id: str) -> dict:
        '''
        Get Serial Number Effectivity by ID.
        
        Args:
            effectivity_id: Effectivity ID
        
        Returns:
            Serial Number Effectivity dictionary
        '''
        return self.get_entity('SerialNumberEffectivities', effectivity_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Lot Effectivity Queries
    # =========================================================================
    
    def get_lot_effectivities(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Lot Effectivity records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Lot Effectivities
        '''
        return self.query_entities('LotEffectivities', filter_expr=filter_expr, top=top)
    
    def get_lot_effectivity_by_id(self, effectivity_id: str) -> dict:
        '''
        Get Lot Effectivity by ID.
        
        Args:
            effectivity_id: Effectivity ID
        
        Returns:
            Lot Effectivity dictionary
        '''
        return self.get_entity('LotEffectivities', effectivity_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Block Effectivity Queries
    # =========================================================================
    
    def get_block_effectivities(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Block Effectivity records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Block Effectivities
        '''
        return self.query_entities('BlockEffectivities', filter_expr=filter_expr, top=top)
    
    def get_block_effectivity_by_id(self, effectivity_id: str) -> dict:
        '''
        Get Block Effectivity by ID.
        
        Args:
            effectivity_id: Effectivity ID
        
        Returns:
            Block Effectivity dictionary
        '''
        return self.get_entity('BlockEffectivities', effectivity_id, domain=self.DOMAIN)
    
    # =========================================================================
    # MSN Effectivity Queries
    # =========================================================================
    
    def get_msn_effectivities(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get MSN (Manufacturer Serial Number) Effectivity records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of MSN Effectivities
        '''
        return self.query_entities('MSNEffectivities', filter_expr=filter_expr, top=top)
    
    def get_msn_effectivity_by_id(self, effectivity_id: str) -> dict:
        '''
        Get MSN Effectivity by ID.
        
        Args:
            effectivity_id: Effectivity ID
        
        Returns:
            MSN Effectivity dictionary
        '''
        return self.get_entity('MSNEffectivities', effectivity_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Effectivity Actions
    # =========================================================================
    
    def get_effectivities_for_entities(self, entity_ids: List[str]) -> dict:
        '''
        Get effectivities for multiple effectivity-managed entities.
        
        Args:
            entity_ids: List of entity IDs
        
        Returns:
            Effectivities for the entities
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/PartEffectivityContexts/PTC.EffectivityMgmt.GetEffectivities"
        
        payload = {"EffectivityManagables": entity_ids}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def set_effectivities_for_entity(self, entity_id: str, effectivities: List[dict]) -> dict:
        '''
        Set effectivities for an effectivity-managed entity.
        
        Args:
            entity_id: Entity ID
            effectivities: List of effectivity definitions
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/PartEffectivityContexts/PTC.EffectivityMgmt.SetEffectivities"
        
        payload = {
            "EffectivityManaged": entity_id,
            "Effectivities": effectivities
        }
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}


def create_effectivity_mgmt_client(config_path: str = None, **kwargs) -> EffectivityMgmtClient:
    '''
    Factory function to create EffectivityMgmt client.
    
    Args:
        config_path: Path to config.json
        **kwargs: Additional client options
    
    Returns:
        EffectivityMgmtClient instance
    '''
    if config_path:
        with open(config_path, 'r') as f:
            config = json.load(f)
        kwargs.update(config)
    
    return EffectivityMgmtClient(**kwargs)
