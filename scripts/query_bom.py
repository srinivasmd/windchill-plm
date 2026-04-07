#!/usr/bin/env python3
"""Query Windchill Bill of Materials (BOM) for a part"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from windchill_client import WindchillClient


def query_bom(
    base_url: str,
    username: str,
    password: str,
    part_number: str,
    expand_children: bool = True,
    expand_parents: bool = True,
    output_file: str = None
):
    """
    Query BOM for a part including children and parents.

    Args:
        base_url: Windchill OData base URL
        username: Windchill username
        password: Windchill password
        part_number: Part number to query
        expand_children: Whether to fetch child part details
        expand_parents: Whether to fetch parent part details
        output_file: Optional file path to save results

    Returns:
        dict: BOM results with part, children, and parents
    """
    client = WindchillClient(base_url=base_url, username=username, password=password)

    # Get the part
    part = client.get_part_by_number(part_number)
    if not part:
        raise ValueError(f"Part {part_number} not found")

    part_id = part.get('ID')

    result = {
        'part': part,
        'children': [],
        'parents': []
    }

    # Get Children (Uses)
    if expand_children:
        children = client.get_part_children(part_id)
        result['children'] = children

    # Get Parents (UsedBy)
    if expand_parents:
        parents = client.get_part_parents(part_id)
        result['parents'] = parents

    # Save to file if specified
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Results saved to: {output_file}")

    return result


def print_bom_summary(result: dict):
    """Print a summary of BOM results"""
    part = result.get('part', {})
    children = result.get('children', [])
    parents = result.get('parents', [])

    print(f"\n{'='*60}")
    print(f"PART: {part.get('Number', 'N/A')} - {part.get('Name', 'N/A')}")
    print(f"ID: {part.get('ID', 'N/A')}")
    print(f"State: {part.get('State', {}).get('Display', 'N/A')}")
    print(f"{'='*60}")

    # Print children
    if children:
        print(f"\nCHILDREN ({len(children)}):")
        for child in children:
            usage = child.get('usage', {})
            child_part = child.get('child_part', {})

            qty = usage.get('Quantity', 0)
            unit = usage.get('Unit', '')
            child_num = child_part.get('Number', 'N/A')
            child_name = child_part.get('Name', 'N/A')
            child_state = child_part.get('State', {}).get('Display', 'N/A')

            print(f"  ├─ {child_num}: {child_name}")
            print(f"  │   Qty: {qty} {unit} | State: {child_state}")

    # Print parents
    if parents:
        print(f"\nPARENTS ({len(parents)}):")
        for parent in parents:
            parent_num = parent.get('Number', 'N/A')
            parent_name = parent.get('Name', 'N/A')
            parent_state = parent.get('State', {}).get('Display', 'N/A')

            print(f"  ├─ {parent_num}: {parent_name}")
            print(f"  │   State: {parent_state}")


def main():
    """Command-line interface for querying BOM"""
    import argparse

    parser = argparse.ArgumentParser(description='Query Windchill BOM')
    parser.add_argument('--url', default='https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/')
    parser.add_argument('--username', default='pat')
    parser.add_argument('--password', default='ptc')
    parser.add_argument('part_number', help='Part number to query')
    parser.add_argument('--no-children', action='store_true', help='Do not fetch children')
    parser.add_argument('--no-parents', action='store_true', help='Do not fetch parents')
    parser.add_argument('--output', help='Output file path (JSON)')

    args = parser.parse_args()

    result = query_bom(
        base_url=args.url,
        username=args.username,
        password=args.password,
        part_number=args.part_number,
        expand_children=not args.no_children,
        expand_parents=not args.no_parents,
        output_file=args.output
    )

    print_bom_summary(result)


if __name__ == '__main__':
    main()