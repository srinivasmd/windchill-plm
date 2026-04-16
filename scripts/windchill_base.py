'''
Windchill PLM OData REST API Base Client

Provides common OData operations shared across all domain modules:
- Entity CRUD operations
- Query operations with OData parameters
- Action invocation
- Navigation property traversal
- Authentication and CSRF token management

This is the foundation for domain-specific clients.
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
import sys
import urllib.parse
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import requests

# Skill directory paths
SKILL_DIR = Path(__file__).parent.parent
CONFIG_PATH = SKILL_DIR / 'config.json'
ENTITIES_PATH = SKILL_DIR / 'references' / 'entities.json'
ACTIONS_PATH = SKILL_DIR / 'references' / 'actions.json'
NAVIGATIONS_PATH = SKILL_DIR / 'references' / 'navigations.json'

# Import property resolver for case-insensitive property handling
try:
    from property_resolver import PropertyResolver, get_resolver, resolve_property, resolve_entity_set, build_filter
    PROPERTY_RESOLVER_AVAILABLE = True
except ImportError:
    PROPERTY_RESOLVER_AVAILABLE = False


class ODataError(Exception):
    '''Exception raised for OData API errors.'''
    
    def __init__(self, status_code: int, message: str, details: dict = None):
        self.status_code = status_code
        self.message = message
        self.details = details or {}
        super().__init__(f"[{status_code}] {message}")


class WindchillBaseClient:
    '''
    Base client for PTC Windchill PLM OData REST API.
    
    Provides core OData operations including:
    - Entity queries with full OData query options
    - Navigation property traversal
    - Action invocation (bound and unbound)
    - CRUD operations
    - CSRF token management
    
    Domain-specific clients inherit from this base class.
    '''
    
    def __init__(self, config_path: str = None, base_url: str = None, 
                 username: str = None, password: str = None, domain: str = 'ProdMgmt'):
        '''
        Initialize client with configuration or direct credentials.
        
        Args:
            config_path: Path to config.json (optional)
            base_url: Direct Windchill server URL (optional)
            username: Direct username (optional)
            password: Direct password (optional)
            domain: Default OData domain (default: ProdMgmt)
        '''
        self.session = requests.Session()
        self.csrf_token = None
        self.default_domain = domain
        
        if base_url and username and password:
            self.config = {
                'server_url': base_url,
                'odata_base_url': f"{base_url.rstrip('/')}/servlet/odata",
                'auth_type': 'basic',
                'basic': {
                    'username': username,
                    'password': password
                },
                'verify_ssl': True
            }
            self.config_path = None
        elif config_path:
            self.config_path = Path(config_path)
            self.config = self._load_config()
        else:
            self.config_path = CONFIG_PATH
            self.config = self._load_config()
        
        self._setup_auth()
        self._load_metadata()
    
    # =========================================================================
    # Configuration and Authentication
    # =========================================================================
    

    # =========================================================================
    # Property Resolution Helpers
    # =========================================================================

    def _resolve_entity_set(self, entity_set: str) -> str:
        """Resolve entity set name to correct case using metadata."""
        if PROPERTY_RESOLVER_AVAILABLE:
            return resolve_entity_set(entity_set)
        return entity_set

    def _resolve_property(self, entity_type: str, property_name: str) -> str:
        """Resolve property name to correct case using metadata."""
        if PROPERTY_RESOLVER_AVAILABLE:
            return resolve_property(entity_type, property_name)
        return property_name

    def _build_filter_from_dict(self, entity_type: str, filters: dict) -> str:
        """Build OData $filter from dict with case-insensitive keys."""
        if PROPERTY_RESOLVER_AVAILABLE:
            return build_filter(entity_type, filters)
        # Fallback
        if not filters:
            return ""
        conditions = []
        for prop, value in filters.items():
            if isinstance(value, str):
                conditions.append(f"{prop} eq '{value.replace(chr(39), chr(39)+chr(39))}'")
            elif isinstance(value, (int, float)):
                conditions.append(f"{prop} eq {value}")
            elif isinstance(value, bool):
                conditions.append(f"{prop} eq {str(value).lower()}")
            elif value is None:
                conditions.append(f"{prop} eq null")
        return " and ".join(conditions)

    def _load_config(self) -> dict:
        '''Load configuration from JSON file.'''
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise ODataError(500, f"Config file not found at {self.config_path}")
        except json.JSONDecodeError as e:
            raise ODataError(500, f"Invalid JSON in config file: {e}")
    
    def _setup_auth(self):
        '''Setup authentication based on config.'''
        auth_type = self.config.get('auth_type', 'basic')
        self.session.verify = self.config.get('verify_ssl', True)
        
        if auth_type == 'oauth':
            self._setup_oauth()
        elif auth_type == 'basic':
            self._setup_basic_auth()
        else:
            raise ODataError(500, f"Unknown auth_type '{auth_type}'. Use 'oauth' or 'basic'.")
    
    def _setup_oauth(self):
        '''Setup OAuth 2.0 authentication.'''
        oauth_config = self.config.get('oauth', {})
        client_id = oauth_config.get('client_id')
        client_secret = oauth_config.get('client_secret')
        token_url = oauth_config.get('token_url')
        scope = oauth_config.get('scope')
        
        if not all([client_id, client_secret, token_url]):
            raise ODataError(500, "OAuth configuration incomplete")
        
        data = {'grant_type': 'client_credentials'}
        if scope:
            data['scope'] = scope
        
        response = requests.post(
            token_url,
            auth=(client_id, client_secret),
            data=data,
            verify=self.session.verify
        )
        response.raise_for_status()
        
        token_data = response.json()
        access_token = token_data.get('access_token')
        
        if not access_token:
            raise ODataError(500, "No access_token in OAuth response")
        
        self.session.headers.update({'Authorization': f"Bearer {access_token}"})
    
    def _setup_basic_auth(self):
        '''Setup Basic authentication.'''
        basic_config = self.config.get('basic', {})
        username = basic_config.get('username')
        password = basic_config.get('password')
        
        if not username or not password:
            raise ODataError(500, "Basic auth configuration incomplete")
        
        self.session.auth = (username, password)
    
    def _load_metadata(self):
        '''Load entity, action, and navigation metadata.'''
        self.entities = {}
        self.entity_sets = {}
        self.actions = {'bound': {}, 'unbound': {}}
        self.navigations = {}
        
        if ENTITIES_PATH.exists():
            with open(ENTITIES_PATH) as f:
                data = json.load(f)
            self.entities = data.get('entity_types', {})
            self.entity_sets = data.get('entity_sets', {})
        
        if ACTIONS_PATH.exists():
            with open(ACTIONS_PATH) as f:
                data = json.load(f)
            self.actions['unbound'] = data.get('unbound_actions', {})
            self.actions['bound'] = data.get('bound_actions', {})
        
        if NAVIGATIONS_PATH.exists():
            with open(NAVIGATIONS_PATH) as f:
                data = json.load(f)
            self.navigations = data.get('navigations', {})
    
    # =========================================================================
    # URL Building
    # =========================================================================
    
    def _get_base_url(self, domain: str = None) -> str:
        '''Get base URL for an OData domain.'''
        domain = domain or self.default_domain
        odata_base = self.config.get('odata_base_url', '')
        odata_base = self.config.get('odata_base_url', '').rstrip('/')
        # Remove version suffix to use latest API
        import re
        odata_base = re.sub(r'/v\d+$', '', odata_base)
        return f"{odata_base}/{domain}"
    
    def _build_url(self, entity_set: str, entity_id: str = None, 
                   domain: str = None, **query_options) -> str:
        '''Build full URL with OData query options.'''
        base_url = self._get_base_url(domain)
        
        if entity_id:
            url = f"{base_url}/{entity_set}('{entity_id}')"
        else:
            url = f"{base_url}/{entity_set}"
        
        params = []
        
        # OData query options
        if query_options.get('$filter'):
            params.append(f"$filter={urllib.parse.quote(query_options['$filter'])}")
        if query_options.get('$select'):
            params.append(f"$select={query_options['$select']}")
        if query_options.get('$expand'):
            params.append(f"$expand={query_options['$expand']}")
        if query_options.get('$orderby'):
            params.append(f"$orderby={query_options['$orderby']}")
        if query_options.get('$top'):
            params.append(f"$top={query_options['$top']}")
        if query_options.get('$skip'):
            params.append(f"$skip={query_options['$skip']}")
        if query_options.get('$search'):
            params.append(f"$search={urllib.parse.quote(query_options['$search'])}")
        if query_options.get('$count'):
            params.append(f"$count={query_options['$count']}")
        
        if params:
            url += '?' + '&'.join(params)
        
        return url
    
    # =========================================================================
    # CSRF Token Management
    # =========================================================================
    
    def get_csrf_token(self) -> str:
        '''
        Get CSRF token for write operations.
        
        Returns:
            CSRF token string
        '''
        if self.csrf_token:
            return self.csrf_token
        
        # Fetch CSRF token from the server
        url = f"{self.config.get('odata_base_url', '')}/ProdMgmt/Parts?$top=1"
        
        response = self.session.get(url)
        
        # Extract CSRF token from response headers
        self.csrf_token = response.headers.get('CSRF_NONCE')
        if not self.csrf_token:
            self.csrf_token = response.headers.get('X-PTC-CSRF-Token')
        
        return self.csrf_token
    
    def _add_csrf_header(self) -> dict:
        '''Get headers with CSRF token for write operations.'''
        token = self.get_csrf_token()
        return {"CSRF_NONCE": token} if token else {}
    
    # =========================================================================
    # Core HTTP Operations
    # =========================================================================
    
    def _request(self, method: str, url: str, **kwargs) -> dict:
        '''Make HTTP request and handle response.'''
        headers = kwargs.pop('headers', {})
        headers.update({'Accept': 'application/json'})
        
        response = self.session.request(method, url, headers=headers, **kwargs)
        
        if response.status_code >= 400:
            error_detail = {}
            try:
                error_detail = response.json()
            except:
                pass
            raise ODataError(
                response.status_code,
                f"Request failed: {response.reason}",
                error_detail
            )
        
        if response.status_code == 204:
            return {}
        
        return response.json()
    
    # =========================================================================
    # Entity Operations
    # =========================================================================
    
    def query_entities(self, entity_set: str, domain: str = None,
                       filter_expr: str = None, select: str = None,
                       expand: str = None, orderby: str = None,
                       top: int = None, skip: int = None,
                       search: str = None, count: bool = None) -> List[dict]:
        '''
        Query entities with OData options.
        
        Args:
            entity_set: Entity set name (e.g., 'Parts', 'Documents')
            domain: OData domain (default: client's default_domain)
            filter_expr: OData $filter expression
            select: Comma-separated properties to select
            expand: Navigation properties to expand
            orderby: Order by expression
            top: Maximum number of results
            skip: Number of results to skip
            search: Search term
            count: Include total count
        
        Returns:
            List of entity dictionaries
        '''
        url = self._build_url(
            entity_set,
            domain=domain,
            **{'$filter': filter_expr, '$select': select, '$expand': expand,
               '$orderby': orderby, '$top': top, '$skip': skip,
               '$search': search, '$count': count}
        )
        
        data = self._request('GET', url)
        return data.get('value', [])
    
    def get_entity(self, entity_set: str, entity_id: str,
                   domain: str = None, select: str = None,
                   expand: str = None) -> dict:
        '''
        Get a single entity by ID.
        
        Args:
            entity_set: Entity set name
            entity_id: Entity ID
            domain: OData domain
            select: Properties to select
            expand: Navigation properties to expand
        
        Returns:
            Entity dictionary
        '''
        url = self._build_url(
            entity_set,
            entity_id=entity_id,
            domain=domain,
            **{'$select': select, '$expand': expand}
        )
        
        return self._request('GET', url)
    
    def create_entity(self, entity_set: str, entity_data: dict,
                      domain: str = None) -> dict:
        '''
        Create a new entity.
        
        Args:
            entity_set: Entity set name
            entity_data: Entity properties
            domain: OData domain
        
        Returns:
            Created entity
        '''
        url = self._build_url(entity_set, domain=domain)
        
        headers = self._add_csrf_header()
        headers['Content-Type'] = 'application/json'
        
        return self._request('POST', url, json=entity_data, headers=headers)
    
    def update_entity(self, entity_set: str, entity_id: str,
                      entity_data: dict, domain: str = None) -> dict:
        '''
        Update an existing entity.
        
        Args:
            entity_set: Entity set name
            entity_id: Entity ID
            entity_data: Updated properties
            domain: OData domain
        
        Returns:
            Updated entity
        '''
        url = self._build_url(entity_set, entity_id=entity_id, domain=domain)
        
        headers = self._add_csrf_header()
        headers['Content-Type'] = 'application/json'
        
        return self._request('PATCH', url, json=entity_data, headers=headers)
    
    def delete_entity(self, entity_set: str, entity_id: str,
                      domain: str = None) -> bool:
        '''
        Delete an entity.
        
        Args:
            entity_set: Entity set name
            entity_id: Entity ID
            domain: OData domain
        
        Returns:
            True if deleted successfully
        '''
        url = self._build_url(entity_set, entity_id=entity_id, domain=domain)
        
        headers = self._add_csrf_header()
        
        self._request('DELETE', url, headers=headers)
        return True
    
    # =========================================================================
    # Navigation Properties
    # =========================================================================
    
    def get_navigation(self, entity_set: str, entity_id: str,
                       navigation: str, domain: str = None,
                       select: str = None, expand: str = None) -> Union[dict, List[dict]]:
        '''
        Get navigation property value.
        
        Args:
            entity_set: Entity set name
            entity_id: Entity ID
            navigation: Navigation property name
            domain: OData domain
            select: Properties to select
            expand: Navigation properties to expand
        
        Returns:
            Navigation property value (single entity or collection)
        '''
        url = self._build_url(
            entity_set,
            entity_id=entity_id,
            domain=domain,
            **{'$select': select, '$expand': expand}
        )
        url += f"/{navigation}"
        
        data = self._request('GET', url)
        return data.get('value', data)
    
    def get_navigation_info(self, entity_type: str = None) -> dict:
        '''
        Get navigation property metadata.
        
        Args:
            entity_type: Entity type name (optional, returns all if not specified)
        
        Returns:
            Navigation property metadata
        '''
        if entity_type:
            return self.navigations.get(entity_type, {})
        return self.navigations
    
    # =========================================================================
    # Actions
    # =========================================================================
    
    def invoke_action(self, action_name: str, parameters: dict = None,
                      entity_id: str = None, entity_type: str = None,
                      domain: str = None) -> Union[dict, List[dict]]:
        '''
        Invoke an OData action.
        
        Args:
            action_name: Action name
            parameters: Action parameters
            entity_id: Entity ID for bound actions
            entity_type: Entity type for bound actions
            domain: OData domain
        
        Returns:
            Action result
        '''
        # Find action metadata
        action_info = None
        
        # Check bound actions first
        if entity_type:
            for bound_type, actions in self.actions['bound'].items():
                if action_name in actions:
                    action_info = actions[action_name]
                    break
        
        # Check unbound actions
        if not action_info:
            action_info = self.actions['unbound'].get(action_name)
        
        # Build URL
        if entity_id and entity_type:
            # Bound action
            entity_set = f"{entity_type}s"  # Simple pluralization
            url = self._build_url(entity_set, entity_id=entity_id, domain=domain)
            url += f"/{action_name}"
        else:
            # Unbound action
            base_url = self._get_base_url(domain)
            url = f"{base_url}/{action_name}"
        
        headers = self._add_csrf_header()
        headers['Content-Type'] = 'application/json'
        
        body = parameters or {}
        
        return self._request('POST', url, json=body, headers=headers)
    
    def get_action_info(self, action_name: str = None) -> dict:
        '''
        Get action metadata.
        
        Args:
            action_name: Action name (optional, returns all if not specified)
        
        Returns:
            Action metadata
        '''
        if action_name:
            # Search in both bound and unbound
            for action_type, actions in self.actions['bound'].items():
                if action_name in actions:
                    return actions[action_name]
            return self.actions['unbound'].get(action_name, {})
        return self.actions
    
    def list_actions(self, bound: bool = True, unbound: bool = True) -> List[str]:
        '''
        List available actions.
        
        Args:
            bound: Include bound actions
            unbound: Include unbound actions
        
        Returns:
            List of action names
        '''
        actions = []
        
        if unbound:
            actions.extend(self.actions['unbound'].keys())
        
        if bound:
            for action_type, type_actions in self.actions['bound'].items():
                actions.extend(type_actions.keys())
        
        return sorted(set(actions))
    
    # =========================================================================
    # Entity Set Information
    # =========================================================================
    
    def list_entity_sets(self, domain: str = None) -> List[str]:
        '''
        List available entity sets.
        
        Args:
            domain: OData domain (optional)
        
        Returns:
            List of entity set names
        '''
        return list(self.entity_sets.keys())
    
    def get_entity_info(self, entity_type: str = None) -> dict:
        '''
        Get entity type metadata.
        
        Args:
            entity_type: Entity type name (optional)
        
        Returns:
            Entity type metadata
        '''
        if entity_type:
            return self.entities.get(entity_type, {})
        return self.entities
    
    # =========================================================================
    # Generic Query and Search
    # =========================================================================
    
    def query(self, entity_set: str, domain: str = None, **kwargs) -> List[dict]:
        '''
        Generic query method (alias for query_entities).
        
        Args:
            entity_set: Entity set name
            domain: OData domain
            **kwargs: OData query options
        
        Returns:
            List of entities
        '''
        return self.query_entities(entity_set, domain=domain, **kwargs)
    
    def search(self, entity_set: str, search_term: str,
               domain: str = None, top: int = 50) -> List[dict]:
        '''
        Search entities by term using Windchill full-text search.

        IMPORTANT: This uses $search (full-text search) which searches across ALL fields
        (Name, Number, Description, etc.) and matches substrings anywhere.

        For field-specific filtering, use query_entities() with filter_expr instead:

        Example - Search only Name field:
            results = client.query_entities('Parts', filter_expr="contains(Name, 'engine')")

        Example - Search only Number field:
            results = client.query_entities('Parts', filter_expr="contains(Number, 'ASM')")

        Args:
            entity_set: Entity set name (e.g., 'Parts', 'Documents')
            search_term: Search term (full-text search across all fields)
            domain: OData domain (e.g., 'ProdMgmt', 'DocMgmt')
            top: Maximum results

        Returns:
            List of matching entities
        '''
        return self.query_entities(
            entity_set,
            domain=domain,
            search=search_term,
            top=top
        )

    # =========================================================================
    # Generic Object Operations
    # =========================================================================
    
    def get_object(self, entity_set: str, object_id: str,
                   domain: str = None, expand: str = None) -> dict:
        '''
        Get object by ID (alias for get_entity).
        
        Args:
            entity_set: Entity set name
            object_id: Object ID
            domain: OData domain
            expand: Navigation properties to expand
        
        Returns:
            Object dictionary
        '''
        return self.get_entity(entity_set, object_id, domain=domain, expand=expand)
    
    def create_object(self, entity_set: str, object_data: dict,
                      domain: str = None) -> dict:
        '''
        Create object (alias for create_entity).
        
        Args:
            entity_set: Entity set name
            object_data: Object properties
            domain: OData domain
        
        Returns:
            Created object
        '''
        return self.create_entity(entity_set, object_data, domain=domain)
    
    def update_object(self, entity_set: str, object_id: str,
                      object_data: dict, domain: str = None) -> dict:
        '''
        Update object (alias for update_entity).
        
        Args:
            entity_set: Entity set name
            object_id: Object ID
            object_data: Updated properties
            domain: OData domain
        
        Returns:
            Updated object
        '''
        return self.update_entity(entity_set, object_id, object_data, domain=domain)
    
    # =========================================================================
    # Related Products
    # =========================================================================
    
    def get_primary_related_product(self, entity_set: str, entity_id: str,
                                     domain: str = None) -> dict:
        '''
        Get primary related product.
        
        Args:
            entity_set: Entity set name
            entity_id: Entity ID
            domain: OData domain
        
        Returns:
            Primary related product
        '''
        return self.get_navigation(entity_set, entity_id, 'PrimaryRelatedProduct', domain)
    
    def get_additional_related_products(self, entity_set: str, entity_id: str,
                                         domain: str = None) -> List[dict]:
        '''
        Get additional related products.
        
        Args:
            entity_set: Entity set name
            entity_id: Entity ID
            domain: OData domain
        
        Returns:
            List of related products
        '''
        return self.get_navigation(entity_set, entity_id, 'AdditionalRelatedProducts', domain)
    
    def create_related_product(self, entity_set: str, entity_id: str,
                                related_product_data: dict, domain: str = None) -> dict:
        '''
        Create related product association.
        
        Args:
            entity_set: Entity set name
            entity_id: Entity ID
            related_product_data: Related product data
            domain: OData domain
        
        Returns:
            Created related product
        '''
        url = self._build_url(entity_set, entity_id=entity_id, domain=domain)
        url += '/RelatedProducts'
        
        headers = self._add_csrf_header()
        headers['Content-Type'] = 'application/json'
        
        return self._request('POST', url, json=related_product_data, headers=headers)
    
    def update_related_product(self, entity_set: str, entity_id: str,
                                related_product_id: str, related_product_data: dict,
                                domain: str = None) -> dict:
        '''
        Update related product.
        
        Args:
            entity_set: Entity set name
            entity_id: Entity ID
            related_product_id: Related product ID
            related_product_data: Updated data
            domain: OData domain
        
        Returns:
            Updated related product
        '''
        url = self._build_url(entity_set, entity_id=entity_id, domain=domain)
        url += f"/RelatedProducts('{related_product_id}')"
        
        headers = self._add_csrf_header()
        headers['Content-Type'] = 'application/json'
        
        return self._request('PATCH', url, json=related_product_data, headers=headers)
    
    def delete_related_product(self, entity_set: str, entity_id: str,
                                related_product_id: str, domain: str = None) -> bool:
        '''
        Delete related product association.
        
        Args:
            entity_set: Entity set name
            entity_id: Entity ID
            related_product_id: Related product ID
            domain: OData domain
        
        Returns:
            True if deleted
        '''
        url = self._build_url(entity_set, entity_id=entity_id, domain=domain)
        url += f"/RelatedProducts('{related_product_id}')"
        
        headers = self._add_csrf_header()
        
        self._request('DELETE', url, headers=headers)
        return True
    
    # =========================================================================
    # Constraints and Properties
    # =========================================================================
    
    def get_constraints(self, entity_set: str, entity_id: str,
                        domain: str = None) -> dict:
        '''
        Get entity constraints.
        
        Args:
            entity_set: Entity set name
            entity_id: Entity ID
            domain: OData domain
        
        Returns:
            Constraints dictionary
        '''
        return self.get_navigation(entity_set, entity_id, 'Constraints', domain)
    
    def get_driver_properties(self, entity_set: str, entity_id: str,
                               domain: str = None) -> dict:
        '''
        Get driver properties.
        
        Args:
            entity_set: Entity set name
            entity_id: Entity ID
            domain: OData domain
        
        Returns:
            Driver properties
        '''
        return self.get_navigation(entity_set, entity_id, 'DriverProperties', domain)
    
    def get_pregenerated_value(self, entity_set: str, entity_id: str,
                                attribute_name: str, domain: str = None) -> dict:
        '''
        Get pre-generated value for attribute.
        
        Args:
            entity_set: Entity set name
            entity_id: Entity ID
            attribute_name: Attribute name
            domain: OData domain
        
        Returns:
            Pre-generated value
        '''
        url = self._build_url(entity_set, entity_id=entity_id, domain=domain)
        url += f"/GetPregeneratedValue(Attribute='{attribute_name}')"
        
        return self._request('GET', url)


# =============================================================================
# Factory Function
# =============================================================================

def create_client(config_path: str = None, base_url: str = None,
                  username: str = None, password: str = None,
                  domain: str = 'ProdMgmt') -> WindchillBaseClient:
    '''
    Factory function to create a Windchill client.
    
    Args:
        config_path: Path to config.json
        base_url: Windchill server URL
        username: Username
        password: Password
        domain: Default OData domain
    
    Returns:
        WindchillBaseClient instance
    '''
    return WindchillBaseClient(
        config_path=config_path,
        base_url=base_url,
        username=username,
        password=password,
        domain=domain
    )


# =============================================================================
# CLI Entry Point
# =============================================================================

def main():
    '''CLI entry point for base client testing.'''
    import argparse
    
    parser = argparse.ArgumentParser(description='Windchill Base Client')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--list-entity-sets', action='store_true', help='List entity sets')
    parser.add_argument('--list-actions', action='store_true', help='List actions')
    parser.add_argument('--get-csrf', action='store_true', help='Get CSRF token')
    
    args = parser.parse_args()
    
    client = create_client(config_path=args.config)
    
    if args.list_entity_sets:
        print("Entity Sets:")
        for es in client.list_entity_sets():
            print(f"  - {es}")
    
    if args.list_actions:
        print("Actions:")
        for action in client.list_actions():
            print(f"  - {action}")
    
    if args.get_csrf:
        token = client.get_csrf_token()
        print(f"CSRF Token: {token}")


if __name__ == '__main__':
    main()
