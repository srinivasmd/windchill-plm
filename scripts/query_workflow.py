#!/usr/bin/env python3
"""Query Workflow items from Windchill PLM with formatted output.

Usage:
    python query_workflow.py --top 10
    python query_workflow.py --state RUNNING
    python query_workflow.py --assignee "john"
"""

import sys
import json
import argparse
from pathlib import Path
import requests

sys.path.insert(0, str(Path(__file__).parent))

from windchill_client import WindchillClient
from output_formatter import OutputFormatter


def query_workflow(state=None, assignee=None, top=50, output_file=None, raw=False, detail=False):
    """Query workflow items with formatted output."""
    formatter = OutputFormatter()
    client = WindchillClient()
    
    # Build URL
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/Workflow/WorkItems"
    
    params = {'$top': top}
    
    # Build filter
    filter_parts = []
    if state:
        filter_parts.append(f"State/Display eq '{state}'")
    if assignee:
        filter_parts.append(f"contains(Assignee/FullName, '{assignee}')")
    
    if filter_parts:
        params['$filter'] = ' and '.join(filter_parts)
    
    try:
        response = client.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        items = data.get('value', [])
        
        if raw:
            formatter.print_json(data)
        elif detail and items:
            formatter.print_entity_header("WorkItem", len(items))
            for item in items[:10]:
                formatter.print_entity_detail(item, "WorkItem", ['ID', 'Name', 'State', 'Assignee', 'DueDate'])
                formatter.divider()
        else:
            if items:
                formatter.print_entity_table(items, "WorkItem", ['Name', 'State', 'Assignee'])
            else:
                formatter.print_warning("No workflow items found matching criteria")
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            formatter.print_success(f"Saved to: {output_file}")
        
        formatter.flush()
        return items
        
    except requests.RequestException as e:
        formatter.print_error("Failed to query workflow items", str(e))
        formatter.flush()
        return None


def main():
    parser = argparse.ArgumentParser(description="Query workflow items from Windchill PLM")
    parser.add_argument('--state', '-s', help='State filter (e.g., RUNNING, COMPLETED)')
    parser.add_argument('--assignee', '-a', help='Assignee name (contains)')
    parser.add_argument('--top', '-t', type=int, default=50, help='Max results')
    parser.add_argument('--output', '-o', help='Output file for JSON')
    parser.add_argument('--raw', '-r', action='store_true', help='Raw JSON output')
    parser.add_argument('--detail', '-d', action='store_true', help='Detailed view')
    
    args = parser.parse_args()
    
    result = query_workflow(
        state=args.state,
        assignee=args.assignee,
        top=args.top,
        output_file=args.output,
        raw=args.raw,
        detail=args.detail
    )
    
    return 0 if result is not None else 1


if __name__ == '__main__':
    sys.exit(main())
