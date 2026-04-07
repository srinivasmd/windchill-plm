#!/usr/bin/env python3
"""
Query BOM with expand
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
            "$expand": "UsedBy",
            "$top": 100
        }
        
        print("Querying Uses with expand=UsedBy...")
        response_uses = session.get(uses_endpoint, params=params)
        
        if response_uses.status_code == 200:
            uses_data = response_uses.json()
            uses_list = uses_data.get("value", [])
            
            print(f"Found {len(uses_list)} Uses items")
            print()
            
            for idx, use in enumerate(uses_list, 1):
                print(f"Use {idx}:")
                print(f"  ID: {use.get('ID')}")
                print(f"  Quantity: {use.get('Quantity')}")
                
                # Check if there's navigation to the child part
                if "UsedBy" in use:
                    print(f"  Has UsedBy: {use['UsedBy']}")
                else:
                    print(f"  Keys: {use.keys()}")
                print()
        
        # Also try querying PartUsageLink directly
        print("\n=== Trying PartUsageLink query ===")
        usagelink_endpoint = f"{odata_base}/ProdMgmt/PartUsageLinks"
        params = {
            "$filter": f"PartUsageLinkID eq '{part_id}'",
            "$top": 100
        }
        
        # Or try filtering by parent - different approaches
        # Let me check if there's a direct relationship
        
        # Another approach: Get ManufacturingBOM
        print("\n=== Trying ManufacturingBOM ===")
        mfg_bom_endpoint = f"{odata_base}/ProdMgmt/ManufacturingBOM"
        response_mfg = session.get(mfg_bom_endpoint, params={"$top": 1})
        
        if response_mfg.status_code == 200:
            mfg_data = response_mfg.json()
            print(f"ManufacturingBOM response keys: {mfg_data.keys()}")
            
            if "value" in mfg_data:
                print(f"Has items: {len(mfg_data['value'])}")
                if mfg_data["value"]:
                    print(f"Sample item keys: {mfg_data['value'][0].keys()}")
        
        # Check what navigation properties are available on Part
        print("\n=== Checking Part schema ===")
        
        # Try getting different navigations
        nav_properties = ["Uses", "UsedBy", "Parents", "Children", "Descendants", "Ancestors", "BOM"]
        
        for nav in nav_properties:
            nav_endpoint = f"{odata_base}/ProdMgmt/Parts('{part_id}')/{nav}"
            response_nav = session.get(nav_endpoint, params={"$top": 1})
            
            if response_nav.status_code == 200:
                data_nav = response_nav.json()
                value_count = len(data_nav.get("value", []))
                print(f"  {nav}: OK ({value_count} items)")
            else:
                print(f"  {nav}: Not available")
