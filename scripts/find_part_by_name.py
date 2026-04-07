#!/usr/bin/env python3
"""
Find part by name in Windchill
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
endpoint = f"{odata_base}/ProdMgmt/Parts"

# Query for part with name TOPLVL
params = {
    "$filter": f"Name eq 'TOPLVL'",
    "$top": 10
}

print(f"Querying: {endpoint}")
print(f"Filter: Name eq 'TOPLVL'")
print()

response = session.get(endpoint, params=params)
print(f"Request URL: {response.request.url}")
print(f"Status: {response.status_code}")
print()

if response.status_code == 200:
    data = response.json()
    results = data.get("value", [])
    print(f"Found {len(results)} part(s):")
    print()
    
    for part in results:
        number = part.get("Number", "N/A")
        name = part.get("Name", "N/A")
        state = part.get("State", {}).get("Display", "N/A")
        oid = part.get("ID", "N/A")
        print(f"  - Number: {number}")
        print(f"    Name: {name}")
        print(f"    State: {state}")
        print(f"    ID: {oid}")
        print()
    
    # Save part number for BOM query
    if results:
        with open("/tmp/toplvl_part.json", 'w') as f:
            json.dump(results[0], f, indent=2)
        print(f"First part saved to /tmp/toplvl_part.json")
else:
    print(f"Error: {response.text}")
