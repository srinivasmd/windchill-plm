#!/usr/bin/env python3
"""Query Suppliers from Windchill PLM with formatted output.

Usage:
    python query_suppliers.py --top 10
    python query_suppliers.py --name "ABC"
    python query_suppliers.py --number SUP-001
"""

import sys
import json
import argparse
from pathlib import Path
import requests

sys.path.insert(0, str(Path(__file__).parent))

from windchill_client import WindchillClient
from output_formatter import OutputFormatter


# SupplierMgmt endpoint
SUPPLIER_BASE_URL_SUFFIX = "/SupplierMgmt/Suppliers"


def query_suppliers(number=None, name=None, top=50, output_file=None, raw=False, detail=False):
    """Query suppliers from Windchill with formatted output."""
    formatter = OutputFormatter()
    client = WindchillClient()
    
    # Build URL
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}{SUPPLIER_BASE_URL_SUFFIX}"
    
    params = {'$top': top}
    
    # Build filter
    filter_parts = []
    if number:
        filter_parts.append(f"Number eq '{number}'")
    if name:
        filter_parts.append(f"contains(Name, '{name}')")
    
    if filter_parts:
        params['$filter'] = ' and '.join(filter_parts)
    
    try:
        response = client.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        suppliers = data.get('value', [])
        
        if raw:
            formatter.print_json(data)
        elif detail and suppliers:
            formatter.print_entity_header("Supplier", len(suppliers))
            for supplier in suppliers[:10]:
                formatter.print_entity_detail(supplier, "Supplier", ['Number', 'Name', 'Description', 'Status'])
                formatter.divider()
        else:
            if suppliers:
                formatter.print_entity_table(suppliers, "Supplier", ['Number', 'Name', 'Status'])
            else:
                formatter.print_warning("No suppliers found matching criteria")
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            formatter.print_success(f"Saved to: {output_file}")
        
        formatter.flush()
        return suppliers
        
    except requests.RequestException as e:
        formatter.print_error("Failed to query suppliers", str(e))
        formatter.flush()
        return None


def main():
    parser = argparse.ArgumentParser(description="Query suppliers from Windchill PLM")
    parser.add_argument('--number', '-n', help='Supplier number')
    parser.add_argument('--name', '-m', help='Supplier name (contains)')
    parser.add_argument('--top', '-t', type=int, default=50, help='Max results')
    parser.add_argument('--output', '-o', help='Output file for JSON')
    parser.add_argument('--raw', '-r', action='store_true', help='Raw JSON output')
    parser.add_argument('--detail', '-d', action='store_true', help='Detailed view')
    
    args = parser.parse_args()
    
    result = query_suppliers(
        number=args.number,
        name=args.name,
        top=args.top,
        output_file=args.output,
        raw=args.raw,
        detail=args.detail
    )
    
    return 0 if result is not None else 1


if __name__ == '__main__':
    sys.exit(main())
