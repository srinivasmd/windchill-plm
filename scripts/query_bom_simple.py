#!/usr/bin/env python3
"""
Simple BOM query script
"""

import json
import requests
from pathlib import Path

# Load config
CONFIG_PATH = Path(__file__).parent.parent / "config.json"
with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

# Setup session
session = requests.Session()
session.verify = config.get("verify_ssl", True)
session.auth = (config["basic"]["username"], config["basic"]["password"])

# OData endpoint
odata_base = config["server_url"] + "/servlet/odata"

# First, get the part by name
part_number = "TOPLVL"  # from our previous search
endpoint = f"{odata_base}/ProdMgmt/Parts"
params = {
    "$filter": f"Number eq '{part_number}'"
}

print(f"=== Finding part with Number: {part_number} ===")
response = session.get(endpoint, params=params)

if response.status_code == 200:
    data = response.json()
    parts = data.get("value", [])
    
    if parts:
        part = parts[0]
        part_id = part.get("ID")
        part_number = part.get("Number")
        part_name = part.get("Name")
        part_state = part.get("State", {}).get("Display")
        
        print(f"Found Part:")
        print(f"  Number: {part_number}")
        print(f"  Name: {part_name}")
        print(f"  State: {part_state}")
        print(f"  ID: {part_id}")
        print()
        
        # Now query for BOM children using the navigation property
        # The children are typically accessed via UsedBy or similar navigation
        print(f"=== Querying BOM (UsedBy/Children) ===")
        
        # Try multiple approaches to get BOM children
        # Approach 1: Use the Children navigation property
        children_endpoint = f"{odata_base}/ProdMgmt/Parts('{part_id}')/Children"
        print(f"Fetching: {children_endpoint}")
        
        response_children = session.get(children_endpoint, params={"$top": 100})
        print(f"Status: {response_children.status_code}")
        
        if response_children.status_code == 200:
            children_data = response_children.json()
            children = children_data.get("value", [])
            print(f"Found {len(children)} children via Children endpoint")
            print()
        else:
            print(f"Children endpoint failed: {response_children.text}")
            children = []
        
        # Approach 2: Try UsedBy (parts that use this part)
        if not children:
            usedby_endpoint = f"{odata_base}/ProdMgmt/Parts('{part_id}')/UsedBy"
            print(f"Trying UsedBy endpoint: {usedby_endpoint}")
            response_usedby = session.get(usedby_endpoint, params={"$top": 100})
            
            if response_usedby.status_code == 200:
                usedby_data = response_usedby.json()
                children = usedby_data.get("value", [])
                print(f"Found {len(children)} items via UsedBy endpoint")
            else:
                print(f"UsedBy endpoint failed: {response_usedby.text}")
        
        # Approach 3: Try getting BOMStructure or similar
        if not children:
            # Use a filter to find parts that have this as parent
            bom_endpoint = f"{odata_base}/ProdMgmt"
            bom_params = {
                "$filter": f"ParentID eq '{part_id}'",
                "$top": 100
            }
            print(f"Trying BOM query with ParentID filter")
            response_bom = session.get(bom_endpoint, params=bom_params)
            print(f"BOM query Status: {response_bom.status_code}")
            
            if response_bom.status_code == 200:
                bom_data = response_bom.json()
                print(f"Response keys: {bom_data.keys()}")
        
        print()
        
        # Display the results
        if children:
            print(f"=== BOM Structure for {part_number} ({part_name}) ===")
            print(f"Total Children: {len(children)}")
            print()
            
            for idx, child in enumerate(children, 1):
                child_num = child.get("Number", "N/A")
                child_name = child.get("Name", "N/A")
                child_state = child.get("State", {}).get("Display", "N/A")
                child_qty = child.get("Quantity", "N/A")
                child_id = child.get("ID", "N/A")
                
                print(f"{idx}. {child_num} - {child_name}")
                print(f"   State: {child_state}")
                if child_qty != "N/A":
                    print(f"   Quantity: {child_qty}")
                print(f"   ID: {child_id}")
                print()
            
            # Save full results
            result_data = {
                "parent_part": part,
                "children": children
            }
            
            with open("/tmp/bom toplvl.json", 'w') as f:
                json.dumps(result_data, f, indent=2)
            print(f"Full BOM data saved to /tmp/bom_toplvl.json")
        else:
            print("No children found. This might be:")
            print("  - A leaf part with no subcomponents")
            print("  - Using a different BOM structure endpoint")
            print()
            print("Full part details:")
            print(json.dumps(part, indent=2))
            print()
            print("Available navigation properties might include:")
            print("  - Children, UsedBy, Uses, Parents, BOMStructure")
    else:
        print(f"Part '{part_number}' not found")
else:
    print(f"Error querying part: {response.text}")
