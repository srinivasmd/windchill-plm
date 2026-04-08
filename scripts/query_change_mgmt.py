#!/usr/bin/env python3
"""Query Change Management entities from Windchill PLM with formatted output.

Usage:
    python query_change_mgmt.py --type ChangeNotice --top 10
    python query_change_mgmt.py --type ChangeRequest --state OPEN
    python query_change_mgmt.py --type ChangeTask --number CT-001
"""

import sys
import json
import argparse
from pathlib import Path
import requests

sys.path.insert(0, str(Path(__file__).parent))

from windchill_client import WindchillClient
from output_formatter import OutputFormatter


ENTITY_TYPES = {
    'ChangeNotice': 'ChangeNotices',
    'ChangeRequest': 'ChangeRequests',
    'ChangeTask': 'ChangeTasks',
    'ChangeOrder': 'ChangeOrders'
}

ENTITY_DISPLAY_PROPS = {
    'ChangeNotice': ['Number', 'Name', 'State', 'NeedDate', 'CreatedBy'],
    'ChangeRequest': ['Number', 'Name', 'State', 'Urgency', 'CreatedBy'],
    'ChangeTask': ['Number', 'Name', 'State', 'DueDate', 'Assignee'],
    'ChangeOrder': ['Number', 'Name', 'State', 'CreatedOn']
}


def query_change_mgmt(entity_type, number=None, name=None, state=None, top=50, output_file=None, raw=False, detail=False):
    """Query change management entities with formatted output."""
    formatter = OutputFormatter()
    client = WindchillClient()
    
    if entity_type not in ENTITY_TYPES:
        formatter.print_error(f"Unknown entity type: {entity_type}")
        formatter.print_info("Supported types: ChangeNotice, ChangeRequest, ChangeTask, ChangeOrder")
        return None
    
    # Build URL
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    endpoint = ENTITY_TYPES[entity_type]
    url = f"{odata_base_url.rstrip('/')}/ChangeMgmt/{endpoint}"
    
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
        
        entities = data.get('value', [])
        
        if raw:
            formatter.print_json(data)
        elif detail and entities:
            formatter.print_entity_header(entity_type, len(entities))
            for entity in entities[:10]:
                formatter.print_entity_detail(entity, entity_type, ENTITY_DISPLAY_PROPS.get(entity_type))
                formatter.divider()
        else:
            if entities:
                formatter.print_entity_table(entities, entity_type, ENTITY_DISPLAY_PROPS.get(entity_type, ['Number', 'Name', 'State']))
            else:
                formatter.print_warning(f"No {entity_type}(s) found matching criteria")
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            formatter.print_success(f"Saved to: {output_file}")
        
        formatter.flush()
        return entities
        
    except requests.RequestException as e:
        formatter.print_error(f"Failed to query {entity_type}", str(e))
        formatter.flush()
        return None


def main():
    parser = argparse.ArgumentParser(description="Query change management entities")
    parser.add_argument('--type', '-t', required=True, choices=['ChangeNotice', 'ChangeRequest', 'ChangeTask', 'ChangeOrder'],
                        help='Entity type to query')
    parser.add_argument('--number', '-n', help='Entity number')
    parser.add_argument('--name', '-m', help='Entity name (contains)')
    parser.add_argument('--state', '-s', help='State filter')
    parser.add_argument('--top', type=int, default=50, help='Max results')
    parser.add_argument('--output', '-o', help='Output file for JSON')
    parser.add_argument('--raw', '-r', action='store_true', help='Raw JSON output')
    parser.add_argument('--detail', '-d', action='store_true', help='Detailed view')
    
    args = parser.parse_args()
    
    result = query_change_mgmt(
        entity_type=args.type,
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
