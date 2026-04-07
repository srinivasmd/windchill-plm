#!/usr/bin/env python3
"""Query Windchill Parts with filtering options"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from windchill_client import WindchillClient


def query_parts(
    base_url: str,
    username: str,
    password: str,
    number: str = None,
    name: str = None,
    state: str = None,
    folder: str = None,
    top: int = None,
    select: str = None,
    expand: str = None,
    output_file: str = None
):
    """
    Query Windchill Parts with various filters.

    Args:
        base_url: Windchill OData base URL
        username: Windchill username
        password: Windchill password
        number: Filter by part number
        name: Filter by part name
        state: Filter by state
        folder: Filter by folder path
        top: Maximum number of results
        select: Comma-separated list of fields to select
        expand: Comma-separated list of navigation properties to expand
        output_file: Optional file path to save results

    Returns:
        dict: Query results
    """
    client = WindchillClient(base_url, username, password)

    # Build filter query
    filters = []
    if number:
        filters.append(f"Number eq '{number}'")
    if name:
        filters.append(f"contains(Name, '{name}')")
    if state:
        filters.append(f"State/Value eq '{state.upper()}'")
    if folder:
        filters.append(f"FolderLocation eq '{folder}'")

    query_params = {}
    if filters:
        query_params['$filter'] = ' and '.join(filters)
    if top:
        query_params['$top'] = top
    if select:
        query_params['$select'] = select
    if expand:
        query_params['$expand'] = expand

    # Query parts
    result = client.query('ProdMgmt/Parts', params=query_params)

    # Save to file if specified
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Results saved to: {output_file}")

    return result


def main():
    """Command-line interface for querying parts"""
    import argparse

    parser = argparse.ArgumentParser(description='Query Windchill Parts')
    parser.add_argument('--url', default='https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/')
    parser.add_argument('--username', default='pat')
    parser.add_argument('--password', default='ptc')
    parser.add_argument('--number', help='Filter by part number')
    parser.add_argument('--name', help='Filter by part name (contains)')
    parser.add_argument('--state', help='Filter by state (e.g., RELEASED, INWORK)')
    parser.add_argument('--folder', help='Filter by folder path')
    parser.add_argument('--top', type=int, help='Maximum number of results')
    parser.add_argument('--select', help='Comma-separated fields to select')
    parser.add_argument('--expand', help='Comma-separated navigation properties to expand')
    parser.add_argument('--output', help='Output file path (JSON)')

    args = parser.parse_args()

    result = query_parts(
        base_url=args.url,
        username=args.username,
        password=args.password,
        number=args.number,
        name=args.name,
        state=args.state,
        folder=args.folder,
        top=args.top,
        select=args.select,
        expand=args.expand,
        output_file=args.output
    )

    # Print summary
    parts = result.get('value', [])
    print(f"\nFound {len(parts)} part(s)")

    for part in parts:
        print(f"  - {part.get('Number', 'N/A')}: {part.get('Name', 'N/A')} [{part.get('State', {}).get('Display', 'N/A')}]")


if __name__ == '__main__':
    main()