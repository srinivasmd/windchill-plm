#!/usr/bin/env python3
"""Query Bill of Materials (BOM) from Windchill PLM with formatted output.

Usage:
    python query_bom.py PART-001
    python query_bom.py --number PART-001 --output bom.json
"""

import sys
import json
import argparse
from pathlib import Path
import requests

sys.path.insert(0, str(Path(__file__).parent))

from windchill_client import WindchillClient
from output_formatter import OutputFormatter


def query_bom(part_number, output_file=None, raw=False):
    """Query BOM for a part with formatted output."""
    formatter = OutputFormatter()
    client = WindchillClient()
    
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    
    # First get the part ID
    formatter.print_info(f"Looking up part: {part_number}")
    
    parts_url = f"{odata_base_url.rstrip('/')}/ProdMgmt/Parts"
    params = {'$filter': f"Number eq '{part_number}'", '$select': 'ID,Name,Number'}
    
    try:
        response = client.session.get(parts_url, params=params)
        response.raise_for_status()
        parts_data = response.json()
        parts = parts_data.get('value', [])
        
        if not parts:
            formatter.print_error(f"Part not found: {part_number}")
            formatter.flush()
            return None
        
        part = parts[0]
        part_id = part['ID']
        part_name = part.get('Name', part_number)
        
        formatter.print_success(f"Found: {part_name}")
        
    except requests.RequestException as e:
        formatter.print_error("Failed to lookup part", str(e))
        formatter.flush()
        return None
    
    # Now get BOM (Uses relationship)
    bom_url = f"{odata_base_url.rstrip('/')}/ProdMgmt/PartUses"
    params = {'$filter': f"PartID eq '{part_id}'", '$expand': 'Part'}
    
    try:
        response = client.session.get(bom_url, params=params)
        response.raise_for_status()
        bom_data = response.json()
        
        bom_items = bom_data.get('value', [])
        
        if raw:
            formatter.print_json(bom_data)
        else:
            formatter.print_header(f"BOM: {part_number}", '📊')
            formatter.print_info(f"Parent: {part_name}")
            formatter.divider()
            
            if bom_items:
                rows = []
                for item in bom_items:
                    child_part = item.get('Part', {})
                    rows.append([
                        child_part.get('Number', 'N/A'),
                        child_part.get('Name', 'N/A'),
                        str(item.get('Quantity', 1)),
                        child_part.get('State', {}).get('Display', 'N/A') if isinstance(child_part.get('State'), dict) else child_part.get('State', 'N/A')
                    ])
                
                formatter.print_table(['Number', 'Name', 'Qty', 'State'], rows, f"Components ({len(bom_items)} items)")
            else:
                formatter.print_warning("No BOM items found - part may be a leaf component")
        
        if output_file:
            full_data = {
                'parent': part,
                'bom': bom_data
            }
            with open(output_file, 'w') as f:
                json.dump(full_data, f, indent=2)
            formatter.print_success(f"Saved to: {output_file}")
        
        formatter.flush()
        return bom_items
        
    except requests.RequestException as e:
        formatter.print_error("Failed to query BOM", str(e))
        formatter.flush()
        return None


def main():
    parser = argparse.ArgumentParser(description="Query BOM for a part")
    parser.add_argument('part_number', nargs='?', help='Part number')
    parser.add_argument('--number', '-n', help='Part number (alternative)')
    parser.add_argument('--output', '-o', help='Output file for JSON')
    parser.add_argument('--raw', '-r', action='store_true', help='Raw JSON output')
    
    args = parser.parse_args()
    
    part_number = args.part_number or args.number
    if not part_number:
        parser.print_help()
        return 1
    
    result = query_bom(
        part_number=part_number,
        output_file=args.output,
        raw=args.raw
    )
    
    return 0 if result is not None else 1


if __name__ == '__main__':
    sys.exit(main())
