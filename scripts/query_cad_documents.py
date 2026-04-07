#!/usr/bin/env python3
"""Query CAD Documents from Windchill CADDocumentMgmt domain"""

import sys
import json
from pathlib import Path
import requests

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from windchill_client import WindchillClient


def get_cad_document_by_number(cad_number, expand=None, select=None):
    """
    Get a CAD document by its number.

    Args:
        cad_number: CAD Document Number
        expand: Optional navigation properties to expand (comma-separated)
        select: Optional properties to select (comma-separated)

    Returns:
        dict: CAD document data or None if not found
    """
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/CADDocumentMgmt/CADDocuments"

    params = {"$filter": f"Number eq '{cad_number}'"}
    if expand:
        params["$expand"] = expand
    if select:
        params["$select"] = select

    try:
        response = client.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        docs = data.get("value", [])

        if docs:
            print(f"\n[OK] Found {len(docs)} CAD Document(s):")
            for doc in docs:
                print(f"\n  Number: {doc.get('Number')}")
                print(f"  Name: {doc.get('Name')}")
                print(f"  ID: {doc.get('ID')}")
                print(f"  FileName: {doc.get('FileName', 'N/A')}")
                print(f"  Revision: {doc.get('Revision', 'N/A')}")
                print(f"  Version: {doc.get('Version', 'N/A')}")
                print(f"  State: {doc.get('State', {}).get('Display', 'N/A')}")
                print(f"  Folder: {doc.get('FolderLocation', 'N/A')}")
                print(f"  Authoring App: {doc.get('AuthoringApplication', {}).get('Display', 'N/A')}")
            return docs[0] if len(docs) == 1 else docs
        else:
            print(f"\n[INFO] No CAD Document found with Number: {cad_number}")
            return None
    except requests.RequestException as e:
        print(f"\n[ERROR] Failed to query CAD document: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None


def get_cad_document_structure(cad_id, expand=None):
    """
    Get CAD structure (uses/references) for a CAD document.

    Args:
        cad_id: CAD Document ID
        expand: Optional navigation properties to expand

    Returns:
        dict: CAD structure data or None if not found
    """
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/CADDocumentMgmt/CADDocuments('{cad_id}')/CADStructure"

    params = {}
    if expand:
        params["$expand"] = expand

    try:
        response = client.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        print(f"\n[OK] CAD Structure retrieved for ID: {cad_id}")
        return data
    except requests.RequestException as e:
        print(f"\n[ERROR] Failed to get CAD structure: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None


def get_cad_document_uses(cad_id, expand=None):
    """
    Get CAD document uses (children/dependencies).

    Args:
        cad_id: CAD Document ID
        expand: Optional navigation properties to expand

    Returns:
        list: CAD uses data or empty list
    """
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/CADDocumentMgmt/CADDocuments('{cad_id}')/Uses"

    params = {}
    if expand:
        params["$expand"] = expand

    try:
        response = client.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        uses = data.get("value", [])

        print(f"\n[OK] Found {len(uses)} CAD Uses:")
        for use in uses:
            print(f"  - {use.get('ID', 'N/A')}: FeatureID={use.get('FeatureID', 'N/A')}, " +
                  f"Qty={use.get('Quantity', 0)}, Suppressed={use.get('Suppressed', False)}")
        return uses
    except requests.RequestException as e:
        print(f"\n[ERROR] Failed to get CAD uses: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return []


def get_cad_document_references(cad_id, expand=None):
    """
    Get CAD document references.

    Args:
        cad_id: CAD Document ID
        expand: Optional navigation properties to expand

    Returns:
        list: CAD references data or empty list
    """
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/CADDocumentMgmt/CADDocuments('{cad_id}')/References"

    params = {}
    if expand:
        params["$expand"] = expand

    try:
        response = client.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        refs = data.get("value", [])

        print(f"\n[OK] Found {len(refs)} CAD References:")
        for ref in refs:
            print(f"  - {ref.get('ID', 'N/A')}: Required={ref.get('Required', False)}")
        return refs
    except requests.RequestException as e:
        print(f"\n[ERROR] Failed to get CAD references: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return []


def get_cad_document_related_parts(cad_id):
    """
    Get parts related to a CAD document via PartDocAssociation.

    Args:
        cad_id: CAD Document ID

    Returns:
        list: Related parts data or empty list
    """
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/CADDocumentMgmt/CADDocuments('{cad_id}')/PartDocAssociations"

    params = {"$expand": "RelatedPart"}

    try:
        response = client.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        associations = data.get("value", [])

        print(f"\n[OK] Found {len(associations)} Part-Document Associations:")
        for assoc in associations:
            part = assoc.get("RelatedPart", {})
            print(f"  - Part: {part.get('Number', 'N/A')} - {part.get('Name', 'N/A')} " +
                  f"| Association: {assoc.get('AssociationType', {}).get('Display', 'N/A')}")
        return associations
    except requests.RequestException as e:
        print(f"\n[ERROR] Failed to get related parts: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return []


def query_cad_documents(filter_expr=None, top=None, select=None, expand=None):
    """
    Query CAD documents with optional filter.

    Args:
        filter_expr: OData filter expression
        top: Maximum number of results
        select: Properties to select (comma-separated)
        expand: Navigation properties to expand (comma-separated)

    Returns:
        list: CAD documents data or empty list
    """
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/CADDocumentMgmt/CADDocuments"

    params = {}
    if filter_expr:
        params["$filter"] = filter_expr
    if top:
        params["$top"] = top
    if select:
        params["$select"] = select
    if expand:
        params["$expand"] = expand

    try:
        response = client.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        docs = data.get("value", [])

        print(f"\n[OK] Found {len(docs)} CAD Document(s):")
        for doc in docs:
            print(f"  - {doc.get('Number', 'N/A')}: {doc.get('Name', 'N/A')} | " +
                  f"{doc.get('FileName', 'N/A')} | {doc.get('State', {}).get('Display', 'N/A')}")
        return docs
    except requests.RequestException as e:
        print(f"\n[ERROR] Failed to query CAD documents: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return []


def main():
    """Command-line interface for querying CAD documents"""
    import argparse

    parser = argparse.ArgumentParser(description="Query CAD Documents from Windchill")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Get by number
    get_parser = subparsers.add_parser("get", help="Get CAD document by number")
    get_parser.add_argument("--number", required=True, help="CAD Document Number")
    get_parser.add_argument("--expand", help="Expand navigation properties")
    get_parser.add_argument("--select", help="Select properties")

    # Query with filter
    query_parser = subparsers.add_parser("query", help="Query CAD documents")
    query_parser.add_argument("--filter", help="OData filter expression")
    query_parser.add_argument("--top", type=int, help="Limit results")
    query_parser.add_argument("--select", help="Select properties")
    query_parser.add_argument("--expand", help="Expand navigation properties")

    # Get structure
    struct_parser = subparsers.add_parser("structure", help="Get CAD structure")
    struct_parser.add_argument("--id", required=True, help="CAD Document ID")
    struct_parser.add_argument("--expand", help="Expand navigation properties")

    # Get uses
    uses_parser = subparsers.add_parser("uses", help="Get CAD uses")
    uses_parser.add_argument("--id", required=True, help="CAD Document ID")
    uses_parser.add_argument("--expand", help="Expand navigation properties")

    # Get references
    refs_parser = subparsers.add_parser("references", help="Get CAD references")
    refs_parser.add_argument("--id", required=True, help="CAD Document ID")
    refs_parser.add_argument("--expand", help="Expand navigation properties")

    # Get related parts
    parts_parser = subparsers.add_parser("parts", help="Get related parts")
    parts_parser.add_argument("--id", required=True, help="CAD Document ID")

    args = parser.parse_args()

    if args.command == "get":
        get_cad_document_by_number(args.number, args.expand, args.select)
    elif args.command == "query":
        query_cad_documents(args.filter, args.top, args.select, args.expand)
    elif args.command == "structure":
        get_cad_document_structure(args.id, args.expand)
    elif args.command == "uses":
        get_cad_document_uses(args.id, args.expand)
    elif args.command == "references":
        get_cad_document_references(args.id, args.expand)
    elif args.command == "parts":
        get_cad_document_related_parts(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()