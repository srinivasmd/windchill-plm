#!/usr/bin/env python3
"""Generic CREATE script for Windchill entities.

This script provides a unified interface to create any entity type
in Windchill PLM with formatted output for Telegram gateway.

Usage:
    python generic_create.py --entity Document --name "My Document" --number "DOC-001"
    python generic_create.py --entity Part --name "My Part" --number "PART-001"
    python generic_create.py --entity Quality --name "Quality Doc" --number "Q-001"

Supported entities:
    All Windchill entities that support CREATE operation.
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
    'General': 'DocMgmt',
    'Record': 'DocMgmt',
    'TestDocument': 'DocMgmt',
    'ReferenceDocument': 'DocMgmt',
    'SoftwareDocument': 'DocMgmt',
    'WorkRecord': 'DocMgmt',
    'ApprovedRecord': 'DocMgmt',
    'Specification': 'DocMgmt',
    'Part': 'ProdMgmt',
    'Folder': 'DataAdmin',
    'ChangeNotice': 'ChangeMgmt',
    'ChangeRequest': 'ChangeMgmt',
    'ChangeTask': 'ChangeMgmt',
    'QualityAction': 'QMS',
    'NonConformance': 'QMS',
    'CAPA': 'QMS',
    'CustomerExperience': 'CEM',
    'Place': 'QMS',
    'Subject': 'QMS',
}

# Required properties for each entity type
ENTITY_REQUIRED_PROPS = {
    'Document': ['Name', 'Number'],
    'Part': ['Name', 'Number'],
    'Folder': ['Name'],
    'ChangeNotice': ['Name', 'Number'],
    'QualityAction': ['Name', 'Number'],
}

# Default properties for each entity type
ENTITY_DEFAULTS = {
    'Document': {'Type': 'Document'},
    'Part': {'Type': 'Part'},
    'Folder': {'Type': 'Folder'},
}


def create_entity(entity_type, name=None, number=None, description=None, 
                  object_type=None, container=None, folder=None, 
                  props=None, output_file=None, raw_output=False):
    """
    Create a new entity in Windchill PLM with formatted output.
    
    Args:
        entity_type: Type of entity to create
        name: Entity name
        number: Entity number (unique identifier)
        description: Entity description
        object_type: Internal object type
        container: Container ID
        folder: Folder ID
        props: Additional properties as dict
        output_file: Optional file to save JSON response
        raw_output: If True, output raw JSON
        
    Returns:
        dict: Created entity or None on failure
    """
    formatter = OutputFormatter()
    client = WindchillClient()
    
    # Get domain for entity type
    domain = ENTITY_DOMAIN_MAP.get(entity_type)
    if not domain:
        formatter.print_error(f"Unknown entity type: {entity_type}")
        formatter.print_info("Supported entity types for CREATE:")
        for domain_name in sorted(set(ENTITY_DOMAIN_MAP.values())):
            entities = [e for e, d in ENTITY_DOMAIN_MAP.items() if d == domain_name]
            formatter.print_list(entities, domain_name, bullet='📁')
        return None
    
    # Validate required properties
    required = ENTITY_REQUIRED_PROPS.get(entity_type, ['Name'])
    if 'Name' in required and not name:
        formatter.print_error(f"Name is required for {entity_type}")
        return None
    if 'Number' in required and not number:
        formatter.print_error(f"Number is required for {entity_type}")
        return None
    
    # Build entity data
    entity_data = {}
    
    # Add defaults
    if entity_type in ENTITY_DEFAULTS:
        entity_data.update(ENTITY_DEFAULTS[entity_type])
    
    # Add basic properties
    if name:
        entity_data['Name'] = name
    if number:
        entity_data['Number'] = number
    if description:
        entity_data['Description'] = description
    if object_type:
        entity_data['Type'] = object_type
    if container:
        entity_data['Container'] = container
    if folder:
        entity_data['Folder'] = folder
    
    # Add additional properties
    if props:
        if isinstance(props, str):
            try:
                props = json.loads(props)
            except json.JSONDecodeError:
                formatter.print_error("Invalid JSON in props")
                return None
        entity_data.update(props)
    
    # Build URL
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/{domain}/{entity_type}s"
    
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
        
        response = client.session.post(url, json=entity_data, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if raw_output:
            formatter.print_json(data)
        else:
            # Show success message
            entity_name = data.get('Name', data.get('Number', 'Unknown'))
            formatter.print_operation_result("Created", entity_type, entity_name, True)
            
            # Show created entity details
            formatter.print_entity_detail(data, entity_type)
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            formatter.print_success(f"Saved to: {output_file}")
        
        formatter.flush()
        return data
        
    except requests.RequestException as e:
        formatter.print_error(f"Failed to create {entity_type}", str(e))
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
        description="Create a new entity in Windchill PLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --entity Document --name "My Document" --number "DOC-001"
  %(prog)s --entity Part --name "My Part" --number "PART-001"
  %(prog)s --entity Quality --name "Quality Doc" --number "Q-001"
  %(prog)s --entity Document --name "Doc" --number "D001" --container "OR:wt.inf.container.WTContainer:12345"
"""
    )
    
    parser.add_argument('--entity', '-e', required=True, help='Entity type to create')
    parser.add_argument('--name', '-n', help='Entity name')
    parser.add_argument('--number', '-u', help='Entity number (unique identifier)')
    parser.add_argument('--description', '-d', help='Entity description')
    parser.add_argument('--type', '-t', dest='object_type', help='Object type (internal name)')
    parser.add_argument('--container', '-c', help='Container ID')
    parser.add_argument('--folder', '-f', help='Folder ID')
    parser.add_argument('--props', '-p', help='Additional properties as JSON string')
    parser.add_argument('--output', '-o', help='Output file for JSON response')
    parser.add_argument('--raw', '-r', action='store_true', help='Output raw JSON response')
    
    args = parser.parse_args()
    
    # Create entity
    result = create_entity(
        entity_type=args.entity,
        name=args.name,
        number=args.number,
        description=args.description,
        object_type=args.object_type,
        container=args.container,
        folder=args.folder,
        props=args.props,
        output_file=args.output,
        raw_output=args.raw
    )
    
    return 0 if result is not None else 1


if __name__ == '__main__':
    sys.exit(main())
