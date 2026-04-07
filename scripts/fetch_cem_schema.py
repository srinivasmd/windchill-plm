#!/usr/bin/env python3
"""
Fetch CEM domain metadata from Windchill OData API
"""

import json
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from windchill_client import WindchillClient

def main():
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/CEM/$metadata"

    print(f"Fetching CEM domain metadata from: {url}")

    try:
        response = client.session.get(url)
        response.raise_for_status()
        metadata_xml = response.text

        # Save to file
        output_path = Path(__file__).parent.parent / "references" / "CEM_METADATA.xml"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(metadata_xml)

        print(f"\n[OK] CEM domain metadata saved to: {output_path}")
        print(f"   Size: {len(metadata_xml)} characters")

        # Also test basic query
        print("\nTesting basic CEM query...")
        test_url = f"{odata_base_url.rstrip('/')}/CEM/EnterpriseItems"
        response = client.session.get(test_url, params={"$top": 1})
        response.raise_for_status()
        data = response.json()
        print(f"[OK] CEM EnterpriseItems query successful. Found {len(data.get('value', []))} items.")

    except Exception as e:
        print(f"\n[ERROR] Failed to fetch CEM metadata: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        sys.exit(1)

if __name__ == "__main__":
    main()