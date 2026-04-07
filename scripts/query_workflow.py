#!/usr/bin/env python3
"""Query Windchill Workflow work items and activities"""

import sys
import os
import json
import argparse

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# For direct requests
import requests


def query_workflow(
    base_url: str,
    username: str,
    password: str,
    top: int = None,
    filter_expr: str = None,
    expand: str = None,
    select: str = None,
    output_file: str = None
):
    """
    Query Windchill Workflow items (work items, activities, etc.).

    Args:
        base_url: Windchill OData base URL
        username: Windchill username
        password: Windchill password
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
    url = f"{base_url}Workflow/WorkItems"

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


def print_work_items_summary(result: dict):
    """Print a summary of work items"""
    value = result.get('value', [])

    print(f"\n{'='*70}")
    print(f"WORK ITEMS ({len(value)})")
    print(f"{'='*70}\n")

    for i, item in enumerate(value, 1):
        task_name = item.get('TaskName', 'N/A')
        status = item.get('State', item.get('Status', {}))
        status_display = status.get('Display') if isinstance(status, dict) else status
        priority = item.get('Priority', 'N/A')
        role = item.get('Role', {})
        role_display = role.get('Display') if isinstance(role, dict) else role

        owner = item.get('Owner', {})
        owner_name = owner.get('Name', 'N/A') if isinstance(owner, dict) else owner

        created_on = item.get('CreatedOn', 'N/A')
        deadline = None
        if item.get('Activity'):
            activity = item.get('Activity', {})
            deadline = activity.get('Deadline', None)

        print(f"{i}. {task_name}")
        print(f"   ID: {item.get('ID', 'N/A')}")
        print(f"   Status: {status_display}")
        print(f"   Priority: {priority}")
        print(f"   Role: {role_display}")
        print(f"   Owner: {owner_name}")
        print(f"   Created: {created_on}")
        if deadline:
            print(f"   Deadline: {deadline}")
        print()

        # Print process data if available
        process_data = item.get('ProcessData', {})
        if process_data:
            comment = process_data.get('WorkitemComment', '')
            if comment:
                print(f"   Comment: {comment}")

            routing_choices = process_data.get('WorkitemRoutingChoices', [])
            if routing_choices:
                print(f"   Routing Choices: {', '.join(routing_choices)}")

            variables = process_data.get('Variables', [])
            if variables:
                print(f"   Variables:")
                for var in variables:
                    val = var.get('Value', '')
                    name = var.get('Name', '')
                    print(f"      - {name}: {val}")
        print()


def print_activity_summary(result: dict):
    """Print a summary of activity"""
    activity = result
    if not activity:
        return

    print(f"\n{'='*70}")
    print(f"ACTIVITY")
    print(f"{'='*70}\n")
    print(f"Name: {activity.get('Name', 'N/A')}")
    print(f"ID: {activity.get('ID', 'N/A')}")
    print(f"Instructions: {activity.get('Instructions', 'N/A')}")
    print(f"Deadline: {activity.get('Deadline', 'N/A')}")
    print(f"Status: {'Overdue' if activity.get('IsOverdue') else 'Not overdue'}")
    print(f"Created: {activity.get('CreatedOn', 'N/A')}")

    user_events = activity.get('UserEventList', [])
    if user_events:
        print(f"\nAvailable Events: {', '.join(user_events)}")

    valid_votes = activity.get('ValidVotes', [])
    if valid_votes:
        print(f"Valid Votes: {', '.join(valid_votes)}")

    # Print work items
    work_items = activity.get('WorkItems', [])
    if work_items:
        print(f"\nWork Items ({len(work_items)}):")
        for wi in work_items:
            wi_name = wi.get('TaskName', 'N/A')
            wi_status = wi.get('Status', {})
            wi_status_display = wi_status.get('Display') if isinstance(wi_status, dict) else wi_status
            print(f"  - {wi_name} ({wi_status_display})")

    # Print voting event audits
    voting_audits = activity.get('VotingEventAudits', [])
    if voting_audits:
        print(f"\nVoting Events ({len(voting_audits)}):")
        for ve in voting_audits:
            comment = ve.get('Comment', 'N/A')
            required = ve.get('Required', False)
            signed = ve.get('Signed', False)
            decision = ve.get('Decision', {})
            routing = decision.get('RoutingEvents', []) if decision else []

            print(f"  - Comment: {comment}")
            print(f"    Required: {required}, Signed: {signed}")
            if routing:
                print(f"    Routing: {', '.join(routing)}")


def print_subject_summary(result: dict):
    """Print a summary of subject (business object)"""
    subject = result
    if not subject:
        return

    print(f"\n{'='*70}")
    print(f"SUBJECT (Business Object)")
    print(f"{'='*70}\n")
    print(f"Name: {subject.get('SubjectName', 'N/A')}")
    print(f"ID: {subject.get('ID', 'N/A')}")
    print(f"Type: {subject.get('Type', 'N/A')}")

    state = subject.get('State', {})
    state_display = state.get('Display') if isinstance(state, dict) else state
    print(f"State: {state_display}")
    print(f"Lifecycle Template: {subject.get('LifeCycleTemplateName', 'N/A')}")
    print(f"Created: {subject.get('CreatedOn', 'N/A')}")


def get_activity_for_workitem(base_url, username, password, workitem_id: str,
                                expand_workitems: bool = False,
                                expand_voting: bool = False) -> dict:
    """Get the Activity for a specific WorkItem"""
    url = f"{base_url}Workflow/WorkItems('{workitem_id}')/Activity"

    expansions = []
    if expand_workitems:
        expansions.append("WorkItems")
    if expand_voting:
        expansions.append("VotingEventAudits")

    if expansions:
        url += f"?$expand={','.join(expansions)}"

    session = requests.Session()
    response = session.get(url, auth=(username, password), verify=True)
    response.raise_for_status()

    return response.json()


def get_subject_for_workitem(base_url, username, password, workitem_id: str) -> dict:
    """Get the Subject (business object) for a specific WorkItem"""
    url = f"{base_url}Workflow/WorkItems('{workitem_id}')/Subject"

    session = requests.Session()
    response = session.get(url, auth=(username, password), verify=True)
    response.raise_for_status()

    return response.json()


def main():
    """Command-line interface for querying workflow"""
    parser = argparse.ArgumentParser(description='Query Windchill Workflow')
    parser.add_argument('--url', default='https://pp-2601081959j0.portal.ptc.io/Windchill/servlet/odata/')
    parser.add_argument('--username', default='pat')
    parser.add_argument('--password', default='ptc')
    parser.add_argument('--top', type=int, help='Maximum number of results')
    parser.add_argument('--filter', dest='filter_expr', help='OData filter expression')
    parser.add_argument('--expand', help='Navigation properties to expand (comma-separated)')
    parser.add_argument('--select', help='Properties to select (comma-separated)')
    parser.add_argument('--output', help='Output file path (JSON)')

    subparsers = parser.add_subparsers(dest='command', help='Sub-commands')

    # Work item command (default)
    workitem_parser = subparsers.add_parser('workitem', help='Query work items')
    workitem_parser.add_argument('workitem_id', nargs='?', help='WorkItem ID')

    # Activity command
    activity_parser = subparsers.add_parser('activity', help='Get activity for work item')
    activity_parser.add_argument('--workitem-id', required=True, help='WorkItem ID')
    activity_parser.add_argument('--no-workitems', action='store_true', help='Do not expand work items')
    activity_parser.add_argument('--no-voting', action='store_true', help='Do not expand voting events')

    # Subject command
    subject_parser = subparsers.add_parser('subject', help='Get subject for work item')
    subject_parser.add_argument('--workitem-id', required=True, help='WorkItem ID')

    args = parser.parse_args()

    # Default to workitem query if no command specified
    if not args.command or args.command == 'workitem':
        workitem_id = getattr(args, 'workitem_id', None)
        if workitem_id:
            # Query specific work item
            filter_expr = f"ID eq '{workitem_id}'"
            # Expand by default for single item
            if not args.expand:
                args.expand = "Owner,Activity,Subject,ProcessTemplate"
        else:
            filter_expr = args.filter_expr

        result = query_workflow(
            base_url=args.url,
            username=args.username,
            password=args.password,
            top=args.top,
            filter_expr=filter_expr,
            expand=args.expand,
            select=args.select,
            output_file=args.output
        )

        print_work_items_summary(result)

    elif args.command == 'activity':
        workitem_id = args.workitem_id
        result = get_activity_for_workitem(
            base_url=args.url,
            username=args.username,
            password=args.password,
            workitem_id=workitem_id,
            expand_workitems=not args.no_workitems,
            expand_voting=not args.no_voting
        )

        print_activity_summary(result)

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Results saved to: {args.output}")

    elif args.command == 'subject':
        workitem_id = args.workitem_id
        result = get_subject_for_workitem(
            base_url=args.url,
            username=args.username,
            password=args.password,
            workitem_id=workitem_id
        )

        print_subject_summary(result)

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Results saved to: {args.output}")


if __name__ == '__main__':
    main()
