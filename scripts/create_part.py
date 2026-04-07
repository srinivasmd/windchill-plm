#!/usr/bin/env python3
"""
Create a new Part in Windchill PLM.

Usage:
    python create_part.py --name "Resistor 10K" --number "PART-001"
    python create_part.py --name "Capacitor 100uF" --number "PART-002" --description "Electrolytic capacitor"
    python create_part.py --name "PCB Board" --number "PART-003" --type "com.ptc.windchill.suma.part.ManufacturerPart"
"""

import json
import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from windchill_client import WindchillClient


def create_part(client, name, number, description=None, part_type=None, 
                container_id=None, folder_id=None, output_file=None, raw=False):
    """
    Create a new part in Windchill.
    
    Args:
        client: WindchillClient instance
        name: Part name
        number: Part number
        description: Optional description
        part_type: Optional part type (internal name)
        container_id: Optional container ID
        folder_id: Optional folder ID
        output_file: Optional output file for JSON response
        raw: If True, output raw JSON
    
    Returns:
        Created part data or None on failure
    """
    # Build the part data
    part_data = {
        "Name": name,
        "Number": number
    }
    
    if description:
        part_data["Description"] = description
    
    print(f"Creating part '{name}' ({number})...")
    
    # Build URL for ProdMgmt domain
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/ProdMgmt/Parts"
    
    # Get CSRF token for write operation
    token = client.get_csrf_token()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["X-CSRF-Token"] = token
    
    try:
        response = client.session.post(url, json=part_data, headers=headers)
        
        if response.status_code == 201:
            result = response.json()
            
            if raw:
                print(json.dumps(result, indent=2))
            else:
                print("\n" + "=" * 70)
                print("PART CREATED SUCCESSFULLY")
                print("=" * 70)
                print(f"  Name: {result.get('Name', 'N/A')}")
                print(f"  Number: {result.get('Number', 'N/A')}")
                print(f"  ID: {result.get('ID', 'N/A')}")
                print(f"  Type: {result.get('@odata.type', 'N/A').split('.')[-1] if result.get('@odata.type') else 'N/A'}")
                print(f"  Description: {result.get('Description', 'N/A')}")
                print(f"  Created: {result.get('CreatedOn', 'N/A')}")
                print("=" * 70)
            
            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"\nResults saved to: {output_file}")
            
            return result
        else:
            print(f"Error: Failed to create part (HTTP {response.status_code})")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Create a new Part in Windchill PLM',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --name "Resistor 10K" --number "PART-001"
  %(prog)s --name "Capacitor 100uF" --number "PART-002" --description "Electrolytic capacitor"
  %(prog)s --name "PCB Board" --number "PART-003" --output part.json
'''
    )
    
    parser.add_argument('--name', '-n', required=True, help='Part name')
    parser.add_argument('--number', '-u', required=True, help='Part number (unique identifier)')
    parser.add_argument('--description', '-d', help='Part description')
    parser.add_argument('--type', '-t', help='Part type (internal name)')
    parser.add_argument('--container', '-c', help='Container ID')
    parser.add_argument('--folder', '-f', help='Folder ID')
    parser.add_argument('--output', '-o', help='Output file for JSON response')
    parser.add_argument('--raw', '-r', action='store_true', help='Output raw JSON response')
    
    args = parser.parse_args()
    
    # Initialize client
    client = WindchillClient()
    
    # Create part
    create_part(
        client=client,
        name=args.name,
        number=args.number,
        description=args.description,
        part_type=args.type,
        container_id=args.container,
        folder_id=args.folder,
        output_file=args.output,
        raw=args.raw
    )


if __name__ == "__main__":
    main()
