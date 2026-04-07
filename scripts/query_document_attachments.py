#!/usr/bin/env python3
"""Query Windchill Document and its Attachments"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from windchill_client import WindchillClient


def query_document_attachments(
    base_url: str,
    username: str,
    password: str,
    document_number: str,
    include_primary_content: bool = False,
    include_thumbnails: bool = False,
    include_versions: bool = False,
    output_file: str = None
):
    """
    Query a Windchill document and its attachments.

    Args:
        base_url: Windchill OData base URL
        username: Windchill username
        password: Windchill password
        document_number: Document number to query
        include_primary_content: Whether to fetch primary content info
        include_thumbnails: Whether to fetch thumbnails
        include_versions: Whether to fetch all versions
        output_file: Optional file path to save results

    Returns:
        dict: Document and attachments results
    """
    client = WindchillClient(base_url, username, password)

    # Get the document
    document = client.get_document_by_number(document_number)
    if not document:
        raise ValueError(f"Document {document_number} not found")

    document_id = document.get('ID')

    result = {
        'document': document,
        'attachments': [],
        'primary_content': None,
        'thumbnails': [],
        'versions': []
    }

    # Get Attachments
    attachments = client.get_document_attachments(document_id)
    result['attachments'] = attachments

    # Get Primary Content
    if include_primary_content:
        primary_content = client.get_document_primary_content(document_id)
        result['primary_content'] = primary_content

    # Get Thumbnails
    if include_thumbnails:
        thumbnails = client.get_document_thumbnails(document_id)
        result['thumbnails'] = thumbnails

    # Get Versions
    if include_versions:
        versions = client.get_document_versions(document_id)
        result['versions'] = versions

    # Save to file if specified
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Results saved to: {output_file}")

    return result


def print_document_summary(result: dict):
    """Print a summary of document and attachments"""
    document = result.get('document', {})
    attachments = result.get('attachments', [])
    primary_content = result.get('primary_content')
    thumbnails = result.get('thumbnails', [])
    versions = result.get('versions', [])

    print(f"\n{'='*60}")
    print(f"DOCUMENT: {document.get('Number', 'N/A')} - {document.get('Name', 'N/A')}")
    print(f"ID: {document.get('ID', 'N/A')}")
    print(f"Type: {document.get('DocTypeName', 'N/A')}")
    print(f"Revision: {document.get('Revision', 'N/A')}")
    print(f"Version: {document.get('Version', 'N/A')}")
    print(f"State: {document.get('State', {}).get('Display', 'N/A')}")
    print(f"Folder: {document.get('FolderLocation', 'N/A')}")
    print(f"{'='*60}")

    # Print attachments
    if attachments:
        print(f"\nATTACHMENTS ({len(attachments)}):")
        for att in attachments:
            file_name = att.get('FileName', 'N/A')
            file_size = att.get('FileSize', 0)
            file_type = att.get('FileType', 'N/A')
            role = att.get('Role', {}).get('Value', 'N/A')

            print(f"  ├─ {file_name}")
            print(f"  │   Size: {file_size} bytes | Type: {file_type} | Role: {role}")

    # Print primary content
    if primary_content:
        print(f"\nPRIMARY CONTENT:")
        if isinstance(primary_content, list) and primary_content:
            pc = primary_content[0]
            print(f"  ├─ {pc.get('FileName', 'N/A')}")
            print(f"  │   Size: {pc.get('FileSize', 0)} bytes")
        elif isinstance(primary_content, dict):
            print(f"  ├─ {primary_content.get('FileName', 'N/A')}")
            print(f"  │   Size: {primary_content.get('FileSize', 0)} bytes")

    # Print thumbnails
    if thumbnails:
        print(f"\nTHUMBNAILS ({len(thumbnails)}):")
        for thumb in thumbnails:
            print(f"  └─ {thumb.get('FileName', 'N/A')}")

    # Print versions
    if versions:
        print(f"\nVERSIONS ({len(versions)}):")
        for ver in versions:
            ver_num = ver.get('Version', 'N/A')
            ver_rev = ver.get('Revision', 'N/A')
            ver_state = ver.get('State', {}).get('Display', 'N/A')
            print(f"  └─ {ver_num}.{ver_rev} - {ver_state}")


def main():
    """Command-line interface for querying document attachments"""
    import argparse

    parser = argparse.ArgumentParser(description='Query Windchill Document and Attachments')
    parser.add_argument('--url', default='https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/')
    parser.add_argument('--username', default='pat')
    parser.add_argument('--password', default='ptc')
    parser.add_argument('document_number', help='Document number to query')
    parser.add_argument('--include-primary', action='store_true', help='Include primary content')
    parser.add_argument('--include-thumbnails', action='store_true', help='Include thumbnails')
    parser.add_argument('--include-versions', action='store_true', help='Include all versions')
    parser.add_argument('--output', help='Output file path (JSON)')

    args = parser.parse_args()

    result = query_document_attachments(
        base_url=args.url,
        username=args.username,
        password=args.password,
        document_number=args.document_number,
        include_primary_content=args.include_primary,
        include_thumbnails=args.include_thumbnails,
        include_versions=args.include_versions,
        output_file=args.output
    )

    print_document_summary(result)


if __name__ == '__main__':
    main()