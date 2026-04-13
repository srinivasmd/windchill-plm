'''
Windchill PLM ClfStructure Domain Client

Classification Structure domain client providing:
- Classification Node queries and management
- Classified Object queries
- Classification hierarchy navigation
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


class ClfStructureClient(WindchillBaseClient):
    '''
    Client for Windchill ClfStructure OData domain.
    
    Provides classification structure operations.
    '''
    
    DOMAIN = 'ClfStructure'
    
    def __init__(self, **kwargs):
        '''Initialize ClfStructure client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Classification Node Queries
    # =========================================================================
    
    def get_clf_nodes(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Classification Node records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Classification Nodes
        '''
        return self.query_entities('ClfNodes', filter_expr=filter_expr, top=top)
    
    def get_clf_node_by_id(self, node_id: str, expand: List[str] = None) -> dict:
        '''
        Get Classification Node by ID.
        
        Args:
            node_id: Node ID (OID format)
            expand: Navigation properties to expand
        
        Returns:
            Classification Node dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('ClfNodes', node_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_clf_node_by_name(self, name: str) -> dict:
        '''
        Get Classification Node by name.
        
        Args:
            name: Node name
        
        Returns:
            Classification Node dictionary
        '''
        nodes = self.query_entities(
            'ClfNodes',
            filter_expr=f"Name eq '{name}'",
            top=1
        )
        return nodes[0] if nodes else None
    
    def get_root_clf_nodes(self, top: int = 50) -> List[dict]:
        '''
        Get root Classification Nodes (nodes without parent).
        
        Args:
            top: Maximum results
        
        Returns:
            List of root Classification Nodes
        '''
        return self.query_entities(
            'ClfNodes',
            filter_expr="Parent eq null",
            top=top
        )
    
    def get_child_clf_nodes(self, parent_id: str, top: int = 50) -> List[dict]:
        '''
        Get child Classification Nodes for a parent.
        
        Args:
            parent_id: Parent Node ID
            top: Maximum results
        
        Returns:
            List of child Classification Nodes
        '''
        return self.query_entities(
            'ClfNodes',
            filter_expr=f"Parent/ID eq '{parent_id}'",
            top=top
        )
    
    def search_clf_nodes(self, search_term: str, top: int = 20) -> List[dict]:
        '''
        Search Classification Nodes by name.
        
        Args:
            search_term: Search string
            top: Maximum results
        
        Returns:
            List of matching Classification Nodes
        '''
        return self.query_entities(
            'ClfNodes',
            filter_expr=f"contains(Name, '{search_term}')",
            top=top
        )
    
    # =========================================================================
    # Classification Node Navigation Properties
    # =========================================================================
    
    def get_node_parent(self, node_id: str) -> dict:
        '''
        Get parent Classification Node.
        
        Args:
            node_id: Node ID
        
        Returns:
            Parent Node dictionary or None if root
        '''
        return self.get_navigation('ClfNodes', node_id, 'Parent', domain=self.DOMAIN)
    
    def get_node_children(self, node_id: str, top: int = 50) -> List[dict]:
        '''
        Get child Classification Nodes.
        
        Args:
            node_id: Node ID
            top: Maximum results
        
        Returns:
            List of child Nodes
        '''
        return self.get_navigation('ClfNodes', node_id, 'Children', domain=self.DOMAIN, top=top)
    
    def get_node_classified_objects(self, node_id: str, top: int = 50) -> List[dict]:
        '''
        Get Classified Objects for a Classification Node.
        
        Args:
            node_id: Node ID
            top: Maximum results
        
        Returns:
            List of Classified Objects
        '''
        return self.get_navigation('ClfNodes', node_id, 'ClassifiedObjects', domain=self.DOMAIN, top=top)
    
    # =========================================================================
    # Classified Object Queries
    # =========================================================================
    
    def get_classified_objects(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Classified Object records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Classified Objects
        '''
        return self.query_entities('ClassifiedObjects', filter_expr=filter_expr, top=top)
    
    def get_classified_object_by_id(self, obj_id: str) -> dict:
        '''
        Get Classified Object by ID.
        
        Args:
            obj_id: Classified Object ID
        
        Returns:
            Classified Object dictionary
        '''
        return self.get_entity('ClassifiedObjects', obj_id, domain=self.DOMAIN)
    
    def get_objects_by_classification(self, node_id: str, top: int = 50) -> List[dict]:
        '''
        Get all objects classified under a specific node.
        
        Args:
            node_id: Classification Node ID
            top: Maximum results
        
        Returns:
            List of Classified Objects
        '''
        return self.query_entities(
            'ClassifiedObjects',
            filter_expr=f"ClassificationNode/ID eq '{node_id}'",
            top=top
        )
    
    # =========================================================================
    # Classification Hierarchy Operations
    # =========================================================================
    
    def get_classification_path(self, node_id: str) -> List[dict]:
        '''
        Get the full classification path from root to a node.
        
        Args:
            node_id: Node ID
        
        Returns:
            List of nodes from root to the specified node
        '''
        path = []
        current_id = node_id
        
        while current_id:
            node = self.get_clf_node_by_id(current_id)
            if node:
                path.insert(0, node)
                # Get parent ID from navigation
                parent = self.get_node_parent(current_id)
                if parent and 'ID' in parent:
                    current_id = parent.get('ID')
                else:
                    break
            else:
                break
        
        return path
    
    def get_all_descendants(self, node_id: str, max_depth: int = 10) -> List[dict]:
        '''
        Get all descendant nodes under a classification.
        
        Args:
            node_id: Parent Node ID
            max_depth: Maximum depth to traverse
        
        Returns:
            List of all descendant nodes
        '''
        all_descendants = []
        
        def collect_descendants(parent_id: str, depth: int):
            if depth > max_depth:
                return
            
            children = self.get_child_clf_nodes(parent_id)
            for child in children:
                all_descendants.append(child)
                child_id = child.get('ID') or child.get('Id')
                if child_id:
                    collect_descendants(child_id, depth + 1)
        
        collect_descendants(node_id, 1)
        return all_descendants
    
    def get_classification_tree(self, root_id: str = None, max_depth: int = 3) -> dict:
        '''
        Get classification tree structure.
        
        Args:
            root_id: Root node ID (None for all roots)
            max_depth: Maximum depth to traverse
        
        Returns:
            Nested dictionary representing the tree
        '''
        def build_tree(node_id: str, depth: int) -> dict:
            node = self.get_clf_node_by_id(node_id)
            if not node:
                return None
            
            tree_node = {
                'id': node.get('ID') or node.get('Id'),
                'name': node.get('Name'),
                'children': []
            }
            
            if depth < max_depth:
                children = self.get_node_children(node_id)
                for child in children:
                    child_id = child.get('ID') or child.get('Id')
                    if child_id:
                        child_tree = build_tree(child_id, depth + 1)
                        if child_tree:
                            tree_node['children'].append(child_tree)
            
            return tree_node
        
        if root_id:
            return build_tree(root_id, 0)
        else:
            roots = self.get_root_clf_nodes()
            return {
                'roots': [
                    build_tree(r.get('ID') or r.get('Id'), 0)
                    for r in roots
                ]
            }


def create_clf_structure_client(config_path: str = None, **kwargs) -> ClfStructureClient:
    '''
    Factory function to create ClfStructure client.
    
    Args:
        config_path: Path to config.json
        **kwargs: Additional client options
    
    Returns:
        ClfStructureClient instance
    '''
    if config_path:
        with open(config_path, 'r') as f:
            config = json.load(f)
        kwargs.update(config)
    
    return ClfStructureClient(**kwargs)
