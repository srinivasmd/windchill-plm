#!/usr/bin/env python3
"""
Simple script to get suppliers from Windchill SupplierMgmt
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
endpoint = f"{odata_base}/SupplierMgmt/Suppliers"

# Query with top 10
params = {
    "$top": 10
}

print(f"Querying: {endpoint}")
print()

try:
    response = session.get(endpoint, params=params, timeout=60)
    print(f"Request URL: {response.request.url}")
    print(f"Status: {response.status_code}")
    print()

    if response.status_code == 200:
        data = response.json()
        results = data.get("value", [])
        print(f"Found {len(results)} suppliers:")
        print()

        # Print summary
        for supplier in results:
            print(f"  - {supplier.get('Identity', 'N/A')}")
            print(f"    Name: {supplier.get('Name', 'N/A')}")
            print(f"    State: {supplier.get('State', {}).get('Display', 'N/A')}")
            print(f"    Organization: {supplier.get('OrganizationName', 'N/A')}")
            print()
    else:
        print(f"Error: {response.text}")
except requests.exceptions.Timeout:
    print("Error: Request timed out after 60 seconds")
except Exception as e:
    print(f"Error: {e}")
