#!/usr/bin/env python3
"""Query Windchill Service Information Management (ServiceInfoMgmt) records"""

import sys
import os
import json
import argparse

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# For direct requests
import requests


def query_service_info(
    base_url: str,
    username: str,
    password: str,
    collection: str = "SIMDocuments",
    top: int = None,
    filter_expr: str = None,
    expand: str = None,
    select: str = None,
    output_file: str = None
):
    """
    Query Windchill Service Information Management records.

    Args:
        base_url: Windchill OData base URL
        username: Windchill username
        password: Windchill password
        collection: Collection to query
        top: Maximum number of results
        filter_expr: OData filter expression
        expand: Navigation properties to expand (comma-separated)
        select: Properties to select (comma-separated)
        output_file: Optional file path to save results

    Returns:
        dict: Query results
    """
    session = requests.Session()

    # Build query
    url = f"{base_url}ServiceInfoMgmt/{collection}"

    params = []
    if top:
        params.append(f"$top={top}")
    if filter_expr:
        params.append(f"$filter={filter_expr}")
    if expand:
        params.append(f"$expand={expand}")
    if select:
        params.append(f"$select={select}")

    url += f"?{ '&'.join(params) }" if params else ""

    print(f"Querying: {url}")

    response = session.get(url, auth=(username, password), verify=True)
    response.raise_for_status()

    result = response.json()

    if output_file:
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Results saved to: {output_file}")

    return result


def print_sim_documents_summary(result: dict):
    """Print a summary of SIMDocuments"""
    value = result.get('value', [])

    print(f"\n{'='*70}")
    print(f"SIM DOCUMENTS ({len(value)})")
    print(f"{'='*70}\n")

    for i, item in enumerate(value, 1):
        name = item.get('Name', 'N/A')
        number = item.get('Number', 'N/A')
        state = item.get('State', {})
        state_display = state.get('Display') if isinstance(state, dict) else state
        revision = item.get('Revision', 'N/A')
        version = item.get('Version', 'N/A')
        desc = item.get('Description', 'N/A')
        folder = item.get('FolderLocation', 'N/A')
        created_by = item.get('CreatedBy', 'N/A')
        created_on = item.get('CreatedOn', 'N/A')

        print(f"{i}. {name}")
        print(f"   Number: {number}")
        print(f"   ID: {item.get('ID', 'N/A')}")
        print(f"   State: {state_display}")
        print(f"   Revision: {revision}, Version: {version}")
        if desc:
            print(f"   Description: {desc}")
        print(f"   Folder: {folder}")
        print(f"   Created by: {created_by}")
        print(f"   Created: {created_on}")

        # Show info elements count if expanded
        info_elements = item.get('InformationElement', [])
        if info_elements:
            print(f"   Information Elements: {len(info_elements)}")

        print()


def print_info_structures_summary(result: dict):
    """Print a summary of Information Structures"""
    value = result.get('value', [])

    print(f"\n{'='*70}")
    print(f"INFORMATION STRUCTURES ({len(value)})")
    print(f"{'='*70}\n")

    for i, item in enumerate(value, 1):
        name = item.get('Name', 'N/A')
        number = item.get('Number', 'N/A')
        state = item.get('State', {})
        state_display = state.get('Display') if isinstance(state, dict) else state
        revision = item.get('Revision', 'N/A')
        version = item.get('Version', 'N/A')
        view = item.get('View', 'N/A')
        lang = item.get('AuthoringLanguage', {})
        lang_display = lang.get('Display') if isinstance(lang, dict) else lang

        is_primary = item.get('IsPrimary', False)
        is_template = item.get('IsTemplate', False)

        print(f"{i}. {name}")
        print(f"   Number: {number}")
        print(f"   ID: {item.get('ID', 'N/A')}")
        print(f"   State: {state_display}")
        print(f"   Revision: {revision}, Version: {version}")
        print(f"   View: {view}")
        if lang_display:
            print(f"   Language: {lang_display}")
        if is_primary:
            print(f"   Primary Structure: Yes")
        if is_template:
            print(f"   Template: Yes")

        print()


def print_publication_structures_summary(result: dict):
    """Print a summary of Publication Structures"""
    value = result.get('value', [])

    print(f"\n{'='*70}")
    print(f"PUBLICATION STRUCTURES ({len(value)})")
    print(f"{'='*70}\n")

    for i, item in enumerate(value, 1):
        name = item.get('Name', 'N/A')
        number = item.get('Number', 'N/A')
        state = item.get('State', {})
        state_display = state.get('Display') if isinstance(state, dict) else state

        is_template = item.get('IsTemplate', False)

        print(f"{i}. {name}")
        print(f"   Number: {number}")
        print(f"   ID: {item.get('ID', 'N/A')}")
        print(f"   State: {state_display}")
        if is_template:
            print(f"   Template: Yes")

        print()


def print_info_elements_summary(result: dict, element_type: str):
    """Print a summary of information elements"""
    value = result.get('value', [])

    print(f"\n{'='*70}")
    print(f"{element_type.upper()} ({len(value)})")
    print(f"{'='*70}\n")

    for i, item in enumerate(value, 1):
        id_val = item.get('ID', 'N/A')
        content_type = item.get('SisContentholderType', 'N/A')
        title_from_content = item.get('SisContentholderTitleFromContent', False)

        # Document elements have symptoms
        if element_type == 'DocumentInformationElement':
            symptoms = item.get('Symptoms', 'N/A')
        else:
            symptoms = None

        print(f"{i}. ID: {id_val}")
        print(f"   Type: {content_type}")
        print(f"   Title from Content: {'Yes' if title_from_content else 'No'}")

        if symptoms:
            print(f"   Symptoms: {symptoms}")

        # Show linked document if DocumentInformationElement
        if element_type == 'DocumentInformationElement':
            content = item.get('Content', {})
            if content and isinstance(content, dict):
                doc_name = content.get('Name', 'N/A')
                doc_number = content.get('Number', 'N/A')
                print(f"   Linked Document: {doc_name} ({doc_number})")

        print()


def print_generic_summary(result: dict, collection: str):
    """Print a generic summary for other collections"""
    value = result.get('value', [])

    print(f"\n{'='*70}")
    print(f"{collection} ({len(value)})")
    print(f"{'='*70}\n")

    for i, item in enumerate(value, 1):
        name = item.get('Name', 'N/A')
        id_val = item.get('ID', 'N/A')
        created_on = item.get('CreatedOn', 'N/A')

        print(f"{i}. Name: {name}")
        print(f"   ID: {id_val}")
        if created_on:
            print(f"   Created: {created_on}")

        # Show additional key properties
        for key in ['Number', 'State', 'Revision', 'Version', 'View']:
            val = item.get(key)
            if val:
                if isinstance(val, dict):
                    val = val.get('Display', val)
                print(f"   {key}: {val}")

        print()


def main():
    """Command-line interface for querying ServiceInfoMgmt"""
    parser = argparse.ArgumentParser(description='Query Windchill Service Information Management')
    parser.add_argument('--url', default='https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/')
    parser.add_argument('--username', default='pat')
    parser.add_argument('--password', default='ptc')
    parser.add_argument('--collection', help='Collection to query (default: SIMDocuments)',
                       choices=['SIMDocuments', 'InformationStructures', 'PublicationStructures',
                               'SIMDynamicDocuments', 'TextualInformationElement',
                               'DocumentInformationElement',
                               'GraphicalInformationElement',
                               'InformationGroups', 'PublicationSections',
                               'Indexes', 'GenericInformationElement',
                               'TableOfContents'])
    parser.add_argument('--top', type=int, help='Maximum number of results')
    parser.add_argument('--filter', dest='filter_expr', help='OData filter expression')
    parser.add_argument('--expand', help='Navigation properties to expand (comma-separated)')
    parser.add_argument('--select', help='Properties to select (comma-separated)')
    parser.add_argument('--output', help='Output file path (JSON)')

    args = parser.parse_args()

    # Default collection
    collection = args.collection or "SIMDocuments"

    result = query_service_info(
        base_url=args.url,
        username=args.username,
        password=args.password,
        collection=collection,
        top=args.top,
        filter_expr=args.filter_expr,
        expand=args.expand,
        select=args.select,
        output_file=args.output
    )

    # Print appropriate summary based on collection
    if collection == "SIMDocuments":
        print_sim_documents_summary(result)
    elif collection == "InformationStructures":
        print_info_structures_summary(result)
    elif collection == "PublicationStructures":
        print_publication_structures_summary(result)
    elif collection == "TextualInformationElement":
        print_info_elements_summary(result, "TextualInformationElement")
    elif collection == "DocumentInformationElement":
        print_info_elements_summary(result, "DocumentInformationElement")
    elif collection == "GraphicalInformationElement":
        print_info_elements_summary(result, "GraphicalInformationElement")
    else:
        print_generic_summary(result, collection)


if __name__ == '__main__':
    main()
