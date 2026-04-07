#!/usr/bin/env python3
"""
Script to fetch all available OData domains from Windchill server.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from windchill_client import WindchillClient

def main():
    # Load configuration
    config_path = Path(__file__).parent.parent / "config.json"
    with open(config_path) as f:
        config = json.load(f)
    
    # Get OData base URL from config
    odata_base_url = config.get("odata_base_url", config["server_url"] + "/servlet/odata/")
    
    print(f"Fetching OData domains from: {odata_base_url}\n")
    
    # Create client (pass config path, not config dict)
    client = WindchillClient(str(config_path))
    
    # Fetch the service document
    response = client.session.get(odata_base_url, verify=config.get("verify_ssl", True))
    
    if response.status_code == 200:
        service_doc = response.json()
        
        print("Available OData Domains:\n")
        print("=" * 80)
        
        # Handle both list and dict formats
        entity_sets = []
        if isinstance(service_doc, list):
            entity_sets = service_doc
        elif "value" in service_doc:
            entity_sets = service_doc["value"]
        
        for entity_set in sorted(entity_sets, key=lambda x: x.get("name", "")):
            name = entity_set.get("name", "N/A")
            url = entity_set.get("url", "N/A")
            title = entity_set.get("title", "")
            
            print(f"[{name}]")
            print(f"   Title: {title}")
            print(f"   URL: {url}")
            print()
        
        print("=" * 80)
        print(f"Total domains: {len(entity_sets)}")
        
    else:
        print(f"Failed to fetch domains")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    main()