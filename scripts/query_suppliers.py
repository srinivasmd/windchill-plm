#!/usr/bin/env python3
"""
Query Windchill SupplierMgmt for suppliers with filtering and expansion options.

Usage:
    python query_suppliers.py
    python query_suppliers.py --top 50
    python query_suppliers.py --filter "contains(Name, 'Texas')"
    python query_suppliers.py --expand Organization --top 100
    python query_suppliers.py --name "Murata" --expand Organization
    python query_suppliers.py --type manufacturer
    python query_suppliers.py --output suppliers.json
"""

import json
import requests
from pathlib import Path
import sys
import argparse

# Load config
CONFIG_PATH = Path(__file__).parent.parent / "config.json"


def load_config():
    """Load configuration from config.json"""
    if not CONFIG_PATH.exists():
        print(f"Error: Config file not found at {CONFIG_PATH}")
        print("Please copy config.example.json to config.json and configure it.")
        sys.exit(1)
    
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)


def create_session(config):
    """Create authenticated requests session"""
    session = requests.Session()
    session.verify = config.get("verify_ssl", True)
    
    auth_type = config.get("auth_type", "basic")
    if auth_type == "basic":
        session.auth = (config["basic"]["username"], config["basic"]["password"])
    
    return session


def query_suppliers(session, config, params):
    """
    Query suppliers with given parameters.
    
    Args:
        session: Authenticated requests session
        config: Configuration dictionary
        params: Dictionary of OData query parameters
    
    Returns:
        Tuple of (results list, total count)
    """
    odata_base = config["server_url"] + "/servlet/odata"
    endpoint = f"{odata_base}/SupplierMgmt/Suppliers"
    
    response = session.get(endpoint, params=params)
    
    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")
    
    data = response.json()
    results = data.get("value", [])
    
    return results


def query_suppliers_by_type(session, config, supplier_type, params):
    """
    Query suppliers filtered by type (Manufacturer or Vendor).
    
    Args:
        session: Authenticated requests session
        config: Configuration dictionary
        supplier_type: 'manufacturer' or 'vendor'
        params: Dictionary of OData query parameters
    
    Returns:
        List of supplier records
    """
    odata_base = config["server_url"] + "/servlet/odata"
    
    if supplier_type.lower() == 'manufacturer':
        endpoint = f"{odata_base}/SupplierMgmt/Manufacturers"
    elif supplier_type.lower() == 'vendor':
        endpoint = f"{odata_base}/SupplierMgmt/Vendors"
    else:
        endpoint = f"{odata_base}/SupplierMgmt/Suppliers"
    
    response = session.get(endpoint, params=params)
    
    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")
    
    data = response.json()
    return data.get("value", [])


def query_all_suppliers(session, config, expand=None, supplier_type=None):
    """
    Query all suppliers with pagination.
    
    Args:
        session: Authenticated requests session
        config: Configuration dictionary
        expand: Navigation properties to expand
        supplier_type: Filter by type ('manufacturer' or 'vendor')
    
    Returns:
        List of all supplier records
    """
    odata_base = config["server_url"] + "/servlet/odata"
    
    if supplier_type:
        if supplier_type.lower() == 'manufacturer':
            endpoint = f"{odata_base}/SupplierMgmt/Manufacturers"
        elif supplier_type.lower() == 'vendor':
            endpoint = f"{odata_base}/SupplierMgmt/Vendors"
        else:
            endpoint = f"{odata_base}/SupplierMgmt/Suppliers"
    else:
        endpoint = f"{odata_base}/SupplierMgmt/Suppliers"
    
    all_suppliers = []
    params = {"$top": 100}
    
    if expand:
        params["$expand"] = expand
    
    while endpoint:
        response = session.get(endpoint, params=params if '?' not in endpoint else None)
        
        if response.status_code != 200:
            raise Exception(f"API Error {response.status_code}: {response.text}")
        
        data = response.json()
        all_suppliers.extend(data.get("value", []))
        
        # Check for next link
        endpoint = data.get("@odata.nextLink")
        params = {}
    
    return all_suppliers


def format_supplier_summary(supplier):
    """Format supplier as a one-line summary"""
    name = supplier.get('Name', 'N/A')
    supplier_id = supplier.get('ID', 'N/A')
    odata_type = supplier.get('@odata.type', '')
    supplier_type = odata_type.split('.')[-1] if odata_type else 'Unknown'
    desc = supplier.get('Description', '') or ''
    if desc:
        desc = f" - {desc[:50]}"
    return f"{name} ({supplier_type}){desc}"


def main():
    parser = argparse.ArgumentParser(
        description='Query Windchill Suppliers with filtering options',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s
  %(prog)s --top 50
  %(prog)s --name "Texas"
  %(prog)s --filter "contains(Name, 'Murata')"
  %(prog)s --expand Organization --top 100
  %(prog)s --type manufacturer
  %(prog)s --all --expand Organization --output suppliers.json
'''
    )
    
    parser.add_argument('--top', '-t', type=int, default=20,
                        help='Maximum number of results (default: 20)')
    parser.add_argument('--skip', '-s', type=int, default=0,
                        help='Number of results to skip (pagination)')
    parser.add_argument('--filter', '-f', help='OData $filter expression')
    parser.add_argument('--name', '-n', help='Filter by supplier name (contains search)')
    parser.add_argument('--expand', '-e', default='Organization',
                        help='Navigation properties to expand (comma-separated)')
    parser.add_argument('--select', help='Properties to select (comma-separated)')
    parser.add_argument('--orderby', '-o', dest='orderby', help='Order by property')
    parser.add_argument('--type', choices=['manufacturer', 'vendor'],
                        help='Filter by supplier type')
    parser.add_argument('--all', '-a', action='store_true',
                        help='Retrieve all suppliers (ignores --top)')
    parser.add_argument('--output', dest='output_file',
                        help='Output file for JSON results')
    parser.add_argument('--raw', '-r', action='store_true',
                        help='Output raw JSON')
    
    args = parser.parse_args()
    
    # Load config and create session
    config = load_config()
    session = create_session(config)
    
    try:
        # Build query parameters
        params = {}
        
        if not args.all:
            params["$top"] = args.top
            params["$skip"] = args.skip
        
        if args.expand:
            params["$expand"] = args.expand
        
        if args.select:
            params["$select"] = args.select
        
        if args.orderby:
            params["$orderby"] = args.orderby
        
        # Build filter
        filter_parts = []
        if args.filter:
            filter_parts.append(args.filter)
        if args.name:
            filter_parts.append(f"contains(Name, '{args.name}')")
        
        if filter_parts:
            params["$filter"] = " and ".join(filter_parts)
        
        # Query suppliers
        if args.all:
            suppliers = query_all_suppliers(session, config, args.expand, args.type)
        else:
            if args.type and not args.all:
                suppliers = query_suppliers_by_type(session, config, args.type, params)
            else:
                suppliers = query_suppliers(session, config, params)
        
        if not suppliers:
            print("No suppliers found matching the criteria.")
            sys.exit(0)
        
        # Output results
        if args.raw:
            output_json = json.dumps(suppliers if len(suppliers) > 1 else suppliers[0], 
                                     indent=2)
            print(output_json)
        else:
            print(f"Found {len(suppliers)} supplier(s)")
            print("=" * 70)
            print()
            
            for supplier in suppliers:
                print(f"  {format_supplier_summary(supplier)}")
            
            print()
            print("-" * 70)
            print(f"Total: {len(suppliers)} supplier(s)")
        
        if args.output_file:
            output_data = suppliers if len(suppliers) > 1 else suppliers[0]
            with open(args.output_file, 'w') as f:
                json.dump(output_data, f, indent=2)
            print(f"\nResults saved to: {args.output_file}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
