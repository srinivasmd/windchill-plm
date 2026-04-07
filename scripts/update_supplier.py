#!/usr/bin/env python3
"""
Update an existing Supplier in Windchill PLM.

Usage:
    python update_supplier.py --id "OR:com.ptc.windchill.suma.supplier.Manufacturer:3678342" --name "New Name"
    python update_supplier.py --number "SUP-001" --description "Updated description"
    python update_supplier.py --id "OR:..." --name "Updated Name" --description "New description"
"""

import json
import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from windchill_client import WindchillClient


def get_supplier_by_id(client, supplier_id):
    """Get supplier by ID"""
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/SupplierMgmt/Suppliers('{supplier_id}')"
    
    response = client.session.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def get_supplier_by_number(client, number):
    """Get supplier by number"""
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/SupplierMgmt/Suppliers"
    params = {"$filter": f"Number eq '{number}'", "$top": 1}
    
    response = client.session.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        suppliers = data.get("value", [])
        return suppliers[0] if suppliers else None
    return None


def update_supplier(client, supplier_id, name=None, description=None, output_file=None, raw=False):
    """
    Update an existing supplier in Windchill.
    
    Args:
        client: WindchillClient instance
        supplier_id: Supplier ID to update
        name: New name (optional)
        description: New description (optional)
        output_file: Optional output file for JSON response
        raw: If True, output raw JSON
    
    Returns:
        Updated supplier data or None on failure
    """
    # Build update data
    update_data = {}
    if name is not None:
        update_data["Name"] = name
    if description is not None:
        update_data["Description"] = description
    
    if not update_data:
        print("Error: No updates provided. Use --name and/or --description")
        return None
    
    print(f"Updating supplier '{supplier_id}'...")
    
    # Build URL
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/SupplierMgmt/Suppliers('{supplier_id}')"
    
    # Get CSRF token
    token = client.get_csrf_token()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["X-CSRF-Token"] = token
    
    try:
        response = client.session.patch(url, json=update_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            
            if raw:
                print(json.dumps(result, indent=2))
            else:
                print("\n" + "=" * 70)
                print("SUPPLIER UPDATED SUCCESSFULLY")
                print("=" * 70)
                print(f"  Name: {result.get('Name', 'N/A')}")
                print(f"  Number: {result.get('Number', 'N/A')}")
                print(f"  ID: {result.get('ID', 'N/A')}")
                print(f"  Description: {result.get('Description', 'N/A')}")
                print(f"  Last Modified: {result.get('LastModified', 'N/A')}")
                print("=" * 70)
            
            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"\nResults saved to: {output_file}")
            
            return result
        else:
            print(f"Error: Failed to update supplier (HTTP {response.status_code})")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Update an existing Supplier in Windchill PLM',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --id "OR:com.ptc.windchill.suma.supplier.Manufacturer:3678342" --name "New Name"
  %(prog)s --number "SUP-001" --description "Updated description"
  %(prog)s --id "OR:..." --name "Updated Name" --description "New description"
'''
    )
    
    parser.add_argument('--id', '-i', help='Supplier ID to update')
    parser.add_argument('--number', '-n', help='Supplier number to update (will lookup ID)')
    parser.add_argument('--name', '-m', help='New supplier name')
    parser.add_argument('--description', '-d', help='New supplier description')
    parser.add_argument('--output', '-o', help='Output file for JSON response')
    parser.add_argument('--raw', '-r', action='store_true', help='Output raw JSON response')
    
    args = parser.parse_args()
    
    if not args.id and not args.number:
        parser.print_help()
        print("\nError: Please provide --id or --number")
        sys.exit(1)
    
    if args.name is None and args.description is None:
        parser.print_help()
        print("\nError: Please provide --name and/or --description to update")
        sys.exit(1)
    
    # Initialize client
    client = WindchillClient()
    
    # Get supplier ID if number provided
    supplier_id = args.id
    if not supplier_id and args.number:
        supplier = get_supplier_by_number(client, args.number)
        if not supplier:
            print(f"Error: Supplier with number '{args.number}' not found")
            sys.exit(1)
        supplier_id = supplier.get("ID")
        print(f"Found supplier: {supplier.get('Name')} (ID: {supplier_id})")
    
    # Update supplier
    update_supplier(
        client=client,
        supplier_id=supplier_id,
        name=args.name,
        description=args.description,
        output_file=args.output,
        raw=args.raw
    )


if __name__ == "__main__":
    main()
