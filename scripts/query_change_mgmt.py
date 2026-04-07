#!/usr/bin/env python3
"""Query Change Management objects from Windchill ChangeMgmt domain"""

import sys
import json
from pathlib import Path
import requests

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from windchill_client import WindchillClient


def get_change_notice_by_number(notice_number, expand=None, select=None):
    """
    Get a Change Notice by its number.

    Args:
        notice_number: Change Notice Number
        expand: Optional navigation properties to expand (comma-separated)
        select: Optional properties to select (comma-separated)

    Returns:
        dict: Change Notice data or None if not found
    """
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/ChangeMgmt/ChangeNotices"

    params = {"$filter": f"Number eq '{notice_number}'"}
    if expand:
        params["$expand"] = expand
    if select:
        params["$select"] = select

    try:
        response = client.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        notices = data.get("value", [])

        if notices:
            print(f"\n[OK] Found {len(notices)} Change Notice(s):")
            for notice in notices:
                print(f"\n  Number: {notice.get('Number')}")
                print(f"  Name: {notice.get('Name')}")
                print(f"  ID: {notice.get('ID')}")
                print(f"  State: {notice.get('State', {}).get('Display', 'N/A')}")
                print(f"  Folder: {notice.get('FolderLocation', 'N/A')}")
                print(f"  CreatedBy: {notice.get('CreatedBy', 'N/A')}")
                print(f"  CreatedOn: {notice.get('CreatedOn', 'N/A')}")
                print(f"  ModifiedBy: {notice.get('ModifiedBy', 'N/A')}")
                print(f"  LastModified: {notice.get('LastModified', 'N/A')}")
            return notices[0] if len(notices) == 1 else notices
        else:
            print(f"\n[INFO] No Change Notice found with Number: {notice_number}")
            return None
    except requests.RequestException as e:
        print(f"\n[ERROR] Failed to query change notice: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None


def get_change_request_by_number(request_number, expand=None, select=None):
    """
    Get a Change Request by its number.

    Args:
        request_number: Change Request Number
        expand: Optional navigation properties to expand (comma-separated)
        select: Optional properties to select (comma-separated)

    Returns:
        dict: Change Request data or None if not found
    """
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/ChangeMgmt/ChangeRequests"

    params = {"$filter": f"Number eq '{request_number}'"}
    if expand:
        params["$expand"] = expand
    if select:
        params["$select"] = select

    try:
        response = client.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        requests_data = data.get("value", [])

        if requests_data:
            print(f"\n[OK] Found {len(requests_data)} Change Request(s):")
            for req in requests_data:
                print(f"\n  Number: {req.get('Number')}")
                print(f"  Name: {req.get('Name')}")
                print(f"  ID: {req.get('ID')}")
                print(f"  State: {req.get('State', {}).get('Display', 'N/A')}")
                print(f"  Folder: {req.get('FolderLocation', 'N/A')}")
                print(f"  CreatedBy: {req.get('CreatedBy', 'N/A')}")
                print(f"  CreatedOn: {req.get('CreatedOn', 'N/A')}")
                print(f"  ModifiedBy: {req.get('ModifiedBy', 'N/A')}")
                print(f"  LastModified: {req.get('LastModified', 'N/A')}")
                print(f"  Description: {req.get('Description', 'N/A')[:100]}...")
            return requests_data[0] if len(requests_data) == 1 else requests_data
        else:
            print(f"\n[INFO] No Change Request found with Number: {request_number}")
            return None
    except requests.RequestException as e:
        print(f"\n[ERROR] Failed to query change request: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None


def get_change_task_by_number(task_number, expand=None, select=None):
    """
    Get a Change Task by its number.

    Args:
        task_number: Change Task Number
        expand: Optional navigation properties to expand (comma-separated)
        select: Optional properties to select (comma-separated)

    Returns:
        dict: Change Task data or None if not found
    """
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/ChangeMgmt/ChangeTasks"

    params = {"$filter": f"Number eq '{task_number}'"}
    if expand:
        params["$expand"] = expand
    if select:
        params["$select"] = select

    try:
        response = client.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        tasks = data.get("value", [])

        if tasks:
            print(f"\n[OK] Found {len(tasks)} Change Task(s):")
            for task in tasks:
                print(f"\n  Number: {task.get('Number')}")
                print(f"  Name: {task.get('Name')}")
                print(f"  ID: {task.get('ID')}")
                print(f"  State: {task.get('State', {}).get('Display', 'N/A')}")
                print(f"  Folder: {task.get('FolderLocation', 'N/A')}")
                print(f"  CreatedBy: {task.get('CreatedBy', 'N/A')}")
                print(f"  CreatedOn: {task.get('CreatedOn', 'N/A')}")
            return tasks[0] if len(tasks) == 1 else tasks
        else:
            print(f"\n[INFO] No Change Task found with Number: {task_number}")
            return None
    except requests.RequestException as e:
        print(f"\n[ERROR] Failed to query change task: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None


def query_change_notices(filter_expr=None, top=None, select=None, expand=None):
    """
    Query Change Notices with optional filter.

    Args:
        filter_expr: OData filter expression
        top: Maximum number of results
        select: Properties to select (comma-separated)
        expand: Navigation properties to expand (comma-separated)

    Returns:
        list: Change Notices data or empty list
    """
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/ChangeMgmt/ChangeNotices"

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
        notices = data.get("value", [])

        print(f"\n[OK] Found {len(notices)} Change Notice(s):")
        for notice in notices:
            print(f"  - {notice.get('Number', 'N/A')}: {notice.get('Name', 'N/A')} | " +
                  f"{notice.get('State', {}).get('Display', 'N/A')}")
        return notices
    except requests.RequestException as e:
        print(f"\n[ERROR] Failed to query change notices: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return []


def query_change_requests(filter_expr=None, top=None, select=None, expand=None):
    """
    Query Change Requests with optional filter.

    Args:
        filter_expr: OData filter expression
        top: Maximum number of results
        select: Properties to select (comma-separated)
        expand: Navigation properties to expand (comma-separated)

    Returns:
        list: Change Requests data or empty list
    """
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/ChangeMgmt/ChangeRequests"

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
        requests_data = data.get("value", [])

        print(f"\n[OK] Found {len(requests_data)} Change Request(s):")
        for req in requests_data:
            print(f"  - {req.get('Number', 'N/A')}: {req.get('Name', 'N/A')} | " +
                  f"{req.get('State', {}).get('Display', 'N/A')}")
        return requests_data
    except requests.RequestException as e:
        print(f"\n[ERROR] Failed to query change requests: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return []


def query_change_tasks(filter_expr=None, top=None, select=None, expand=None):
    """
    Query Change Tasks with optional filter.

    Args:
        filter_expr: OData filter expression
        top: Maximum number of results
        select: Properties to select (comma-separated)
        expand: Navigation properties to expand (comma-separated)

    Returns:
        list: Change Tasks data or empty list
    """
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/ChangeMgmt/ChangeTasks"

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
        tasks = data.get("value", [])

        print(f"\n[OK] Found {len(tasks)} Change Task(s):")
        for task in tasks:
            print(f"  - {task.get('Number', 'N/A')}: {task.get('Name', 'N/A')} | " +
                  f"{task.get('State', {}).get('Display', 'N/A')}")
        return tasks
    except requests.RequestException as e:
        print(f"\n[ERROR] Failed to query change tasks: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return []


def get_resulting_objects(change_id):
    """
    Get resulting objects (parts, documents, etc.) from a change object.

    Args:
        change_id: Change object ID

    Returns:
        list: Resulting objects data or empty list
    """
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/ChangeMgmt/ChangeNotices('{change_id}')/ResultingObjects"

    try:
        response = client.session.get(url)
        response.raise_for_status()
        data = response.json()
        results = data.get("value", [])

        print(f"\n[OK] Found {len(results)} Resulting Objects:")
        for result in results:
            print(f"  - {result.get('ID', 'N/A')}: {result.get('ObjectType', 'N/A')}")
        return results
    except requests.RequestException as e:
        print(f"\n[ERROR] Failed to get resulting objects: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return []


def get_affected_objects(change_id):
    """
    Get affected objects from a change object.

    Args:
        change_id: Change object ID

    Returns:
        list: Affected objects data or empty list
    """
    client = WindchillClient()

    odata_base_url = client.config.get("odata_base_url", client.config["server_url"] + "/servlet/odata")
    url = f"{odata_base_url.rstrip('/')}/ChangeMgmt/ChangeNotices('{change_id}')/AffectedObjects"

    try:
        response = client.session.get(url)
        response.raise_for_status()
        data = response.json()
        results = data.get("value", [])

        print(f"\n[OK] Found {len(results)} Affected Objects:")
        for result in results:
            print(f"  - {result.get('ID', 'N/A')}: {result.get('ObjectType', 'N/A')}")
        return results
    except requests.RequestException as e:
        print(f"\n[ERROR] Failed to get affected objects: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return []


def main():
    """Command-line interface for querying change management objects"""
    import argparse

    parser = argparse.ArgumentParser(description="Query Change Management from Windchill")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Get Change Notice
    cn_parser = subparsers.add_parser("notice", help="Get Change Notice by number")
    cn_parser.add_argument("--number", required=True, help="Change Notice Number")
    cn_parser.add_argument("--expand", help="Expand navigation properties")
    cn_parser.add_argument("--select", help="Select properties")

    # Get Change Request
    cr_parser = subparsers.add_parser("request", help="Get Change Request by number")
    cr_parser.add_argument("--number", required=True, help="Change Request Number")
    cr_parser.add_argument("--expand", help="Expand navigation properties")
    cr_parser.add_argument("--select", help="Select properties")

    # Get Change Task
    ct_parser = subparsers.add_parser("task", help="Get Change Task by number")
    ct_parser.add_argument("--number", required=True, help="Change Task Number")
    ct_parser.add_argument("--expand", help="Expand navigation properties")
    ct_parser.add_argument("--select", help="Select properties")

    # Query Change Notices
    qcn_parser = subparsers.add_parser("query-notices", help="Query Change Notices")
    qcn_parser.add_argument("--filter", help="OData filter expression")
    qcn_parser.add_argument("--top", type=int, help="Limit results")
    qcn_parser.add_argument("--select", help="Select properties")
    qcn_parser.add_argument("--expand", help="Expand navigation properties")

    # Query Change Requests
    qcr_parser = subparsers.add_parser("query-requests", help="Query Change Requests")
    qcr_parser.add_argument("--filter", help="OData filter expression")
    qcr_parser.add_argument("--top", type=int, help="Limit results")
    qcr_parser.add_argument("--select", help="Select properties")
    qcr_parser.add_argument("--expand", help="Expand navigation properties")

    # Query Change Tasks
    qct_parser = subparsers.add_parser("query-tasks", help="Query Change Tasks")
    qct_parser.add_argument("--filter", help="OData filter expression")
    qct_parser.add_argument("--top", type=int, help="Limit results")
    qct_parser.add_argument("--select", help="Select properties")
    qct_parser.add_argument("--expand", help="Expand navigation properties")

    # Get Resulting Objects
    ro_parser = subparsers.add_parser("resulting", help="Get Resulting Objects")
    ro_parser.add_argument("--id", required=True, help="Change object ID")

    # Get Affected Objects
    ao_parser = subparsers.add_parser("affected", help="Get Affected Objects")
    ao_parser.add_argument("--id", required=True, help="Change object ID")

    args = parser.parse_args()

    if args.command == "notice":
        get_change_notice_by_number(args.number, args.expand, args.select)
    elif args.command == "request":
        get_change_request_by_number(args.number, args.expand, args.select)
    elif args.command == "task":
        get_change_task_by_number(args.number, args.expand, args.select)
    elif args.command == "query-notices":
        query_change_notices(args.filter, args.top, args.select, args.expand)
    elif args.command == "query-requests":
        query_change_requests(args.filter, args.top, args.select, args.expand)
    elif args.command == "query-tasks":
        query_change_tasks(args.filter, args.top, args.select, args.expand)
    elif args.command == "resulting":
        get_resulting_objects(args.id)
    elif args.command == "affected":
        get_affected_objects(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()