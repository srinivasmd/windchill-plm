#!/usr/bin/env python3
"""
Get attachments for a specific Windchill document
"""

import json
import requests
from pathlib import Path
from urllib.parse import quote

# Load config
CONFIG_PATH = Path(__file__).parent.parent / "config.json"
with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

# Setup session
session = requests.Session()
session.verify = config.get("verify_ssl", True)
session.auth = (config["basic"]["username"], config["basic"]["password"])

# OData base URL
base_url = config["server_url"] + "/servlet/odata"

# Document ID from our previous query - needs URL encoding
document_id = "OR:wt.doc.WTDocument:2347188"
document_number = "0000000161"

# Properly encode the document ID for OData
encoded_id = document_id.replace(":", "%3A")

print(f"Getting attachments for document: {document_number}")
print(f"Document ID: {document_id}")
print()

# First, get the document with attachments expanded
doc_endpoint = f"{base_url}/DocMgmt/Documents('{encoded_id}')"
params = {
    "$select": "*",
    "$expand": "PrimaryContent,Attachments"
}

print(f"Querying: {doc_endpoint}")
response = session.get(doc_endpoint, params=params)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()

    print("\n" + "="*60)
    print("DOCUMENT SUMMARY")
    print("="*60)
    print(f"Number: {data.get('Number', 'N/A')}")
    print(f"Name: {data.get('Name', 'N/A')}")
    print(f"Version: {data.get('Version', 'N/A')}.{data.get('Revision', 'N/A')}")
    print(f"State: {data.get('State', {}).get('Display', 'N/A')}")
    print(f"Created: {data.get('CreatedOn', 'N/A')}")
    print(f"ID: {data.get('ID', 'N/A')}")

    # Primary Content
    primary_content = data.get("PrimaryContent")
    if primary_content:
        print("\n" + "-"*60)
        print("PRIMARY CONTENT:")
        print("-"*60)
        if isinstance(primary_content, dict):
            print(f"FileName: {primary_content.get('FileName', 'N/A')}")
            print(f"FileSize: {primary_content.get('FileSize', 'N/A')} bytes")
            print(f"FileType: {primary_content.get('FileType', 'N/A')}")
            print(f"ID: {primary_content.get('ID', 'N/A')}")
        elif isinstance(primary_content, list) and primary_content:
            for pc in primary_content:
                print(f"  FileName: {pc.get('FileName', 'N/A')}")
                print(f"  FileSize: {pc.get('FileSize', 'N/A')} bytes")
                print(f"  FileType: {pc.get('FileType', 'N/A')}")
                print(f"  ID: {pc.get('ID', 'N/A')}")

    # Attachments
    attachments = data.get("Attachments", [])
    if attachments:
        print(f"\n" + "-"*60)
        print(f"ATTACHMENTS ({len(attachments)}):")
        print("-"*60)
        for i, att in enumerate(attachments, 1):
            print(f"\n{i}. {att.get('FileName', 'N/A')}")
            print(f"   Role: {att.get('Role', {}).get('Display', 'N/A')}")
            print(f"   FileType: {att.get('FileType', 'N/A')}")
            print(f"   FileSize: {att.get('FileSize', 'N/A')} bytes")
            print(f"   ID: {att.get('ID', 'N/A')}")
            print(f"   MasterID: {att.get('MasterID', 'N/A')}")

            # Get the download URL for this attachment
            content_id = att.get('ID')
            if content_id:
                encoded_content_id = content_id.replace(":", "%3A")
                download_url = f"{base_url}/DocMgmt/Contents('{encoded_content_id}')/$value"
                print(f"   Download URL: {download_url}")
    else:
        print("\n" + "-"*60)
        print("ATTACHMENTS: None found")

    # Save full response for reference
    with open(Path(__file__).parent / f"document_{document_number}_attachments.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"\nFull data saved to: document_{document_number}_attachments.json")
else:
    print(f"Error: {response.text}")
