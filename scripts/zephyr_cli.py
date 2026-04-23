#!/usr/bin/env python3
"""
Zephyr CLI - Command-line interface for PTC Windchill PLM.

Quick one-off queries from the terminal, shell scripts, and CI pipelines.

Usage:
 zephyr parts --filter "State/Value eq 'RELEASED'" --top 20
 zephyr bom PART-001
 zephyr search bracket
 zephyr get OR:wt.part.WTPart:12345
 zephyr documents --filter "contains(Name,'spec')" --top 10
 zephyr changes --state RELEASED
 zephyr domains # list all available domains
 zephyr cache stats # show cache statistics
 zephyr cache clear # clear all cached responses

OData Filter Notes:
 - Enum properties (State, Priority, Severity, Status) require /Value:
     State/Value eq 'RELEASED'   (NOT: State eq 'RELEASED')
 - String properties use direct comparison:
     Number eq 'PART-001'
     contains(Name,'bracket')
 - All property names are PascalCase: Number, Name, State (not number, name)
"""
# Copyright 2025 Windchill PLM Client Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# ---------------------------------------------------------------------------
# Path setup - ensure scripts/ is importable
# ---------------------------------------------------------------------------
SCRIPTS_DIR = Path(__file__).parent
SKILL_DIR = SCRIPTS_DIR.parent
CONFIG_PATH = SKILL_DIR / 'config.json'

sys.path.insert(0, str(SCRIPTS_DIR))


# ---------------------------------------------------------------------------
# Domain registry - maps CLI resource names to domain clients + entity sets
# ---------------------------------------------------------------------------
# Format: resource_name -> (domain_module, client_class, entity_set, search_method, get_by_number_method)
DOMAIN_REGISTRY = {
    'parts':              ('domains.ProdMgmt',           'ProdMgmtClient',           'Parts',              'search_parts',              'get_part_by_number'),
    'documents':          ('domains.DocMgmt',            'DocMgmtClient',            'Documents',          'search_documents',          'get_document_by_number'),
 'cad-documents': ('domains.CADDocumentMgmt', 'CADDocumentMgmtClient', 'CADDocuments', 'search_cad_documents', 'get_cad_document_by_number'),
    'dynamic-documents':  ('domains.DynamicDocMgmt',     'DynamicDocMgmtClient',     'DynamicDocuments',   'search_dynamic_documents',  'get_dynamic_document_by_number'),
 'changes': ('domains.ChangeMgmt', 'ChangeMgmtClient', 'ChangeNotices', 'search_change_notices', 'get_change_notice_by_number'),
    'change-requests': ('domains.ChangeMgmt', 'ChangeMgmtClient', 'ChangeRequests', 'search_change_requests', 'get_change_request_by_number'),
 'suppliers': ('domains.SupplierMgmt', 'SupplierMgmtClient', 'Suppliers', 'search_suppliers', 'get_supplier_by_name'),
    'capas':              ('domains.CAPA',               'CAPAClient',               'CAPAs',              'search_capas',              'get_capa_by_number'),
 'qms-capas': ('domains.QMS', 'QMSClient', 'Quality', 'get_capas', None),
    'ncrs':               ('domains.NC',                 'NCClient',                 'Nonconformances',    'get_nonconformances',       'get_nonconformance_by_number'),
    'audits':             ('domains.Audit',              'AuditClient',              'Audits',             'get_audits',                None),
 'baselines': ('domains.BACMgmt', 'BACMgmtClient', 'BACReceivedDeliveries', 'get_baselines', None),
    'containers':         ('domains.DataAdmin',          'DataAdminClient',          'Containers',         'get_containers',            None),
 'folders': ('domains.DataAdmin', 'DataAdminClient', 'ProjectContainers', 'get_folders', None),
    'users':              ('domains.PrincipalMgmt',      'PrincipalMgmtClient',      'Users',              'get_users',                 None),
    'groups':             ('domains.PrincipalMgmt',      'PrincipalMgmtClient',      'Groups',             'get_groups',                None),
 'workflows': ('domains.Workflow', 'WorkflowClient', 'WorkItems', 'get_workflow_processes', None),
    'lifecycle-templates': ('domains.Workflow', 'WorkflowClient', 'WorkItems', 'get_lifecycle_templates', None),
 'registrations': ('domains.RegMstr', 'RegMstrClient', 'RegulatorySubmissions', 'get_registrations', None),
 'udi-records': ('domains.UDI', 'UDIClient', 'UDISuperSets', 'get_udi_records', None),
    'classifications':    ('domains.ClfStructure',        'ClfStructureClient',       'ClfNodes',           'search_clf_nodes',          None),
 'control-documents': ('domains.DocumentControl', 'DocumentControlClient', 'TrainingRecords', 'search_control_documents', 'get_control_document_by_number'),
    'effectivities':      ('domains.EffectivityMgmt',    'EffectivityMgmtClient',    'PartEffectivityContexts', 'get_part_effectivity_contexts', None),
    'projects':           ('domains.ProjMgmt',           'ProjMgmtClient',           'ProjectPlans',       'get_project_plans',         None),
    'variant-specs':      ('domains.ProdPlatformMgmt',   'ProdPlatformMgmtClient',   'VariantSpecifications', 'get_variant_specifications', 'get_variant_specification_by_number'),
    'partlists':          ('domains.PartListMgmt',       'PartListMgmtClient',       'PartLists',          'get_partlists',             'get_partlist_by_number'),
 'service-docs': ('domains.ServiceInfoMgmt', 'ServiceInfoMgmtClient', 'SIMDocuments', 'get_service_documents', 'get_service_document_by_number'),
    'customer-experiences': ('domains.CEM',             'CEMClient',                'CustomerExperiences','get_customer_experiences',  None),
 'process-plans': ('domains.MfgProcMgmt', 'MfgProcMgmtClient', 'ProcessPlans', 'search_process_plans', 'get_process_plan_by_number'),
    'nav-criteria':       ('domains.NavCriteria',        'NavCriteriaClient',        'NavigationCriterias','get_navigation_criteria',   None),
    'factory-operations': ('domains.Factory',            'FactoryClient',            'Documents',          'get_standard_operations',   'get_standard_operation_by_number'),
    'factory-procedures': ('domains.Factory',            'FactoryClient',            'Documents',          'get_standard_procedures',   'get_standard_procedure_by_number'),
}


# ---------------------------------------------------------------------------
# Client cache - reuse across subcommands in same invocation
# ---------------------------------------------------------------------------
_client_cache: Dict[str, Any] = {}


def get_client(domain_module: str, client_class: str, config_path: str = None):
    """Instantiate (or retrieve cached) domain client."""
    cache_key = f"{domain_module}.{client_class}"
    if cache_key not in _client_cache:
        module = importlib.import_module(domain_module)
        cls = getattr(module, client_class)
        kwargs = {}
        if config_path:
            kwargs['config_path'] = config_path
        _client_cache[cache_key] = cls(**kwargs)
    return _client_cache[cache_key]


# ---------------------------------------------------------------------------
# Output formatting - terminal-friendly (no emoji/markdown fluff)
# ---------------------------------------------------------------------------
def format_table(entities: List[Dict], columns: List[str] = None, max_width: int = 120) -> str:
    """Format entities as a plain-text table for terminal output."""
    if not entities:
        return "No results found."

    # Default columns: common important fields, filtered by what's present
    if not columns:
        default_cols = ['Number', 'Name', 'State', 'ID', 'Description', 'Version']
        columns = [c for c in default_cols if any(c in e for e in entities)]
        if not columns:
            # Fallback: use all keys from first entity (skip @odata keys)
            columns = [k for k in entities[0].keys() if not k.startswith('@')][:6]

    # Extract values
    def cell_value(entity: Dict, col: str) -> str:
        val = entity.get(col)
        if val is None:
            return ''
        if isinstance(val, dict):
            # State objects like {'Display': 'RELEASED', 'Value': 'RELEASED'}
            return val.get('Display', val.get('Value', str(val)[:30]))
        return str(val)

    rows = [[cell_value(e, c) for c in columns] for e in entities]

    # Calculate column widths (cap each at 40 chars)
    widths = [min(max(len(str(h)), max((len(r[i]) for r in rows), default=0)), 40)
              for i, h in enumerate(columns)]

    # Build table
    lines = []
    header = ' | '.join(h.ljust(widths[i]) for i, h in enumerate(columns))
    sep = '-+-'.join('-' * w for w in widths)
    lines.append(header)
    lines.append(sep)
    for row in rows:
        line = ' | '.join(row[i][:widths[i]].ljust(widths[i]) for i in range(len(columns)))
        lines.append(line)

    return '\n'.join(lines)


def format_detail(entity: Dict, title: str = None) -> str:
    """Format a single entity as key-value detail view."""
    lines = []
    if title:
        lines.append(f"=== {title} ===")
        lines.append('')

    # Put important fields first
    important = ['ID', 'Number', 'Name', 'State', 'Description', 'Version',
                 'CreatedBy', 'ModifiedBy', 'CreatedOn', 'ModifiedOn']
    # Exclude metadata/OData keys
    exclude_keys = {'@odata.context', '@odata.etag', 'AdditionalMetadata', '__metadata'}
    keys = [k for k in important if k in entity]
    keys += [k for k in entity.keys() if k not in important and k not in exclude_keys and not k.startswith('@')]

    max_key_len = max((len(k) for k in keys), default=10)

    for key in keys:
        val = entity.get(key)
        if val is None:
            val_str = 'N/A'
        elif isinstance(val, dict):
            if 'Display' in val:
                val_str = val['Display']
            elif 'Value' in val:
                val_str = val['Value']
            else:
                val_str = json.dumps(val, indent=2)
                if len(val_str) > 200:
                    val_str = val_str[:200] + '...'
        elif isinstance(val, list):
            val_str = f"[{len(val)} items]"
        else:
            val_str = str(val)

        lines.append(f"  {key.ljust(max_key_len)}  {val_str}")

    return '\n'.join(lines)


def format_bom(bom_items: List[Dict], parent_number: str = None) -> str:
    """Format BOM as an indented list."""
    if not bom_items:
        return f"No BOM items found for {parent_number or 'part'}."

    lines = [f"=== BOM: {parent_number or 'Part'} ===", '']
    lines.append(f"{'Number':<20} {'Name':<35} {'Qty':>5}")
    lines.append('-' * 62)

    for item in bom_items:
        # 'Uses' is the child Part (from $expand=Uses on PartUse navigation)
        # 'Part' may also appear in some response shapes
        part = item.get('Uses', item.get('Part', {}))
        number = part.get('Number', 'N/A') if isinstance(part, dict) else 'N/A'
        name = part.get('Name', 'N/A') if isinstance(part, dict) else 'N/A'
        # Handle enum-type Name (rare but possible)
        if isinstance(name, dict):
            name = name.get('Display', name.get('Value', 'N/A'))
        qty = item.get('Quantity', item.get('Amount', 1))
        if isinstance(name, str) and len(name) > 35:
            name = name[:32] + '...'
        lines.append(f"{number:<20} {name:<35} {str(qty):>5}")

    lines.append('')
    lines.append(f"Total: {len(bom_items)} items")
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------

def cmd_query(args):
    """Handle: zephyr <resource> [--filter ...] [--top N] [--select ...]"""
    resource = args.resource
    if resource not in DOMAIN_REGISTRY:
        print(f"Unknown resource: '{resource}'", file=sys.stderr)
        print(f"Available: {', '.join(sorted(DOMAIN_REGISTRY.keys()))}", file=sys.stderr)
        return 1

    domain_module, client_class, entity_set, _, get_by_num = DOMAIN_REGISTRY[resource]
    client = get_client(domain_module, client_class, args.config)

    # If user passed a positional NUMBER arg, look up by number
    if args.number and get_by_num:
        try:
            entity = getattr(client, get_by_num)(args.number)
            if args.json:
                print(json.dumps(entity, indent=2))
            else:
                print(format_detail(entity, title=f"{resource.rstrip('s')}: {args.number}"))
            return 0
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    elif args.number and not get_by_num:
        # Try filtering by Number
        filter_expr = f"Number eq '{args.number}'"
    else:
        filter_expr = args.filter

    # Auto-correct Windchill enum properties in filter expressions
    # Enum properties require /Value suffix: State eq 'X' -> State/Value eq 'X'
    WINDCHILL_ENUM_PROPERTIES = {
        'State', 'Status', 'Priority', 'Severity', 'AssemblyMode',
        'CheckoutState', 'ChangeStatus', 'GeneralStatus', 'CheckOutStatus',
        'LifecycleState', 'DocTypeName',
    }
    if filter_expr:
        import re as _re
        enum_fix_re = _re.compile(
            r'\b(' + '|'.join(WINDCHILL_ENUM_PROPERTIES) + r')\s+eq\s+\''
        )
        corrected = enum_fix_re.sub(r"\1/Value eq '", filter_expr)
        if corrected != filter_expr:
            print(f"Note: Auto-corrected filter: {filter_expr} -> {corrected}",
                  file=sys.stderr)
            filter_expr = corrected

    # Build query
    kwargs = {}
    if filter_expr:
        kwargs['filter_expr'] = filter_expr
    if args.top:
        kwargs['top'] = args.top
    if args.select:
        kwargs['select'] = args.select
    if args.expand:
        kwargs['expand'] = args.expand
    if args.orderby:
        kwargs['orderby'] = args.orderby

    try:
        results = client.query_entities(entity_set, **kwargs)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        columns = args.select.split(',') if args.select else None
        print(format_table(results, columns=columns))
        print(f"\n({len(results)} results)")

    return 0


def cmd_search(args):
    """Handle: zephyr search <term> [--domain D] [--top N]"""
    term = args.term
    domain = args.domain or 'parts'
    top = args.top or 20

    # Find matching resource in registry
    search_method = None
    client = None

    if domain in DOMAIN_REGISTRY:
        domain_module, client_class, entity_set, search_meth, _ = DOMAIN_REGISTRY[domain]
        if search_meth:
            client = get_client(domain_module, client_class, args.config)
            search_method = search_meth
    else:
        # Try direct domain name (e.g. 'ProdMgmt')
        try:
            mod = importlib.import_module(f'domains.{domain}')
            for attr_name in dir(mod):
                if attr_name.endswith('Client') and attr_name != 'WindchillBaseClient':
                    client = getattr(mod, attr_name)(config_path=args.config)
                    for meth in dir(client):
                        if meth.startswith('search_'):
                            search_method = meth
                            break
                    break
        except (ImportError, AttributeError):
            pass

    if not client or not search_method:
        print(f"No search method found for domain '{domain}'.", file=sys.stderr)
        print(f"Try: zephyr search <term> --domain <resource>", file=sys.stderr)
        print(f"Resources with search: {', '.join(k for k,v in DOMAIN_REGISTRY.items() if v[3])}", file=sys.stderr)
        return 1

    try:
        results = getattr(client, search_method)(term, top=top)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_table(results))
        print(f"\n({len(results)} results for '{term}')")

    return 0


def cmd_bom(args):
    """Handle: zephyr bom <PART-NUMBER> [--depth N]"""
    client = get_client('domains.ProdMgmt', 'ProdMgmtClient', args.config)

    try:
        part = client.get_part_by_number(args.number)
        part_id = part.get('ID')
    except Exception as e:
        print(f"Part '{args.number}' not found: {e}", file=sys.stderr)
        return 1

    try:
        if args.depth and args.depth > 1:
            structure = client.get_part_structure(part_id, depth=args.depth)
            if args.json:
                print(json.dumps(structure, indent=2))
            else:
                _print_bom_tree(structure, indent=0)
            return 0
        else:
            bom = client.get_bom(part_id, expand_uses=True)
            if args.json:
                print(json.dumps(bom, indent=2))
            else:
                print(format_bom(bom, parent_number=args.number))
            return 0
    except Exception as e:
        print(f"Error fetching BOM: {e}", file=sys.stderr)
        return 1


def _print_bom_tree(node: Dict, indent: int = 0):
    """Recursively print BOM tree structure."""
    part = node.get('Uses', node.get('Part', {}))
    number = part.get('Number', 'N/A') if isinstance(part, dict) else 'N/A'
    name = part.get('Name', 'N/A') if isinstance(part, dict) else 'N/A'
    if isinstance(name, dict):
        name = name.get('Display', name.get('Value', 'N/A'))
    prefix = ' ' * indent + ('+-- ' if indent > 0 else '')
    print(f"{prefix}{number}: {name}")
    for use in node.get('Components', node.get('Uses', [])):
        child = use.get('Uses', use.get('Child', use.get('Part', {})))
        if child:
            _print_bom_tree(child, indent + 1)


def cmd_get(args):
    """Handle: zephyr get <ENTITY-ID> [--expand E] [--select S]"""
    entity_id = args.entity_id
    domain = args.domain

    if not domain:
        # Try to extract domain from OID
        if ':' in entity_id:
            parts = entity_id.split(':')
            if len(parts) >= 3:
                type_part = parts[1]
                domain = _oid_to_domain(type_part)
        if not domain:
            domain = 'ProdMgmt'

    # Find matching registry entry for domain
    client = None
    entity_set = None
    for res_name, (mod, cls, eset, _, _) in DOMAIN_REGISTRY.items():
        if mod == f'domains.{domain}' or domain == mod.split('.')[-1]:
            client = get_client(mod, cls, args.config)
            entity_set = eset
            break

    if not client:
        try:
            mod = importlib.import_module(f'domains.{domain}')
            for attr_name in dir(mod):
                if attr_name.endswith('Client') and attr_name != 'WindchillBaseClient':
                    client = getattr(mod, attr_name)(config_path=args.config)
                    break
        except ImportError:
            print(f"Unknown domain: '{domain}'. Use --domain flag.", file=sys.stderr)
            return 1

    if not client:
        print(f"Could not create client for domain '{domain}'.", file=sys.stderr)
        return 1

    try:
        entity = client.get_entity(entity_set or 'Parts', entity_id,
                                   domain=domain,
                                   expand=args.expand,
                                   select=args.select)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(entity, indent=2))
    else:
        print(format_detail(entity, title=entity_set or 'Entity'))

    return 0


def _oid_to_domain(type_part: str) -> Optional[str]:
    """Map OID type prefix to domain name."""
    oid_map = {
        'wt.part.WTPart': 'ProdMgmt',
        'wt.doc.WTDocument': 'DocMgmt',
        'wt.change2.WTChangeOrder2': 'ChangeMgmt',
        'wt.change2.WTChangeRequest2': 'ChangeMgmt',
        'wt.org.WTUser': 'PrincipalMgmt',
        'wt.org.WTGroup': 'PrincipalMgmt',
        'wt.workflow.engine.WfProcess': 'Workflow',
        'com.ptc.windchill.suma.supplier.Manufacturer': 'SupplierMgmt',
        'com.ptc.windchill.suma.supplier.Vendor': 'SupplierMgmt',
        'com.ptc.quality.QualityAction': 'QMS',
        'com.ptc.capa.CAPA': 'CAPA',
    }
    return oid_map.get(type_part)


def cmd_nav(args):
    """Handle: zephyr nav <ENTITY-ID> <PROPERTY> [--expand E]"""
    entity_id = args.entity_id
    nav_prop = args.navigation
    domain = args.domain or 'ProdMgmt'

    client = None
    entity_set = None
    for res_name, (mod, cls, eset, _, _) in DOMAIN_REGISTRY.items():
        if mod == f'domains.{domain}':
            client = get_client(mod, cls, args.config)
            entity_set = eset
            break

    if not client:
        try:
            mod = importlib.import_module(f'domains.{domain}')
            for attr_name in dir(mod):
                if attr_name.endswith('Client') and attr_name != 'WindchillBaseClient':
                    client = getattr(mod, attr_name)(config_path=args.config)
                    break
        except ImportError:
            print(f"Unknown domain: '{domain}'.", file=sys.stderr)
            return 1

    try:
        entity_set_name = entity_set or 'Parts'
        result = client.get_navigation(entity_set_name, entity_id, nav_prop,
                                       domain=domain, expand=args.expand)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, indent=2))
    elif isinstance(result, list):
        print(format_table(result))
        print(f"\n({len(result)} results)")
    else:
        print(format_detail(result, title=nav_prop))

    return 0


def cmd_domains(args):
    """Handle: zephyr domains - list all available domains/resources."""
    print("Available Zephyr CLI resources:\n")
    print(f"{'Resource':<25} {'Domain':<20} {'Entity Set':<25} {'Search':<8}")
    print('-' * 78)
    for name, (mod, cls, eset, search_meth, get_meth) in sorted(DOMAIN_REGISTRY.items()):
        domain = mod.split('.')[-1]
        has_search = 'Yes' if search_meth else '-'
        print(f"{name:<25} {domain:<20} {eset:<25} {has_search:<8}")

    print(f"\nTotal: {len(DOMAIN_REGISTRY)} resources across {len(set(v[0] for v in DOMAIN_REGISTRY.values()))} domains")
    return 0


def cmd_cache(args):
    """Handle: zephyr cache [stats|clear|cleanup]."""
    client = get_client('domains.ProdMgmt', 'ProdMgmtClient', args.config)

    if args.cache_action == 'stats':
        stats = client.cache_stats()
        print("Cache Statistics:")
        for k, v in stats.items():
            print(f"  {k}: {v}")
    elif args.cache_action == 'clear':
        client.cache_clear()
        print("Cache cleared.")
    elif args.cache_action == 'cleanup':
        result = client.cache_cleanup()
        print(f"Cleaned up: {result}")
    else:
        print(f"Unknown cache action: {args.cache_action}", file=sys.stderr)
        return 1
    return 0


def cmd_count(args):
    """Handle: zephyr count <resource> [--filter ...]."""
    resource = args.resource
    if resource not in DOMAIN_REGISTRY:
        print(f"Unknown resource: '{resource}'", file=sys.stderr)
        return 1

    domain_module, client_class, entity_set, _, _ = DOMAIN_REGISTRY[resource]
    client = get_client(domain_module, client_class, args.config)

    try:
        count = client.count_entities(entity_set, filter_expr=args.filter)
        print(f"{count}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    # Common args shared by all subcommands via parents=[common]
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--config', '-c', default=None,
                        help='Path to config.json (default: skill dir/config.json)')
    common.add_argument('--json', '-j', action='store_true',
                        help='Output raw JSON instead of formatted tables')
    common.add_argument('--no-cache', action='store_true',
                        help='Disable response caching for this request')

    parser = argparse.ArgumentParser(
        prog='zephyr',
        description='Zephyr CLI - Query PTC Windchill PLM from the terminal',
        epilog='Examples:\n'
               '  zephyr parts --filter "State eq \'RELEASED\'" --top 20\n'
               '  zephyr parts V0056726\n'
               '  zephyr bom PART-001\n'
               '  zephyr search bracket --domain parts\n'
               '  zephyr get OR:wt.part.WTPart:12345\n'
               '  zephyr nav OR:wt.part.WTPart:12345 Uses\n'
               '  zephyr count parts --filter "State eq \'RELEASED\'"\n',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[common],
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # --- Generic 'query' subcommand ---
    query_parser = subparsers.add_parser(
        'query', help='Query a resource (generic)',
        usage='zephyr query <resource> [options]',
        parents=[common])
    query_parser.add_argument('resource',
                              help=f'Resource name (e.g. parts, documents, changes...)')
    query_parser.add_argument('number', nargs='?', help='Look up by number (optional)')
    query_parser.add_argument('--filter', '-f', help='OData $filter expression')
    query_parser.add_argument('--top', '-t', type=int, help='Max results (default: 50)')
    query_parser.add_argument('--select', '-s', help='Comma-separated properties to select')
    query_parser.add_argument('--expand', '-e', help='Navigation properties to expand')
    query_parser.add_argument('--orderby', '-o', help='Order by expression')
    query_parser.set_defaults(func=cmd_query)

    # --- Resource name aliases as top-level subcommands ---
    # e.g. 'zephyr parts --filter ...' instead of 'zephyr query parts --filter ...'
    for resource_name in DOMAIN_REGISTRY:
        res_parser = subparsers.add_parser(
            resource_name,
            help=f'Query {resource_name}',
            usage=f'zephyr {resource_name} [NUMBER] [options]',
            parents=[common])
        res_parser.add_argument('number', nargs='?', help='Look up by number (optional)')
        res_parser.add_argument('--filter', '-f', help='OData $filter expression')
        res_parser.add_argument('--top', '-t', type=int, help='Max results (default: 50)')
        res_parser.add_argument('--select', '-s', help='Comma-separated properties to select')
        res_parser.add_argument('--expand', '-e', help='Navigation properties to expand')
        res_parser.add_argument('--orderby', '-o', help='Order by expression')
        # Inject the resource name so cmd_query knows which resource
        res_parser.set_defaults(func=cmd_query, resource=resource_name)

    # --- search ---
    search_parser = subparsers.add_parser(
        'search', help='Full-text search across a domain',
        parents=[common])
    search_parser.add_argument('term', help='Search term')
    search_parser.add_argument('--domain', '-d', default='parts',
                               help='Resource/domain to search (default: parts)')
    search_parser.add_argument('--top', '-t', type=int, default=20, help='Max results')
    search_parser.set_defaults(func=cmd_search)

    # --- bom ---
    bom_parser = subparsers.add_parser(
        'bom', help='Get Bill of Materials for a part',
        parents=[common])
    bom_parser.add_argument('number', help='Part number')
    bom_parser.add_argument('--depth', type=int, help='BOM depth (default: 1, single-level)')
    bom_parser.set_defaults(func=cmd_bom)

    # --- get ---
    get_parser = subparsers.add_parser(
        'get', help='Get entity by ID (OID)',
        parents=[common])
    get_parser.add_argument('entity_id', help='Entity ID (e.g. OR:wt.part.WTPart:12345)')
    get_parser.add_argument('--domain', '-d', help='Domain name (auto-detected from OID if possible)')
    get_parser.add_argument('--expand', '-e', help='Navigation properties to expand')
    get_parser.add_argument('--select', '-s', help='Properties to select')
    get_parser.set_defaults(func=cmd_get)

    # --- nav (navigation property) ---
    nav_parser = subparsers.add_parser(
        'nav', help='Get navigation property value',
        parents=[common])
    nav_parser.add_argument('entity_id', help='Entity ID')
    nav_parser.add_argument('navigation', help='Navigation property name (e.g. Uses, Versions, Attachments)')
    nav_parser.add_argument('--domain', '-d', default='ProdMgmt', help='Domain name')
    nav_parser.add_argument('--expand', '-e', help='Expand navigation')
    nav_parser.set_defaults(func=cmd_nav)

    # --- count ---
    count_parser = subparsers.add_parser(
        'count', help='Count entities (no data fetched)',
        parents=[common])
    count_parser.add_argument('resource', help='Resource name')
    count_parser.add_argument('--filter', '-f', help='OData $filter expression')
    count_parser.set_defaults(func=cmd_count)

    # --- domains ---
    domains_parser = subparsers.add_parser(
        'domains', help='List all available domains/resources',
        parents=[common])
    domains_parser.set_defaults(func=cmd_domains)

    # --- cache ---
    cache_parser = subparsers.add_parser(
        'cache', help='Cache management',
        parents=[common])
    cache_parser.add_argument('cache_action', choices=['stats', 'clear', 'cleanup'],
                              help='Cache action: stats, clear, or cleanup')
    cache_parser.set_defaults(func=cmd_cache)

    return parser


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():
    parser = build_parser()
    args = parser.parse_args()

    # Handle no subcommand -> show help
    if not args.command:
        parser.print_help()
        return 0

    # Dispatch to handler
    if hasattr(args, 'func'):
        try:
            return args.func(args)
        except KeyboardInterrupt:
            print("\nInterrupted.", file=sys.stderr)
            return 130
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return 1
    else:
        parser.print_help()
        return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
