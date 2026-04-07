#!/usr/bin/env python3
"""
Delete a Folder from Windchill PLM DataAdmin domain.

Usage:
    python delete_folder.py --id "OR:com.ptc.windchill.suma.folder.Folder:12345"
    python delete_folder.py --id "OR:..." --force
"""

import json
import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from windchill_client import WindchillClient


def delete_folder(client, folder_id, force=False):
    """
    Delete a folder from Windchill.
    
    Args:
        client: WindchillClient instance
        folder_id: Folder ID to delete
        force: If True, skip confirmation
    
    Returns:
        True on success, None on failure
    """
    # First get the folder to show what will be deleted
    print(f"Fetching folder '{folder_id}'...")
    
    # Get folder contents first to warn user
    contents = client.get_folder_contents(folder_id)
    if contents:
        items = contents.get("value", [])
        if items and not force:
            print(f"\nWarning: Folder contains {len(items)} items:")
            for item in items[:5]:
                print(f"  - {item.get('Name', 'N/A')}")
            if len(items) > 5:
                print(f"  ... and {len(items) - 5} more items")
            
            confirm = input("\nDelete folder and all contents? (yes/no): ")
            if confirm.lower() != 'yes':
                print("Aborted.")
                return None
    
    # Use the client's delete_folder method
    print(f"\nDeleting folder '{folder_id}'...")
    
    result = client.delete_folder(folder_id)
    
    if result:
        print("\n" + "=" * 70)
        print("FOLDER DELETED SUCCESSFULLY")
        print("=" * 70)
        print(f"  Folder ID: {folder_id}")
        print("=" * 70)
        return True
    
    return None


def main():
    parser = argparse.ArgumentParser(
        description='Delete a Folder from Windchill PLM',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --id "OR:com.ptc.windchill.suma.folder.Folder:12345"
  %(prog)s --id "OR:..." --force
'''
    )
    
    parser.add_argument('--id', '-i', required=True, help='Folder ID to delete')
    parser.add_argument('--force', '-f', action='store_true', help='Skip confirmation prompt')
    
    args = parser.parse_args()
    
    # Initialize client
    client = WindchillClient()
    
    # Delete folder
    delete_folder(
        client=client,
        folder_id=args.id,
        force=args.force
    )


if __name__ == "__main__":
    main()
