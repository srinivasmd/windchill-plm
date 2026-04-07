#!/usr/bin/env python3
"""Query Windchill UDI (Unique Device Identification) records"""

import sys
import os
import json
import argparse

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# For direct requests
import requests


def query_udi(
    base_url: str,
    username: str,
    password: str,
    collection: str = "UDISuperSets2",
    top: int = None,
    filter_expr: str = None,
    expand: str = None,
    select: str = None,
    output_file: str = None
):
    """
    Query Windchill UDI records.

    Args:
        base_url: Windchill OData base URL
        username: Windchill username
        password: Windchill password
        collection: Collection to query (UDISuperSets, UDISuperSets2, or UDISubjects)
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
    url = f"{base_url}UDI/{collection}"

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


def print_udi_supersets_summary(result: dict, collection: str = "UDISuperSets2"):
    """Print a summary of UDI supersets"""
    value = result.get('value', [])

    print(f"\n{'='*70}")
    print(f"UDI {collection} ({len(value)})")
    print(f"{'='*70}\n")

    for i, item in enumerate(value, 1):
        if collection == "UDISubjects":
            # Handle UDISubjects (parts)
            name = item.get('Name', 'N/A')
            number = item.get('Number', 'N/A')
            version = item.get('Version', 'N/A')
            identity = item.get('Identity', 'N/A')

            print(f"{i}. {name}")
            print(f"   Number: {number}")
            print(f"   Version: {version}")
            print(f"   ID: {item.get('ID', 'N/A')}")
            print(f"   Identity: {identity}")
            print(f"   Organization: {item.get('OrganizationID', 'N/A')}")
            print(f"   Created: {item.get('CreatedOn', 'N/A')}")
            print()

        else:
            # Handle UDISuperSet or UDISuperSet2
            di = item.get('DeviceIdentifier', 'N/A')
            brand = item.get('BrandName', 'N/A')
            catalog = item.get('CatalogNumber', 'N/A')
            state = item.get('State', {})
            state_display = state.get('Display') if isinstance(state, dict) else state

            name = item.get('Name', 'N/A')
            number = item.get('Number', 'N/A')

            device_desc = item.get('DeviceDescription', 'N/A')

            discontinued = item.get('DiscontinuedDate', None)

            print(f"{i}. {brand} - {catalog}")
            print(f"   Device Identifier: {di}")
            print(f"   Name: {name}")
            print(f"   Number: {number}")
            print(f"   ID: {item.get('ID', 'N/A')}")

            if device_desc:
                print(f"   Description: {device_desc}")

            print(f"   Status: {state_display}")

            if collection == "UDISuperSets2":
                # Show multi-subject info for UDISuperSet2
                subjects = item.get('Subjects', [])
                if subjects:
                    print(f"   Linked Subjects: {len(subjects)}")
            else:
                # Show single subject for UDISuperSet
                subject = item.get('Subject', {})
                if subject:
                    subj_name = subject.get('Name', 'N/A')
                    subj_number = subject.get('Number', 'N/A') if isinstance(subject, dict) else subject
                    print(f"   Subject: {subj_name} ({subj_number})")

            if discontinued:
                print(f"   Discontinued: {discontinued}")

            print(f"   Created: {item.get('CreatedOn', 'N/A')}")

            # Show details summary
            details = item.get('Details', [])
            if details:
                print(f"   Details: {len(details)} records")

            # Show packaging info
            packaging = item.get('PackagingConfigurations', [])
            if packaging:
                print(f"   Packaging: {len(packaging)} configs")

            print()


def print_details_summary(result: dict):
    """Print summary of details for a UDI record"""
    value = result.get('value', [])

    if not value:
        return

    print(f"\n{'='*70}")
    print(f"UDI DETAILS ({len(value)})")
    print(f"{'='*70}\n")

    for i, detail in enumerate(value, 1):
        detail_type = detail.get('ObjectType', 'N/A')

        print(f"{i}. {detail_type}")

        # Print based on detail type
        if detail_type == 'DeviceContact':
            phone = detail.get('PhoneNumber', 'N/A')
            email = detail.get('EmailAddress', 'N/A')
            print(f"   Phone: {phone}")
            print(f"   Email: {email}")

        elif detail_type == 'FDAProductCode':
            code = detail.get('Udiss_fdaProductCode', 'N/A')
            print(f"   FDA Product Code: {code}")

        elif detail_type == 'FDAPremarketAuthorizationNumber':
            pma = detail.get('Udiss_fdaPremarketAuthorizationNumber', 'N/A')
            supplement = detail.get('Udiss_fdaSupplementNumber', 'N/A')
            print(f"   PMA: {pma}")
            print(f"   Supplement: {supplement}")

        elif detail_type == 'FDAListingNumber':
            listing = detail.get('Udiss_fdaListingNumber', 'N/A')
            print(f"   FDA Listing: {listing}")

        elif detail_type == 'SterilizationMethod':
            method = detail.get('SterilizationMethod', {})
            method_display = method.get('Display') if isinstance(method, dict) else method
            print(f"   Method: {method_display}")

        elif detail_type == 'DeviceSizeCharacteristic':
            size_value = detail.get('Value', 'N/A')
            size_type = detail.get('SizeType', {})
            unit = detail.get('UnitOfMeasure', {})
            type_display = size_type.get('Display') if isinstance(size_type, dict) else size_type
            unit_display = unit.get('Display') if isinstance(unit, dict) else unit
            desc = detail.get('Description', 'N/A')
            print(f"   Value: {size_value}")
            print(f"   Type: {type_display}")
            print(f"   Unit: {unit_display}")
            if desc:
                print(f"   Description: {desc}")

        elif detail_type == 'GMDNTermCode':
            code = detail.get('GMDNTermCode', 'N/A')
            print(f"   GMDN Code: {code}")

        elif detail_type == 'StorageAndHandlingRequirement':
            desc = detail.get('Description', 'N/A')
            low_val = detail.get('LowValue', 'N/A')
            high_val = detail.get('HighValue', 'N/A')
            storage_type = detail.get('StorageType', {})
            storage_display = storage_type.get('Display') if isinstance(storage_type, dict) else storage_type
            print(f"   Type: {storage_display}")
            print(f"   Range: {low_val} - {high_val}")
            if desc:
                print(f"   Description: {desc}")

        elif detail_type == 'AlternateIdentifier':
            id_type = detail.get('IdentifierType', 'N/A')
            id_value = detail.get('IdentifierValue', 'N/A')
            print(f"   Type: {id_type}")
            print(f"   Value: {id_value}")

        else:
            # Generic detail
            for key, value in detail.items():
                if key not in ['ID', 'CreatedOn', 'LastModified', 'ObjectType']:
                    print(f"   {key}: {value}")

        print()


def print_subjects_summary(result: dict):
    """Print summary of subjects linked to UDI superset"""
    value = result.get('value', [])

    if not value:
        return

    print(f"\n{'='*70}")
    print(f"SUBJECTS ({len(value)})")
    print(f"{'='*70}\n")

    for i, subject in enumerate(value, 1):
        subj = subject.get('Subject') if isinstance(subject, dict) else None

        if subj and isinstance(subj, dict):
            name = subj.get('Name', 'N/A')
            number = subj.get('Number', 'N/A')
            version = subj.get('Version', 'N/A')
            view = subj.get('View', 'N/A')

            print(f"{i}. {name}")
            print(f"   Number: {number}")
            print(f"   Version: {version}")
            print(f"   View: {view}")
            print(f"   Subject ID: {subj.get('ID', 'N/A')}")
        else:
            # SubjectLink without expanded Subject
            print(f"{i}. SubjectLink ID: {subject.get('ID', 'N/A')}")

        print()


def print_packaging_summary(result: dict):
    """Print summary of packaging configurations"""
    value = result.get('value', [])

    if not value:
        return

    print(f"\n{'='*70}")
    print(f"PACKAGING CONFIGURATIONS ({len(value)})")
    print(f"{'='*70}\n")

    for i, pkg in enumerate(value, 1):
        pkg_di = pkg.get('PackageDeviceIdentifier', 'N/A')
        quantity = pkg.get('Quantity', 'N/A')
        desc = pkg.get('Description', 'N/A')
        discontinued = pkg.get('DiscontinuedDate', None)

        print(f"{i}. Package DI: {pkg_di}")
        print(f"   Quantity: {quantity}")
        if desc:
            print(f"   Description: {desc}")
        if discontinued:
            print(f"   Discontinued: {discontinued}")
        print()


def get_details_for_udi(base_url, username, password, udi_id: str, collection: str = "UDISuperSets2") -> dict:
    """Get the Details for a specific UDI record"""
    url = f"{base_url}UDI/{collection}('{udi_id}')/Details"

    session = requests.Session()
    response = session.get(url, auth=(username, password), verify=True)
    response.raise_for_status()

    return response.json()


def get_subjects_for_udi(base_url, username, password, udi_id: str, collection: str = "UDISuperSets2") -> dict:
    """Get the Subjects for a specific UDI record"""
    url = f"{base_url}UDI/{collection}('{udi_id}')/Subjects"

    session = requests.Session()
    response = session.get(url, auth=(username, password), verify=True)
    response.raise_for_status()

    return response.json()


def get_packaging_for_udi(base_url, username, password, udi_id: str, collection: str = "UDISuperSets2") -> dict:
    """Get the Packaging Configurations for a specific UDI record"""
    url = f"{base_url}UDI/{collection}('{udi_id}')/PackagingConfigurations"

    session = requests.Session()
    response = session.get(url, auth=(username, password), verify=True)
    response.raise_for_status()

    return response.json()


def main():
    """Command-line interface for querying UDI"""
    parser = argparse.ArgumentParser(description='Query Windchill UDI')
    parser.add_argument('--url', default='https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/')
    parser.add_argument('--username', default='pat')
    parser.add_argument('--password', default='ptc')
    parser.add_argument('--collection', choices=['UDISuperSets', 'UDISuperSets2', 'UDISubjects'],
                       default='UDISuperSets2', help='Collection to query')
    parser.add_argument('--top', type=int, help='Maximum number of results')
    parser.add_argument('--filter', dest='filter_expr', help='OData filter expression')
    parser.add_argument('--expand', help='Navigation properties to expand (comma-separated)')
    parser.add_argument('--select', help='Properties to select (comma-separated)')
    parser.add_argument('--output', help='Output file path (JSON)')

    subparsers = parser.add_subparsers(dest='command', help='Sub-commands')

    # UDI record command (default)
    udi_parser = subparsers.add_parser('udi', help='Query UDI records')
    udi_parser.add_argument('udi_id', nargs='?', help='UDI record ID')

    # Details command
    details_parser = subparsers.add_parser('details', help='Get details for UDI record')
    details_parser.add_argument('--udi-id', required=True, help='UDI record ID')
    details_parser.add_argument('--collection', default='UDISuperSets2', help='Collection name')

    # Subjects command
    subjects_parser = subparsers.add_parser('subjects', help='Get subjects for UDI record')
    subjects_parser.add_argument('--udi-id', required=True, help='UDI record ID')
    subjects_parser.add_argument('--collection', default='UDISuperSets2', help='Collection name')

    # Packaging command
    packaging_parser = subparsers.add_parser('packaging', help='Get packaging for UDI record')
    packaging_parser.add_argument('--udi-id', required=True, help='UDI record ID')
    packaging_parser.add_argument('--collection', default='UDISuperSets2', help='Collection name')

    args = parser.parse_args()

    # Default to UDI query if no command specified
    if not args.command or args.command == 'udi':
        if getattr(args, 'udi_id', None):
            # Query specific UDI record
            filter_expr = f"ID eq '{args.udi_id}'"
            # Expand by default for single item
            if not args.expand:
                args.expand = "Subjects,Details,PackagingConfigurations"
        else:
            filter_expr = args.filter_expr

        result = query_udi(
            base_url=args.url,
            username=args.username,
            password=args.password,
            collection=args.collection,
            top=args.top,
            filter_expr=filter_expr,
            expand=args.expand,
            select=args.select,
            output_file=args.output
        )

        print_udi_supersets_summary(result, args.collection)

    elif args.command == 'details':
        udi_id = args.udi_id
        result = get_details_for_udi(
            base_url=args.url,
            username=args.username,
            password=args.password,
            udi_id=udi_id,
            collection=args.collection
        )

        print_details_summary(result)

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Results saved to: {args.output}")

    elif args.command == 'subjects':
        udi_id = args.udi_id
        result = get_subjects_for_udi(
            base_url=args.url,
            username=args.username,
            password=args.password,
            udi_id=udi_id,
            collection=args.collection
        )

        print_subjects_summary(result)

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Results saved to: {args.output}")

    elif args.command == 'packaging':
        udi_id = args.udi_id
        result = get_packaging_for_udi(
            base_url=args.url,
            username=args.username,
            password=args.password,
            udi_id=udi_id,
            collection=args.collection
        )

        print_packaging_summary(result)

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Results saved to: {args.output}")


if __name__ == '__main__':
    main()
