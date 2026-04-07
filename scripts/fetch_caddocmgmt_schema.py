#!/usr/bin/env python3
"""
Fetch CAD Document Management domain schema from Windchill OData API
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from windchill_client import WindchillClient

def fetch_caddocmgmt_schema():
    """Fetch CAD Document Management domain metadata"""
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    schema_url = f"{odata_base_url.rstrip('/')}/CADDocumentMgmt/$metadata"

    print(f"Fetching CAD Document Management schema from:")
    print(f"  {schema_url}")

    try:
        response = client.session.get(schema_url)
        response.raise_for_status()

        xml_content = response.text

        # Save XML metadata
        output_dir = Path(__file__).parent.parent / "references"
        output_dir.mkdir(exist_ok=True)
        xml_file = output_dir / "CADDocumentMgmt_METADATA.xml"

        with open(xml_file, 'w', encoding='utf-8') as f:
            f.write(xml_content)

        print(f"\n[OK] Saved XML metadata to: {xml_file}")

        # Also save as JSON for easier parsing
        schema_data = {
            "domain": "CADDocumentMgmt",
            "base_url": f"{odata_base_url.rstrip('/')}/CADDocumentMgmt/",
            "metadata_url": schema_url,
            "xml_content": xml_content
        }

        json_file = output_dir / "CADDocumentMgmt_METADATA.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(schema_data, f, indent=2)

        print(f"[OK] Saved JSON metadata to: {json_file}")

        # Parse and display key entities
        print("\n[INFO] Parsing entities from schema...")
        entities = parse_entities_from_xml(xml_content)

        print(f"\n[OK] Found {len(entities)} entity types:")
        for i, entity in enumerate(entities, 1):
            print(f"  {i}. {entity}")

        return schema_data

    except Exception as e:
        print(f"\n[ERROR] Failed to fetch schema: {e}")
        return None

def parse_entities_from_xml(xml_content):
    """Parse entity type names from XML metadata"""
    entities = []
    in_entity_type = False

    for line in xml_content.split('\n'):
        line = line.strip()
        if '<EntityType Name="' in line:
            # Extract entity name
            start = line.find('Name="') + 6
            end = line.find('"', start)
            entity_name = line[start:end]
            if not entity_name.startswith('PTC.'):  # Skip internal PTC types
                entities.append(entity_name)
        elif '<ComplexType Name="' in line:
            # Extract complex type name
            start = line.find('Name="') + 6
            end = line.find('"', start)
            type_name = line[start:end]
            if not type_name.startswith('PTC.'):
                entities.append(f"[Complex] {type_name}")

    return entities

if __name__ == "__main__":
    fetch_caddocmgmt_schema()