#!/usr/bin/env python3
"""
Parse Document Management Domain metadata and extract entities with operations.
"""

import xml.etree.ElementTree as ET
import json

# Load the metadata
metadata_file = 'C:/Users/11746/.nanobot/workspace/skills/windchill-plm/references/DocMgmt_Metadata.xml'
with open(metadata_file, 'r', encoding='utf-8') as f:
    metadata_content = f.read()

# Parse XML
ET.register_namespace('', 'http://docs.oasis-open.org/odata/ns/edm')
ET.register_namespace('edmx', 'http://docs.oasis-open.org/odata/ns/edmx')
ET.register_namespace('annotation', 'http://docs.oasis-open.org/odata/ns/edm')

root = ET.fromstring(metadata_content)

# Define namespaces
ns = {'edm': 'http://docs.oasis-open.org/odata/ns/edm',
      'edmx': 'http://docs.oasis-open.org/odata/ns/edmx'}

# Find all EntityType elements
entities = {}
for entity_type in root.findall('.//edm:EntityType', ns):
    name = entity_type.get('Name')
    base_type = entity_type.get('BaseType', '')
    description = ""

    # Find description annotation
    for annotation in entity_type.findall('.//edm:Annotation[@Term="Core.Description"]/edm:String', ns):
        description = annotation.text if annotation.text else ""

    # Find operations annotation
    operations = ""
    for annotation in entity_type.findall('.//edm:Annotation[@Term="PTC.Operations"]/edm:String', ns):
        operations = annotation.text if annotation.text else ""

    # Find capabilities annotation
    capabilities = ""
    for annotation in entity_type.findall('.//edm:Annotation[@Term="PTC.Capabilities"]/edm:String', ns):
        capabilities = annotation.text if annotation.text else ""

    # Find properties
    properties = []
    for prop in entity_type.findall('edm:Property', ns):
        prop_name = prop.get('Name')
        prop_type = prop.get('Type')
        properties.append(f"{prop_name}: {prop_type}")

    entities[name] = {
        'base_type': base_type,
        'description': description,
        'operations': operations,
        'capabilities': capabilities,
        'properties': properties
    }

# Print summary
print("="*80)
print("DOCUMENT MANAGEMENT DOMAIN - ENTITY SUMMARY")
print("="*80)
print()

# Group by base type
base_types = {}
for name, data in entities.items():
    base = data['base_type'].split('.')[-1] if data['base_type'] else 'Root'
    if base not in base_types:
        base_types[base] = []
    base_types[base].append((name, data))

# Print by base type
for base, items in sorted(base_types.items()):
    print(f"\n{'='*80}")
    print(f"Base Type: {base}")
    print(f"{'='*80}")
    for name, data in items:
        print(f"\n[ENTITY] {name}")
        if data['description']:
            print(f"   Description: {data['description']}")
        if data['operations']:
            print(f"   Operations: {data['operations']}")
        if data['capabilities']:
            print(f"   Capabilities: {data['capabilities']}")
        if data['properties']:
            print(f"   Properties ({len(data['properties'])}):")
            for prop in data['properties'][:10]:
                print(f"      - {prop}")
            if len(data['properties']) > 10:
                print(f"      ... and {len(data['properties']) - 10} more")

# Save JSON summary
output_file = 'C:/Users/11746/.nanobot/workspace/skills/windchill-plm/references/DocMgmt_Entities.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(entities, f, indent=2)
print(f"\n\n[OK] Entity summary saved to: {output_file}")