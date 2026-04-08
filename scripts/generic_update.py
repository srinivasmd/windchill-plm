#!/usr/bin/env python3
"""Generic UPDATE script for Windchill entities.

This script provides a unified interface to update any entity type
in Windchill PLM with formatted output for Telegram gateway.

Usage:
    python generic_update.py --entity Document --id "OR:..." --name "New Name"
    python generic_update.py --entity Part --number "PART-001" --description "Updated"
    python generic_update.py --entity ChangeNotice --id "OR:..." --props '{"Priority": "High"}'

Supported entities:
    All Windchill entities that support UPDATE operation.
"""

import sys
import json
import argparse
from pathlib import Path
import requests

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from windchill_client import WindchillClient
from output_formatter import OutputFormatter


# Entity to domain mapping
ENTITY_DOMAIN_MAP = {
    'Document': 'DocMgmt',
    'ControlledDocument': 'DocMgmt',
    'Quality': 'DocMgmt',
    'Part': 'ProdMgmt',
    'Folder': 'DataAdmin',
    'ChangeNotice': 'ChangeMgmt',
    'ChangeRequest': 'ChangeMgmt',
    'ChangeTask': 'ChangeMgmt',
    'QualityAction': 'QMS',
    'NonConformance': 'QMS',
    'CAPA': 'QMS',
    'CustomerExperience': 'CEM',
    'User': 'PrincipalMgmt',
    'Group': 'PrincipalMgmt',
}


def get_entity_id(entity_type, number):
    """Get entity ID by number."""
    client = WindchillClient()
    domain = ENTITY_DOMAIN_MAP.get(entity_type)
    if not domain:
        return None
    
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/{domain}/{entity_type}s"
    params = {'$filter': f"Number eq '{number}'", '$select': 'ID'}
    
    try:
        response = client.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        entities = data.get('value', [])
        if entities:
            return entities[0].get('ID')
    except:
        pass
    
    return None


def update_entity(entity_type, entity_id=None, number=None, name=None, 
                  description=None, props=None, output_file=None, raw_output=False):
    """
    Update an existing entity in Windchill PLM with formatted output.
    
    Args:
        entity_type: Type of entity to update
        entity_id: Entity ID to update
        number: Entity number (will lookup ID if not provided)
        name: New name
        description: New description
        props: Additional properties as dict
        output_file: Optional file to save JSON response
        raw_output: If True, output raw JSON
        
    Returns:
        dict: Updated entity or None on failure
    """
    formatter = OutputFormatter()
    client = WindchillClient()
    
    # Get domain for entity type
    domain = ENTITY_DOMAIN_MAP.get(entity_type)
    if not domain:
        formatter.print_error(f"Unknown entity type: {entity_type}")
        formatter.print_info("Supported entity types for UPDATE:")
        for domain_name in sorted(set(ENTITY_DOMAIN_MAP.values())):
            entities = [e for e, d in ENTITY_DOMAIN_MAP.items() if d == domain_name]
            formatter.print_list(entities, domain_name, bullet='📁')
        return None
    
    # Get entity ID if not provided
    if not entity_id and number:
        formatter.print_info(f"Looking up {entity_type} with number: {number}")
        entity_id = get_entity_id(entity_type, number)
        if not entity_id:
            formatter.print_error(f"Entity not found", f"{entity_type} with number '{number}'")
            return None
    
    if not entity_id:
        formatter.print_error("Entity ID or number is required")
        return None
    
    # Build update data
    update_data = {}
    
    if name:
        update_data['Name'] = name
    if description:
        update_data['Description'] = description
    
    # Add additional properties
    if props:
        if isinstance(props, str):
            try:
                props = json.loads(props)
            except json.JSONDecodeError:
                formatter.print_error("Invalid JSON in props")
                return None
        update_data.update(props)
    
    if not update_data:
        formatter.print_warning("No properties to update")
        return None
    
    # Build URL
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/{domain}/{entity_type}s('{entity_id}')"
    
    try:
        # Get CSRF token for write operations
        headers = {'Content-Type': 'application/json'}
        if hasattr(client, 'csrf_token') and client.csrf_token:
            headers['X-CSRF-Token'] = client.csrf_token
        else:
            # Try to get CSRF token
            try:
                csrf_url = f"{odata_base_url.rstrip('/')}/$csrf"
                csrf_resp = client.session.get(csrf_url)
                if csrf_resp.status_code == 200:
                    csrf_data = csrf_resp.json()
                    client.csrf_token = csrf_data.get('value', {}).get('token')
                    if client.csrf_token:
                        headers['X-CSRF-Token'] = client.csrf_token
            except:
                pass
        
        response = client.session.patch(url, json=update_data, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if raw_output:
            formatter.print_json(data)
        else:
            # Show success message
            entity_name = data.get('Name', data.get('Number', number or entity_id))
            formatter.print_operation_result("Updated", entity_type, entity_name, True)
            
            # Show updated entity details
            formatter.print_entity_detail(data, entity_type)
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            formatter.print_success(f"Saved to: {output_file}")
        
        formatter.flush()
        return data
        
    except requests.RequestException as e:
        formatter.print_error(f"Failed to update {entity_type}", str(e))
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                formatter.print_json(error_data, "Error Details")
            except:
                formatter.print_info(f"Status: {e.response.status_code}")
        formatter.flush()
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
    
    # Update entity
    result = update_entity(
        entity_type=args.entity,
        entity_id=args.id,
        number=args.number,
        name=args.name,
        description=args.description,
        props=args.props,
        output_file=args.output,
        raw_output=args.raw
    )
    
    return 0 if result is not None else 1


if __name__ == '__main__':
    sys.exit(main())
