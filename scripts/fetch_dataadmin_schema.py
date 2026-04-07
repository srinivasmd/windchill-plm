#!/usr/bin/env python3
"""
Fetch Data Administration domain schema from Windchill OData service
"""

import json
from pathlib import Path
from windchill_client import WindchillClient


def fetch_dataadmin_metadata():
    """Fetch Data Administration domain metadata"""
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/DataAdmin/$metadata"

    print(f"Fetching metadata from: {url}")

    try:
        response = client.session.get(url)
        response.raise_for_status()

        # Save the XML metadata
        schemas_dir = Path(__file__).parent.parent / "schemas"
        schemas_dir.mkdir(exist_ok=True)
        output_file = schemas_dir / "DataAdmin_metadata.xml"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)

        print(f"\n[OK] Saved metadata to: {output_file}")
        print(f"Total characters: {len(response.text)}")

        return response.text

    except Exception as e:
        print(f"Error: Failed to fetch metadata: {e}")
        return None


if __name__ == "__main__":
    fetch_dataadmin_metadata()