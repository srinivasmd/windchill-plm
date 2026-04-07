#!/usr/bin/env python3
"""
Simple script to query Windchill Parts
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

# Query with top parameter
params = {
    "$top": 10
}

print(f"Querying: {endpoint}")
print()

response = session.get(endpoint, params=params)
print(f"Request URL: {response.request.url}")
print(f"Status: {response.status_code}")
print()

if response.status_code == 200:
    data = response.json()
    results = data.get("value", [])
    print(f"Found {len(results)} parts:")
    print()
    
    for part in results:
        number = part.get("Number", "N/A")
        name = part.get("Name", "N/A")
        state = part.get("State", {}).get("Display", "N/A")
        print(f"  - {number}: {name} [{state}]")
    
    print("\nFull JSON:")
    print(json.dumps(data, indent=2))
else:
    print(f"Error: {response.text}")
