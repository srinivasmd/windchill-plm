#!/usr/bin/env python3
"""Query Parts from Windchill PLM with formatted output.

Usage:
    python query_parts.py --number TOPLVL
    python query_parts.py --state RELEASED --top 10
    python query_parts.py --name "Bolt" --output parts.json
"""

import sys
import json
import argparse
from pathlib import Path
import requests

sys.path.insert(0, str(Path(__file__).parent))

from windchill_client import WindchillClient
from output_formatter import OutputFormatter


def query_parts(number=None, name=None, state=None, top=50, output_file=None, raw=False, detail=False):
    """Query parts from Windchill with formatted output."""
    formatter = OutputFormatter()
    client = WindchillClient()
    
    # Build URL and params
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/ProdMgmt/Parts"
    
    params = {'$top': top}
    
    # Build filter
    filter_parts = []
    if number:
        filter_parts.append(f"Number eq '{number}'")
    if name:
        filter_parts.append(f"contains(Name, '{name}')")
    if state:
        filter_parts.append(f"State/Display eq '{state}'")
    
    if filter_parts:
        params['$filter'] = ' and '.join(filter_parts)
    
    try:
        response = client.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        parts = data.get('value', [])
        
        if raw:
            formatter.print_json(data)
        elif detail and parts:
            formatter.print_entity_header("Part", len(parts))
            for part in parts[:10]:
                formatter.print_entity_detail(part, "Part")
                formatter.divider()
        else:
            if parts:
                formatter.print_entity_table(parts, "Part", ['Number', 'Name', 'State', 'CreatedBy'])
            else:
                formatter.print_warning("No parts found matching criteria")
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            formatter.print_success(f"Saved to: {output_file}")
        
        formatter.flush()
        return parts
        
    except requests.RequestException as e:
        formatter.print_error("Failed to query parts", str(e))
        formatter.flush()
        return None


def main():
    parser = argparse.ArgumentParser(description="Query parts from Windchill PLM")
    parser.add_argument('--number', '-n', help='Part number')
    parser.add_argument('--name', '-m', help='Part name (contains)')
    parser.add_argument('--state', '-s', help='State filter (e.g., RELEASED, INWORK)')
    parser.add_argument('--top', '-t', type=int, default=50, help='Max results')
    parser.add_argument('--output', '-o', help='Output file for JSON')
    parser.add_argument('--raw', '-r', action='store_true', help='Raw JSON output')
    parser.add_argument('--detail', '-d', action='store_true', help='Detailed view')
    
    args = parser.parse_args()
    
    result = query_parts(
        number=args.number,
        name=args.name,
        state=args.state,
        top=args.top,
        output_file=args.output,
        raw=args.raw,
        detail=args.detail
    )
    
    return 0 if result is not None else 1


if __name__ == '__main__':
    sys.exit(main())
