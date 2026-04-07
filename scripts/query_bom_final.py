#!/usr/bin/env python3
"""
Query BOM with Uses expand
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

# Find part TOPLVL
part_number = "TOPLVL"
endpoint = f"{odata_base}/ProdMgmt/Parts"
response = session.get(endpoint, params={"$filter": f"Number eq '{part_number}'"})

if response.status_code == 200:
    data = response.json()
    parts = data.get("value", [])
    
    if parts:
        part = parts[0]
        part_id = part.get("ID")
        
        print(f"Parent Part: {part.get('Number')} - {part.get('Name')}")
        print(f"ID: {part_id}")
        print()
        
        # Query Uses with expand to get child parts
        uses_endpoint = f"{odata_base}/ProdMgmt/Parts('{part_id}')/Uses"
        params = {
            "$expand": "Uses",
            "$top": 100
        }
        
        print("Querying Uses with expand=Uses...")
        response_uses = session.get(uses_endpoint, params=params)
        
        if response_uses.status_code == 200:
            uses_data = response_uses.json()
            uses_list = uses_data.get("value", [])
            
            print(f"Found {len(uses_list)} Uses items")
            print()
            
            bom_result = {
                "parent_part": part,
                "bom_items": []
            }
            
            for idx, use in enumerate(uses_list, 1):
                print(f"BOM Item {idx}:")
                print(f"  Usage ID: {use.get('ID')}")
                print(f"  Quantity: {use.get('Quantity')} {use.get('Unit', {}).get('Display', '')}")
                
                # Check if there's a Uses navigation (which contains the child part)
                if "Uses" in use and isinstance(use["Uses"], dict):
                    child_part = use["Uses"]
                    child_num = child_part.get("Number", "N/A")
                    child_name = child_part.get("Name", "N/A")
                    child_state = child_part.get("State", {}).get("Display", "N/A")
                    child_id = child_part.get("ID", "N/A")
                    
                    print(f"  Child Part:")
                    print(f"    Number: {child_num}")
                    print(f"    Name: {child_name}")
                    print(f"    State: {child_state}")
                    print(f"    ID: {child_id}")
                    
                    bom_result["bom_items"].append({
                        "usage": use,
                        "child_part": child_part
                    })
                else:
                    print(f"  No child part data available")
                    print(f"  Available keys: {use.keys()}")
                print()
            
            # Save results
            with open("/tmp/bom_topvl.json", 'w') as f:
                json.dump(bom_result, f, indent=2)
            print(f"Full BOM saved to /tmp/bom_topvl.json")
            
            # Summary
            print()
            print("="*60)
            print("BOM SUMMARY FOR TOPLVL")
            print("="*60)
            print(f"Parent: {part.get('Number')} - {part.get('Name')}")
            print(f"Total Components: {len(bom_result['bom_items'])}")
            print()
            
            for idx, item in enumerate(bom_result['bom_items'], 1):
                child = item['child_part']
                usage = item['usage']
                child_num = child.get('Number', 'N/A')
                child_name = child.get('Name', 'N/A')
                qty = usage.get('Quantity', 'N/A')
                state = child.get('State', {}).get('Display', 'N/A')
                
                print(f"{idx}. {child_num} - {child_name}")
                print(f"   Quantity: {qty} | State: {state}")
                print()
