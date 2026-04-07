#!/usr/bin/env python3
"""Generic DELETE script for Windchill entities.

This script provides a unified interface to delete any entity type
that supports DELETE operations in Windchill PLM.

Usage:
    python generic_delete.py --entity Document --id "OR:..."
    python generic_delete.py --entity Part --number "PART-001"
    python generic_delete.py --entity Folder --id "OR:..." --force

Supported entities for DELETE (most entities support this):
    Document, Part, Folder, Container, ChangeNotice, ChangeRequest,
    QualityAction, NonConformance, CAPA, CustomerExperience, etc.
"""

import sys
import json
import argparse
from pathlib import Path
import requests

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from windchill_client import WindchillClient


# Entity to domain mapping
ENTITY_DOMAIN_MAP = {
    'Document': 'DocMgmt',
    'Part': 'ProdMgmt',
    'Folder': 'DataAdmin',
    'Container': 'DataAdmin',
    'ChangeNotice': 'ChangeMgmt',
    'ChangeRequest': 'ChangeMgmt',
    'ChangeTask': 'ChangeMgmt',
    'QualityAction': 'QMS',
    'QualityObject': 'QMS',
    'NonConformance': 'QMS',
    'CAPA': 'QMS',
    'Place': 'QMS',
    'QualityContact': 'QMS',
    'Subject': 'QMS',
    'CustomerExperience': 'CEM',
    'RelatedProduct': 'CEM',
    'User': 'PrincipalMgmt',
    'Group': 'PrincipalMgmt',
    'Organization': 'PrincipalMgmt',
}


def get_entity_id_by_number(entity_type, number):
    """Look up entity ID by number."""
    client = WindchillClient()
    
    domain = ENTITY_DOMAIN_MAP.get(entity_type)
    if not domain:
        return None
    
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/{domain}/{entity_type}s"
    
    params = {"$filter": f"Number eq '{number}'", "$select": "ID,Name,Number"}
    
    try:
        response = client.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("value"):
            entity = data["value"][0]
            return entity.get("ID"), entity.get("Name"), entity.get("Number")
    except:
        pass
    
    return None, None, None


def delete_entity(entity_type, entity_id=None, entity_number=None, force=False, dry_run=False):
    """
    Delete an entity from Windchill PLM.
    
    Args:
        entity_type: Type of entity to delete
        entity_id: Entity ID to delete (preferred)
        entity_number: Entity number to delete (will lookup ID)
        force: Skip confirmation prompt
        dry_run: Only show what would be deleted
        
    Returns:
        bool: True on success, False on failure
    """
    client = WindchillClient()
    
    # Get domain for entity type
    domain = ENTITY_DOMAIN_MAP.get(entity_type)
    if not domain:
        print(f"[ERROR] Unknown entity type: {entity_type}")
        print(f"Supported types: {', '.join(ENTITY_DOMAIN_MAP.keys())}")
        return False
    
    # Resolve entity ID
    entity_name = None
    entity_num = None
    
    if not entity_id and entity_number:
        entity_id, entity_name, entity_num = get_entity_id_by_number(entity_type, entity_number)
        if not entity_id:
            print(f"[ERROR] Could not find {entity_type} with number: {entity_number}")
            return False
    
    if not entity_id:
        print("[ERROR] Either --id or --number must be provided")
        return False
    
    # Build URL
    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/{domain}/{entity_type}s('{entity_id}')"
    
    # Get entity details for confirmation
    if not entity_name:
        try:
            response = client.session.get(url)
            response.raise_for_status()
            data = response.json()
            entity_name = data.get('Name', 'Unknown')
            entity_num = data.get('Number', 'N/A')
        except:
            entity_name = 'Unknown'
            entity_num = 'N/A'
    
    # Confirmation prompt
    if not force:
        print(f"\n[WARNING] About to delete {entity_type}:")
        print(f"  ID: {entity_id}")
        print(f"  Name: {entity_name}")
        print(f"  Number: {entity_num}")
        
        if dry_run:
            print("\n[DRY RUN] Would delete this entity (use --force to actually delete)")
            return True
        
        confirm = input("\nConfirm delete? (yes/no): ")
        if confirm.lower() != 'yes':
            print("[CANCELLED] Delete cancelled")
            return False
    else:
        print(f"\n[INFO] Deleting {entity_type}:")
        print(f"  ID: {entity_id}")
        print(f"  Name: {entity_name}")
        print(f"  Number: {entity_num}")
    
    if dry_run:
        print("\n[DRY RUN] Would delete this entity")
        return True
    
    # Get CSRF token for write operation
    csrf_token = client.get_csrf_token()
    headers = {
        'Accept': 'application/json'
    }
    if csrf_token:
        headers['CSRF_NONCE'] = csrf_token
    
    try:
        response = client.session.delete(url, headers=headers)
        
        # Check for various success status codes
        if response.status_code in [200, 202, 204]:
            print(f"\n[OK] {entity_type} deleted successfully!")
            return True
        else:
            response.raise_for_status()
            return True
        
    except requests.RequestException as e:
        print(f"\n[ERROR] Failed to delete {entity_type}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status: {e.response.status_code}")
            try:
                error_data = e.response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Response: {e.response.text}")
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
    result = delete_entity(
        entity_type=args.entity,
        entity_id=args.id,
        entity_number=args.number,
        force=args.force,
        dry_run=args.dry_run
    )
    
    return 0 if result else 1


if __name__ == '__main__':
    sys.exit(main())
