#!/usr/bin/env python3
"""Generic QUERY script for Windchill entities.

This script provides a unified interface to query any entity type
from Windchill PLM with formatted output for Telegram gateway.

Usage:
    python generic_query.py --entity Document --top 10
    python generic_query.py --entity ChangeNotice --filter "State eq 'OPEN'"
    python generic_query.py --entity QualityAction --number "QA-001"
    python generic_query.py --entity User --name "john"

Supported entities:
    All Windchill entities across all domains.
"""

import sys
import json
import argparse
from pathlib import Path
import requests

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from windchill_client import WindchillClient
from output_formatter import OutputFormatter


# Entity to domain mapping
ENTITY_DOMAIN_MAP = {
    # DocMgmt
    'Document': 'DocMgmt',
    'ControlledDocument': 'DocMgmt',
    'Quality': 'DocMgmt',
    'General': 'DocMgmt',
    'Record': 'DocMgmt',
    'TestDocument': 'DocMgmt',
    'ReferenceDocument': 'DocMgmt',
    'SoftwareDocument': 'DocMgmt',
    'WorkRecord': 'DocMgmt',
    'ApprovedRecord': 'DocMgmt',
    'Specification': 'DocMgmt',
    # ProdMgmt
    'Part': 'ProdMgmt',
    'PartUse': 'ProdMgmt',
    # DataAdmin
    'Folder': 'DataAdmin',
    'Container': 'DataAdmin',
    'ProductContainer': 'DataAdmin',
    'LibraryContainer': 'DataAdmin',
    'ProjectContainer': 'DataAdmin',
    # ChangeMgmt
    'ChangeNotice': 'ChangeMgmt',
    'ChangeRequest': 'ChangeMgmt',
    'ChangeTask': 'ChangeMgmt',
    'ChangeOrder': 'ChangeMgmt',
    # QMS
    'QualityAction': 'QMS',
    'QualityObject': 'QMS',
    'NonConformance': 'QMS',
    'CAPA': 'QMS',
    'Place': 'QMS',
    'QualityContact': 'QMS',
    'Subject': 'QMS',
    # CEM
    'CustomerExperience': 'CEM',
    'RelatedProduct': 'CEM',
    # PrincipalMgmt
    'User': 'PrincipalMgmt',
    'Group': 'PrincipalMgmt',
    'Organization': 'PrincipalMgmt',
    # CADDocumentMgmt
    'CADDocument': 'CADDocumentMgmt',
    'EPMDocument': 'CADDocumentMgmt',
    # MfgProcMgmt
    'ProcessPlan': 'MfgProcMgmt',
    'Operation': 'MfgProcMgmt',
    # ServiceInfoMgmt
    'SIMDocument': 'ServiceInfoMgmt',
    'InformationStructure': 'ServiceInfoMgmt',
}

# Properties to display for each entity type
ENTITY_DISPLAY_PROPS = {
    'Document': ['Number', 'Name', 'State', 'CreatedBy', 'CreatedOn'],
    'Part': ['Number', 'Name', 'State', 'CreatedBy', 'CreatedOn'],
    'ChangeNotice': ['Number', 'Name', 'State', 'NeedDate', 'CreatedBy'],
    'ChangeRequest': ['Number', 'Name', 'State', 'Urgency', 'CreatedBy'],
    'ChangeTask': ['Number', 'Name', 'State', 'DueDate', 'Assignee'],
    'QualityAction': ['Number', 'Name', 'State', 'ActionType', 'Priority'],
    'NonConformance': ['Number', 'Name', 'State', 'NCType', 'Severity'],
    'CAPA': ['Number', 'Name', 'State', 'CAPAType', 'Priority'],
    'QualityObject': ['Number', 'Name', 'State', 'QualityType', 'Severity'],
    'Place': ['Name', 'Address', 'City', 'Country', 'PlaceType'],
    'QualityContact': ['Name', 'ContactType', 'Email', 'Phone', 'Role'],
    'Subject': ['Number', 'Name', 'SubjectType', 'ProductNumber', 'SerialNumber'],
    'CustomerExperience': ['Number', 'Name', 'State', 'PrimaryCode', 'Date'],
    'User': ['Name', 'FullName', 'Email', 'Organization', 'Disabled'],
    'Group': ['Name', 'Description', 'GroupType'],
    'Organization': ['Name', 'Description'],
    'Folder': ['Name', 'Description', 'CreatedBy'],
    'Container': ['Name', 'Description', 'OrganizationName'],
}


def query_entities(entity_type, filter_clause=None, expand=None, select=None, 
                   top=50, skip=0, output_file=None, raw_output=False, detail=False):
    """
    Query entities from Windchill PLM with formatted output.
    
    Args:
        entity_type: Type of entity to query
        filter_clause: OData $filter clause
        expand: Navigation properties to expand
        select: Properties to select
        top: Maximum number of results
        skip: Number of results to skip
        output_file: Optional file to save JSON response
        raw_output: If True, output raw JSON
        detail: If True, show detailed view for each entity
        
    Returns:
        list: Query results or None on failure
    """
    formatter = OutputFormatter()
    client = WindchillClient()
    
    # Get domain for entity type
    domain = ENTITY_DOMAIN_MAP.get(entity_type)
    if not domain:
        formatter.print_error(f"Unknown entity type: {entity_type}")
        formatter.print_info("Supported entity types:")
        for domain_name in sorted(set(ENTITY_DOMAIN_MAP.values())):
            entities = [e for e, d in ENTITY_DOMAIN_MAP.items() if d == domain_name]
            formatter.print_list(entities, domain_name, bullet='📁')
        return None
    
    # Build URL
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/{domain}/{entity_type}s"
    
    # Build query parameters
    params = {}
    if filter_clause:
        params['$filter'] = filter_clause
    if expand:
        params['$expand'] = expand
    if select:
        params['$select'] = select
    if top:
        params['$top'] = top
    if skip:
        params['$skip'] = skip
    
    try:
        response = client.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        entities = data.get('value', [])
        
        if raw_output:
            formatter.print_json(data)
        elif detail and entities:
            # Show detailed view for each entity
            formatter.print_entity_header(entity_type, len(entities))
            for i, entity in enumerate(entities[:10], 1):
                props = ENTITY_DISPLAY_PROPS.get(entity_type, ['Number', 'Name'])
                formatter.print_entity_detail(entity, entity_type, props)
                if i < len(entities[:10]):
                    formatter.divider()
        else:
            # Show table view
            if entities:
                display_props = ENTITY_DISPLAY_PROPS.get(entity_type, ['Number', 'Name', 'State'])
                formatter.print_entity_table(entities, entity_type, display_props)
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
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                formatter.print_json(error_data, "Error Details")
            except:
                pass
        formatter.flush()
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Query entities from Windchill PLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --entity Document --top 10
  %(prog)s --entity ChangeNotice --filter "State/Display eq 'OPEN'"
  %(prog)s --entity QualityAction --number "QA-001"
  %(prog)s --entity User --name "john"
  %(prog)s --entity Part --filter "contains(Name, 'Test')" --top 20
  %(prog)s --entity Part --number "PART-001" --detail
"""
    )
    
    parser.add_argument('--entity', '-e', required=True, help='Entity type to query')
    parser.add_argument('--filter', '-f', help='OData $filter clause')
    parser.add_argument('--number', '-n', help='Filter by entity number')
    parser.add_argument('--name', '-m', help='Filter by entity name (contains)')
    parser.add_argument('--expand', '-x', help='Navigation properties to expand')
    parser.add_argument('--select', '-s', help='Properties to select')
    parser.add_argument('--top', '-t', type=int, default=50, help='Maximum results (default: 50)')
    parser.add_argument('--skip', '-k', type=int, default=0, help='Skip N results')
    parser.add_argument('--output', '-o', help='Output file for JSON response')
    parser.add_argument('--raw', '-r', action='store_true', help='Output raw JSON response')
    parser.add_argument('--detail', '-d', action='store_true', help='Show detailed view for each entity')
    
    args = parser.parse_args()
    
    # Build filter clause
    filter_parts = []
    
    if args.filter:
        filter_parts.append(f"({args.filter})")
    
    if args.number:
        filter_parts.append(f"Number eq '{args.number}'")
    
    if args.name:
        filter_parts.append(f"contains(Name, '{args.name}')")
    
    filter_clause = ' and '.join(filter_parts) if filter_parts else None
    
    # Query entities
    result = query_entities(
        entity_type=args.entity,
        filter_clause=filter_clause,
        expand=args.expand,
        select=args.select,
        top=args.top,
        skip=args.skip,
        output_file=args.output,
        raw_output=args.raw,
        detail=args.detail
    )
    
    return 0 if result is not None else 1


if __name__ == '__main__':
    sys.exit(main())
