#!/usr/bin/env python3
"""
Create a new Supplier in Windchill PLM.

Usage:
    python create_supplier.py --name "Texas Instruments" --number "SUP-001"
    python create_supplier.py --name "New Vendor" --number "SUP-002" --description "Electronics vendor"
    python create_supplier.py --name "Test Supplier" --number "SUP-003" --type manufacturer --output supplier.json
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from windchill_client import WindchillClient


def create_supplier(client, name, number, description=None, supplier_type="Manufacturer", 
                    organization_id=None, output_file=None, raw=False):
    """
    Create a new supplier in Windchill.
    
    Args:
        client: WindchillClient instance
        name: Supplier name
        number: Supplier number
        description: Optional description
        supplier_type: Type of supplier (Manufacturer or Vendor)
        organization_id: Optional organization ID
        output_file: Optional output file for JSON response
        raw: If True, output raw JSON
    
    Returns:
        Created supplier data or None on failure
    """
    # Build the supplier data
    supplier_data = {
        "Name": name,
        "Number": number
    }
    
    if description:
        supplier_data["Description"] = description
    
    # Get CSRF token for write operation
    print(f"Creating supplier '{name}'...")
    
    # Build URL for SupplierMgmt domain
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/SupplierMgmt/Suppliers"
    
    # Get CSRF token
    token = client.get_csrf_token()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["X-CSRF-Token"] = token
    
    try:
        response = client.session.post(url, json=supplier_data, headers=headers)
        
        if response.status_code == 201:
            result = response.json()
            
            if raw:
                print(json.dumps(result, indent=2))
            else:
                print("\n" + "=" * 70)
                print("SUPPLIER CREATED SUCCESSFULLY")
                print("=" * 70)
                print(f"  Name: {result.get('Name', 'N/A')}")
                print(f"  Number: {result.get('Number', 'N/A')}")
                print(f"  ID: {result.get('ID', 'N/A')}")
                print(f"  Type: {result.get('@odata.type', 'N/A').split('.')[-1] if result.get('@odata.type') else 'N/A'}")
                print(f"  Created: {result.get('CreatedOn', 'N/A')}")
                print("=" * 70)
            
            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"\nResults saved to: {output_file}")
            
            return result
        else:
            print(f"Error: Failed to create supplier (HTTP {response.status_code})")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Create a new Supplier in Windchill PLM',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --name "Texas Instruments" --number "SUP-001"
  %(prog)s --name "New Vendor" --number "SUP-002" --description "Electronics vendor"
  %(prog)s --name "Test Supplier" --number "SUP-003" --type manufacturer --output supplier.json
'''
    )
    
    parser.add_argument('--name', '-n', required=True, help='Supplier name')
    parser.add_argument('--number', '-u', required=True, help='Supplier number (unique identifier)')
    parser.add_argument('--description', '-d', help='Supplier description')
    parser.add_argument('--type', '-t', choices=['manufacturer', 'vendor'], default='manufacturer',
                        help='Supplier type (default: manufacturer)')
    parser.add_argument('--organization', '-o', help='Organization ID to associate with')
    parser.add_argument('--output', '-f', help='Output file for JSON response')
    parser.add_argument('--raw', '-r', action='store_true', help='Output raw JSON response')
    
    args = parser.parse_args()
    
    # Initialize client
    client = WindchillClient()
    
    # Create supplier
    create_supplier(
        client=client,
        name=args.name,
        number=args.number,
        description=args.description,
        supplier_type=args.type,
        organization_id=args.organization,
        output_file=args.output,
        raw=args.raw
    )


if __name__ == "__main__":
    main()
