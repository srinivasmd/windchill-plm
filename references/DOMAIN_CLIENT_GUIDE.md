# Creating Domain Clients from OData Metadata

This guide documents the process for creating new domain clients from Windchill OData metadata XML files.

## Overview

When a new Windchill OData domain metadata file is available, follow this process to create:
1. Reference documentation (entities, navigations, actions)
2. Domain client scripts
3. Update SKILL.md

## Prerequisites

- OData metadata XML file (e.g., `DomainName_Metadata.xml`)
- Access to the Zephyr skill directory structure

## Step-by-Step Process

### 1. Parse the Metadata XML

Use this Python function to extract entities, actions, entity sets, and navigation properties:

```python
import xml.etree.ElementTree as ET

def parse_metadata_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    ns = {
        'edmx': 'http://docs.oasis-open.org/odata/ns/edmx',
        'edm': 'http://docs.oasis-open.org/odata/ns/edm'
    }
    
    entities = []
    actions = []
    entity_sets = []
    complex_types = []
    
    for schema in root.findall('.//edm:Schema', ns):
        namespace = schema.get('Namespace', '')
        
        # Parse EntityTypes
        for entity_type in schema.findall('edm:EntityType', ns):
            entity_name = entity_type.get('Name')
            base_type = entity_type.get('BaseType', '')
            
            # Get properties
            properties = []
            for prop in entity_type.findall('edm:Property', ns):
                prop_info = {
                    'name': prop.get('Name'),
                    'type': prop.get('Type'),
                    'nullable': prop.get('Nullable', 'true') == 'true',
                    'annotations': [ann.get('Term') for ann in prop.findall('edm:Annotation', ns)]
                }
                properties.append(prop_info)
            
            # Get navigation properties
            nav_props = []
            for nav_prop in entity_type.findall('edm:NavigationProperty', ns):
                nav_info = {
                    'name': nav_prop.get('Name'),
                    'type': nav_prop.get('Type'),
                    'partner': nav_prop.get('Partner', ''),
                    'contains_target': nav_prop.get('ContainsTarget', 'false') == 'true'
                }
                nav_props.append(nav_info)
            
            entities.append({
                'namespace': namespace,
                'name': entity_name,
                'base_type': base_type,
                'properties': properties,
                'navigation_properties': nav_props
            })
        
        # Parse Actions
        for action in schema.findall('edm:Action', ns):
            action_name = action.get('Name')
            is_bound = action.get('IsBound', 'false') == 'true'
            parameters = [{'name': p.get('Name'), 'type': p.get('Type')} 
                         for p in action.findall('edm:Parameter', ns)]
            ret_elem = action.find('edm:ReturnType', ns)
            return_type = ret_elem.get('Type') if ret_elem is not None else None
            
            actions.append({
                'namespace': namespace,
                'name': action_name,
                'is_bound': is_bound,
                'parameters': parameters,
                'return_type': return_type
            })
        
        # Parse EntitySets
        for entity_set in schema.findall('.//edm:EntitySet', ns):
            entity_sets.append({
                'name': entity_set.get('Name'),
                'entity_type': entity_set.get('EntityType', '')
            })
    
    return {'entities': entities, 'actions': actions, 'entity_sets': entity_sets}
```

### 2. Create Reference Files Directory

```bash
mkdir -p references/{DomainName}
```

### 3. Generate Reference Files

Generate these files for each domain:

#### a. `{DomainName}_Entities.json`
Machine-readable entity definitions for programmatic access.

```python
entities_json = {
    'domain': domain_name,
    'namespace': 'PTC.DomainName',
    'entities': {entity['name']: {...} for entity in parsed_entities},
    'entity_sets': parsed_entity_sets,
    'actions': parsed_actions
}
```

#### b. `{DomainName}_Navigations.md`
Navigation properties reference for each entity type.

```markdown
# DomainName Navigation Properties

| Entity | Navigation Property | Type | Partner | Contains Target |
|--------|---------------------|------|---------|-----------------|
| Entity1 | Nav1 | TargetEntity | PartnerNav | Yes/No |
```

#### c. `{DomainName}_Actions.md`
OData actions reference with usage examples.

```markdown
# DomainName Actions

## Unbound Actions
Actions callable directly on entity set.

## Bound Actions
Actions that require an entity instance.

### ActionName
Description of action.

**Parameters:**
| Parameter | Type | Nullable | Description |

**Example:**
```http
POST /DomainName/EntitySet('{id}')/PTC.DomainName.ActionName
```
```

#### d. `{DomainName}_REFERENCE.md`
Comprehensive usage guide combining entity info, key properties, and examples.

#### e. Copy Metadata XML
Place the original metadata XML in the reference folder.

### 4. Create Domain Client Scripts

#### Directory Structure
```
scripts/domains/{DomainName}/
├── __init__.py
└── client.py
```

#### `__init__.py` Template
```python
'''
Windchill PLM {DomainName} Domain Client
'''

from .client import {DomainName}Client, create_{domain_name}_client

__all__ = ['{DomainName}Client', 'create_{domain_name}_client']
```

#### `client.py` Template
```python
'''
Windchill PLM {DomainName} Domain Client
'''

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class {DomainName}Client(WindchillBaseClient):
    '''
    Client for Windchill {DomainName} OData domain.
    '''
    
    DOMAIN = '{DomainName}'
    
    def __init__(self, **kwargs):
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # Entity Queries
    def get_{entity_lower}s(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        return self.query_entities('{EntitySet}', filter_expr=filter_expr, top=top)
    
    def get_{entity_lower}_by_id(self, entity_id: str, expand: List[str] = None) -> dict:
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('{EntitySet}', entity_id, domain=self.DOMAIN, expand=expand_str)
    
    # Navigation Properties
    def get_{entity_lower}_{nav}(self, entity_id: str) -> dict:
        return self.get_navigation('{EntitySet}', entity_id, '{NavProperty}', domain=self.DOMAIN)
    
    # Actions (if any)
    def set_{entity_lower}_state(self, entity_id: str, state: str) -> dict:
        self._ensure_csrf_token()
        action_url = f"{self._get_base_url()}/{EntitySet}('{entity_id}')/PTC.{DomainName}.SetState"
        payload = {"State": state}
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json() if response.content else {'success': True}


def create_{domain_name}_client(config_path: str = None, **kwargs) -> {DomainName}Client:
    if config_path:
        with open(config_path, 'r') as f:
            config = json.load(f)
        kwargs.update(config)
    return {DomainName}Client(**kwargs)
```

### 5. Update SKILL.md

Add to the Domain Clients table:
```markdown
| {DomainName} | `{DomainName}Client` | Purpose description |
```

Add to Common Patterns section with usage example.

Add to Reference Documentation table:
```markdown
| {DomainName} | `references/{DomainName}/{DomainName}_REFERENCE.md` | Key entities |
```

Add navigation properties to Key Navigation Properties table.

### 6. Verification

Run verification to ensure all files are in place:
```python
# Check reference files
for f in ['_REFERENCE.md', '_Entities.json', '_Navigations.md', '_Actions.md', '_Metadata.xml']:
    assert os.path.exists(f'references/{DomainName}/{DomainName}{f}')

# Check scripts
assert os.path.exists(f'scripts/domains/{DomainName}/__init__.py')
assert os.path.exists(f'scripts/domains/{DomainName}/client.py')
```

## Key Patterns

### Standard Methods
Every domain client should include:
- `get_{entities}()` - Query with optional filter
- `get_{entity}_by_id()` - Get by OID
- `get_{entity}_by_number()` - Get by business identifier
- `get_{entity}_{navigation}()` - Navigation property accessors
- `set_{entity}_state()` - Lifecycle state change (if applicable)

### Entity Set Naming
Entity sets typically follow pattern: `{Entity}s` (plural)
- Parts, Documents, ChangeNotices, CAPAs
- Exception: Some use singular naming

### Navigation Property Naming
Common navigation properties:
- `Creator`, `Modifier` - User references
- `Folder`, `Container` - Location
- `Attachments` - File attachments
- `Versions`, `Revisions` - Version history
- `Parent`, `Children` - Hierarchical relationships

### Action Naming
- Bound actions: Called on entity instance (`/EntitySet('{id}')/Namespace.Action`)
- Unbound actions: Called on entity set (`/EntitySet/Namespace.Action`)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Empty entity sets | Check metadata XML namespace and EntityContainer path |
| Missing navigation | Some nav properties may be on base type (check inheritance) |
| Action 404 | Verify action namespace matches domain, check if bound/unbound |
| Metadata parse error | Check XML namespace URIs match expected OData namespaces |

## Example Domains

Refer to existing implementations:
- **CAPA**: Complex domain with nested entities (CAPA -> Plan -> Actions)
- **ClfStructure**: Hierarchical domain with parent/children navigation
- **DocumentControl**: Two-entity domain with training records relationship
- **NC**: Nonconformance domain with 4 entities, 7 actions, and containment navigation
- **NavCriteria**: Complex types (41) for configuration specifications and filters

## Full Implementation Script

Use this script to generate all files from metadata XML:

```python
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime

def generate_domain_from_metadata(domain_name: str, xml_path: str, output_refs: str, output_scripts: str):
    '''
    Generate all domain files from OData metadata XML.
    
    Args:
        domain_name: Domain name (e.g., 'NC', 'NavCriteria')
        xml_path: Path to DomainName_Metadata.xml
        output_refs: Path to references directory
        output_scripts: Path to scripts/domains directory
    '''
    # Parse XML
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    ns = {
        'edmx': 'http://docs.oasis-open.org/odata/ns/edmx',
        'edm': 'http://docs.oasis-open.org/odata/ns/edm'
    }
    
    entities = []
    actions = []
    entity_sets = []
    complex_types = []
    
    for schema in root.findall('.//edm:Schema', ns):
        namespace = schema.get('Namespace', '')
        
        # Entity Types
        for entity_type in schema.findall('edm:EntityType', ns):
            entity_name = entity_type.get('Name')
            key_props = [k.get('Name') for k in entity_type.findall('edm:Key/edm:PropertyRef', ns)]
            
            properties = []
            for prop in entity_type.findall('edm:Property', ns):
                properties.append({
                    'name': prop.get('Name'),
                    'type': prop.get('Type'),
                    'nullable': prop.get('Nullable', 'true') == 'true',
                    'annotations': [a.get('Term') for a in prop.findall('edm:Annotation', ns)]
                })
            
            nav_props = []
            for nav in entity_type.findall('edm:NavigationProperty', ns):
                nav_props.append({
                    'name': nav.get('Name'),
                    'type': nav.get('Type'),
                    'contains_target': nav.get('ContainsTarget', 'false') == 'true'
                })
            
            entities.append({
                'namespace': namespace,
                'name': entity_name,
                'key': key_props,
                'properties': properties,
                'navigation_properties': nav_props
            })
        
        # Actions
        for action in schema.findall('edm:Action', ns):
            actions.append({
                'namespace': namespace,
                'name': action.get('Name'),
                'is_bound': action.get('IsBound', 'false') == 'true',
                'parameters': [{'name': p.get('Name'), 'type': p.get('Type')} 
                              for p in action.findall('edm:Parameter', ns)]
            })
        
        # Entity Sets
        for es in schema.findall('.//edm:EntitySet', ns):
            entity_sets.append({'name': es.get('Name'), 'entity_type': es.get('EntityType', '')})
        
        # Complex Types
        for ct in schema.findall('edm:ComplexType', ns):
            complex_types.append({
                'name': ct.get('Name'),
                'properties': [{'name': p.get('Name'), 'type': p.get('Type')} 
                              for p in ct.findall('edm:Property', ns)]
            })
    
    # Generate Entities.json
    entities_json = {
        'domain': domain_name,
        'namespace': namespace,
        'generated': datetime.now().isoformat(),
        'entities': {e['name']: {
            'key': e['key'],
            'properties': {p['name']: {'type': p['type'], 'nullable': p['nullable']} 
                          for p in e['properties']},
            'navigation_properties': {n['name']: {'type': n['type']} 
                                     for n in e['navigation_properties']}
        } for e in entities},
        'entity_sets': entity_sets,
        'actions': actions,
        'complex_types': complex_types
    }
    
    ref_dir = os.path.join(output_refs, domain_name)
    os.makedirs(ref_dir, exist_ok=True)
    
    with open(os.path.join(ref_dir, f'{domain_name}_Entities.json'), 'w') as f:
        json.dump(entities_json, f, indent=2)
    
    print(f'Generated: {domain_name}_Entities.json')
    return entities, actions, entity_sets, complex_types
```

## Key Learnings from NC Domain Implementation

### Containment Navigation
When `ContainsTarget="true"`, entities are contained within parent:
- Create via: `POST /Nonconformances('{nc_id}')/AffectedObjects`
- Query via: `GET /Nonconformances('{nc_id}')/AffectedObjects`

### Multi-Stage File Upload
Windchill uses 3-stage upload for attachments:
1. **Stage 1**: Initialize upload with ContentID and file metadata
2. **Stage 2**: (handled by Windchill) Upload binary content
3. **Stage 3**: Complete upload with confirmation

### Action Types
- **Bound actions**: Require entity context (`/EntitySet('{id}')/Namespace.Action`)
- **Unbound actions**: Called on entity set (`/EntitySet/Namespace.Action`)
- Always require CSRF token: `headers['CSRF_NONCE'] = csrf_token`

### Navigation Property Methods
The `get_navigation()` method signature is:
```python
get_navigation(entity_set: str, entity_id: str, navigation: str, domain: str = None, 
               select: str = None, expand: str = None) -> Union[dict, List[dict]]
```

**IMPORTANT:** `get_navigation()` does NOT accept a `top` parameter. If you need to limit results from a navigation property that returns a collection, use `query_entities()` with `$filter` on the parent ID instead:
```python
# WRONG - will raise TypeError
items = client.get_navigation('PartLists', partlist_id, 'Uses', domain=self.DOMAIN, top=10)

# CORRECT - navigation properties return all related entities
items = client.get_navigation('PartLists', partlist_id, 'Uses', domain=self.DOMAIN)

# Alternative - use query_entities with filter if pagination needed
items = client.query_entities('PartListItems', filter_expr=f"UsedBy/ID eq '{partlist_id}'", top=10)
```
