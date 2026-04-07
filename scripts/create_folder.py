#!/usr/bin/env python3
"""
Create a new Folder in Windchill PLM DataAdmin domain.

Usage:
    python create_folder.py --name "Design Documents" --description "Product design documentation"
    python create_folder.py --name "Test Folder" --parent "OR:com.ptc.windchill.suma.folder.Folder:12345"
    python create_folder.py --name "New Folder" --output folder.json
"""

import json
import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from windchill_client import WindchillClient


def create_folder(client, name, description=None, parent_folder_id=None, output_file=None, raw=False):
    """
    Create a new folder in Windchill.
    
    Args:
        client: WindchillClient instance
        name: Folder name
        description: Optional description
        parent_folder_id: Optional parent folder ID
        output_file: Optional output file for JSON response
        raw: If True, output raw JSON
    
    Returns:
        Created folder data or None on failure
    """
    # Use the client's create_folder method
    print(f"Creating folder '{name}'...")
    
    result = client.create_folder(name, description, parent_folder_id)
    
    if result:
        if raw:
            print(json.dumps(result, indent=2))
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\nResults saved to: {output_file}")
        
        return result
    
    return None


def main():
    parser = argparse.ArgumentParser(
        description='Create a new Folder in Windchill PLM',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --name "Design Documents" --description "Product design documentation"
  %(prog)s --name "Test Folder" --parent "OR:com.ptc.windchill.suma.folder.Folder:12345"
  %(prog)s --name "New Folder" --output folder.json
'''
    )
    
    parser.add_argument('--name', '-n', required=True, help='Folder name')
    parser.add_argument('--description', '-d', help='Folder description')
    parser.add_argument('--parent', '-p', help='Parent folder ID')
    parser.add_argument('--output', '-o', help='Output file for JSON response')
    parser.add_argument('--raw', '-r', action='store_true', help='Output raw JSON response')
    
    args = parser.parse_args()
    
    # Initialize client
    client = WindchillClient()
    
    # Create folder
    create_folder(
        client=client,
        name=args.name,
        description=args.description,
        parent_folder_id=args.parent,
        output_file=args.output,
        raw=args.raw
    )


if __name__ == "__main__":
    main()
