#!/usr/bin/env python3
"""
Fetch Document Management Domain schema from Windchill OData API.
"""

import requests
from requests.auth import HTTPBasicAuth
import json

# Configuration
base_url = 'https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/DocMgmt/'
username = 'pat'
password = 'ptc'

print(f"Fetching schema from: {base_url}")
print(f"Username: {username}")
print()

# Fetch service document
print("=== Fetching Service Document ===")
response = requests.get(base_url, auth=HTTPBasicAuth(username, password), verify=True)
print(f"Status Code: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")
if response.status_code == 200:
    print(f"Content:\n{json.dumps(response.json(), indent=2)}")
else:
    print(f"Error: {response.text}")

print("\n" + "="*60 + "\n")

# Fetch metadata
print("=== Fetching Metadata ===")
metadata_url = base_url + '$metadata'
response = requests.get(metadata_url, auth=HTTPBasicAuth(username, password), verify=True)
print(f"Status Code: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")
print(f"Content Length: {len(response.text)} characters")

if response.status_code == 200:
    # Save metadata to file
    output_file = 'C:/Users/11746/.nanobot/workspace/skills/windchill-plm/references/DocMgmt_Metadata.xml'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f"\n[OK] Metadata saved to: {output_file}")
    print("\n--- METADATA PREVIEW ---")
    print(response.text[:3000])
else:
    print(f"Error: {response.text}")