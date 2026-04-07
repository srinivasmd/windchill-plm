#!/usr/bin/env python3
"""Get Windchill Document with Primary Content"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from windchill_client import WindchillClient


def main():
    # Get command line arguments
    if len(sys.argv) < 2:
        print("Usage: python get_document.py <document_number> [base_url] [username] [password]")
        sys.exit(1)

    document_number = sys.argv[1]
    base_url = sys.argv[2] if len(sys.argv) > 2 else "https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/"
    username = sys.argv[3] if len(sys.argv) > 3 else "pat"
    password = sys.argv[4] if len(sys.argv) > 4 else "ptc"

    # Create client with direct credentials
    client = WindchillClient(base_url=base_url, username=username, password=password)

    # Get the document
    print(f"Fetching document: {document_number}")
    document = client.get_document_by_number(document_number)

    if not document:
        print(f"Error: Document {document_number} not found")
        sys.exit(1)

    document_id = document.get('ID')

    print(f"\n{'='*60}")
    print(f"DOCUMENT: {document.get('Number', 'N/A')} - {document.get('Name', 'N/A')}")
    print(f"ID: {document.get('ID', 'N/A')}")
    print(f"Type: {document.get('DocTypeName', 'N/A')}")
    print(f"Revision: {document.get('Revision', 'N/A')}")
    print(f"Version: {document.get('Version', 'N/A')}")
    print(f"State: {document.get('State', {}).get('Display', 'N/A')}")
    print(f"Folder: {document.get('FolderLocation', 'N/A')}")
    print(f"{'='*60}")

    # Get Attachments
    attachments = client.get_document_attachments(document_id)
    if attachments:
        print(f"\nATTACHMENTS ({len(attachments)}):")
        for att in attachments:
            file_name = att.get('FileName', 'N/A')
            file_size = att.get('FileSize', 0)
            file_type = att.get('FileType', 'N/A')
            role = att.get('Role', {}).get('Value', 'N/A')
            print(f"  ├─ {file_name}")
            print(f"  │   Size: {file_size} bytes | Type: {file_type} | Role: {role}")

    # Get Primary Content
    print(f"\nFetching primary content...")
    primary_content = client.get_document_primary_content(document_id)

    if primary_content:
        print(f"\nPRIMARY CONTENT:")
        if isinstance(primary_content, list) and primary_content:
            pc = primary_content[0]
            print(f"  ├─ File Name: {pc.get('FileName', 'N/A')}")
            print(f"  ├─ File Size: {pc.get('FileSize', 0)} bytes")
            print(f"  ├─ File Type: {pc.get('FileType', 'N/A')}")
            print(f"  ├─ Content URL: {pc.get('URL', 'N/A')}")
            print(f"  └─ Download URL: {pc.get('DownloadURL', 'N/A')}")
        elif isinstance(primary_content, dict):
            print(f"  ├─ File Name: {primary_content.get('FileName', 'N/A')}")
            print(f"  ├─ File Size: {primary_content.get('FileSize', 0)} bytes")
            print(f"  ├─ File Type: {primary_content.get('FileType', 'N/A')}")
            print(f"  ├─ Content URL: {primary_content.get('URL', 'N/A')}")
            print(f"  └─ Download URL: {primary_content.get('DownloadURL', 'N/A')}")
    else:
        print(f"\nNo primary content found")

    # Save full result to JSON
    result = {
        'document': document,
        'attachments': attachments,
        'primary_content': primary_content
    }

    output_file = f"document_{document_number}.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\nFull data saved to: {output_file}")


if __name__ == '__main__':
    main()