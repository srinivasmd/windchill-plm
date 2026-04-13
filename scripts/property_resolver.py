'''
Property Resolver for Windchill OData API

Handles case-insensitive property name resolution using metadata files.
Maps user-provided property names to the correct case-sensitive OData names.

Usage:
    resolver = PropertyResolver()
    correct_name = resolver.resolve_property('Part', 'number')  # Returns 'Number'
    correct_name = resolver.resolve_property('Part', 'NUMBER')  # Returns 'Number'
    correct_name = resolver.resolve_property('Part', 'Name')    # Returns 'Name'
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

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Set

# Path to metadata files
METADATA_DIR = Path(__file__).parent.parent / 'references'


class PropertyResolver:
    '''
    Resolves case-insensitive property names to correct OData names.
    
    Uses entities.json, navigations.json, and actions.json metadata files
    to map user-provided names to the exact case-sensitive names expected
    by Windchill.
    '''
    
    def __init__(self):
        '''Initialize the resolver by loading metadata files.'''
        self._entities: Dict = {}
        self._navigations: Dict = {}
        self._actions: Dict = {}
        self._property_cache: Dict[str, Dict[str, str]] = {}
        self._entity_set_cache: Dict[str, str] = {}
        self._loaded = False
        
    def _load_metadata(self):
        '''Load metadata files if not already loaded.'''
        if self._loaded:
            return
            
        # Load entities
        entities_path = METADATA_DIR / 'entities.json'
        if entities_path.exists():
            with open(entities_path) as f:
                self._entities = json.load(f)
        
        # Load navigations
        nav_path = METADATA_DIR / 'navigations.json'
        if nav_path.exists():
            with open(nav_path) as f:
                self._navigations = json.load(f)
        
        # Load actions
        actions_path = METADATA_DIR / 'actions.json'
        if actions_path.exists():
            with open(actions_path) as f:
                self._actions = json.load(f)
        
        self._loaded = True
        
        # Build caches
        self._build_caches()
    
    def _build_caches(self):
        '''Build lookup caches for fast resolution.'''
        # Build property cache for each entity type
        entity_types = self._entities.get('entity_types', {})
        for entity_name, entity_def in entity_types.items():
            props = entity_def.get('properties', {})
            self._property_cache[entity_name] = {
                name.lower(): name for name in props.keys()
            }
            # Also add navigation properties
            nav_props = entity_def.get('navigation_properties', {})
            for nav_name in nav_props.keys():
                self._property_cache[entity_name][nav_name.lower()] = nav_name
        
        # Build entity set cache (maps lowercase to correct case)
        entity_sets = self._entities.get('entity_sets', {})
        for set_name in entity_sets.keys():
            self._entity_set_cache[set_name.lower()] = set_name
    
    def resolve_property(self, entity_type: str, property_name: str) -> str:
        '''
        Resolve a property name to the correct case-sensitive name.
        
        Args:
            entity_type: Entity type name (e.g., 'Part', 'Document')
            property_name: Property name in any case
            
        Returns:
            Correctly-cased property name
            
        Raises:
            ValueError: If property not found for entity type
        '''
        self._load_metadata()
        
        # Get property map for this entity
        entity_key = self.resolve_entity_type(entity_type)
        prop_map = self._property_cache.get(entity_key, {})
        
        # Look up case-insensitively
        lower_name = property_name.lower()
        if lower_name in prop_map:
            return prop_map[lower_name]
        
        # If not found, check if it's already correct case
        if property_name in prop_map.values():
            return property_name
        
        # Return as-is if not found (might be a custom property)
        return property_name
    
    def resolve_entity_type(self, entity_type: str) -> str:
        '''
        Resolve entity type name to correct case.
        
        Args:
            entity_type: Entity type name in any case
            
        Returns:
            Correctly-cased entity type name
        '''
        self._load_metadata()
        
        entity_types = self._entities.get('entity_types', {})
        
        # Check exact match first
        if entity_type in entity_types:
            return entity_type
        
        # Check case-insensitively
        lower_type = entity_type.lower()
        for name in entity_types.keys():
            if name.lower() == lower_type:
                return name
        
        # Return as-is if not found
        return entity_type
    
    def resolve_entity_set(self, entity_set: str) -> str:
        '''
        Resolve entity set name to correct case.
        
        Args:
            entity_set: Entity set name in any case (e.g., 'parts', 'PARTS')
            
        Returns:
            Correctly-cased entity set name (e.g., 'Parts')
        '''
        self._load_metadata()
        
        # Check cache
        lower_set = entity_set.lower()
        if lower_set in self._entity_set_cache:
            return self._entity_set_cache[lower_set]
        
        # Check exact match
        if entity_set in self._entity_set_cache.values():
            return entity_set
        
        return entity_set
    
    def resolve_navigation(self, entity_type: str, nav_name: str) -> str:
        '''
        Resolve navigation property name to correct case.
        
        Args:
            entity_type: Entity type name
            nav_name: Navigation property name in any case
            
        Returns:
            Correctly-cased navigation property name
        '''
        # Navigation properties are stored with entity properties
        return self.resolve_property(entity_type, nav_name)
    
    def resolve_action(self, action_name: str) -> str:
        '''
        Resolve action name to correct case.
        
        Args:
            action_name: Action name in any case
            
        Returns:
            Correctly-cased action name
        '''
        self._load_metadata()
        
        # Check unbound actions
        unbound = self._actions.get('unbound_actions', {})
        for name in unbound.keys():
            if name.lower() == action_name.lower():
                return name
        
        # Check bound actions
        bound = self._actions.get('bound_actions', {})
        for name in bound.keys():
            if name.lower() == action_name.lower():
                return name
        
        return action_name
    
    def get_entity_properties(self, entity_type: str) -> List[str]:
        '''
        Get all property names for an entity type.
        
        Args:
            entity_type: Entity type name
            
        Returns:
            List of property names
        '''
        self._load_metadata()
        
        entity_key = self.resolve_entity_type(entity_type)
        entity_types = self._entities.get('entity_types', {})
        entity_def = entity_types.get(entity_key, {})
        props = entity_def.get('properties', {})
        
        return list(props.keys())
    
    def get_entity_navigation_properties(self, entity_type: str) -> List[str]:
        '''
        Get all navigation property names for an entity type.
        
        Args:
            entity_type: Entity type name
            
        Returns:
            List of navigation property names
        '''
        self._load_metadata()
        
        entity_key = self.resolve_entity_type(entity_type)
        entity_types = self._entities.get('entity_types', {})
        entity_def = entity_types.get(entity_key, {})
        nav_props = entity_def.get('navigation_properties', {})
        
        return list(nav_props.keys())
    
    def get_property_type(self, entity_type: str, property_name: str) -> str:
        '''
        Get the OData type of a property.
        
        Args:
            entity_type: Entity type name
            property_name: Property name
            
        Returns:
            Property type string
        '''
        self._load_metadata()
        
        entity_key = self.resolve_entity_type(entity_type)
        prop_key = self.resolve_property(entity_key, property_name)
        
        entity_types = self._entities.get('entity_types', {})
        entity_def = entity_types.get(entity_key, {})
        props = entity_def.get('properties', {})
        prop_def = props.get(prop_key, {})
        
        return prop_def.get('type', 'unknown')
    
    def build_filter(self, entity_type: str, filters: Dict[str, any]) -> str:
        '''
        Build an OData $filter expression with correct property names.
        
        Args:
            entity_type: Entity type name
            filters: Dictionary of {property_name: value} pairs
            
        Returns:
            OData filter expression string
            
        Example:
            >>> resolver.build_filter('Part', {'number': 'V0056686', 'state': 'RELEASED'})
            "Number eq 'V0056686' and State eq 'RELEASED'"
        '''
        if not filters:
            return ''
        
        conditions = []
        for prop_name, value in filters.items():
            correct_name = self.resolve_property(entity_type, prop_name)
            
            # Format value based on type
            prop_type = self.get_property_type(entity_type, correct_name)
            
            if value is None:
                conditions.append(f"{correct_name} eq null")
            elif prop_type in ('String', 'DateTime', 'EnumType') or isinstance(value, str):
                # Escape single quotes
                escaped_value = str(value).replace("'", "''")
                conditions.append(f"{correct_name} eq '{escaped_value}'")
            elif prop_type in ('Boolean',) or isinstance(value, bool):
                conditions.append(f"{correct_name} eq {str(value).lower()}")
            elif prop_type in ('Int32', 'Int64', 'Double') or isinstance(value, (int, float)):
                conditions.append(f"{correct_name} eq {value}")
            else:
                # Default to string
                escaped_value = str(value).replace("'", "''")
                conditions.append(f"{correct_name} eq '{escaped_value}'")
        
        return ' and '.join(conditions)
    
    def resolve_expand(self, entity_type: str, expand: str) -> str:
        '''
        Resolve navigation property names in $expand clause.
        
        Args:
            entity_type: Entity type name
            expand: Comma-separated navigation property names
            
        Returns:
            Expand clause with correct property names
        '''
        if not expand:
            return expand
        
        nav_names = [n.strip() for n in expand.split(',')]
        resolved = [self.resolve_navigation(entity_type, n) for n in nav_names]
        
        return ','.join(resolved)
    
    def resolve_select(self, entity_type: str, select: str) -> str:
        '''
        Resolve property names in $select clause.
        
        Args:
            entity_type: Entity type name
            select: Comma-separated property names
            
        Returns:
            Select clause with correct property names
        '''
        if not select:
            return select
        
        prop_names = [n.strip() for n in select.split(',')]
        resolved = [self.resolve_property(entity_type, n) for n in prop_names]
        
        return ','.join(resolved)


# Global resolver instance
_resolver: Optional[PropertyResolver] = None


def get_resolver() -> PropertyResolver:
    '''Get the global PropertyResolver instance.'''
    global _resolver
    if _resolver is None:
        _resolver = PropertyResolver()
    return _resolver


def resolve_property(entity_type: str, property_name: str) -> str:
    '''Convenience function to resolve a single property name.'''
    return get_resolver().resolve_property(entity_type, property_name)


def resolve_entity_set(entity_set: str) -> str:
    '''Convenience function to resolve an entity set name.'''
    return get_resolver().resolve_entity_set(entity_set)


def build_filter(entity_type: str, filters: Dict[str, any]) -> str:
    '''Convenience function to build a filter expression.'''
    return get_resolver().build_filter(entity_type, filters)


# Test function
def _test():
    '''Test the resolver.'''
    resolver = PropertyResolver()
    
    print("Testing PropertyResolver")
    print("=" * 60)
    
    # Test property resolution
    tests = [
        ('Part', 'number', 'Number'),
        ('Part', 'NUMBER', 'Number'),
        ('Part', 'name', 'Name'),
        ('Part', 'STATE', 'State'),
        ('Part', 'createdon', 'CreatedOn'),
        ('Part', 'DoesNotExist', 'DoesNotExist'),  # Returns as-is
    ]
    
    print("\nProperty Resolution Tests:")
    for entity, prop, expected in tests:
        result = resolver.resolve_property(entity, prop)
        status = "PASS" if result == expected else "FAIL"
        print(f"  {status}: {entity}.{prop} -> {result} (expected: {expected})")
    
    # Test entity set resolution
    print("\nEntity Set Resolution Tests:")
    for es, expected in [('parts', 'Parts'), ('PARTS', 'Parts'), ('Parts', 'Parts')]:
        result = resolver.resolve_entity_set(es)
        status = "PASS" if result == expected else "FAIL"
        print(f"  {status}: {es} -> {result} (expected: {expected})")
    
    # Test filter building
    print("\nFilter Building Tests:")
    filters = {'number': 'V0056686', 'state': 'RELEASED'}
    result = resolver.build_filter('Part', filters)
    print(f"  Input: {filters}")
    print(f"  Output: {result}")


if __name__ == '__main__':
    _test()
