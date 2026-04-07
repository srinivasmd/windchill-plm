#!/usr/bin/env python3
"""
Query Windchill Supplier by name with full details.

Usage:
    python query_supplier_by_name.py "Texas Instruments"
    python query_supplier_by_name.py --name "Murata" --expand Organization
    python query_supplier_by_name.py --name "Panasonic" --output supplier.json
    python query_supplier_by_name.py --name "Texas" --all-matches
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
    # OAuth support can be added here if needed
    
    return session


def query_supplier_by_name(session, config, name, expand=None, all_matches=False):
    """
    Query supplier(s) by name.
    
    Args:
        session: Authenticated requests session
        config: Configuration dictionary
        name: Supplier name to search for
        expand: Comma-separated list of navigation properties to expand
        all_matches: If True, return all matches; if False, return first match
    
    Returns:
        List of supplier records
    """
    odata_base = config["server_url"] + "/servlet/odata"
    endpoint = f"{odata_base}/SupplierMgmt/Suppliers"
    
    # Build query parameters
    params = {
        "$filter": f"contains(Name, '{name}')"
    }
    
    if expand:
        params["$expand"] = expand
    else:
        # Default: expand Organization
        params["$expand"] = "Organization"
    
    response = session.get(endpoint, params=params)
    
    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")
    
    data = response.json()
    results = data.get("value", [])
    
    if not all_matches and results:
        return [results[0]]
    
    return results


def get_supplier_by_id(session, config, supplier_id, expand=None):
    """
    Get a specific supplier by ID.
    
    Args:
        session: Authenticated requests session
        config: Configuration dictionary
        supplier_id: Supplier ID (e.g., OR:com.ptc.windchill.suma.supplier.Manufacturer:12345)
        expand: Comma-separated list of navigation properties to expand
    
    Returns:
        Supplier record or None
    """
    odata_base = config["server_url"] + "/servlet/odata"
    endpoint = f"{odata_base}/SupplierMgmt/Suppliers('{supplier_id}')"
    
    params = {}
    if expand:
        params["$expand"] = expand
    else:
        params["$expand"] = "Organization"
    
    response = session.get(endpoint, params=params)
    
    if response.status_code == 404:
        return None
    
    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")
    
    return response.json()


def format_supplier_summary(supplier):
    """Format supplier as a summary string"""
    lines = []
    lines.append(f"Name: {supplier.get('Name', 'N/A')}")
    lines.append(f"ID: {supplier.get('ID', 'N/A')}")
    
    # Extract type from @odata.type
    odata_type = supplier.get('@odata.type', '')
    if odata_type:
        supplier_type = odata_type.split('.')[-1]
        lines.append(f"Type: {supplier_type}")
    
    lines.append(f"Description: {supplier.get('Description', 'N/A')}")
    lines.append(f"Created: {supplier.get('CreatedOn', 'N/A')}")
    lines.append(f"Last Modified: {supplier.get('LastModified', 'N/A')}")
    
    # Organization details
    org = supplier.get('Organization', {})
    if org:
        lines.append("")
        lines.append("Organization:")
        lines.append(f"  - Name: {org.get('Name', 'N/A')}")
        lines.append(f"  - Identity: {org.get('Identity', 'N/A')}")
        lines.append(f"  - Domain: {org.get('DomainName', 'N/A')}")
        lines.append(f"  - Internet Domain: {org.get('InternetDomain', 'N/A')}")
        status = org.get('Status', {})
        if status:
            lines.append(f"  - Status: {status.get('Display', 'N/A')}")
        lines.append(f"  - Description: {org.get('Description', 'N/A')}")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Query Windchill Supplier by name',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s "Texas Instruments"
  %(prog)s --name "Murata" --expand Organization
  %(prog)s --name "Panasonic" --output supplier.json
  %(prog)s --id "OR:com.ptc.windchill.suma.supplier.Manufacturer:3678248"
  %(prog)s --name "Texas" --all-matches
'''
    )
    
    parser.add_argument('name', nargs='?', help='Supplier name to search for')
    parser.add_argument('--name', '-n', dest='name_opt', help='Supplier name to search for')
    parser.add_argument('--id', '-i', help='Supplier ID to query directly')
    parser.add_argument('--expand', '-e', default='Organization', 
                        help='Navigation properties to expand (comma-separated)')
    parser.add_argument('--all-matches', '-a', action='store_true',
                        help='Return all matching suppliers, not just the first')
    parser.add_argument('--output', '-o', help='Output file for JSON results')
    parser.add_argument('--raw', '-r', action='store_true',
                        help='Output raw JSON instead of formatted summary')
    
    args = parser.parse_args()
    
    # Determine name to search
    name = args.name or args.name_opt
    if not name and not args.id:
        parser.print_help()
        print("\nError: Please provide a supplier name or ID")
        sys.exit(1)
    
    # Load config and create session
    config = load_config()
    session = create_session(config)
    
    try:
        if args.id:
            # Query by ID
            supplier = get_supplier_by_id(session, config, args.id, args.expand)
            if not supplier:
                print(f"Supplier not found with ID: {args.id}")
                sys.exit(1)
            suppliers = [supplier]
        else:
            # Query by name
            suppliers = query_supplier_by_name(
                session, config, name, args.expand, args.all_matches
            )
            
            if not suppliers:
                print(f"No supplier found matching: {name}")
                sys.exit(1)
        
        # Output results
        if args.raw:
            output_data = suppliers[0] if len(suppliers) == 1 else suppliers
            output_json = json.dumps(output_data, indent=2)
        else:
            print(f"Found {len(suppliers)} supplier(s)")
            print("=" * 70)
            
            for i, supplier in enumerate(suppliers, 1):
                if len(suppliers) > 1:
                    print(f"\n[{i}]")
                print(format_supplier_summary(supplier))
                print()
            
            output_data = suppliers if len(suppliers) > 1 else suppliers[0]
            output_json = json.dumps(output_data, indent=2)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output_json)
            print(f"Results saved to: {args.output}")
        
        if args.raw:
            print(output_json)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
