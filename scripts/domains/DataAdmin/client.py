'''
Windchill PLM DataAdmin Domain Client

Data Administration domain client providing:
- Container management
- Organization queries
- Site information
'''

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class DataAdminClient(WindchillBaseClient):
    '''
    Client for Windchill DataAdmin OData domain.
    
    Provides data administration operations.
    '''
    
    DOMAIN = 'DataAdmin'
    
    def __init__(self, **kwargs):
        '''Initialize DataAdmin client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Container Queries
    # =========================================================================
    
    def get_containers(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get containers.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of containers
        '''
        return self.query_entities('Containers', filter_expr=filter_expr, top=top)
    
    def get_container_by_id(self, container_id: str) -> dict:
        '''
        Get container by ID.
        
        Args:
            container_id: Container ID
        
        Returns:
            Container dictionary
        '''
        return self.get_entity('Containers', container_id, domain=self.DOMAIN)
    
    def get_org_containers(self, org_id: str = None) -> List[dict]:
        '''
        Get containers for an organization.
        
        Args:
            org_id: Organization ID (optional)
        
        Returns:
            List of containers
        '''
        if org_id:
            return self.query_entities('Containers', filter_expr=f"organizationID eq '{org_id}'")
        return self.query_entities('Containers')
    
    # =========================================================================
    # Products
    # =========================================================================
    
    def get_products(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get products.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of products
        '''
        return self.query_entities('Products', filter_expr=filter_expr, top=top)
    
    def get_product_by_id(self, product_id: str) -> dict:
        '''
        Get product by ID.
        
        Args:
            product_id: Product ID
        
        Returns:
            Product dictionary
        '''
        return self.get_entity('Products', product_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Projects
    # =========================================================================
    
    def get_projects(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get projects.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of projects
        '''
        return self.query_entities('Projects', filter_expr=filter_expr, top=top)
    
    def get_project_by_id(self, project_id: str) -> dict:
        '''
        Get project by ID.
        
        Args:
            project_id: Project ID
        
        Returns:
            Project dictionary
        '''
        return self.get_entity('Projects', project_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Libraries
    # =========================================================================
    
    def get_libraries(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get libraries.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of libraries
        '''
        return self.query_entities('Libraries', filter_expr=filter_expr, top=top)
    
    def get_library_by_id(self, library_id: str) -> dict:
        '''
        Get library by ID.
        
        Args:
            library_id: Library ID
        
        Returns:
            Library dictionary
        '''
        return self.get_entity('Libraries', library_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Sites
    # =========================================================================
    
    def get_sites(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get sites.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of sites
        '''
        return self.query_entities('Sites', filter_expr=filter_expr, top=top)
    
    def get_site_by_id(self, site_id: str) -> dict:
        '''
        Get site by ID.
        
        Args:
            site_id: Site ID
        
        Returns:
            Site dictionary
        '''
        return self.get_entity('Sites', site_id, domain=self.DOMAIN)


def create_dataadmin_client(config_path: str = None, base_url: str = None,
                             username: str = None, password: str = None) -> DataAdminClient:
    '''
    Factory function to create a DataAdmin client.
    
    Args:
        config_path: Path to config.json
        base_url: Windchill server URL
        username: Username
        password: Password
    
    Returns:
        DataAdminClient instance
    '''
    return DataAdminClient(
        config_path=config_path,
        base_url=base_url,
        username=username,
        password=password
    )


def main():
    '''CLI entry point for DataAdmin client.'''
    import argparse
    
    parser = argparse.ArgumentParser(description='Windchill DataAdmin Client')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--containers', action='store_true', help='List containers')
    parser.add_argument('--container-id', help='Get container by ID')
    parser.add_argument('--products', action='store_true', help='List products')
    parser.add_argument('--product-id', help='Get product by ID')
    parser.add_argument('--projects', action='store_true', help='List projects')
    parser.add_argument('--project-id', help='Get project by ID')
    parser.add_argument('--libraries', action='store_true', help='List libraries')
    parser.add_argument('--library-id', help='Get library by ID')
    parser.add_argument('--sites', action='store_true', help='List sites')
    parser.add_argument('--site-id', help='Get site by ID')
    
    args = parser.parse_args()
    
    client = create_dataadmin_client(config_path=args.config)
    
    if args.containers:
        result = client.get_containers()
        print(json.dumps(result, indent=2))
    
    if args.container_id:
        result = client.get_container_by_id(args.container_id)
        print(json.dumps(result, indent=2))
    
    if args.products:
        result = client.get_products()
        print(json.dumps(result, indent=2))
    
    if args.product_id:
        result = client.get_product_by_id(args.product_id)
        print(json.dumps(result, indent=2))
    
    if args.projects:
        result = client.get_projects()
        print(json.dumps(result, indent=2))
    
    if args.project_id:
        result = client.get_project_by_id(args.project_id)
        print(json.dumps(result, indent=2))
    
    if args.libraries:
        result = client.get_libraries()
        print(json.dumps(result, indent=2))
    
    if args.library_id:
        result = client.get_library_by_id(args.library_id)
        print(json.dumps(result, indent=2))
    
    if args.sites:
        result = client.get_sites()
        print(json.dumps(result, indent=2))
    
    if args.site_id:
        result = client.get_site_by_id(args.site_id)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
