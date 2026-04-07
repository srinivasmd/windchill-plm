#!/usr/bin/env python3
"""Generic UPDATE script for Windchill entities.

This script provides a unified interface to update any entity type
that supports UPDATE operations in Windchill PLM.

Usage:
    python generic_update.py --entity Document --id "OR:..." --name "New Name"
    python generic_update.py --entity Part --number "PART-001" --description "Updated"
    python generic_update.py --entity Quality --id "OR:..." --description "Updated desc"

Supported entities for UPDATE (most entities support this):
    Document, Part, Folder, Container, ChangeNotice, ChangeRequest,
    QualityAction, NonConformance, CAPA, CustomerExperience, etc.
"""

import sys
import json
import argparse
from pathlib import Path
import requests

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from windchill_client import WindchillClient


# Entity to domain mapping
ENTITY_DOMAIN_MAP = {
    'Document': 'DocMgmt',
    'Part': 'ProdMgmt',
    'Folder': 'DataAdmin',
    'Container': 'DataAdmin',
    'ChangeNotice': 'ChangeMgmt',
    'ChangeRequest': 'ChangeMgmt',
    'ChangeTask': 'ChangeMgmt',
    'QualityAction': 'QMS',
    'QualityObject': 'QMS',
    'NonConformance': 'QMS',
    'CAPA': 'QMS',
    'Place': 'QMS',
    'QualityContact': 'QMS',
    'Subject': 'QMS',
    'CustomerExperience': 'CEM',
    'RelatedProduct': 'CEM',
    'User': 'PrincipalMgmt',
    'Group': 'PrincipalMgmt',
    'Organization': 'PrincipalMgmt',
}


def get_entity_id_by_number(entity_type, number):
    """Look up entity ID by number."""
    client = WindchillClient()
    
    domain = ENTITY_DOMAIN_MAP.get(entity_type)
    if not domain:
        return None
    
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/{domain}/{entity_type}s"
    
    params = {"$filter": f"Number eq '{number}'", "$select": "ID,Name,Number"}
    
    try:
        response = client.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("value"):
            entity = data["value"][0]
            return entity.get("ID")
    except:
        pass
    
    return None


def update_entity(entity_type, entity_id=None, entity_number=None, properties=None, output_file=None, raw_output=False):
    """
    Update an entity in Windchill PLM.
    
    Args:
        entity_type: Type of entity to update
        entity_id: Entity ID to update (preferred)
        entity_number: Entity number to update (will lookup ID)
        properties: Dictionary of properties to update
        output_file: Optional file to save JSON response
        raw_output: If True, output raw JSON
        
    Returns:
        dict: Updated entity data or None on failure
    """
    if properties is None:
        properties = {}
    
    client = WindchillClient()
    
    # Get domain for entity type
    domain = ENTITY_DOMAIN_MAP.get(entity_type)
    if not domain:
        print(f"[ERROR] Unknown entity type: {entity_type}")
        print(f"Supported types: {', '.join(ENTITY_DOMAIN_MAP.keys())}")
        return None
    
    # Resolve entity ID
    if not entity_id and entity_number:
        entity_id = get_entity_id_by_number(entity_type, entity_number)
        if not entity_id:
            print(f"[ERROR] Could not find {entity_type} with number: {entity_number}")
            return None
        print(f"[INFO] Found ID: {entity_id}")
    
    if not entity_id:
        print("[ERROR] Either --id or --number must be provided")
        return None
    
    # Build URL
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/{domain}/{entity_type}s('{entity_id}')"
    
    # Get CSRF token for write operation
    csrf_token = client.get_csrf_token()
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    if csrf_token:
        headers['CSRF_NONCE'] = csrf_token
    
    try:
        response = client.session.patch(url, json=properties, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if raw_output:
            print(json.dumps(data, indent=2))
        else:
            print(f"\n[OK] {entity_type} updated successfully!")
            print(f"  ID: {data.get('ID', 'N/A')}")
            print(f"  Name: {data.get('Name', 'N/A')}")
            print(f"  Number: {data.get('Number', 'N/A')}")
            if 'State' in data:
                state = data['State']
                if isinstance(state, dict):
                    print(f"  State: {state.get('Display', 'N/A')}")
                else:
                    print(f"  State: {state}")
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"  Saved to: {output_file}")
        
        return data
        
    except requests.RequestException as e:
        print(f"\n[ERROR] Failed to update {entity_type}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status: {e.response.status_code}")
            try:
                error_data = e.response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Response: {e.response.text}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Update an existing entity in Windchill PLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --entity Document --id "OR:com.ptc.DocMgmt.Document:12345" --name "New Name"
  %(prog)s --entity Part --number "PART-001" --description "Updated description"
  %(prog)s --entity ChangeNotice --id "OR:..." --props '{"Priority": "High"}'
"""
    )
    
    parser.add_argument('--entity', '-e', required=True, help='Entity type to update')
    parser.add_argument('--id', '-i', help='Entity ID to update')
    parser.add_argument('--number', '-n', help='Entity number (will lookup ID)')
    parser.add_argument('--name', '-m', help='New name')
    parser.add_argument('--description', '-d', help='New description')
    parser.add_argument('--props', '-p', help='Additional properties as JSON string')
    parser.add_argument('--output', '-o', help='Output file for JSON response')
    parser.add_argument('--raw', '-r', action='store_true', help='Output raw JSON response')
    
    args = parser.parse_args()
    
    # Build properties dictionary
    properties = {}
    
    if args.name:
        properties['Name'] = args.name
    if args.description:
        properties['Description'] = args.description
    
    # Parse additional properties
    if args.props:
        try:
            additional_props = json.loads(args.props)
            properties.update(additional_props)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON in --props: {e}")
            return 1
    
    if not properties:
        print("[ERROR] No properties to update. Provide --name, --description, or --props")
        return 1
    
    # Update entity
    result = update_entity(
        entity_type=args.entity,
        entity_id=args.id,
        entity_number=args.number,
        properties=properties,
        output_file=args.output,
        raw_output=args.raw
    )
    
    return 0 if result else 1


if __name__ == '__main__':
    sys.exit(main())
