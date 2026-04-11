#!/usr/bin/env python3
"""
Windchill PLM OData REST API Client
Comprehensive client supporting all OData operations for Windchill PLM

Supports:
- Entity queries (GET, $filter, $expand, $select, $orderby, $top, $skip)
- Navigation property expansion
- Bound and Unbound Actions
- CSRF token management
- CRUD operations
- BOM queries and traversal
"""

import json
import sys
import urllib.parse
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import requests

# Default paths
SKILL_DIR = Path(__file__).parent.parent
CONFIG_PATH = SKILL_DIR / "config.json"
ENTITIES_PATH = SKILL_DIR / "references" / "entities.json"
ACTIONS_PATH = SKILL_DIR / "references" / "actions.json"
NAVIGATIONS_PATH = SKILL_DIR / "references" / "navigations.json"


class ODataError(Exception):
    """Exception for OData API errors"""
    def __init__(self, status_code: int, message: str, details: dict = None):
        self.status_code = status_code
        self.message = message
        self.details = details or {}
        super().__init__(f"OData Error {status_code}: {message}")


class WindchillODataClient:
    """
    Client for PTC Windchill PLM OData REST API
    
    Provides comprehensive OData operations including:
    - Entity queries with full OData query options
    - Navigation property traversal
    - Action invocation (bound and unbound)
    - CRUD operations
    - BOM structure queries
    """
    
    def __init__(self, config_path: str = None, 
                 base_url: str = None, 
                 username: str = None, 
                 password: str = None,
                 domain: str = "ProdMgmt"):
        """
        Initialize client with configuration or direct credentials.
        
        Args:
            config_path: Path to config.json (optional)
            base_url: Direct Windchill server URL (optional)
            username: Direct username (optional)
            password: Direct password (optional)
            domain: Default OData domain (default: ProdMgmt)
        """
        self.session = requests.Session()
        self.csrf_token = None
        self.default_domain = domain
        
        # Load configuration
        if base_url and username and password:
            self.config = {
                "server_url": base_url,
                "odata_base_url": f"{base_url.rstrip('/')}/servlet/odata",
                "auth_type": "basic",
                "basic": {"username": username, "password": password},
                "verify_ssl": True
            }
            self.config_path = None
        else:
            self.config_path = Path(config_path) if config_path else CONFIG_PATH
            self.config = self._load_config()
        
        self._setup_auth()
        self._load_metadata()
    
    def _load_config(self) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise ODataError(500, f"Config file not found at {self.config_path}")
        except json.JSONDecodeError as e:
            raise ODataError(500, f"Invalid JSON in config file: {e}")
    
    def _setup_auth(self):
        """Setup authentication based on config"""
        auth_type = self.config.get("auth_type", "basic")
        self.session.verify = self.config.get("verify_ssl", True)
        
        if auth_type == "oauth":
            self._setup_oauth()
        elif auth_type == "basic":
            self._setup_basic_auth()
        else:
            raise ODataError(500, f"Unknown auth_type '{auth_type}'. Use 'oauth' or 'basic'.")
    
    def _setup_oauth(self):
        """Setup OAuth 2.0 authentication"""
        oauth_config = self.config.get("oauth", {})
        client_id = oauth_config.get("client_id")
        client_secret = oauth_config.get("client_secret")
        token_url = oauth_config.get("token_url")
        scope = oauth_config.get("scope")
        
        if not all([client_id, client_secret, token_url]):
            raise ODataError(500, "OAuth configuration incomplete")
        
        data = {"grant_type": "client_credentials"}
        if scope:
            data["scope"] = scope
        
        response = requests.post(token_url, auth=(client_id, client_secret), 
                                data=data, verify=self.session.verify)
        response.raise_for_status()
        token_data = response.json()
        
        access_token = token_data.get("access_token")
        if not access_token:
            raise ODataError(500, "No access_token in OAuth response")
        
        self.session.headers.update({"Authorization": f"Bearer {access_token}"})
    
    def _setup_basic_auth(self):
        """Setup Basic authentication"""
        basic_config = self.config.get("basic", {})
        username = basic_config.get("username")
        password = basic_config.get("password")
        
        if not username or not password:
            raise ODataError(500, "Basic auth configuration incomplete")
        
        self.session.auth = (username, password)
    
    def _load_metadata(self):
        """Load entity, action, and navigation metadata"""
        self.entities = {}
        self.actions = {"bound": {}, "unbound": {}}
        self.navigations = {}
        
        # Load entities.json
        if ENTITIES_PATH.exists():
            with open(ENTITIES_PATH) as f:
                data = json.load(f)
                self.entities = data.get("entity_types", {})
                self.entity_sets = data.get("entity_sets", {})
        
        # Load actions.json
        if ACTIONS_PATH.exists():
            with open(ACTIONS_PATH) as f:
                data = json.load(f)
                self.actions["unbound"] = data.get("unbound_actions", {})
                self.actions["bound"] = data.get("bound_actions", {})
        
        # Load navigations.json
        if NAVIGATIONS_PATH.exists():
            with open(NAVIGATIONS_PATH) as f:
                data = json.load(f)
                self.navigations = data.get("navigations", {})
    
    # =========================================================================
    # URL Building
    # =========================================================================
    
    def _get_base_url(self, domain: str = None) -> str:
        """Get base URL for OData domain"""
        odata_base = self.config.get("odata_base_url", 
                                      self.config["server_url"] + "/servlet/odata")
        domain = domain or self.default_domain
        return f"{odata_base.rstrip('/')}/{domain}"
    
    def _build_url(self, endpoint: str, domain: str = None) -> str:
        """Build full URL for endpoint"""
        base = self._get_base_url(domain)
        return f"{base}/{endpoint.lstrip('/')}"
    
    def _build_query_url(self, entity_set: str, 
                         filter_expr: str = None,
                         expand: List[str] = None,
                         select: List[str] = None,
                         orderby: str = None,
                         top: int = None,
                         skip: int = None,
                         search: str = None,
                         domain: str = None) -> str:
        """
        Build URL with OData query options.
        
        Args:
            entity_set: Entity set name (e.g., "Parts")
            filter_expr: OData $filter expression
            expand: List of navigation properties to expand
            select: List of properties to select
            orderby: Order by expression
            top: Maximum number of results
            skip: Number of results to skip
            search: Search expression
            domain: OData domain (default: ProdMgmt)
        
        Returns:
            Full URL with query string
        """
        base = self._get_base_url(domain)
        url = f"{base}/{entity_set}"
        
        params = []
        
        if filter_expr:
            params.append(f"$filter={urllib.parse.quote(filter_expr)}")
        
        if expand:
            expand_str = ",".join(expand)
            params.append(f"$expand={expand_str}")
        
        if select:
            select_str = ",".join(select)
            params.append(f"$select={select_str}")
        
        if orderby:
            params.append(f"$orderby={urllib.parse.quote(orderby)}")
        
        if top is not None:
            params.append(f"$top={top}")
        
        if skip is not None:
            params.append(f"$skip={skip}")
        
        if search:
            params.append(f"$search={urllib.parse.quote(search)}")
        
        if params:
            url += "?" + "&".join(params)
        
        return url
    
    # =========================================================================
    # CSRF Token Management
    # =========================================================================
    
    def get_csrf_token(self, force_refresh: bool = False) -> str:
        """
        Get CSRF token for write operations.
        
        Args:
            force_refresh: Force refresh of cached token
        
        Returns:
            CSRF token string
        """
        if self.csrf_token and not force_refresh:
            return self.csrf_token
        
        odata_base = self.config.get("odata_base_url",
                                      self.config["server_url"] + "/servlet/odata")
        url = f"{odata_base.rstrip('/')}/PTC/GetCSRFToken()"
        
        response = self.session.get(url)
        response.raise_for_status()
        
        data = response.json()
        self.csrf_token = data.get("NonceValue")
        
        if not self.csrf_token:
            raise ODataError(500, "No NonceValue in CSRF token response")
        
        return self.csrf_token
    
    def _add_csrf_header(self) -> dict:
        """Add CSRF token to headers"""
        token = self.get_csrf_token()
        return {"X-PTC-CSRF-Token": token}
    
    # =========================================================================
    # Core Query Methods
    # =========================================================================
    
    def query_entities(self, entity_set: str,
                       filter_expr: str = None,
                       expand: List[str] = None,
                       select: List[str] = None,
                       orderby: str = None,
                       top: int = None,
                       skip: int = None,
                       search: str = None,
                       domain: str = None) -> List[dict]:
        """
        Query entities from an entity set with OData options.
        
        Args:
            entity_set: Entity set name (e.g., "Parts")
            filter_expr: OData $filter expression
            expand: List of navigation properties to expand
            select: List of properties to select
            orderby: Order by expression
            top: Maximum number of results
            skip: Number of results to skip
            search: Search expression
            domain: OData domain (default: ProdMgmt)
        
        Returns:
            List of entity dictionaries
        """
        url = self._build_query_url(entity_set, filter_expr, expand, select, 
                                     orderby, top, skip, search, domain)
        
        response = self.session.get(url)
        
        if response.status_code != 200:
            self._handle_error(response)
        
        data = response.json()
        return data.get("value", [])
    
    def get_entity(self, entity_set: str, 
                   entity_id: str,
                   expand: List[str] = None,
                   select: List[str] = None,
                   domain: str = None) -> dict:
        """
        Get a single entity by ID.
        
        Args:
            entity_set: Entity set name (e.g., "Parts")
            entity_id: Entity ID (e.g., "OR:wt.part.WTPart:12345")
            expand: List of navigation properties to expand
            select: List of properties to select
            domain: OData domain (default: ProdMgmt)
        
        Returns:
            Entity dictionary
        """
        # URL encode the ID
        encoded_id = urllib.parse.quote(entity_id, safe='')
        url = self._get_base_url(domain) + f"/{entity_set}('{encoded_id}')"
        
        params = []
        if expand:
            params.append(f"$expand={','.join(expand)}")
        if select:
            params.append(f"$select={','.join(select)}")
        
        if params:
            url += "?" + "&".join(params)
        
        response = self.session.get(url)
        
        if response.status_code != 200:
            self._handle_error(response)
        
        return response.json()
    
    def get_navigation(self, entity_set: str,
        entity_id: str,
        navigation: str,
        filter_expr: str = None,
        expand: List[str] = None,
        select: List[str] = None,
        orderby: str = None,
        top: int = None,
        skip: int = None,
        domain: str = None,
        is_collection: bool = None) -> Union[dict, List[dict]]:
        """
        Get entities via navigation property.

        Args:
            entity_set: Entity set name (e.g., "Parts")
            entity_id: Entity ID
            navigation: Navigation property name (e.g., "Uses", "UsedBy")
            filter_expr: OData $filter expression
            expand: List of navigation properties to expand
            select: List of properties to select
            orderby: OData $orderby expression
            top: Maximum number of results (only for collection navigations)
            skip: Number of results to skip (only for collection navigations)
            domain: OData domain (default: ProdMgmt)
            is_collection: Override auto-detection of collection vs single entity

        Returns:
            Single entity or list of entities depending on navigation cardinality
        """
        encoded_id = urllib.parse.quote(entity_id, safe='')
        url = self._get_base_url(domain) + f"/{entity_set}('{encoded_id}')/{navigation}"

        # Check if this navigation returns a collection
        if is_collection is None:
            # Try to determine from metadata
            nav_info = self.get_navigation_info(entity_set.rstrip('s'), navigation)
            is_collection = nav_info.get('is_collection', True) if nav_info else True

        params = []
        if filter_expr:
            params.append(f"$filter={urllib.parse.quote(filter_expr)}")
        if expand:
            params.append(f"$expand={','.join(expand)}")
        if select:
            params.append(f"$select={','.join(select)}")
        # Only add $top, $skip, $orderby for collection navigations
        if is_collection:
            if orderby:
                params.append(f"$orderby={orderby}")
            if top is not None:
                params.append(f"$top={top}")
            if skip is not None:
                params.append(f"$skip={skip}")

        if params:
            url += "?" + "&".join(params)

        response = self.session.get(url)

        if response.status_code != 200:
            self._handle_error(response)

        data = response.json()
        # Navigation can return single entity or collection
        if "value" in data:
            return data["value"]
        return data
    
    # =========================================================================
    # Action Methods
    # =========================================================================
    
    def invoke_action(self, action_name: str,
                      parameters: dict = None,
                      entity_id: str = None,
                      entity_type: str = None,
                      domain: str = None) -> Union[dict, List[dict]]:
        """
        Invoke an OData action (bound or unbound).
        
        For bound actions, provide entity_id and entity_type.
        For unbound actions, omit entity_id.
        
        Args:
            action_name: Action name
            parameters: Action parameters
            entity_id: Entity ID for bound actions
            entity_type: Entity type for bound actions (e.g., "Part")
            domain: OData domain (default: ProdMgmt)
        
        Returns:
            Action result
        """
        domain = domain or self.default_domain
        parameters = parameters or {}
        
        # Check if it's a bound action
        if action_name in self.actions["bound"]:
            action_info = self.actions["bound"][action_name]
            if not entity_id or not entity_type:
                raise ODataError(400, f"Action '{action_name}' is bound and requires entity_id and entity_type")
            
            # Build URL for bound action
            encoded_id = urllib.parse.quote(entity_id, safe='')
            url = self._get_base_url(domain) + f"/{entity_type}s('{encoded_id}')/{action_name}"
        else:
            # Unbound action
            url = self._get_base_url(domain) + f"/{action_name}"
        
        # Add CSRF token for POST
        headers = self._add_csrf_header()
        headers["Content-Type"] = "application/json"
        
        response = self.session.post(url, json=parameters, headers=headers)
        
        if response.status_code not in [200, 201, 204]:
            self._handle_error(response)
        
        if response.status_code == 204:
            return {"success": True}
        
        data = response.json()
        if "value" in data:
            return data["value"]
        return data
    
    # =========================================================================
    # CRUD Operations
    # =========================================================================
    
    def create_entity(self, entity_set: str,
                      data: dict,
                      domain: str = None) -> dict:
        """
        Create a new entity.
        
        Args:
            entity_set: Entity set name
            data: Entity data
            domain: OData domain
        
        Returns:
            Created entity
        """
        url = self._get_base_url(domain) + f"/{entity_set}"
        
        headers = self._add_csrf_header()
        headers["Content-Type"] = "application/json"
        
        response = self.session.post(url, json=data, headers=headers)
        
        if response.status_code not in [200, 201]:
            self._handle_error(response)
        
        return response.json()
    
    def update_entity(self, entity_set: str,
                      entity_id: str,
                      data: dict,
                      domain: str = None) -> dict:
        """
        Update an existing entity (PATCH).
        
        Args:
            entity_set: Entity set name
            entity_id: Entity ID
            data: Updated data
            domain: OData domain
        
        Returns:
            Updated entity
        """
        encoded_id = urllib.parse.quote(entity_id, safe='')
        url = self._get_base_url(domain) + f"/{entity_set}('{encoded_id}')"
        
        headers = self._add_csrf_header()
        headers["Content-Type"] = "application/json"
        
        response = self.session.patch(url, json=data, headers=headers)
        
        if response.status_code not in [200, 204]:
            self._handle_error(response)
        
        if response.status_code == 204:
            return {"success": True}
        return response.json()
    
    def delete_entity(self, entity_set: str,
                      entity_id: str,
                      domain: str = None) -> bool:
        """
        Delete an entity.
        
        Args:
            entity_set: Entity set name
            entity_id: Entity ID
            domain: OData domain
        
        Returns:
            True if deleted
        """
        encoded_id = urllib.parse.quote(entity_id, safe='')
        url = self._get_base_url(domain) + f"/{entity_set}('{encoded_id}')"
        
        headers = self._add_csrf_header()
        
        response = self.session.delete(url, headers=headers)
        
        if response.status_code not in [200, 204]:
            self._handle_error(response)
        
        return True
    
    # =========================================================================
    # Part-Specific Methods (ProdMgmt)
    # =========================================================================
    
    def get_part_by_number(self, part_number: str,
                           expand: List[str] = None,
                           select: List[str] = None) -> Optional[dict]:
        """
        Get a part by its number.
        
        Args:
            part_number: Part number
            expand: Navigation properties to expand
            select: Properties to select
        
        Returns:
            Part dictionary or None
        """
        parts = self.query_entities("Parts", 
                                     filter_expr=f"Number eq '{part_number}'",
                                     expand=expand,
                                     select=select,
                                     top=1)
        return parts[0] if parts else None
    
    def get_part_by_id(self, part_id: str,
                       expand: List[str] = None,
                       select: List[str] = None) -> dict:
        """
        Get a part by its ID.
        
        Args:
            part_id: Part ID (e.g., "OR:wt.part.WTPart:12345")
            expand: Navigation properties to expand
            select: Properties to select
        
        Returns:
            Part dictionary
        """
        return self.get_entity("Parts", part_id, expand=expand, select=select)
    
    def get_bom(self, part_id: str,
                expand_child: bool = True,
                select: List[str] = None) -> List[dict]:
        """
        Get Bill of Materials (Uses) for a part.
        
        Args:
            part_id: Part ID
            expand_child: Expand to include child part details
            select: Properties to select for child parts
        
        Returns:
            List of BOM items with child part details
        """
        if expand_child:
            if select:
                expand_str = [f"Uses($select={','.join(select)})"]
            else:
                expand_str = ["Uses"]
        else:
            expand_str = None
        
        uses = self.get_navigation("Parts", part_id, "Uses", expand=expand_str)
        
        # Transform into cleaner BOM structure
        bom_items = []
        for use in uses:
            child_part = use.get("Uses", {})
            bom_items.append({
                "use_id": use.get("ID"),
                "quantity": use.get("Quantity", 1.0),
                "unit": use.get("Unit", {}).get("Display", "each"),
                "line_number": use.get("LineNumber"),
                "child_part": {
                    "id": child_part.get("ID") if child_part else None,
                    "number": child_part.get("Number") if child_part else None,
                    "name": child_part.get("Name") if child_part else None,
                    "state": child_part.get("State", {}).get("Display") if child_part else None,
                    "type": child_part.get("ObjectType") if child_part else None
                }
            })
        
        return bom_items
    
    def get_where_used(self, part_id: str,
                        expand_parent: bool = True,
                        select: List[str] = None) -> List[dict]:
        """
        Get where-used (parent assemblies) for a part.
        
        Args:
            part_id: Part ID
            expand_parent: Expand to include parent part details
            select: Properties to select for parent parts
        
        Returns:
            List of parent assemblies
        """
        if expand_parent:
            expand_str = [f"UsedBy($select={','.join(select)})"] if select else ["UsedBy"]
        else:
            expand_str = None
        
        parents = self.get_navigation("Parts", part_id, "UsedBy", expand=expand_str)
        
        return parents
    
    def get_part_structure(self, part_id: str,
                           levels: int = 1,
                           include_details: bool = True) -> dict:
        """
        Get hierarchical part structure.
        
        Args:
            part_id: Part ID
            levels: Number of levels to traverse (1 = single level)
            include_details: Include part details for each node
        
        Returns:
            Hierarchical structure dictionary
        """
        def build_structure(pid: str, level: int) -> dict:
            if level > levels:
                return None
            
            # Get part details
            part = self.get_part_by_id(pid)
            
            structure = {
                "id": part.get("ID"),
                "number": part.get("Number"),
                "name": part.get("Name"),
                "state": part.get("State", {}).get("Display"),
                "type": part.get("ObjectType"),
                "children": []
            }
            
            if level < levels:
                # Get children
                bom = self.get_bom(pid, expand_child=True)
                for item in bom:
                    child_id = item.get("child_part", {}).get("id")
                    if child_id:
                        child_structure = build_structure(child_id, level + 1)
                        if child_structure:
                            child_structure["quantity"] = item.get("quantity")
                            structure["children"].append(child_structure)
            
            return structure
        
        return build_structure(part_id, 1)
    
    def search_parts(self, search_term: str,
                     top: int = 50,
                     expand: List[str] = None,
                     select: List[str] = None) -> List[dict]:
        """
        Search parts by number or name.
        
        Args:
            search_term: Search term
            top: Maximum results
            expand: Navigation properties to expand
            select: Properties to select
        
        Returns:
            List of matching parts
        """
        filter_expr = f"contains(Number, '{search_term}') or contains(Name, '{search_term}')"
        return self.query_entities("Parts", 
                                    filter_expr=filter_expr,
                                    top=top,
                                    expand=expand,
                                    select=select)
    
    def get_part_versions(self, part_id: str) -> List[dict]:
        """
        Get all versions of a part.
        
        Args:
            part_id: Part ID
        
        Returns:
            List of versions
        """
        return self.get_navigation("Parts", part_id, "Versions")
    
    def get_part_revisions(self, part_id: str) -> List[dict]:
        """
        Get all revisions of a part.
        
        Args:
            part_id: Part ID
        
        Returns:
            List of revisions
        """
        return self.get_navigation("Parts", part_id, "Revisions")
    
    def get_part_documents(self, part_id: str) -> List[dict]:
        """
        Get documents associated with a part (via DescribedBy).
        
        Args:
            part_id: Part ID
        
        Returns:
            List of associated documents
        """
        links = self.get_navigation("Parts", part_id, "DescribedBy", 
                                     expand=["DescribedBy"])
        
        documents = []
        for link in links:
            doc = link.get("DescribedBy", {})
            if doc:
                documents.append({
                    "id": doc.get("ID"),
                    "number": doc.get("Number"),
                    "name": doc.get("Name"),
                    "state": doc.get("State", {}).get("Display")
                })
        
        return documents
    
    # =========================================================================
    # Part Actions
    # =========================================================================
    
    def check_out_part(self, part_id: str, 
                       check_out_note: str = None) -> dict:
        """
        Check out a part.
        
        Args:
            part_id: Part ID
            check_out_note: Optional check-out note
        
        Returns:
            Updated part
        """
        params = {"CheckOutNote": check_out_note} if check_out_note else {}
        return self.invoke_action("CheckOut", parameters=params,
                                   entity_id=part_id, entity_type="Part")
    
    def check_in_part(self, part_id: str,
                      check_in_note: str = None,
                      keep_checked_out: bool = False) -> dict:
        """
        Check in a part.
        
        Args:
            part_id: Part ID
            check_in_note: Optional check-in note
            keep_checked_out: Keep part checked out
        
        Returns:
            Updated part
        """
        params = {"CheckInNote": check_in_note, "KeepCheckedOut": keep_checked_out}
        return self.invoke_action("CheckIn", parameters=params,
                                   entity_id=part_id, entity_type="Part")
    
    def revise_part(self, part_id: str,
                    version_id: str = None) -> dict:
        """
        Revise a part.
        
        Args:
            part_id: Part ID
            version_id: Optional version ID
        
        Returns:
            New revision
        """
        params = {"VersionId": version_id} if version_id else {}
        return self.invoke_action("Revise", parameters=params,
                                   entity_id=part_id, entity_type="Part")
    
    def set_part_state(self, part_id: str, state: str) -> dict:
        """
        Set lifecycle state of a part.
        
        Args:
            part_id: Part ID
            state: Target state value
        
        Returns:
            Updated part
        """
        return self.invoke_action("SetState", parameters={"State": state},
entity_id=part_id, entity_type="Part")

    # =========================================================================
    # Unbound Actions (ProdMgmt domain)
    # =========================================================================

    def create_associations(self, associations: List[dict]) -> List[dict]:
        """Create Part-Document associations.

        Args:
            associations: List of PartDocAssociation objects

        Returns:
            List of created associations
        """
        return self.invoke_action("CreateAssociations", 
            parameters={"PartDocAssociations": associations},
            domain="ProdMgmt")

    def delete_associations(self, associations: List[dict]) -> bool:
        """Delete Part-Document associations.

        Args:
            associations: List of PartDocAssociation objects to delete

        Returns:
            True if successful
        """
        self.invoke_action("DeleteAssociations",
            parameters={"PartDocAssociations": associations},
            domain="ProdMgmt")
        return True

    def move_associations(self, associations: List[dict]) -> List[dict]:
        """Move Part-Document associations.

        Args:
            associations: List of MovePartDocAssociation objects

        Returns:
            List of moved associations
        """
        return self.invoke_action("MoveAssociations",
            parameters={"MovePartDocAssociations": associations},
            domain="ProdMgmt")

    def set_state_managed_baselines(self, baselines: List[dict], state: str) -> List[dict]:
        """Set state for multiple ManagedBaselines.

        Args:
            baselines: List of ManagedBaseline objects
            state: Target state value

        Returns:
            List of updated baselines
        """
        return self.invoke_action("SetStateManagedBaselines",
            parameters={"ManagedBaselines": baselines, "State": state},
            domain="ProdMgmt")

    def set_state_supplier_parts(self, parts: List[dict], state: str) -> List[dict]:
        """Set state for multiple SupplierParts.

        Args:
            parts: List of SupplierPart objects
            state: Target state value

        Returns:
            List of updated parts
        """
        return self.invoke_action("SetStateSupplierParts",
            parameters={"SupplierParts": parts, "State": state},
            domain="ProdMgmt")

    # =========================================================================
    # Bound Actions - ManagedBaseline
    # =========================================================================

    def add_to_baseline(self, baseline_id: str, baselineables: List[dict]) -> dict:
        """Add items to a ManagedBaseline.

        Args:
            baseline_id: ManagedBaseline ID
            baselineables: List of objects to add

        Returns:
            Updated baseline
        """
        return self.invoke_action("AddToBaseline",
            parameters={"Baselineables": baselineables},
            entity_id=baseline_id, entity_type="ManagedBaseline")

    def remove_from_baseline(self, baseline_id: str, baselineables: List[dict]) -> dict:
        """Remove items from a ManagedBaseline.

        Args:
            baseline_id: ManagedBaseline ID
            baselineables: List of objects to remove

        Returns:
            Updated baseline
        """
        return self.invoke_action("RemoveFromBaseline",
            parameters={"Baselineables": baselineables},
            entity_id=baseline_id, entity_type="ManagedBaseline")

    # =========================================================================
    # Bound Actions - Part BOM Rollup
    # =========================================================================

    def get_multi_level_bom_rollup(self, part_id: str,
        navigation_criteria: dict = None,
        include_bom: bool = True,
        rollup_attributes: List[str] = None) -> dict:
        """Get multi-level BOM with rolled-up attributes.

        Args:
            part_id: Part ID
            navigation_criteria: Navigation criteria for BOM traversal
            include_bom: Include BOM structure in response
            rollup_attributes: Attributes to roll up

        Returns:
            BOM rollup with aggregated values
        """
        params = {
            "NavigationCriteria": navigation_criteria or {},
            "IncludeBOM": include_bom,
            "RollupAttributes": rollup_attributes or []
        }
        return self.invoke_action("GetMultiLevelBOMRollup",
            parameters=params,
            entity_id=part_id, entity_type="Part")

    def get_multi_level_components_report(self, part_id: str,
        navigation_criteria: dict = None,
        show_single_level: bool = False) -> List[dict]:
        """Get multi-level components report.

        Args:
            part_id: Part ID
            navigation_criteria: Navigation criteria
            show_single_level: Show single-level report only

        Returns:
            List of components with quantities
        """
        return self.invoke_action("GetMultiLevelComponentsReport",
            parameters={
                "NavigationCriteria": navigation_criteria or {},
                "ShowSingleLevelReport": show_single_level
            },
            entity_id=part_id, entity_type="Part")

    # =========================================================================
    # Batch Operations
    # =========================================================================
    
    def create_parts_batch(self, parts_data: List[dict]) -> List[dict]:
        """
        Create multiple parts in a batch.
        
        Args:
            parts_data: List of part data dictionaries
        
        Returns:
            List of created parts
        """
        return self.invoke_action("CreateParts", 
                                   parameters={"Parts": parts_data})
    
    def update_parts_batch(self, parts_data: List[dict]) -> List[dict]:
        """
        Update multiple parts in a batch.
        
        Args:
            parts_data: List of part data dictionaries with IDs
        
        Returns:
            List of updated parts
        """
        return self.invoke_action("UpdateParts",
                                   parameters={"Parts": parts_data})
    
    def delete_parts_batch(self, part_ids: List[str]) -> bool:
        """
        Delete multiple parts in a batch.
        
        Args:
            part_ids: List of part IDs
        
        Returns:
            True if successful
        """
        parts_data = [{"ID": pid} for pid in part_ids]
        self.invoke_action("DeleteParts", parameters={"Parts": parts_data})
        return True
    
    # =========================================================================
    # Error Handling
    # =========================================================================
    
    def _handle_error(self, response: requests.Response):
        """Handle HTTP error responses"""
        try:
            error_data = response.json()
            message = error_data.get("error", {}).get("message", response.text)
        except:
            message = response.text or f"HTTP {response.status_code}"
        
        raise ODataError(response.status_code, message, 
                        {"url": response.url, "response": response.text[:500]})
    
    # =========================================================================
    # Utility Methods
    # =========================================================================
    
    def get_entity_info(self, entity_name: str) -> Optional[dict]:
        """Get entity type information"""
        return self.entities.get(entity_name)
    
    def get_navigation_info(self, entity_name: str, nav_name: str) -> Optional[dict]:
        """Get navigation property information"""
        key = f"{entity_name}.{nav_name}"
        return self.navigations.get(key)
    
    def get_action_info(self, action_name: str) -> Optional[dict]:
        """Get action information"""
        if action_name in self.actions["bound"]:
            return self.actions["bound"][action_name]
        if action_name in self.actions["unbound"]:
            return self.actions["unbound"][action_name]
        return None
    
    def list_entity_sets(self) -> List[str]:
        """List available entity sets"""
        return list(self.entity_sets.keys())
    
    def list_actions(self, bound: bool = None) -> List[str]:
        """List available actions"""
        if bound is True:
            return list(self.actions["bound"].keys())
        elif bound is False:
            return list(self.actions["unbound"].keys())
        return list(self.actions["bound"].keys()) + list(self.actions["unbound"].keys())


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    """CLI interface for the OData client"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Windchill OData Client")
    parser.add_argument("--config", help="Config file path")
    parser.add_argument("--domain", default="ProdMgmt", help="OData domain")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query entities")
    query_parser.add_argument("entity_set", help="Entity set name")
    query_parser.add_argument("--filter", help="OData filter expression")
    query_parser.add_argument("--expand", help="Expand (comma-separated)")
    query_parser.add_argument("--select", help="Select (comma-separated)")
    query_parser.add_argument("--top", type=int, help="Max results")
    
    # Get command
    get_parser = subparsers.add_parser("get", help="Get single entity")
    get_parser.add_argument("entity_set", help="Entity set name")
    get_parser.add_argument("entity_id", help="Entity ID")
    get_parser.add_argument("--expand", help="Expand (comma-separated)")
    
    # BOM command
    bom_parser = subparsers.add_parser("bom", help="Get BOM")
    bom_parser.add_argument("part_id", help="Part ID")
    
    # Where-used command
    wu_parser = subparsers.add_parser("where-used", help="Get where-used")
    wu_parser.add_argument("part_id", help="Part ID")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search parts")
    search_parser.add_argument("term", help="Search term")
    search_parser.add_argument("--top", type=int, default=10, help="Max results")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List entity sets or actions")
    list_parser.add_argument("type", choices=["sets", "actions"], help="What to list")
    
    args = parser.parse_args()
    
    # Initialize client
    try:
        client = WindchillODataClient(config_path=args.config)
    except Exception as e:
        print(f"Error initializing client: {e}")
        sys.exit(1)
    
    # Execute command
    if args.command == "query":
        expand = args.expand.split(",") if args.expand else None
        select = args.select.split(",") if args.select else None
        results = client.query_entities(args.entity_set, 
                                         filter_expr=args.filter,
                                         expand=expand,
                                         select=select,
                                         top=args.top)
        print(json.dumps(results, indent=2))
    
    elif args.command == "get":
        expand = args.expand.split(",") if args.expand else None
        entity = client.get_entity(args.entity_set, args.entity_id, expand=expand)
        print(json.dumps(entity, indent=2))
    
    elif args.command == "bom":
        bom = client.get_bom(args.part_id)
        print(json.dumps(bom, indent=2))
    
    elif args.command == "where-used":
        parents = client.get_where_used(args.part_id)
        print(json.dumps(parents, indent=2))
    
    elif args.command == "search":
        results = client.search_parts(args.term, top=args.top)
        print(json.dumps(results, indent=2))
    
    elif args.command == "list":
        if args.type == "sets":
            for es in client.list_entity_sets():
                print(f"  {es}")
        else:
            for action in client.list_actions():
                print(f"  {action}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
