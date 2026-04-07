#!/usr/bin/env python3
"""
Find a document ending with the specified number suffix
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
endpoint = config["server_url"] + "/servlet/odata/DocMgmt/Documents"

# Search for document ending with 000161
target_suffix = "000161"
skip = 0
found = None
max_docs = 5000  # Limit to avoid infinite loops

print(f"Searching for document ending with {target_suffix}...")
print()

while not found and skip < max_docs:
    params = {"$top": 100, "$skip": skip}
    response = session.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
        results = data.get("value", [])

        if not results:
            break

        for doc in results:
            number = doc.get("Number", "")
            if number.endswith(target_suffix):
                found = doc
                break

        skip += len(results)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        break

if found:
    print("FOUND DOCUMENT:")
    print("=" * 60)
    print(f"Number: {found['Number']}")
    print(f"Name: {found['Name']}")
    print(f"Type: {found['DocTypeName']}")
    print(f"Version: {found['Version']}")
    print(f"Revision: {found['Revision']}")
    print(f"State: {found['State']['Display']}")
    print(f"Folder: {found.get('FolderLocation', 'N/A')}")
    print(f"Created: {found['CreatedOn']}")
    print(f"ID: {found['ID']}")
    print()
    print("Full Document JSON:")
    print(json.dumps(found, indent=2))
else:
    print(f"No document found ending with {target_suffix}")
