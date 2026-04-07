#!/usr/bin/env python3
"""
Extract Navigation Properties from DocMgmt Metadata XML and update DocMgmt_Entities.json
"""

import xml.etree.ElementTree as ET
import json
from pathlib import Path

# Namespaces
NS_EDM = "http://docs.oasis-open.org/odata/ns/edm"
NS_EDMX = "http://docs.oasis-open.org/odata/ns/edmx"

# Paths
SKILL_DIR = Path(__file__).parent.parent
METADATA_FILE = SKILL_DIR / "references" / "DocMgmt_Metadata.xml"
ENTITIES_FILE = SKILL_DIR / "references" / "DocMgmt_Entities.json"

def parse_metadata_xml(xml_path):
    """Parse the metadata XML and extract entities with their navigation properties"""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Find the PTC.DocMgmt schema
    schema = root.find(f".//{{{NS_EDMX}}}DataServices//{{{NS_EDM}}}Schema[@Namespace='PTC.DocMgmt']")
    
    if schema is None:
        return None
    
    entities_data = {}
    
    # Find all EntityTypes
    for entity_type in schema.findall(f".//{{{NS_EDM}}}EntityType"):
        entity_name = entity_type.get("Name")
        base_type = entity_type.get("BaseType", "")
        
        # Get description
        description = ""
        desc_annotation = entity_type.find(f".//{{{NS_EDM}}}Annotation[@Term='Core.Description']//{{{NS_EDM}}}String")
        if desc_annotation is not None:
            description = desc_annotation.text or ""
        
        # Get operations
        operations = ""
        ops_annotation = entity_type.find(f".//{{{NS_EDM}}}Annotation[@Term='PTC.Operations']//{{{NS_EDM}}}String")
        if ops_annotation is not None:
            operations = ops_annotation.text or ""
        
        # Get capabilities
        capabilities = ""
        cap_annotation = entity_type.find(f".//{{{NS_EDM}}}Annotation[@Term='PTC.Capabilities']//{{{NS_EDM}}}String")
        if cap_annotation is not None:
            capabilities = cap_annotation.text or ""
        
        # Get properties
        properties = []
        for prop in entity_type.findall(f".//{{{NS_EDM}}}Property"):
            prop_name = prop.get("Name")
            prop_type = prop.get("Type")
            properties.append(f"{prop_name}: {prop_type}")
        
        # Get navigation properties
        navigation_properties = []
        for nav_prop in entity_type.findall(f".//{{{NS_EDM}}}NavigationProperty"):
            nav_name = nav_prop.get("Name")
            nav_type = nav_prop.get("Type")
            contains_target = nav_prop.get("ContainsTarget", "false")
            
            # Get annotations
            read_only = False
            read_only_annotation = nav_prop.find(f".//{{{NS_EDM}}}Annotation[@Term='PTC.ReadOnly']")
            if read_only_annotation is not None:
                read_only = True
            
            navigation_properties.append({
                "name": nav_name,
                "type": nav_type,
                "contains_target": contains_target == "true",
                "read_only": read_only
            })
        
        # Determine base type display
        if base_type:
            base_display = base_type.split(".")[-1] if "." in base_type else base_type
        else:
            base_display = ""
        
        entities_data[entity_name] = {
            "base_type": base_display,
            "description": description,
            "operations": operations,
            "capabilities": capabilities,
            "properties": properties,
            "navigations": navigation_properties
        }
    
    return entities_data

def update_entities_file(entities_file, entities_data):
    """Update the DocMgmt_Entities.json file with navigation properties"""
    
    # Read existing file to preserve any custom changes
    if entities_file.exists():
        with open(entities_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = {}
    
    # Update with navigation properties
    for entity_name, entity_info in entities_data.items():
        if entity_name in existing_data:
            # Preserve existing data, add navigations
            existing_data[entity_name]["navigations"] = entity_info["navigations"]
        else:
            # Add new entity
            existing_data[entity_name] = {
                "base_type": entity_info["base_type"],
                "description": entity_info["description"],
                "operations": entity_info["operations"],
                "capabilities": entity_info["capabilities"],
                "properties": entity_info["properties"],
                "navigations": entity_info["navigations"]
            }
    
    # Write updated file
    with open(entities_file, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)
    
    print(f"Updated {entities_file}")
    print(f"Total entities: {len(existing_data)}")
    
    # Count entities with navigations
    with_navigations = sum(1 for e in existing_data.values() if e.get("navigations"))
    print(f"Entities with navigation properties: {with_navigations}")
    
    # Print navigation summary
    print("\nNavigation Properties Summary:")
    for entity_name, entity_info in sorted(existing_data.items()):
        navs = entity_info.get("navigations", [])
        if navs:
            print(f"\n  {entity_name}:")
            for nav in navs:
                target = nav["type"].split(".")[-1] if "." in nav["type"] else nav["type"]
                collection = "Collection of " if nav["type"].startswith("Collection(") else ""
                readonly = " [Read-Only]" if nav["read_only"] else ""
                contains = " [Contains]" if nav["contains_target"] else ""
                print(f"    - {nav['name']} -> {collection}{target}{readonly}{contains}")

def main():
    print("Extracting navigation properties from DocMgmt metadata...")
    
    # Parse metadata
    entities_data = parse_metadata_xml(METADATA_FILE)
    
    if entities_data is None:
        print("Error: Could not parse metadata XML")
        return
    
    # Update entities file
    update_entities_file(ENTITIES_FILE, entities_data)
    
    print("\nDone!")

if __name__ == "__main__":
    main()