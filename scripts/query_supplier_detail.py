#!/usr/bin/env python3
"""
Get full details for a specific supplier by ID or name.

Usage:
    python query_supplier_detail.py --id "OR:com.ptc.windchill.suma.supplier.Manufacturer:3678342"
    python query_supplier_detail.py --name "Texas Instruments"
    python query_supplier_detail.py --name "Murata" --expand Organization
    python query_supplier_detail.py --id "OR:..." --output supplier.json
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


def get_supplier_by_id(session, config, supplier_id, expand="Organization"):
    """
    Get supplier by ID.
    
    Args:
        session: Authenticated requests session
        config: Configuration dictionary
        supplier_id: Supplier ID
        expand: Navigation properties to expand
    
    Returns:
        Supplier record or None
    """
    odata_base = config["server_url"] + "/servlet/odata"
    endpoint = f"{odata_base}/SupplierMgmt/Suppliers('{supplier_id}')"
    
    params = {}
    if expand:
        params["$expand"] = expand
    
    response = session.get(endpoint, params=params)
    
    if response.status_code == 404:
        return None
    
    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")
    
    return response.json()


def get_supplier_by_name(session, config, name, expand="Organization"):
    """
    Get first supplier matching name.
    
    Args:
        session: Authenticated requests session
        config: Configuration dictionary
        name: Supplier name to search for
        expand: Navigation properties to expand
    
    Returns:
        Supplier record or None
    """
    odata_base = config["server_url"] + "/servlet/odata"
    endpoint = f"{odata_base}/SupplierMgmt/Suppliers"
    
    params = {
        "$filter": f"contains(Name, '{name}')",
        "$top": 1
    }
    if expand:
        params["$expand"] = expand
    
    response = session.get(endpoint, params=params)
    
    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")
    
    data = response.json()
    results = data.get("value", [])
    
    return results[0] if results else None


def format_supplier_detail(supplier):
    """Format supplier as detailed output"""
    lines = []
    lines.append("=" * 70)
    lines.append("SUPPLIER DETAILS")
    lines.append("=" * 70)
    lines.append("")
    
    # Basic info
    lines.append("SUPPLIER RECORD:")
    lines.append("-" * 70)
    lines.append(f"  Name: {supplier.get('Name', 'N/A')}")
    lines.append(f"  ID: {supplier.get('ID', 'N/A')}")
    
    odata_type = supplier.get('@odata.type', '')
    if odata_type:
        supplier_type = odata_type.split('.')[-1]
        lines.append(f"  Type: {supplier_type}")
    
    lines.append(f"  Description: {supplier.get('Description', 'N/A')}")
    lines.append(f"  Created: {supplier.get('CreatedOn', 'N/A')}")
    lines.append(f"  Last Modified: {supplier.get('LastModified', 'N/A')}")
    
    # Organization details
    org = supplier.get('Organization', {})
    if org:
        lines.append("")
        lines.append("ORGANIZATION:")
        lines.append("-" * 70)
        lines.append(f"  Name: {org.get('Name', 'N/A')}")
        lines.append(f"  Identity: {org.get('Identity', 'N/A')}")
        lines.append(f"  Domain: {org.get('DomainName', 'N/A')}")
        lines.append(f"  Internet Domain: {org.get('InternetDomain', 'N/A')}")
        status = org.get('Status', {})
        if status:
            lines.append(f"  Status: {status.get('Display', 'N/A')}")
        lines.append(f"  Description: {org.get('Description', 'N/A')}")
    
    lines.append("")
    lines.append("=" * 70)
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Get detailed information for a specific supplier',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --id "OR:com.ptc.windchill.suma.supplier.Manufacturer:3678342"
  %(prog)s --name "Texas Instruments"
  %(prog)s --name "Murata" --expand Organization
  %(prog)s --id "OR:..." --output supplier.json --raw
'''
    )
    
    parser.add_argument('--id', '-i', help='Supplier ID to query')
    parser.add_argument('--name', '-n', help='Supplier name to search for')
    parser.add_argument('--expand', '-e', default='Organization',
                        help='Navigation properties to expand')
    parser.add_argument('--output', '-o', help='Output file for JSON results')
    parser.add_argument('--raw', '-r', action='store_true',
                        help='Output raw JSON instead of formatted')
    
    args = parser.parse_args()
    
    if not args.id and not args.name:
        parser.print_help()
        print("\nError: Please provide --id or --name")
        sys.exit(1)
    
    # Load config and create session
    config = load_config()
    session = create_session(config)
    
    try:
        if args.id:
            supplier = get_supplier_by_id(session, config, args.id, args.expand)
        else:
            supplier = get_supplier_by_name(session, config, args.name, args.expand)
        
        if not supplier:
            print(f"Supplier not found")
            sys.exit(1)
        
        # Output results
        if args.raw:
            output_json = json.dumps(supplier, indent=2)
            print(output_json)
        else:
            print(format_supplier_detail(supplier))
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(supplier, f, indent=2)
            print(f"\nResults saved to: {args.output}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
