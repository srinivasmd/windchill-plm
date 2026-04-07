#!/usr/bin/env python3
"""
Fetch SupplierMgmt domain metadata from Windchill OData.
"""
import os
import sys
import json
import requests
from requests.auth import HTTPBasicAuth

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_windchill_credentials():
    """Get Windchill credentials from environment or hardcoded."""
    return {
        'base_url': 'https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/SupplierMgmt',
        'username': 'wcadmin',
        'password': 'wcadmin'
    }

def fetch_metadata():
    """Fetch SupplierMgmt metadata from Windchill."""
    creds = get_windchill_credentials()
    metadata_url = f"{creds['base_url']}/$metadata"

    response = requests.get(
        metadata_url,
        auth=HTTPBasicAuth(creds['username'], creds['password']),
        headers={'Accept': 'application/xml'}
    )

    if response.status_code == 200:
        return response.text
    else:
        print(f"Error fetching metadata: {response.status_code}")
        return None

def main():
    """Main function."""
    metadata = fetch_metadata()
    if metadata:
        # Save metadata
        refs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'references')
        os.makedirs(refs_dir, exist_ok=True)

        # Save XML metadata
        xml_file = os.path.join(refs_dir, 'SupplierMgmt_Metadata.xml')
        with open(xml_file, 'w', encoding='utf-8') as f:
            f.write(metadata)

        # Save JSON metadata
        json_file = os.path.join(refs_dir, 'SupplierMgmt_Metadata.json')
        import xml.etree.ElementTree as ET
        root = ET.fromstring(metadata)

        # Extract entities and navigation properties
        entities = {}
        namespace = {'edm': 'http://docs.oasis-open.org/odata/ns/edm',
                     'm': 'http://docs.oasis-open.org/odata/ns/metadata'}

        # Find all EntityType elements
        for entity_type in root.findall('.//edm:EntityType', namespace):
            name = entity_type.get('Name')
            base_type = entity_type.get('BaseType')

            properties = []
            nav_properties = []

            # Regular properties
            for prop in entity_type.findall('edm:Property', namespace):
                properties.append({
                    'name': prop.get('Name'),
                    'type': prop.get('Type'),
                    'nullable': prop.get('Nullable', 'true')
                })

            # Navigation properties
            for nav_prop in entity_type.findall('edm:NavigationProperty', namespace):
                nav_properties.append({
                    'name': nav_prop.get('Name'),
                    'type': nav_prop.get('Type'),
                    'containsTarget': nav_prop.get('ContainsTarget', 'false')
                })

            # If has base type, we'll handle inheritance
            entity_data = {
                'description': f"{name} entity",
                'properties': properties,
                'navigationProperties': nav_properties
            }

            if base_type:
                entity_data['baseType'] = base_type

            entities[name] = entity_data

        # Save entities JSON
        entities_file = os.path.join(refs_dir, 'SupplierMgmt_Entities.json')
        with open(entities_file, 'w', encoding='utf-8') as f:
            json.dump({'domain': 'SupplierMgmt', 'entities': entities}, f, indent=2)

        print(f"Metadata saved to: {xml_file}")
        print(f"Entities saved to: {entities_file}")

        # Generate navigation documentation
        nav_doc = "# SupplierMgmt Navigation Properties\n\n"
        nav_doc += "## Entity Navigation Properties\n\n"

        for entity_name, entity_data in entities.items():
            if entity_data['navigationProperties']:
                nav_doc += f"### {entity_name}\n\n"
                nav_doc += "| Property | Type | Contains Target |\n"
                nav_doc += "|----------|------|-----------------|\n"
                for nav_prop in entity_data['navigationProperties']:
                    nav_doc += f"| {nav_prop['name']} | {nav_prop['type']} | {nav_prop['containsTarget']} |\n"
                nav_doc += "\n"

        nav_file = os.path.join(refs_dir, 'SupplierMgmt_Navigations.md')
        with open(nav_file, 'w', encoding='utf-8') as f:
            f.write(nav_doc)

        print(f"Navigation documentation saved to: {nav_file}")

if __name__ == '__main__':
    main()