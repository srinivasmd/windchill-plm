#!/usr/bin/env python3
"""Generic DELETE script for Windchill entities.

This script provides a unified interface to delete any entity type
from Windchill PLM with formatted output for Telegram gateway.

Usage:
    python generic_delete.py --entity Document --id "OR:..."
    python generic_delete.py --entity Part --number "PART-001" --force
    python generic_delete.py --entity Folder --id "OR:..." --dry-run

Supported entities:
    All Windchill entities that support DELETE operation.
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
    'Document': 'DocMgmt',
    'ControlledDocument': 'DocMgmt',
    'Quality': 'DocMgmt',
    'Part': 'ProdMgmt',
    'Folder': 'DataAdmin',
    'ChangeNotice': 'ChangeMgmt',
    'ChangeRequest': 'ChangeMgmt',
    'ChangeTask': 'ChangeMgmt',
    'QualityAction': 'QMS',
    'NonConformance': 'QMS',
    'CAPA': 'QMS',
    'CustomerExperience': 'CEM',
}


def get_entity_info(entity_type, number):
    """Get entity info by number."""
    client = WindchillClient()
    domain = ENTITY_DOMAIN_MAP.get(entity_type)
    if not domain:
        return None
    
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/{domain}/{entity_type}s"
    params = {'$filter': f"Number eq '{number}'", '$select': 'ID,Name,Number,State'}
    
    try:
        response = client.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        entities = data.get('value', [])
        if entities:
            return entities[0]
    except:
        pass
    
    return None


def get_entity_by_id(entity_type, entity_id):
    """Get entity info by ID."""
    client = WindchillClient()
    domain = ENTITY_DOMAIN_MAP.get(entity_type)
    if not domain:
        return None
    
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/{domain}/{entity_type}s('{entity_id}')"
    
    try:
        response = client.session.get(url)
        response.raise_for_status()
        return response.json()
    except:
        pass
    
    return None


def delete_entity(entity_type, entity_id=None, number=None, force=False, dry_run=False):
    """
    Delete an entity from Windchill PLM with formatted output.
    
    Args:
        entity_type: Type of entity to delete
        entity_id: Entity ID to delete
        number: Entity number (will lookup ID if not provided)
        force: Skip confirmation prompt
        dry_run: Show what would be deleted without deleting
        
    Returns:
        bool: True on success, False on failure
    """
    formatter = OutputFormatter()
    client = WindchillClient()
    
    # Get domain for entity type
    domain = ENTITY_DOMAIN_MAP.get(entity_type)
    if not domain:
        formatter.print_error(f"Unknown entity type: {entity_type}")
        formatter.print_info("Supported entity types for DELETE:")
        for domain_name in sorted(set(ENTITY_DOMAIN_MAP.values())):
            entities = [e for e, d in ENTITY_DOMAIN_MAP.items() if d == domain_name]
            formatter.print_list(entities, domain_name, bullet='📁')
        return False
    
    # Get entity info
    entity_info = None
    if entity_id:
        entity_info = get_entity_by_id(entity_type, entity_id)
    elif number:
        entity_info = get_entity_info(entity_type, number)
        if entity_info:
            entity_id = entity_info.get('ID')
    
    if not entity_id and not number:
        formatter.print_error("Entity ID or number is required")
        return False
    
    if not entity_id:
        formatter.print_error(f"Entity not found", f"{entity_type} with number '{number}'")
        return False
    
    # Show entity details
    formatter.print_header(f"Entity to Delete", '🗑️')
    if entity_info:
        formatter.print_entity_detail(entity_info, entity_type)
    else:
        formatter.print_info(f"ID: {entity_id}")
    
    # Dry run - show what would be deleted
    if dry_run:
        formatter.print_warning("DRY RUN - No changes will be made")
        formatter.print_info("Run without --dry-run to actually delete")
        formatter.flush()
        return True
    
    # Confirm deletion (unless force)
    if not force:
        formatter.print_warning("This action cannot be undone!")
        formatter.print_info("Use --force to skip confirmation")
        formatter.flush()
        return False
    
    # Build URL
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/{domain}/{entity_type}s('{entity_id}')"
    
    try:
        # Get CSRF token for write operations
        headers = {}
        if hasattr(client, 'csrf_token') and client.csrf_token:
            headers['X-CSRF-Token'] = client.csrf_token
        else:
            # Try to get CSRF token
            try:
                csrf_url = f"{odata_base_url.rstrip('/')}/$csrf"
                csrf_resp = client.session.get(csrf_url)
                if csrf_resp.status_code == 200:
                    csrf_data = csrf_resp.json()
                    client.csrf_token = csrf_data.get('value', {}).get('token')
                    if client.csrf_token:
                        headers['X-CSRF-Token'] = client.csrf_token
            except:
                pass
        
        response = client.session.delete(url, headers=headers)
        response.raise_for_status()
        
        # Show success
        entity_name = entity_info.get('Name', number) if entity_info else number or entity_id
        formatter.print_operation_result("Deleted", entity_type, entity_name, True)
        formatter.flush()
        return True
        
    except requests.RequestException as e:
        formatter.print_error(f"Failed to delete {entity_type}", str(e))
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                formatter.print_json(error_data, "Error Details")
            except:
                formatter.print_info(f"Status: {e.response.status_code}")
        formatter.flush()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Delete an entity from Windchill PLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --entity Document --id "OR:com.ptc.DocMgmt.Document:12345"
  %(prog)s --entity Part --number "PART-001" --force
  %(prog)s --entity Folder --id "OR:..." --dry-run
"""
    )
    
    parser.add_argument('--entity', '-e', required=True, help='Entity type to delete')
    parser.add_argument('--id', '-i', help='Entity ID to delete')
    parser.add_argument('--number', '-n', help='Entity number (will lookup ID)')
    parser.add_argument('--force', '-f', action='store_true', help='Skip confirmation prompt')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be deleted without deleting')
    
    args = parser.parse_args()
    
    # Delete entity
    success = delete_entity(
        entity_type=args.entity,
        entity_id=args.id,
        number=args.number,
        force=args.force,
        dry_run=args.dry_run
    )
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
