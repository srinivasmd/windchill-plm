#!/usr/bin/env python3
"""
Query BOM and show full raw response
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
        
        # Query Uses
        uses_endpoint = f"{odata_base}/ProdMgmt/Parts('{part_id}')/Uses"
        response_uses = session.get(uses_endpoint)
        
        if response_uses.status_code == 200:
            uses_data = response_uses.json()
            print("RAW USES RESPONSE:")
            print(json.dumps(uses_data, indent=2))
        else:
            print(f"Error: {response_uses.text}")
