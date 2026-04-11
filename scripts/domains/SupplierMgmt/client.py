'''
Windchill PLM SupplierMgmt Domain Client

Supplier Management domain client providing:
- Supplier queries
- Manufacturer part management
- Vendor part queries
'''

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class SupplierMgmtClient(WindchillBaseClient):
    '''
    Client for Windchill SupplierMgmt OData domain.
    
    Provides supplier management operations.
    '''
    
    DOMAIN = 'SupplierMgmt'
    
    def __init__(self, **kwargs):
        '''Initialize SupplierMgmt client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Supplier Queries
    # =========================================================================
    
    def query_suppliers(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Query suppliers.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of suppliers
        '''
        return self.query_entities('Suppliers', filter_expr=filter_expr, top=top)
    
    def get_supplier_by_id(self, supplier_id: str) -> dict:
        '''
        Get supplier by ID.
        
        Args:
            supplier_id: Supplier ID
        
        Returns:
            Supplier dictionary
        '''
        return self.get_entity('Suppliers', supplier_id, domain=self.DOMAIN)
    
    def get_supplier_by_name(self, name: str) -> dict:
        '''
        Get supplier by name.
        
        Args:
            name: Supplier name
        
        Returns:
            Supplier dictionary
        '''
        suppliers = self.query_entities(
            'Suppliers',
            filter_expr=f"name eq '{name}'",
            top=1
        )
        if not suppliers:
            raise ODataError(404, f"Supplier with name '{name}' not found")
        return suppliers[0]
    
    # =========================================================================
    # Manufacturer Parts
    # =========================================================================
    
    def query_manufacturer_parts(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Query manufacturer parts.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of manufacturer parts
        '''
        return self.query_entities('ManufacturerParts', filter_expr=filter_expr, top=top)
    
    # =========================================================================
    # Vendor Parts
    # =========================================================================
    
    def query_vendor_parts(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Query vendor parts.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of vendor parts
        '''
        return self.query_entities('VendorParts', filter_expr=filter_expr, top=top)


def create_suppliermgmt_client(config_path: str = None, base_url: str = None,
                                username: str = None, password: str = None) -> SupplierMgmtClient:
    '''
    Factory function to create a SupplierMgmt client.
    
    Args:
        config_path: Path to config.json
        base_url: Windchill server URL
        username: Username
        password: Password
    
    Returns:
        SupplierMgmtClient instance
    '''
    return SupplierMgmtClient(
        config_path=config_path,
        base_url=base_url,
        username=username,
        password=password
    )


def main():
    '''CLI entry point for SupplierMgmt client.'''
    import argparse
    
    parser = argparse.ArgumentParser(description='Windchill SupplierMgmt Client')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--suppliers', action='store_true', help='List suppliers')
    parser.add_argument('--supplier-id', help='Get supplier by ID')
    parser.add_argument('--supplier-name', help='Get supplier by name')
    parser.add_argument('--mfr-parts', action='store_true', help='List manufacturer parts')
    parser.add_argument('--vendor-parts', action='store_true', help='List vendor parts')
    
    args = parser.parse_args()
    
    client = create_suppliermgmt_client(config_path=args.config)
    
    if args.suppliers:
        result = client.query_suppliers()
        print(json.dumps(result, indent=2))
    
    if args.supplier_id:
        result = client.get_supplier_by_id(args.supplier_id)
        print(json.dumps(result, indent=2))
    
    if args.supplier_name:
        result = client.get_supplier_by_name(args.supplier_name)
        print(json.dumps(result, indent=2))
    
    if args.mfr_parts:
        result = client.query_manufacturer_parts()
        print(json.dumps(result, indent=2))
    
    if args.vendor_parts:
        result = client.query_vendor_parts()
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
