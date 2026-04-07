#!/usr/bin/env python3
"""
Windchill PLM REST API Client
Supports OAuth 2.0 and Basic Authentication
"""

import json
import sys
import argparse
from pathlib import Path
import requests

# Default config path relative to skill directory
CONFIG_PATH = Path(__file__).parent.parent / "config.json"


class WindchillClient:
    """Client for PTC Windchill PLM REST API"""

    def __init__(self, config_path=None, base_url=None, username=None, password=None):
        """Initialize client with configuration or direct credentials"""
        self.session = requests.Session()

        # If direct credentials provided, use them
        if base_url and username and password:
            self.config = {
                "server_url": base_url,
                "odata_base_url": base_url,
                "auth_type": "basic",
                "basic": {"username": username, "password": password},
                "verify_ssl": True
            }
        else:
            self.config_path = config_path or CONFIG_PATH
            self.config = self._load_config()

        self._setup_auth()

    def _load_config(self):
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Config file not found at {self.config_path}")
            print(f"Copy config.example.json to config.json and configure your settings.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in config file: {e}")
            sys.exit(1)

    def _setup_auth(self):
        """Setup authentication based on config"""
        auth_type = self.config.get("auth_type", "basic")
        verify_ssl = self.config.get("verify_ssl", True)
        self.session.verify = verify_ssl

        if auth_type == "oauth":
            self._setup_oauth()
        elif auth_type == "basic":
            self._setup_basic_auth()
        else:
            print(f"Error: Unknown auth_type '{auth_type}'. Use 'oauth' or 'basic'.")
            sys.exit(1)

    def _setup_oauth(self):
        """Setup OAuth 2.0 authentication"""
        oauth_config = self.config.get("oauth", {})
        client_id = oauth_config.get("client_id")
        client_secret = oauth_config.get("client_secret")
        token_url = oauth_config.get("token_url")
        scope = oauth_config.get("scope")

        if not all([client_id, client_secret, token_url]):
            print("Error: OAuth configuration incomplete. Need client_id, client_secret, and token_url.")
            sys.exit(1)

        # Request token
        auth = (client_id, client_secret)
        data = {"grant_type": "client_credentials"}
        if scope:
            data["scope"] = scope

        try:
            response = requests.post(token_url, auth=auth, data=data, verify=self.session.verify)
            response.raise_for_status()
            token_data = response.json()
            access_token = token_data.get("access_token")

            if not access_token:
                print("Error: No access_token in OAuth response")
                print(f"Response: {token_data}")
                sys.exit(1)

            self.session.headers.update({"Authorization": f"Bearer {access_token}"})
            print("[OK] OAuth authentication successful")

        except requests.RequestException as e:
            print(f"Error: OAuth token request failed: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            sys.exit(1)

    def _setup_basic_auth(self):
        """Setup Basic authentication"""
        basic_config = self.config.get("basic", {})
        username = basic_config.get("username")
        password = basic_config.get("password")

        if not username or not password:
            print("Error: Basic auth configuration incomplete. Need username and password.")
            sys.exit(1)

        self.session.auth = (username, password)
        print("[OK] Basic authentication configured")

    def _get_url(self, endpoint):
        """Build full URL for an endpoint"""
        server_url = self.config["server_url"]
        return f"{server_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def get_object(self, object_type, identifier=None, oid=None):
        """Get a Windchill object by type and identifier/oid"""
        if oid:
            url = self._get_url(f"api/v3/objects/{oid}")
        elif identifier:
            url = self._get_url(f"api/v3/objects/{object_type}/{identifier}")
        else:
            print("Error: Must provide either --oid or --identifier")
            return None

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            print(f"\n[OK] Retrieved {object_type}:")
            print(json.dumps(data, indent=2))
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to get object: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def search(self, object_type, criteria=None):
        """Search for Windchill objects"""
        url = self._get_url(f"api/v3/objects/{object_type}/search")

        params = {"type": object_type}
        if criteria:
            params.update(criteria)

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            results = data.get("items", [])
            print(f"\n[OK] Found {len(results)} {object_type} objects:")
            for item in results:
                print(f"  - {item.get('displayIdentifier')}: {item.get('name')}")
            return data
        except requests.RequestException as e:
            print(f"Error: Search failed: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def create_object(self, object_type, attributes):
        """Create a new Windchill object"""
        url = self._get_url(f"api/v3/objects/{object_type}")

        try:
            response = self.session.post(url, json=attributes)
            response.raise_for_status()
            data = response.json()
            print(f"\n[OK] Created {object_type}:")
            print(json.dumps(data, indent=2))
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to create object: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def update_object(self, oid, attributes):
        """Update an existing Windchill object"""
        url = self._get_url(f"api/v3/objects/{oid}")

        try:
            response = self.session.patch(url, json=attributes)
            response.raise_for_status()
            data = response.json()
            print(f"\n[OK] Updated object {oid}:")
            print(json.dumps(data, indent=2))
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to update object: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_bom(self, part_oid):
        """Get Bill of Materials for a part"""
        url = self._get_url(f"api/v3/parts/{part_oid}/bom")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            print(f"\n[OK] BOM for part {part_oid}:")
            print(json.dumps(data, indent=2))
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to get BOM: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_csrf_token(self):
        """Get CSRF token from PTC Common domain"""
        odata_base_url = self.config.get("odata_base_url", self.config["server_url"] + "/servlet/odata")
        url = f"{odata_base_url.rstrip('/')}/PTC/GetCSRFToken()"

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            token = data.get("NonceValue")
            print(f"\n[OK] CSRF Token: {token}")
            return token
        except requests.RequestException as e:
            print(f"Error: Failed to get CSRF token: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    # ==================== Generic Query Methods ====================

    def query(self, endpoint, params=None):
        """Generic query method for OData endpoints"""
        odata_base_url = self.config.get("odata_base_url", self.config["server_url"] + "/servlet/odata")
        url = f"{odata_base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error: Query failed: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    # ==================== Product Management (Parts) Methods ====================

    def _get_prodmgmt_url(self, endpoint):
        """Build full URL for ProdMgmt domain endpoint"""
        odata_base_url = self.config.get("odata_base_url", self.config["server_url"] + "/servlet/odata")
        return f"{odata_base_url.rstrip('/')}/ProdMgmt/{endpoint.lstrip('/')}"

    def get_part_by_number(self, part_number):
        """Get a part by its number"""
        url = self._get_prodmgmt_url("Parts")
        params = {"$filter": f"Number eq '{part_number}'", "$top": 1}

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            parts = data.get("value", [])
            return parts[0] if parts else None
        except requests.RequestException as e:
            print(f"Error: Failed to get part: {e}")
            return None

    def get_part_children(self, part_id):
        """Get child parts (Uses) for a part"""
        url = self._get_prodmgmt_url(f"Parts('{part_id}')/Uses")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            uses_data = response.json()
            uses_list = uses_data.get("value", [])

            # Build full result with child part details
            children_result = []
            for use in uses_list:
                child_part_id = use.get("Uses", {}).get("ID")
                if child_part_id:
                    child_part_url = self._get_prodmgmt_url(f"Parts('{child_part_id}')")
                    child_response = self.session.get(child_part_url)
                    if child_response.status_code == 200:
                        child_part = child_response.json()
                        children_result.append({
                            "usage": use,
                            "child_part": child_part
                        })
            return children_result
        except requests.RequestException as e:
            print(f"Error: Failed to get part children: {e}")
            return []

    def get_part_parents(self, part_id):
        """Get parent parts (UsedBy) for a part"""
        url = self._get_prodmgmt_url(f"Parts('{part_id}')/UsedBy")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])
        except requests.RequestException as e:
            print(f"Error: Failed to get part parents: {e}")
            return []

    # ==================== Document Management Methods ====================

    def _get_docmgmt_url(self, endpoint):
        """Build full URL for DocMgmt domain endpoint"""
        odata_base_url = self.config.get("odata_base_url", self.config["server_url"] + "/servlet/odata")
        return f"{odata_base_url.rstrip('/')}/DocMgmt/{endpoint.lstrip('/')}"

    def get_document_by_number(self, document_number):
        """Get a document by its number"""
        url = self._get_docmgmt_url("Documents")
        params = {"$filter": f"Number eq '{document_number}'", "$top": 1}

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            documents = data.get("value", [])
            return documents[0] if documents else None
        except requests.RequestException as e:
            print(f"Error: Failed to get document: {e}")
            return None

    def get_document_attachments(self, document_id):
        """Get attachments for a document"""
        from urllib.parse import quote
        encoded_doc_id = quote(document_id, safe='')
        url = self._get_docmgmt_url(f"Documents('{encoded_doc_id}')/Attachments")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])
        except requests.RequestException as e:
            print(f"Error: Failed to get document attachments: {e}")
            return []

    def get_document_primary_content(self, document_id):
        """Get primary content for a document"""
        from urllib.parse import quote
        encoded_doc_id = quote(document_id, safe='')
        url = self._get_docmgmt_url(f"Documents('{encoded_doc_id}')/PrimaryContent")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])
        except requests.RequestException as e:
            print(f"Error: Failed to get document primary content: {e}")
            return None

    def get_document_thumbnails(self, document_id):
        """Get thumbnails for a document"""
        from urllib.parse import quote
        encoded_doc_id = quote(document_id, safe='')
        url = self._get_docmgmt_url(f"Documents('{encoded_doc_id}')/Thumbnails")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])
        except requests.RequestException as e:
            print(f"Error: Failed to get document thumbnails: {e}")
            return []

    def get_document_versions(self, document_id):
        """Get all versions for a document"""
        from urllib.parse import quote
        encoded_doc_id = quote(document_id, safe='')
        url = self._get_docmgmt_url(f"Documents('{encoded_doc_id}')/Versions")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])
        except requests.RequestException as e:
            print(f"Error: Failed to get document versions: {e}")
            return []

    def query_suppliers(self, search_term=None, top=None, select=None):
        """Query Suppliers from SupplierMgmt domain"""
        odata_base_url = self.config.get("odata_base_url", self.config["server_url"] + "/servlet/odata")
        url = f"{odata_base_url.rstrip('/')}/SupplierMgmt/Suppliers"

        params = {}
        if search_term:
            params["$filter"] = f"contains(Name, '{search_term}') or contains(Number, '{search_term}')"
        if top:
            params["$top"] = top
        if select:
            params["$select"] = select

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            suppliers = data.get("value", [])
            print(f"\n[OK] Found {len(suppliers)} Suppliers:")
            for supplier in suppliers:
                print(f"  - {supplier.get('Number')}: {supplier.get('Name')} - {supplier.get('State', {}).get('Display', 'N/A')}")
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to query suppliers: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    # ==================== Manufacturing Process Management (MfgProcMgmt) Domain Methods ====================

    def _get_mfg_proc_mgmt_url(self, endpoint):
        """Build full URL for MfgProcMgmt domain endpoint"""
        odata_base_url = self.config.get("odata_base_url", self.config["server_url"] + "/servlet/odata")
        return f"{odata_base_url.rstrip('/')}/MfgProcMgmt/{endpoint.lstrip('/')}"

    def get_process_plan_by_number(self, plan_number):
        """Get a process plan by its number"""
        url = self._get_mfg_proc_mgmt_url("ProcessPlans")
        params = {"$filter": f"Number eq '{plan_number}'"}

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            plans = data.get("value", [])
            return plans[0] if plans else None
        except requests.RequestException as e:
            print(f"Error: Failed to get process plan: {e}")
            return None

    def get_process_plan_operations(self, plan_id):
        """Get operations for a process plan"""
        url = self._get_mfg_proc_mgmt_url(f"ProcessPlans('{plan_id}')/Operations")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])
        except requests.RequestException as e:
            print(f"Error: Failed to get process plan operations: {e}")
            return []

    def query_process_plans(self, filter_expr=None, top=None, select=None):
        """Query Process Plans from MfgProcMgmt domain"""
        url = self._get_mfg_proc_mgmt_url("ProcessPlans")

        params = {}
        if filter_expr:
            params["$filter"] = filter_expr
        if top:
            params["$top"] = top
        if select:
            params["$select"] = select

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            plans = data.get("value", [])
            print(f"\n[OK] Found {len(plans)} Process Plans:")
            for plan in plans:
                print(f"  - {plan.get('Number')}: {plan.get('Name')} - {plan.get('State', {}).get('Display', 'N/A')}")
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to query process plans: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    # ==================== Change Management Domain Methods ====================

    def _get_change_mgmt_url(self, endpoint):
        """Build full URL for ChangeMgmt domain endpoint"""
        odata_base_url = self.config.get("odata_base_url", self.config["server_url"] + "/servlet/odata")
        return f"{odata_base_url.rstrip('/')}/ChangeMgmt/{endpoint.lstrip('/')}"

    def get_change_notice_by_number(self, notice_number):
        """Get a change notice by its number"""
        url = self._get_change_mgmt_url("ChangeNotices")
        params = {"$filter": f"Number eq '{notice_number}'"}

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            notices = data.get("value", [])
            return notices[0] if notices else None
        except requests.RequestException as e:
            print(f"Error: Failed to get change notice: {e}")
            return None

    def get_change_request_by_number(self, request_number):
        """Get a change request by its number"""
        url = self._get_change_mgmt_url("ChangeRequests")
        params = {"$filter": f"Number eq '{request_number}'"}

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            requests_data = data.get("value", [])
            return requests_data[0] if requests_data else None
        except requests.RequestException as e:
            print(f"Error: Failed to get change request: {e}")
            return None

    def get_change_task_by_number(self, task_number):
        """Get a change task by its number"""
        url = self._get_change_mgmt_url("ChangeTasks")
        params = {"$filter": f"Number eq '{task_number}'"}

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            tasks = data.get("value", [])
            return tasks[0] if tasks else None
        except requests.RequestException as e:
            print(f"Error: Failed to get change task: {e}")
            return None

    def query_change_notices(self, filter_expr=None, top=None, select=None):
        """Query Change Notices from ChangeMgmt domain"""
        url = self._get_change_mgmt_url("ChangeNotices")

        params = {}
        if filter_expr:
            params["$filter"] = filter_expr
        if top:
            params["$top"] = top
        if select:
            params["$select"] = select

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            notices = data.get("value", [])
            print(f"\n[OK] Found {len(notices)} Change Notices:")
            for notice in notices:
                print(f"  - {notice.get('Number')}: {notice.get('Name')} - {notice.get('State', {}).get('Display', 'N/A')}")
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to query change notices: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def query_change_requests(self, filter_expr=None, top=None, select=None):
        """Query Change Requests from ChangeMgmt domain"""
        url = self._get_change_mgmt_url("ChangeRequests")

        params = {}
        if filter_expr:
            params["$filter"] = filter_expr
        if top:
            params["$top"] = top
        if select:
            params["$select"] = select

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            requests_data = data.get("value", [])
            print(f"\n[OK] Found {len(requests_data)} Change Requests:")
            for req in requests_data:
                print(f"  - {req.get('Number')}: {req.get('Name')} - {req.get('State', {}).get('Display', 'N/A')}")
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to query change requests: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_change_resulting_objects(self, change_id):
        """Get resulting objects from a change notice"""
        url = self._get_change_mgmt_url(f"ChangeNotices('{change_id}')/ResultingObjects")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])
        except requests.RequestException as e:
            print(f"Error: Failed to get resulting objects: {e}")
            return []

    def get_change_affected_objects(self, change_id):
        """Get affected objects from a change notice"""
        url = self._get_change_mgmt_url(f"ChangeNotices('{change_id}')/AffectedObjects")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])
        except requests.RequestException as e:
            print(f"Error: Failed to get affected objects: {e}")
            return []

    # ==================== CAD Document Management Domain Methods ====================

    def _get_cad_doc_mgmt_url(self, endpoint):
        """Build full URL for CADDocumentMgmt domain endpoint"""
        odata_base_url = self.config.get("odata_base_url", self.config["server_url"] + "/servlet/odata")
        return f"{odata_base_url.rstrip('/')}/CADDocumentMgmt/{endpoint.lstrip('/')}"

    def get_cad_document_by_number(self, cad_number):
        """Get a CAD document by its number"""
        url = self._get_cad_doc_mgmt_url("CADDocuments")
        params = {"$filter": f"Number eq '{cad_number}'"}

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            docs = data.get("value", [])
            return docs[0] if docs else None
        except requests.RequestException as e:
            print(f"Error: Failed to get CAD document: {e}")
            return None

    def get_cad_document_uses(self, cad_id):
        """Get CAD document uses (children/dependencies)"""
        url = self._get_cad_doc_mgmt_url(f"CADDocuments('{cad_id}')/Uses")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])
        except requests.RequestException as e:
            print(f"Error: Failed to get CAD uses: {e}")
            return []

    def get_cad_document_references(self, cad_id):
        """Get CAD document references"""
        url = self._get_cad_doc_mgmt_url(f"CADDocuments('{cad_id}')/References")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])
        except requests.RequestException as e:
            print(f"Error: Failed to get CAD references: {e}")
            return []

    def get_cad_document_structure(self, cad_id):
        """Get CAD structure for a CAD document"""
        url = self._get_cad_doc_mgmt_url(f"CADDocuments('{cad_id}')/CADStructure")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error: Failed to get CAD structure: {e}")
            return None

    def get_cad_document_drawings(self, cad_id):
        """Get associated drawings for a CAD document"""
        url = self._get_cad_doc_mgmt_url(f"CADDocuments('{cad_id}')/Drawings")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])
        except requests.RequestException as e:
            print(f"Error: Failed to get CAD drawings: {e}")
            return []

    def get_cad_document_related_parts(self, cad_id):
        """Get parts related to a CAD document"""
        url = self._get_cad_doc_mgmt_url(f"CADDocuments('{cad_id}')/PartDocAssociations")
        params = {"$expand": "RelatedPart"}

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])
        except requests.RequestException as e:
            print(f"Error: Failed to get related parts: {e}")
            return []

    def query_cad_documents(self, filter_expr=None, top=None, select=None):
        """Query CAD Documents from CADDocumentMgmt domain"""
        url = self._get_cad_doc_mgmt_url("CADDocuments")

        params = {}
        if filter_expr:
            params["$filter"] = filter_expr
        if top:
            params["$top"] = top
        if select:
            params["$select"] = select

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            docs = data.get("value", [])
            print(f"\n[OK] Found {len(docs)} CAD Documents:")
            for doc in docs:
                print(f"  - {doc.get('Number')}: {doc.get('Name')} | {doc.get('FileName', 'N/A')}")
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to query CAD documents: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    # ==================== Data Administration Domain Methods ====================

    def _get_dataadmin_url(self, endpoint):
        """Build full URL for DataAdmin domain endpoint"""
        odata_base_url = self.config.get("odata_base_url", self.config["server_url"] + "/servlet/odata")
        return f"{odata_base_url.rstrip('/')}/DataAdmin/{endpoint.lstrip('/')}"

    def get_containers(self, filter_expr=None, top=None, select=None, expand=None):
        """Query Containers from DataAdmin domain"""
        url = self._get_dataadmin_url("Containers")

        params = {}
        if filter_expr:
            params["$filter"] = filter_expr
        if top:
            params["$top"] = top
        if select:
            params["$select"] = select
        if expand:
            params["$expand"] = expand

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            containers = data.get("value", [])
            print(f"\n[OK] Found {len(containers)} Containers:")
            for container in containers:
                print(f"  - {container.get('ID')}: {container.get('Name')} - {container.get('OrganizationName', 'N/A')}")
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to query containers: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_container_by_id(self, container_id, expand=None):
        """Get a specific container by ID"""
        url = self._get_dataadmin_url(f"Containers('{container_id}')")

        params = {}
        if expand:
            params["$expand"] = expand

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            print(f"\n[OK] Retrieved Container:")
            print(json.dumps(data, indent=2))
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to get container: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_products(self, filter_expr=None, top=None, select=None):
        """Query Product containers from DataAdmin domain"""
        url = self._get_dataadmin_url("Products")

        params = {}
        if filter_expr:
            params["$filter"] = filter_expr
        if top:
            params["$top"] = top
        if select:
            params["$select"] = select

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            products = data.get("value", [])
            print(f"\n[OK] Found {len(products)} Product Containers:")
            for product in products:
                print(f"  - {product.get('ID')}: {product.get('Name')}")
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to query products: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_libraries(self, filter_expr=None, top=None, select=None):
        """Query Library containers from DataAdmin domain"""
        url = self._get_dataadmin_url("Libraries")

        params = {}
        if filter_expr:
            params["$filter"] = filter_expr
        if top:
            params["$top"] = top
        if select:
            params["$select"] = select

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            libraries = data.get("value", [])
            print(f"\n[OK] Found {len(libraries)} Library Containers:")
            for library in libraries:
                print(f"  - {library.get('ID')}: {library.get('Name')}")
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to query libraries: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_projects(self, filter_expr=None, top=None, select=None):
        """Query Project containers from DataAdmin domain"""
        url = self._get_dataadmin_url("Projects")

        params = {}
        if filter_expr:
            params["$filter"] = filter_expr
        if top:
            params["$top"] = top
        if select:
            params["$select"] = select

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            projects = data.get("value", [])
            print(f"\n[OK] Found {len(projects)} Project Containers:")
            for project in projects:
                print(f"  - {project.get('ID')}: {project.get('Name')}")
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to query projects: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_org_containers(self, filter_expr=None, top=None, select=None):
        """Query Organization containers from DataAdmin domain"""
        url = self._get_dataadmin_url("Organizations")

        params = {}
        if filter_expr:
            params["$filter"] = filter_expr
        if top:
            params["$top"] = top
        if select:
            params["$select"] = select

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            orgs = data.get("value", [])
            print(f"\n[OK] Found {len(orgs)} Organization Containers:")
            for org in orgs:
                print(f"  - {org.get('ID')}: {org.get('Name')}")
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to query organization containers: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_sites(self, filter_expr=None, top=None, select=None):
        """Query Site containers from DataAdmin domain"""
        url = self._get_dataadmin_url("Sites")

        params = {}
        if filter_expr:
            params["$filter"] = filter_expr
        if top:
            params["$top"] = top
        if select:
            params["$select"] = select

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            sites = data.get("value", [])
            print(f"\n[OK] Found {len(sites)} Site Containers:")
            for site in sites:
                print(f"  - {site.get('ID')}: {site.get('Name')}")
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to query sites: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_folders(self, filter_expr=None, top=None, select=None, expand=None):
        """Query Folders from DataAdmin domain"""
        url = self._get_dataadmin_url("Folders")

        params = {}
        if filter_expr:
            params["$filter"] = filter_expr
        if top:
            params["$top"] = top
        if select:
            params["$select"] = select
        if expand:
            params["$expand"] = expand

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            folders = data.get("value", [])
            print(f"\n[OK] Found {len(folders)} Folders:")
            for folder in folders:
                print(f"  - {folder.get('ID')}: {folder.get('Name')} - {folder.get('Location', 'N/A')}")
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to query folders: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_folder_by_id(self, folder_id, expand=None):
        """Get a specific folder by ID"""
        url = self._get_dataadmin_url(f"Folders('{folder_id}')")

        params = {}
        if expand:
            params["$expand"] = expand

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            print(f"\n[OK] Retrieved Folder:")
            print(json.dumps(data, indent=2))
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to get folder: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def create_folder(self, name, description=None, parent_folder_id=None):
        """Create a new folder in DataAdmin domain"""
        url = self._get_dataadmin_url("Folders")

        data = {"Name": name}
        if description:
            data["Description"] = description

        # Add CSRF token for POST
        headers = {"Content-Type": "application/json"}
        token = self.get_csrf_token()
        if token:
            headers["X-CSRF-Token"] = token

        try:
            response = self.session.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            print(f"\n[OK] Created Folder:")
            print(json.dumps(result, indent=2))
            return result
        except requests.RequestException as e:
            print(f"Error: Failed to create folder: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def update_folder(self, folder_id, name=None, description=None):
        """Update an existing folder"""
        url = self._get_dataadmin_url(f"Folders('{folder_id}')")

        data = {}
        if name:
            data["Name"] = name
        if description:
            data["Description"] = description

        if not data:
            print("Error: No updates provided. At least one of name or description is required.")
            return None

        headers = {"Content-Type": "application/json"}
        token = self.get_csrf_token()
        if token:
            headers["X-CSRF-Token"] = token

        try:
            response = self.session.patch(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            print(f"\n[OK] Updated Folder:")
            print(json.dumps(result, indent=2))
            return result
        except requests.RequestException as e:
            print(f"Error: Failed to update folder: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def delete_folder(self, folder_id):
        """Delete a folder"""
        url = self._get_dataadmin_url(f"Folders('{folder_id}')")

        headers = {}
        token = self.get_csrf_token()
        if token:
            headers["X-CSRF-Token"] = token

        try:
            response = self.session.delete(url, headers=headers)
            response.raise_for_status()
            print(f"\n[OK] Deleted Folder {folder_id}")
            return True
        except requests.RequestException as e:
            print(f"Error: Failed to delete folder: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_folder_contents(self, folder_id):
        """Get contents of a folder"""
        url = self._get_dataadmin_url(f"Folders('{folder_id}')/FolderContents")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            contents = data.get("value", [])
            print(f"\n[OK] Found {len(contents)} items in Folder:")
            for item in contents:
                print(f"  - {item.get('ID', 'N/A')}: {item.get('Name', 'N/A')}")
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to get folder contents: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_driver_properties(self, container_id, entity_name, entity_version=None):
        """Get driver properties for a Windchill type using GetDriverProperties function"""
        url = self._get_dataadmin_url(f"Containers('{container_id}')/PTC.DataAdmin.GetDriverProperties")

        params = {"EntityName": entity_name}
        if entity_version:
            params["EntityVersion"] = entity_version

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            print(f"\n[OK] Retrieved Driver Properties for {entity_name}:")
            print(json.dumps(data, indent=2))
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to get driver properties: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_constraints(self, container_id, entity_name, driver_properties, entity_version=None, property_name=None):
        """Get constraints for a Windchill type using GetConstraints function"""
        url = self._get_dataadmin_url(f"Containers('{container_id}')/PTC.DataAdmin.GetConstraints")

        data = {
            "EntityName": entity_name,
            "DriverProperties": driver_properties
        }
        if entity_version:
            data["EntityVersion"] = entity_version
        if property_name:
            data["PropertyName"] = property_name

        headers = {"Content-Type": "application/json"}

        try:
            response = self.session.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            print(f"\n[OK] Retrieved Constraints:")
            print(json.dumps(result, indent=2))
            return result
        except requests.RequestException as e:
            print(f"Error: Failed to get constraints: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_pregenerated_value(self, container_id, entity_name, property_name, driver_properties, entity_version=None):
        """Get a pregenerated value (like Number) before entity creation"""
        url = self._get_dataadmin_url(f"Containers('{container_id}')/PTC.DataAdmin.GetPregeneratedValue")

        data = {
            "EntityName": entity_name,
            "PropertyName": property_name,
            "DriverProperties": driver_properties
        }
        if entity_version:
            data["EntityVersion"] = entity_version

        headers = {"Content-Type": "application/json"}

        try:
            response = self.session.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.text.strip('"')
            print(f"\n[OK] Pregenerated Value for {property_name}: {result}")
            return result
        except requests.RequestException as e:
            print(f"Error: Failed to get pregenerated value: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    # ==================== CEM (Customer Experience Management) Domain Methods ====================

    def _get_cem_url(self, endpoint):
        """Build full URL for CEM domain endpoint"""
        odata_base_url = self.config.get("odata_base_url", self.config["server_url"] + "/servlet/odata")
        return f"{odata_base_url.rstrip('/')}/CEM/{endpoint.lstrip('/')}"

    def get_customer_experiences(self, filter_expr=None, top=None, select=None, expand=None):
        """Query CustomerExperiences from CEM domain"""
        url = self._get_cem_url("CustomerExperiences")

        params = {}
        if filter_expr:
            params["$filter"] = filter_expr
        if top:
            params["$top"] = top
        if select:
            params["$select"] = select
        if expand:
            params["$expand"] = expand

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            experiences = data.get("value", [])
            print(f"\n[OK] Found {len(experiences)} Customer Experiences:")
            for exp in experiences:
                print(f"  - {exp.get('Number')}: {exp.get('Name')} - {exp.get('State', {}).get('Display', 'N/A')}")
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to query customer experiences: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_customer_experience_by_id(self, experience_id, expand=None):
        """Get a specific customer experience by ID"""
        url = self._get_cem_url(f"CustomerExperiences('{experience_id}')")

        params = {}
        if expand:
            params["$expand"] = expand

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            print(f"\n[OK] Retrieved Customer Experience:")
            print(json.dumps(data, indent=2))
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to get customer experience: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def create_customer_experience(self, name, summary, date=None, primary_code=None, additional_information=None):
        """Create a new customer experience in CEM domain"""
        url = self._get_cem_url("CustomerExperiences")

        data = {"Name": name, "Summary": summary}
        if date:
            data["Date"] = date
        if primary_code:
            data["PrimaryCode"] = primary_code
        if additional_information:
            data["AdditionalInformation"] = additional_information

        headers = {"Content-Type": "application/json"}
        token = self.get_csrf_token()
        if token:
            headers["X-CSRF-Token"] = token

        try:
            response = self.session.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            print(f"\n[OK] Created Customer Experience:")
            print(json.dumps(result, indent=2))
            return result
        except requests.RequestException as e:
            print(f"Error: Failed to create customer experience: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def update_customer_experience(self, experience_id, name=None, summary=None, additional_information=None, primary_code=None):
        """Update an existing customer experience"""
        url = self._get_cem_url(f"CustomerExperiences('{experience_id}')")

        data = {}
        if name:
            data["Name"] = name
        if summary:
            data["Summary"] = summary
        if additional_information:
            data["AdditionalInformation"] = additional_information
        if primary_code:
            data["PrimaryCode"] = primary_code

        if not data:
            print("Error: No updates provided. At least one field is required.")
            return None

        headers = {"Content-Type": "application/json"}
        token = self.get_csrf_token()
        if token:
            headers["X-CSRF-Token"] = token

        try:
            response = self.session.patch(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            print(f"\n[OK] Updated Customer Experience:")
            print(json.dumps(result, indent=2))
            return result
        except requests.RequestException as e:
            print(f"Error: Failed to update customer experience: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_primary_related_product(self, experience_id, expand=None):
        """Get primary related product for a customer experience"""
        url = self._get_cem_url(f"CustomerExperiences('{experience_id}')/PrimaryRelatedProduct")

        params = {}
        if expand:
            params["$expand"] = expand

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            print(f"\n[OK] Retrieved Primary Related Product:")
            print(json.dumps(data, indent=2))
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to get primary related product: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_additional_related_products(self, experience_id, expand=None):
        """Get additional related products for a customer experience"""
        url = self._get_cem_url(f"CustomerExperiences('{experience_id}')/AdditionalRelatedProducts")

        params = {}
        if expand:
            params["$expand"] = expand

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            products = data.get("value", [])
            print(f"\n[OK] Found {len(products)} Additional Related Products:")
            for product in products:
                print(f"  - {product.get('ReportedName', 'N/A')}: {product.get('Quantity', 'N/A')} {product.get('UnitOfMeasure', 'N/A')}")
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to get additional related products: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def create_related_product(self, experience_id, quantity, unit_of_measure, primary=False, reported_name=None,
                             reported_number=None, serial_lot_number=None, expected_return=False, date_return_expected=None):
        """Create a related product for a customer experience"""
        url = self._get_cem_url(f"CustomerExperiences('{experience_id}')/AdditionalRelatedProducts")

        data = {
            "Primary": primary,
            "Quantity": quantity,
            "UnitOfMeasure": unit_of_measure
        }
        if reported_name:
            data["ReportedName"] = reported_name
        if reported_number:
            data["ReportedNumber"] = reported_number
        if serial_lot_number:
            data["SerialLotNumber"] = serial_lot_number
        if expected_return:
            data["ExpectedReturn"] = expected_return
        if date_return_expected:
            data["DateReturnExpected"] = date_return_expected

        headers = {"Content-Type": "application/json"}
        token = self.get_csrf_token()
        if token:
            headers["X-CSRF-Token"] = token

        try:
            response = self.session.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            print(f"\n[OK] Created Related Product:")
            print(json.dumps(result, indent=2))
            return result
        except requests.RequestException as e:
            print(f"Error: Failed to create related product: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def update_related_product(self, experience_id, related_product_id, quantity=None, expected_return=None, date_return_expected=None):
        """Update a related product"""
        url = self._get_cem_url(f"CustomerExperiences('{experience_id}')/AdditionalRelatedProducts('{related_product_id}')")

        data = {}
        if quantity is not None:
            data["Quantity"] = quantity
        if expected_return is not None:
            data["ExpectedReturn"] = expected_return
        if date_return_expected is not None:
            data["DateReturnExpected"] = date_return_expected

        if not data:
            print("Error: No updates provided.")
            return None

        headers = {"Content-Type": "application/json"}
        token = self.get_csrf_token()
        if token:
            headers["X-CSRF-Token"] = token

        try:
            response = self.session.patch(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            print(f"\n[OK] Updated Related Product:")
            print(json.dumps(result, indent=2))
            return result
        except requests.RequestException as e:
            print(f"Error: Failed to update related product: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def delete_related_product(self, experience_id, related_product_id):
        """Delete a related product"""
        url = self._get_cem_url(f"CustomerExperiences('{experience_id}')/AdditionalRelatedProducts('{related_product_id}')")

        headers = {}
        token = self.get_csrf_token()
        if token:
            headers["X-CSRF-Token"] = token

        try:
            response = self.session.delete(url, headers=headers)
            response.raise_for_status()
            print(f"\n[OK] Deleted Related Product {related_product_id}")
            return True
        except requests.RequestException as e:
            print(f"Error: Failed to delete related product: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def set_customer_experience_state(self, experience_id, state):
        """Set the lifecycle state for a single customer experience"""
        url = self._get_cem_url(f"CustomerExperiences('{experience_id}')/PTC.CEM.SetState")

        data = {"State": state}
        headers = {"Content-Type": "application/json"}
        token = self.get_csrf_token()
        if token:
            headers["X-CSRF-Token"] = token

        try:
            response = self.session.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            print(f"\n[OK] Set Customer Experience state to {state}:")
            print(json.dumps(result, indent=2))
            return result
        except requests.RequestException as e:
            print(f"Error: Failed to set customer experience state: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def set_customer_experiences_state(self, experience_ids, state):
        """Set the lifecycle state for multiple customer experiences"""
        url = self._get_cem_url("SetStateCustomerExperiences")

        data = {
            "CustomerExperiences": [{"ID": exp_id} for exp_id in experience_ids],
            "State": state
        }
        headers = {"Content-Type": "application/json"}
        token = self.get_csrf_token()
        if token:
            headers["X-CSRF-Token"] = token

        try:
            response = self.session.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            print(f"\n[OK] Set {len(experience_ids)} Customer Experiences state to {state}:")
            print(json.dumps(result, indent=2))
            return result
        except requests.RequestException as e:
            print(f"Error: Failed to set customer experiences state: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_valid_state_transitions(self, experience_id):
        """Get valid state transitions for a customer experience"""
        url = self._get_cem_url(f"CustomerExperiences('{experience_id}')/PTC.CEM.GetValidStateTransitions")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            print(f"\n[OK] Valid State Transitions:")
            print(json.dumps(data, indent=2))
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to get valid state transitions: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_lifecycle_template(self, experience_id):
        """Get the lifecycle template for a customer experience"""
        url = self._get_cem_url(f"CustomerExperiences('{experience_id}')/PTC.CEM.GetLifeCycleTemplate")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            print(f"\n[OK] Lifecycle Template:")
            print(json.dumps(data, indent=2))
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to get lifecycle template: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def get_customer_experience_attachments(self, experience_id):
        """Get attachments for a customer experience"""
        url = self._get_cem_url(f"CustomerExperiences('{experience_id}')/Attachments")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            attachments = data.get("value", [])
            print(f"\n[OK] Found {len(attachments)} Attachments:")
            for att in attachments:
                print(f"  - {att.get('FileName', 'N/A')}: {att.get('FileSize', 'N/A')} bytes - {att.get('Description', 'N/A')}")
            return data
        except requests.RequestException as e:
            print(f"Error: Failed to get attachments: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None


def main():
    parser = argparse.ArgumentParser(description="Windchill PLM REST API Client")
    subparsers = parser.add_subparsers(dest="operation", help="Operation to perform")

    # Get Object
    get_parser = subparsers.add_parser("get-object", help="Get a Windchill object")
    get_parser.add_argument("--type", required=True, help="Object type (e.g., WTPart, WTDocument)")
    get_parser.add_argument("--number", help="Object number/identifier")
    get_parser.add_argument("--oid", help="Object OID")

    # Search
    search_parser = subparsers.add_parser("search", help="Search for objects")
    search_parser.add_argument("--type", required=True, help="Object type to search")
    search_parser.add_argument("--name", help="Name filter")

    # Create Object
    create_parser = subparsers.add_parser("create", help="Create a new object")
    create_parser.add_argument("--type", required=True, help="Object type")
    create_parser.add_argument("--attributes", help="JSON string of attributes")

    # Update Object
    update_parser = subparsers.add_parser("update", help="Update an object")
    update_parser.add_argument("--oid", required=True, help="Object OID")
    update_parser.add_argument("--attributes", help="JSON string of attributes")

    # Get BOM
    bom_parser = subparsers.add_parser("get-bom", help="Get Bill of Materials")
    bom_parser.add_argument("--oid", required=True, help="Part OID")

    # ==================== Data Administration Domain ====================

    # Get Containers
    containers_parser = subparsers.add_parser("get-containers", help="Query Containers")
    containers_parser.add_argument("--filter", help="Filter expression")
    containers_parser.add_argument("--top", type=int, help="Limit results")
    containers_parser.add_argument("--select", help="Select properties")
    containers_parser.add_argument("--expand", help="Expand navigation properties")

    # Get Container by ID
    container_parser = subparsers.add_parser("get-container", help="Get Container by ID")
    container_parser.add_argument("--id", required=True, help="Container ID")
    container_parser.add_argument("--expand", help="Expand navigation properties")

    # Get Products
    products_parser = subparsers.add_parser("get-products", help="Query Product Containers")
    products_parser.add_argument("--filter", help="Filter expression")
    products_parser.add_argument("--top", type=int, help="Limit results")
    products_parser.add_argument("--select", help="Select properties")

    # Get Libraries
    libraries_parser = subparsers.add_parser("get-libraries", help="Query Library Containers")
    libraries_parser.add_argument("--filter", help="Filter expression")
    libraries_parser.add_argument("--top", type=int, help="Limit results")
    libraries_parser.add_argument("--select", help="Select properties")

    # Get Projects
    projects_parser = subparsers.add_parser("get-projects", help="Query Project Containers")
    projects_parser.add_argument("--filter", help="Filter expression")
    projects_parser.add_argument("--top", type=int, help="Limit results")
    projects_parser.add_argument("--select", help="Select properties")

    # Get Organization Containers
    orgs_parser = subparsers.add_parser("get-org-containers", help="Query Organization Containers")
    orgs_parser.add_argument("--filter", help="Filter expression")
    orgs_parser.add_argument("--top", type=int, help="Limit results")
    orgs_parser.add_argument("--select", help="Select properties")

    # Get Sites
    sites_parser = subparsers.add_parser("get-sites", help="Query Site Containers")
    sites_parser.add_argument("--filter", help="Filter expression")
    sites_parser.add_argument("--top", type=int, help="Limit results")
    sites_parser.add_argument("--select", help="Select properties")

    # Get Folders
    folders_parser = subparsers.add_parser("get-folders", help="Query Folders")
    folders_parser.add_argument("--filter", help="Filter expression")
    folders_parser.add_argument("--top", type=int, help="Limit results")
    folders_parser.add_argument("--select", help="Select properties")
    folders_parser.add_argument("--expand", help="Expand navigation properties")

    # Get Folder by ID
    folder_parser = subparsers.add_parser("get-folder", help="Get Folder by ID")
    folder_parser.add_argument("--id", required=True, help="Folder ID")
    folder_parser.add_argument("--expand", help="Expand navigation properties")

    # Create Folder
    create_folder_parser = subparsers.add_parser("create-folder", help="Create a new Folder")
    create_folder_parser.add_argument("--name", required=True, help="Folder name")
    create_folder_parser.add_argument("--description", help="Folder description")

    # Update Folder
    update_folder_parser = subparsers.add_parser("update-folder", help="Update a Folder")
    update_folder_parser.add_argument("--id", required=True, help="Folder ID")
    update_folder_parser.add_argument("--name", help="New folder name")
    update_folder_parser.add_argument("--description", help="New folder description")

    # Delete Folder
    delete_folder_parser = subparsers.add_parser("delete-folder", help="Delete a Folder")
    delete_folder_parser.add_argument("--id", required=True, help="Folder ID")

    # Get Folder Contents
    folder_contents_parser = subparsers.add_parser("get-folder-contents", help="Get Folder Contents")
    folder_contents_parser.add_argument("--id", required=True, help="Folder ID")

    # Get Driver Properties
    driver_props_parser = subparsers.add_parser("get-driver-properties", help="Get Driver Properties")
    driver_props_parser.add_argument("--container-id", required=True, help="Container ID")
    driver_props_parser.add_argument("--entity-name", required=True, help="Entity name (e.g., PTC.ProdMgmt.Part)")
    driver_props_parser.add_argument("--entity-version", help="Entity version (optional)")

    # Get Constraints
    constraints_parser = subparsers.add_parser("get-constraints", help="Get Constraints")
    constraints_parser.add_argument("--container-id", required=True, help="Container ID")
    constraints_parser.add_argument("--entity-name", required=True, help="Entity name")
    constraints_parser.add_argument("--driver-properties", required=True, help="Driver properties JSON (from get-driver-properties)")
    constraints_parser.add_argument("--entity-version", help="Entity version (optional)")
    constraints_parser.add_argument("--property-name", help="Specific property name (optional)")

    # Get Pregenerated Value
    pregen_parser = subparsers.add_parser("get-pregenerated-value", help="Get Pregenerated Value")
    pregen_parser.add_argument("--container-id", required=True, help="Container ID")
    pregen_parser.add_argument("--entity-name", required=True, help="Entity name")
    pregen_parser.add_argument("--property-name", required=True, help="Property name (e.g., Number)")
    pregen_parser.add_argument("--driver-properties", required=True, help="Driver properties JSON")
    pregen_parser.add_argument("--entity-version", help="Entity version (optional)")

    # ==================== CEM (Customer Experience Management) Domain ====================

    # Get Customer Experiences
    cx_parser = subparsers.add_parser("get-customer-experiences", help="Query Customer Experiences")
    cx_parser.add_argument("--filter", help="Filter expression")
    cx_parser.add_argument("--top", type=int, help="Limit results")
    cx_parser.add_argument("--select", help="Select properties")
    cx_parser.add_argument("--expand", help="Expand navigation properties")

    # Get Customer Experience by ID
    cx_by_id_parser = subparsers.add_parser("get-customer-experience", help="Get Customer Experience by ID")
    cx_by_id_parser.add_argument("--id", required=True, help="Customer Experience ID")
    cx_by_id_parser.add_argument("--expand", help="Expand navigation properties")

    # Create Customer Experience
    create_cx_parser = subparsers.add_parser("create-customer-experience", help="Create a new Customer Experience")
    create_cx_parser.add_argument("--name", required=True, help="Customer Experience name")
    create_cx_parser.add_argument("--summary", required=True, help="Summary/description")
    create_cx_parser.add_argument("--date", help="Date of the event (ISO format)")
    create_cx_parser.add_argument("--primary-code", help="Primary code")
    create_cx_parser.add_argument("--additional-information", help="Additional information")

    # Update Customer Experience
    update_cx_parser = subparsers.add_parser("update-customer-experience", help="Update a Customer Experience")
    update_cx_parser.add_argument("--id", required=True, help="Customer Experience ID")
    update_cx_parser.add_argument("--name", help="New name")
    update_cx_parser.add_argument("--summary", help="New summary")
    update_cx_parser.add_argument("--additional-information", help="Additional information")
    update_cx_parser.add_argument("--primary-code", help="Primary code")

    # Get Primary Related Product
    primary_product_parser = subparsers.add_parser("get-primary-related-product", help="Get Primary Related Product")
    primary_product_parser.add_argument("--experience-id", required=True, help="Customer Experience ID")
    primary_product_parser.add_argument("--expand", help="Expand navigation properties")

    # Get Additional Related Products
    additional_products_parser = subparsers.add_parser("get-additional-related-products", help="Get Additional Related Products")
    additional_products_parser.add_argument("--experience-id", required=True, help="Customer Experience ID")
    additional_products_parser.add_argument("--expand", help="Expand navigation properties")

    # Create Related Product
    create_rp_parser = subparsers.add_parser("create-related-product", help="Create a Related Product")
    create_rp_parser.add_argument("--experience-id", required=True, help="Customer Experience ID")
    create_rp_parser.add_argument("--quantity", type=float, required=True, help="Quantity")
    create_rp_parser.add_argument("--unit-of-measure", required=True, help="Unit of measure")
    create_rp_parser.add_argument("--primary", action="store_true", help="Is primary product")
    create_rp_parser.add_argument("--reported-name", help="Reported product name")
    create_rp_parser.add_argument("--reported-number", help="Reported product number")
    create_rp_parser.add_argument("--serial-lot-number", help="Serial/lot number")
    create_rp_parser.add_argument("--expected-return", action="store_true", help="Is return expected")
    create_rp_parser.add_argument("--date-return-expected", help="Expected return date (ISO format)")

    # Update Related Product
    update_rp_parser = subparsers.add_parser("update-related-product", help="Update a Related Product")
    update_rp_parser.add_argument("--experience-id", required=True, help="Customer Experience ID")
    update_rp_parser.add_argument("--related-product-id", required=True, help="Related Product ID")
    update_rp_parser.add_argument("--quantity", type=float, help="New quantity")
    update_rp_parser.add_argument("--expected-return", type=bool, help="Expected return")
    update_rp_parser.add_argument("--date-return-expected", help="Expected return date (ISO format)")

    # Delete Related Product
    delete_rp_parser = subparsers.add_parser("delete-related-product", help="Delete a Related Product")
    delete_rp_parser.add_argument("--experience-id", required=True, help="Customer Experience ID")
    delete_rp_parser.add_argument("--related-product-id", required=True, help="Related Product ID")

    # Set Customer Experience State
    set_state_parser = subparsers.add_parser("set-customer-experience-state", help="Set Customer Experience State")
    set_state_parser.add_argument("--experience-id", required=True, help="Customer Experience ID")
    set_state_parser.add_argument("--state", required=True, help="Target state")

    # Set Multiple Customer Experiences State
    set_states_parser = subparsers.add_parser("set-customer-experiences-state", help="Set Multiple Customer Experiences State")
    set_states_parser.add_argument("--experience-ids", required=True, help="Comma-separated Customer Experience IDs")
    set_states_parser.add_argument("--state", required=True, help="Target state")

    # Get Valid State Transitions
    transitions_parser = subparsers.add_parser("get-valid-state-transitions", help="Get Valid State Transitions")
    transitions_parser.add_argument("--experience-id", required=True, help="Customer Experience ID")

    # Get Lifecycle Template
    template_parser = subparsers.add_parser("get-lifecycle-template", help="Get Lifecycle Template")
    template_parser.add_argument("--experience-id", required=True, help="Customer Experience ID")

    # Get Customer Experience Attachments
    attachments_parser = subparsers.add_parser("get-customer-experience-attachments", help="Get Customer Experience Attachments")
    attachments_parser.add_argument("--experience-id", required=True, help="Customer Experience ID")

    args = parser.parse_args()

    if not args.operation:
        parser.print_help()
        sys.exit(1)

    client = WindchillClient()

    if args.operation == "get-object":
        client.get_object(args.type, identifier=args.number, oid=args.oid)

    elif args.operation == "search":
        criteria = {}
        if args.name:
            criteria["name"] = args.name
        client.search(args.type, criteria)

    elif args.operation == "create":
        if not args.attributes:
            print("Error: --attributes required for create operation")
            sys.exit(1)
        attributes = json.loads(args.attributes)
        client.create_object(args.type, attributes)

    elif args.operation == "update":
        if not args.attributes:
            print("Error: --attributes required for update operation")
            sys.exit(1)
        attributes = json.loads(args.attributes)
        client.update_object(args.oid, attributes)

    elif args.operation == "get-bom":
        client.get_bom(args.oid)

    # ==================== Data Administration Domain ====================

    elif args.operation == "get-containers":
        client.get_containers(filter_expr=getattr(args, 'filter', None), top=args.top,
                            select=args.select, expand=args.expand)

    elif args.operation == "get-container":
        client.get_container_by_id(args.id, expand=args.expand)

    elif args.operation == "get-products":
        client.get_products(filter_expr=getattr(args, 'filter', None), top=args.top, select=args.select)

    elif args.operation == "get-libraries":
        client.get_libraries(filter_expr=getattr(args, 'filter', None), top=args.top, select=args.select)

    elif args.operation == "get-projects":
        client.get_projects(filter_expr=getattr(args, 'filter', None), top=args.top, select=args.select)

    elif args.operation == "get-org-containers":
        client.get_org_containers(filter_expr=getattr(args, 'filter', None), top=args.top, select=args.select)

    elif args.operation == "get-sites":
        client.get_sites(filter_expr=getattr(args, 'filter', None), top=args.top, select=args.select)

    elif args.operation == "get-folders":
        client.get_folders(filter_expr=getattr(args, 'filter', None), top=args.top,
                          select=args.select, expand=args.expand)

    elif args.operation == "get-folder":
        client.get_folder_by_id(args.id, expand=args.expand)

    elif args.operation == "create-folder":
        client.create_folder(args.name, args.description)

    elif args.operation == "update-folder":
        client.update_folder(args.id, args.name, args.description)

    elif args.operation == "delete-folder":
        client.delete_folder(args.id)

    elif args.operation == "get-folder-contents":
        client.get_folder_contents(args.id)

    elif args.operation == "get-driver-properties":
        client.get_driver_properties(args.container_id, args.entity_name, args.entity_version)

    elif args.operation == "get-constraints":
        driver_props = json.loads(args.driver_properties)
        client.get_constraints(args.container_id, args.entity_name, driver_props,
                             args.entity_version, args.property_name)

    elif args.operation == "get-pregenerated-value":
        driver_props = json.loads(args.driver_properties)
        client.get_pregenerated_value(args.container_id, args.entity_name,
                                    args.property_name, driver_props, args.entity_version)

    # ==================== CEM (Customer Experience Management) Domain ====================

    elif args.operation == "get-customer-experiences":
        client.get_customer_experiences(filter_expr=getattr(args, 'filter', None), top=args.top,
                                       select=args.select, expand=args.expand)

    elif args.operation == "get-customer-experience":
        client.get_customer_experience_by_id(args.id, expand=args.expand)

    elif args.operation == "create-customer-experience":
        client.create_customer_experience(args.name, args.summary, args.date,
                                        args.primary_code, args.additional_information)

    elif args.operation == "update-customer-experience":
        client.update_customer_experience(args.id, args.name, args.summary,
                                        args.additional_information, args.primary_code)

    elif args.operation == "get-primary-related-product":
        client.get_primary_related_product(args.experience_id, expand=args.expand)

    elif args.operation == "get-additional-related-products":
        client.get_additional_related_products(args.experience_id, expand=args.expand)

    elif args.operation == "create-related-product":
        client.create_related_product(args.experience_id, args.quantity, args.unit_of_measure,
                                    args.primary, args.reported_name, args.reported_number,
                                    args.serial_lot_number, args.expected_return,
                                    args.date_return_expected)

    elif args.operation == "update-related-product":
        client.update_related_product(args.experience_id, args.related_product_id,
                                    args.quantity, args.expected_return, args.date_return_expected)

    elif args.operation == "delete-related-product":
        client.delete_related_product(args.experience_id, args.related_product_id)

    elif args.operation == "set-customer-experience-state":
        client.set_customer_experience_state(args.experience_id, args.state)

    elif args.operation == "set-customer-experiences-state":
        exp_ids = [id.strip() for id in args.experience_ids.split(',')]
        client.set_customer_experiences_state(exp_ids, args.state)

    elif args.operation == "get-valid-state-transitions":
        client.get_valid_state_transitions(args.experience_id)

    elif args.operation == "get-lifecycle-template":
        client.get_lifecycle_template(args.experience_id)

    elif args.operation == "get-customer-experience-attachments":
        client.get_customer_experience_attachments(args.experience_id)


if __name__ == "__main__":
    main()