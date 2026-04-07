#!/usr/bin/env python3
"""
Query BOM for part using Uses navigation property
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

# Query the BOM for part TOPLVL
part_number = "TOPLVL"

# First get the part
endpoint = f"{odata_base}/ProdMgmt/Parts"
params = {"$filter": f"Number eq '{part_number}'"}

print(f"=== Finding part: {part_number} ===")
response = session.get(endpoint, params=params)

if response.status_code == 200:
    data = response.json()
    parts = data.get("value", [])
    
    if parts:
        part = parts[0]
        part_id = part.get("ID")
        part_num = part.get("Number")
        part_name = part.get("Name")
        
        print(f"Found: {part_num} - {part_name}")
        print(f"ID: {part_id}")
        print(f"State: {part.get('State', {}).get('Display')}")
        print(f"EndItem: {part.get('EndItem')}")
        print()
        
        # Query Uses (children in BOM)
        uses_endpoint = f"{odata_base}/ProdMgmt/Parts('{part_id}')/Uses"
        print(f"=== Querying BOM (Uses) ===")
        print(f"URL: {uses_endpoint}")
        
        response_uses = session.get(uses_endpoint, params={"$top": 200})
        print(f"Status: {response_uses.status_code}")
        
        if response_uses.status_code == 200:
            uses_data = response_uses.json()
            uses_list = uses_data.get("value", [])
            
            print(f"Found {len(uses_list)} BOM items (Uses):")
            print()
            
            # Build full result with child part details
            bom_result = {
                "parent_part": part,
                "bom_items": []
            }
            
            for idx, use in enumerate(uses_list, 1):
                # Extract usage information
                quantity = use.get("Quantity", "N/A")
                line_item_num = use.get("LineNumber", "N/A")
                find_number = use.get("FindNumber", "N/A")
                
                # Get the child part (Uses contains a reference to the child)
                uses_ref = use.get("Uses", {})
                child_part_id = uses_ref.get("ID")
                child_part_link = uses_ref.get("__deferred", {}).get("uri")
                
                print(f"{idx}. Line Item: {line_item_num} | Find Number: {find_number} | Qty: {quantity}")
                
                # Query the actual child part
                if child_part_id:
                    child_endpoint = f"{odata_base}/ProdMgmt/Parts('{child_part_id}')"
                    response_child = session.get(child_endpoint)
                    
                    if response_child.status_code == 200:
                        child_part = response_child.json()
                        child_num = child_part.get("Number", "N/A")
                        child_name = child_part.get("Name", "N/A")
                        child_state = child_part.get("State", {}).get("Display", "N/A")
                        child_type = child_part.get("ObjectType", "N/A")
                        
                        print(f"   Part: {child_num} - {child_name}")
                        print(f"   Type: {child_type} | State: {child_state}")
                        
                        # Add to result
                        bom_result["bom_items"].append({
                            "usage": use,
                            "child_part": child_part
                        })
                    else:
                        print(f"   Failed to get child part: {response_child.text}")
                else:
                    print(f"   No child part ID found")
                
                print()
            
            # Save results
            with open("/tmp/bom_toplvl.json", 'w') as f:
                json.dump(bom_result, f, indent=2)
            print(f"Full BOM data saved to /tmp/bom_toplvl.json")
            
            # Summary
            print()
            print("="*60)
            print("BOM SUMMARY")
            print("="*60)
            print(f"Parent Part: {part_num} - {part_name}")
            print(f"Total BOM Items: {len(bom_result['bom_items'])}")
            print()
            
            for idx, item in enumerate(bom_result['bom_items'], 1):
                child = item['child_part']
                usage = item['usage']
                print(f"{idx}. {child.get('Number')}: {child.get('Name')}")
                print(f"   Qty: {usage.get('Quantity')} | State: {child.get('State', {}).get('Display')}")
            
        else:
            print(f"Error querying Uses: {response_uses.text}")
    else:
        print(f"Part '{part_number}' not found")
else:
    print(f"Error: {response.text}")
