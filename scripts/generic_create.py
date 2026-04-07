#!/usr/bin/env python3
"""Generic CREATE script for Windchill entities.

This script provides a unified interface to create any entity type
that supports CREATE operations in Windchill PLM.

Usage:
    python generic_create.py --entity Document --name "My Doc" --number "DOC-001"
    python generic_create.py --entity Part --name "My Part" --number "PART-001"
    python generic_create.py --entity Quality --name "Quality Doc" --number "QUAL-001"

Supported entities for CREATE (DocMgmt domain):
    Document, ControlledDocument, Quality, General, Record, TestDocument,
    ReferenceDocument, SoftwareDocument, InterCommData, Presentation,
    SoftwareBuild, Msds, PublishedContent, Minutes, QMSDocument,
    TranslationDocument, Plan, StandardOperatingProcedure, GarrettTRL,
    SoftwareConfigurationData

Other domains:
    ProdMgmt: Part
    SupplierMgmt: Manufacturer, Vendor
    DataAdmin: Folder, Container
    CEM: CustomerExperience, RelatedProduct
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
    # DocMgmt
    'Document': 'DocMgmt',
    'ControlledDocument': 'DocMgmt',
    'Quality': 'DocMgmt',
    'General': 'DocMgmt',
    'Record': 'DocMgmt',
    'TestDocument': 'DocMgmt',
    'ReferenceDocument': 'DocMgmt',
    'SoftwareDocument': 'DocMgmt',
    'InterCommData': 'DocMgmt',
    'Presentation': 'DocMgmt',
    'SoftwareBuild': 'DocMgmt',
    'Msds': 'DocMgmt',
    'PublishedContent': 'DocMgmt',
    'Minutes': 'DocMgmt',
    'QMSDocument': 'DocMgmt',
    'TranslationDocument': 'DocMgmt',
    'Plan': 'DocMgmt',
    'StandardOperatingProcedure': 'DocMgmt',
    'GarrettTRL': 'DocMgmt',
    'SoftwareConfigurationData': 'DocMgmt',
    'ApprovedRecord': 'DocMgmt',
    'Specification': 'DocMgmt',
    'WorkRecord': 'DocMgmt',
    # ProdMgmt
    'Part': 'ProdMgmt',
    # DataAdmin
    'Folder': 'DataAdmin',
    'Container': 'DataAdmin',
    # ChangeMgmt
    'ChangeNotice': 'ChangeMgmt',
    'ChangeRequest': 'ChangeMgmt',
    'ChangeTask': 'ChangeMgmt',
    # QMS
    'QualityAction': 'QMS',
    'QualityObject': 'QMS',
    'NonConformance': 'QMS',
    'CAPA': 'QMS',
    'Place': 'QMS',
    'QualityContact': 'QMS',
    'Subject': 'QMS',
    # CEM
    'CustomerExperience': 'CEM',
    'RelatedProduct': 'CEM',
    # PrincipalMgmt
    'User': 'PrincipalMgmt',
    'Group': 'PrincipalMgmt',
    'Organization': 'PrincipalMgmt',
}

# Required properties for each entity type
ENTITY_REQUIRED_PROPS = {
    'Document': ['Name', 'Number'],
    'Part': ['Name', 'Number'],
    'Folder': ['Name'],
    'Container': ['Name'],
    'ControlledDocument': ['Name', 'Number'],
    'Quality': ['Name', 'Number'],
    'Record': ['Name', 'Number'],
    'ChangeNotice': ['Name', 'Number'],
    'ChangeRequest': ['Name', 'Number'],
    'ChangeTask': ['Name', 'Number'],
    'CustomerExperience': ['Name'],
    'QualityAction': ['Name', 'Number'],
    'NonConformance': ['Name', 'Number'],
    'CAPA': ['Name', 'Number'],
}

# Default properties for entity creation
ENTITY_DEFAULT_PROPS = {
    'Document': {'ObjectType': 'WCTYPE|com.ptc.DocMgmt.Document'},
    'Part': {'ObjectType': 'WCTYPE|com.ptc.ProdMgmt.Part'},
    'Folder': {'ObjectType': 'WCTYPE|com.ptc.DataAdmin.Folder'},
}


def create_entity(entity_type, properties, container_id=None, folder_id=None, output_file=None, raw_output=False):
    """
    Create an entity in Windchill PLM.
    
    Args:
        entity_type: Type of entity to create (Document, Part, etc.)
        properties: Dictionary of entity properties
        container_id: Optional container ID
        folder_id: Optional folder ID
        output_file: Optional file to save JSON response
        raw_output: If True, output raw JSON
        
    Returns:
        dict: Created entity data or None on failure
    """
    client = WindchillClient()
    
    # Get domain for entity type
    domain = ENTITY_DOMAIN_MAP.get(entity_type)
    if not domain:
        print(f"[ERROR] Unknown entity type: {entity_type}")
        print(f"Supported types: {', '.join(ENTITY_DOMAIN_MAP.keys())}")
        return None
    
    # Build URL
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/{domain}/{entity_type}s"
    
    # Merge default properties
    entity_props = ENTITY_DEFAULT_PROPS.get(entity_type, {})
    entity_props.update(properties)
    
    # Add container and folder if provided
    if container_id:
        entity_props['Context@odata.bind'] = container_id
    if folder_id:
        entity_props['Folder@odata.bind'] = folder_id
    
    # Get CSRF token for write operation
    csrf_token = client.get_csrf_token()
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    if csrf_token:
        headers['CSRF_NONCE'] = csrf_token
    
    try:
        response = client.session.post(url, json=entity_props, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if raw_output:
            print(json.dumps(data, indent=2))
        else:
            print(f"\n[OK] {entity_type} created successfully!")
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
        print(f"\n[ERROR] Failed to create {entity_type}: {e}")
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
        description=f"Create a new entity in Windchill PLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Supported entity types:
  DocMgmt: {', '.join([e for e, d in ENTITY_DOMAIN_MAP.items() if d == 'DocMgmt'])}
  ProdMgmt: {', '.join([e for e, d in ENTITY_DOMAIN_MAP.items() if d == 'ProdMgmt'])}
  DataAdmin: {', '.join([e for e, d in ENTITY_DOMAIN_MAP.items() if d == 'DataAdmin'])}
  ChangeMgmt: {', '.join([e for e, d in ENTITY_DOMAIN_MAP.items() if d == 'ChangeMgmt'])}
  QMS: {', '.join([e for e, d in ENTITY_DOMAIN_MAP.items() if d == 'QMS'])}
  CEM: {', '.join([e for e, d in ENTITY_DOMAIN_MAP.items() if d == 'CEM'])}

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
    
    # Build properties dictionary
    properties = {}
    
    if args.name:
        properties['Name'] = args.name
    if args.number:
        properties['Number'] = args.number
    if args.description:
        properties['Description'] = args.description
    if args.object_type:
        properties['ObjectType'] = args.object_type
    
    # Parse additional properties
    if args.props:
        try:
            additional_props = json.loads(args.props)
            properties.update(additional_props)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON in --props: {e}")
            return 1
    
    # Validate required properties
    required = ENTITY_REQUIRED_PROPS.get(args.entity, ['Name'])
    missing = [r for r in required if r not in properties]
    if missing:
        print(f"[ERROR] Missing required properties: {', '.join(missing)}")
        print(f"Required for {args.entity}: {', '.join(required)}")
        return 1
    
    # Create entity
    result = create_entity(
        entity_type=args.entity,
        properties=properties,
        container_id=args.container,
        folder_id=args.folder,
        output_file=args.output,
        raw_output=args.raw
    )
    
    return 0 if result else 1


if __name__ == '__main__':
    sys.exit(main())
