#!/usr/bin/env python3
"""
Get Suppliers from Windchill using REST API
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

# REST API endpoint for suppliers
server_url = config["server_url"].rstrip('/')
url = f"{server_url}/api/v3/objects/WTPart/search"

print(f"Querying: {url}")
print()

try:
    response = session.get(url, timeout=30)
    print(f"Status: {response.status_code}")
    print()

    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        print(f"Found {len(items)} parts:")
        print()
        for item in items[:10]:
            print(f"  - {item.get('displayIdentifier', item.get('number', 'N/A'))}: {item.get('name', 'N/A')}")
    else:
        print(f"Error: {response.text}")
except requests.exceptions.Timeout:
    print("Error: Request timed out")
except Exception as e:
    print(f"Error: {e}")
