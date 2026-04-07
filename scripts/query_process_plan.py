#!/usr/bin/env python
"""
Query Windchill Process Plans with Operations
"""
import sys
import json
import requests
from requests.auth import HTTPBasicAuth

def query_process_plan(base_url, username, password, number):
    """Query process plan by number with operations expanded"""
    auth = HTTPBasicAuth(username, password)

    # Query process plan with operations
    url = f"{base_url}/MfgProcMgmt/ProcessPlan?$filter=Number eq '{number}'&$expand=Operations"
    headers = {"Accept": "application/json"}

    response = requests.get(url, auth=auth, headers=headers, verify=True, timeout=30)
    response.raise_for_status()

    data = response.json()
    process_plans = data.get('value', [])

    if not process_plans:
        print(f"No process plan found with number {number}")
        return

    for pp in process_plans:
        print("Process Plan:")
        print(f"Number: {pp.get('Number')}")
        print(f"Name: {pp.get('Name')}")
        print(f"ID: {pp.get('ID')}")
        print(f"Revision: {pp.get('Revision')}")
        print(f"Version: {pp.get('Version')}")
        print(f"State: {pp.get('State')}")
        print(f"Folder: {pp.get('FolderLocation')}")
        print(f"CreatedBy: {pp.get('CreatedBy')}")
        print(f"CreatedOn: {pp.get('CreatedOn')}")
        print()

        # Get operations
        ops = pp.get('Operations', [])
        if ops:
            print(f"Operations ({len(ops)}):")
            for op in ops:
                print(f"  Seq: {op.get('SequenceNumber')}, Name: {op.get('Name')}, Number: {op.get('Number')}, Type: {op.get('ObjectType')}, State: {op.get('State')}")
        else:
            print("No operations found")

if __name__ == "__main__":
    base_url = "https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata"
    username = "pat"
    password = "ptc"

    number = sys.argv[1] if len(sys.argv) > 1 else "0000000061"

    query_process_plan(base_url, username, password, number)