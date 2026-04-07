#!/usr/bin/env python3
"""Explore Windchill OData domains and available endpoints"""

import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from windchill_client import WindchillClient


# Known Windchill OData domains
WINDCHILL_DOMAINS = [
    "ProdMgmt",
    "DocMgmt",
    "CADDocumentMgmt",
    "MfgProcMgmt",
    "ChangeMgmt",
    "SupplierMgmt",
    "DataAdmin",
    "CEM",
    "PrincipalMgmt",
    "QualityMgmt",
    "ProgramMgmt",
    "RequirementMgmt",
    "Windchill",
    "PDM",
    "Common"
]


def explore_domains(client):
    """
    Explore all known Windchill OData domains to find available collections.

    Args:
        client: WindchillClient instance

    Returns:
        dict: Dictionary of domain -> list of available collections
    """
    results = {}

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")

    print(f"\n{'='*80}")
    print(f"Exploring Windchill OData Domains")
    print(f"{'='*80}\n")

    for domain in WINDCHILL_DOMAINS:
        print(f"Checking domain: {domain}...")
        url = f"{odata_base_url.rstrip('/')}/{domain}"

        try:
            response = client.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()

                # Extract entity sets (collections)
                if "EntitySets" in data:
                    collections = data.get("EntitySets", [])
                    results[domain] = collections
                    print(f"  [OK] Found {len(collections)} collections:")
                    for coll in collections[:10]:  # Show first 10
                        print(f"    - {coll}")
                    if len(collections) > 10:
                        print(f"    ... and {len(collections) - 10} more")
                else:
                    print(f"  [WARN] No EntitySets found")
            else:
                print(f"  [FAIL] Status: {response.status_code}")
        except Exception as e:
            print(f"  [ERROR] {str(e)}")

    return results


def get_domain_metadata(domain):
    """
    Get full metadata for a specific domain.

    Args:
        domain: Domain name (e.g., "ProdMgmt")

    Returns:
        dict or str: Metadata data or error message
    """
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/{domain}/$metadata"

    print(f"\nFetching metadata for domain: {domain}")
    print(f"URL: {url}")

    try:
        response = client.session.get(url, timeout=30)
        if response.status_code == 200:
            print(f"  [OK] Metadata retrieved")
            return response.text  # Metadata is XML
        else:
            print(f"  [FAIL] Status: {response.status_code}")
            return None
    except Exception as e:
        print(f"  [ERROR] {str(e)}")
        return None


def query_collection(domain, collection, top=5, select=None):
    """
    Query a specific collection to see sample data.

    Args:
        domain: Domain name (e.g., "ProdMgmt")
        collection: Collection name (e.g., "Parts")
        top: Number of records to retrieve
        select: Properties to select (comma-separated)

    Returns:
        list: Query results or empty list
    """
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/{domain}/{collection}"

    params = {"$top": top}
    if select:
        params["$select"] = select

    print(f"\nQuerying: {domain}/{collection}")
    print(f"URL: {url}")

    try:
        response = client.session.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            results = data.get("value", [])
            print(f"  [OK] Found {len(results)} records")
            return results
        else:
            print(f"  [FAIL] Status: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
            return []
    except Exception as e:
        print(f"  [ERROR] {str(e)}")
        return []


def check_csrf_token():
    """
    Check if CSRF token endpoint is available.

    Returns:
        str: CSRF token or None
    """
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")

    # Try different CSRF token endpoint paths
    csrf_paths = [
        "PTC/GetCSRFToken",
        "Common/GetCSRFToken",
        "GetCSRFToken",
        "v5/PTC/GetCSRFToken"
    ]

    print(f"\n{'='*80}")
    print(f"Checking CSRF Token Endpoints")
    print(f"{'='*80}\n")

    for path in csrf_paths:
        url = f"{odata_base_url.rstrip('/')}/{path}"
        print(f"Trying: {path}")

        try:
            response = client.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                token = data.get("NonceValue") or data.get("CSRF_NONCE") or data.get("Token")
                if token:
                    print(f"  [OK] Found token: {token}")
                    return token
                else:
                    print(f"  [WARN] No token in response")
            else:
                print(f"  [FAIL] Status: {response.status_code}")
        except Exception as e:
            print(f"  [ERROR] {str(e)}")

    return None


def check_authentication():
    """
    Check if authentication is working by querying a simple endpoint.

    Returns:
        bool: True if authentication works
    """
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")

    print(f"\n{'='*80}")
    print(f"Checking Authentication")
    print(f"{'='*80}\n")

    # Try base OData endpoint
    url = f"{odata_base_url.rstrip('/')}"
    print(f"Trying base OData endpoint: {url}")

    try:
        response = client.session.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"  [OK] Authentication successful")
            print(f"  Service Document contains: {list(data.keys())}")
            return True
        else:
            print(f"  [FAIL] Status: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"  [ERROR] {str(e)}")
        return False


def print_summary(results):
    """
    Print a summary of exploration results.

    Args:
        results: Dictionary from explore_domains()
    """
    print(f"\n{'='*80}")
    print(f"EXPLORATION SUMMARY")
    print(f"{'='*80}\n")

    total_collections = 0
    for domain, collections in results.items():
        if collections:
            total_collections += len(collections)
            print(f"{domain:20} : {len(collections):3} collections")

    print(f"\nTotal: {total_collections} collections across {len(results)} domains")


def main():
    """Command-line interface for exploring Windchill"""
    import argparse

    parser = argparse.ArgumentParser(description="Explore Windchill OData")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Explore all domains
    explore_parser = subparsers.add_parser("explore", help="Explore all domains")

    # Get metadata
    metadata_parser = subparsers.add_parser("metadata", help="Get domain metadata")
    metadata_parser.add_argument("--domain", required=True, help="Domain name (e.g., ProdMgmt)")

    # Query collection
    query_parser = subparsers.add_parser("query", help="Query a collection")
    query_parser.add_argument("--domain", required=True, help="Domain name")
    query_parser.add_argument("--collection", required=True, help="Collection name")
    query_parser.add_argument("--top", type=int, default=5, help="Limit results")
    query_parser.add_argument("--select", help="Select properties")

    # Check CSRF
    csrf_parser = subparsers.add_parser("csrf", help="Check CSRF token endpoint")

    # Check authentication
    auth_parser = subparsers.add_parser("auth", help="Check authentication")

    args = parser.parse_args()

    client = WindchillClient()

    if args.command == "explore":
        results = explore_domains(client)
        print_summary(results)

        # Save results to file
        output_path = Path(__file__).parent.parent / "references" / "domain_exploration.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {output_path}")

    elif args.command == "metadata":
        metadata = get_domain_metadata(args.domain)
        if metadata:
            # Save metadata to file
            output_path = Path(__file__).parent.parent / "references" / f"{args.domain}_metadata.xml"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(metadata)
            print(f"\nMetadata saved to: {output_path}")

    elif args.command == "query":
        results = query_collection(args.domain, args.collection, args.top, args.select)
        if results:
            print(f"\nResults:")
            print(json.dumps(results, indent=2, default=str))

    elif args.command == "csrf":
        check_csrf_token()

    elif args.command == "auth":
        check_authentication()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()