'''
Windchill PLM PTC Common Domain Client

PTC namespace provides shared entities used across all Windchill OData domains:
- ContentItem, ApplicationData: Attachment/content handling
- UserRef: User references for Creator/Modifier navigation
- DownloadContentAsZip: Cross-domain content download action
'''
# Copyright 2025 Windchill PLM Client Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, BinaryIO
import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class PTCClient(WindchillBaseClient):
    '''
    Client for Windchill PTC Common OData namespace.
    
    Provides access to shared entities and cross-domain operations:
    - Content/attachment management
    - User reference resolution
    - Content download (DownloadContentAsZip action)
    
    Note: PTC is a namespace, not a domain with entity sets.
    Most entities here are abstract base types or complex types.
    '''
    
    DOMAIN = 'PTC'
    
    def __init__(self, **kwargs):
        '''Initialize PTC client.'''
        # PTC doesn't have a standard domain endpoint
        # It's a namespace for shared types
        kwargs.setdefault('domain', None)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Content Download Action
    # =========================================================================
    
    def download_content_as_zip(self, content_infos: List[Dict]) -> bytes:
        '''
        Download multiple content items as a ZIP file.
        
        Uses the PTC.DownloadContentAsZip action to bundle content
        from multiple entities into a single ZIP archive.
        
        Args:
            content_infos: List of content info dicts with keys:
                - ID: Entity OID (e.g., "OR:wt.doc.WTDocument:12345")
                - ContentLocation: Location hint (optional)
                
        Returns:
            ZIP file content as bytes
            
        Example:
            >>> client = PTCClient(config_path='config.json')
            >>> content_infos = [
            ...     {'ID': 'OR:wt.doc.WTDocument:12345'},
            ...     {'ID': 'OR:wt.doc.WTDocument:67890'}
            ... ]
            >>> zip_data = client.download_content_as_zip(content_infos)
            >>> with open('download.zip', 'wb') as f:
            ...     f.write(zip_data)
        '''
        # Get CSRF token
        csrf_token = self.get_csrf_token()
        
        # Build action URL
        url = f"{self.odata_base_url.rstrip('/')}/PTC.DownloadContentAsZip"
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/zip',
            'CSRF_NONCE': csrf_token
        }
        
        payload = {
            'DownloadContentInfos': content_infos
        }
        
        response = self.session.post(
            url,
            headers=headers,
            json=payload,
            timeout=self.timeout
        )
        
        if response.status_code != 200:
            raise ODataError(f"Download failed: {response.status_code} - {response.text}")
        
        return response.content
    
    # =========================================================================
    # Content Info Helpers
    # =========================================================================
    
    def get_content_info_for_entity(self, entity_id: str) -> Dict:
        '''
        Get content info structure for an entity.
        
        Creates a content info dict suitable for DownloadContentAsZip.
        
        Args:
            entity_id: Entity OID (e.g., "OR:wt.doc.WTDocument:12345")
            
        Returns:
            Content info dict
        '''
        return {
            'ID': entity_id
        }
    
    def build_download_request(self, entity_ids: List[str]) -> List[Dict]:
        '''
        Build content info list for multiple entities.
        
        Args:
            entity_ids: List of entity OIDs
            
        Returns:
            List of content info dicts
        '''
        return [self.get_content_info_for_entity(eid) for eid in entity_ids]
    
    # =========================================================================
    # Entity Type Helpers
    # =========================================================================
    
    def get_entity_type_info(self, entity_type: str) -> Dict:
        '''
        Get information about a PTC entity type.
        
        PTC namespace contains these base types:
        - WindchillEntity: Abstract base for all business objects
        - ObjectReferenceable: Base for referenceable objects
        - ContentItem: Base for content/attachment entities
        - ApplicationData: File attachments
        - ExternalStoredData: External content references
        - URLData: URL attachments
        - UserRef: User reference type
        - ContentInfo: Content metadata
        - CacheDescriptor: Cache management
        
        Args:
            entity_type: Entity type name (e.g., 'ApplicationData')
            
        Returns:
            Dict with entity type information
        '''
        entity_types = {
            'WindchillEntity': {
                'name': 'WindchillEntity',
                'type': 'PTC.WindchillEntity',
                'description': 'Abstract base entity type for all Windchill business objects',
                'isAbstract': True,
                'properties': {
                    'ID': {'type': 'Edm.String', 'description': 'Unique identifier (OID)'},
                    'CreatedOn': {'type': 'Edm.DateTimeOffset', 'description': 'Creation timestamp'},
                    'LastModified': {'type': 'Edm.DateTimeOffset', 'description': 'Last modification timestamp'}
                }
            },
            'ObjectReferenceable': {
                'name': 'ObjectReferenceable',
                'type': 'PTC.ObjectReferenceable',
                'description': 'Base type for referenceable objects with Identity',
                'isAbstract': True,
                'properties': {
                    'ID': {'type': 'Edm.String', 'description': 'Unique identifier (OID)'},
                    'Identity': {'type': 'Edm.String', 'description': 'Object identity (read-only)'},
                    'CreatedOn': {'type': 'Edm.DateTimeOffset', 'description': 'Creation timestamp'},
                    'LastModified': {'type': 'Edm.DateTimeOffset', 'description': 'Last modification timestamp'}
                }
            },
            'ContentItem': {
                'name': 'ContentItem',
                'type': 'PTC.ContentItem',
                'description': 'Abstract base for content entities (HasStream=true)',
                'isAbstract': True,
                'properties': {
                    'ID': {'type': 'Edm.String', 'description': 'Content item ID'},
                    'Category': {'type': 'Edm.String', 'description': 'Content category'},
                    'Comments': {'type': 'Edm.String', 'description': 'Content comments'},
                    'CreatedBy': {'type': 'Edm.String', 'description': 'Creator name'},
                    'CreatedOn': {'type': 'Edm.DateTimeOffset', 'description': 'Creation timestamp'},
                    'Description': {'type': 'Edm.String', 'description': 'Content description'},
                    'FormatIcon': {'type': 'PTC.Icon', 'description': 'Format icon'},
                    'LastModified': {'type': 'Edm.DateTimeOffset', 'description': 'Last modification timestamp'},
                    'ModifiedBy': {'type': 'Edm.String', 'description': 'Modifier name'}
                },
                'navigationProperties': {
                    'Creator': {'type': 'PTC.UserRef', 'description': 'Creator user reference'},
                    'Modifier': {'type': 'PTC.UserRef', 'description': 'Modifier user reference'}
                }
            },
            'ApplicationData': {
                'name': 'ApplicationData',
                'type': 'PTC.ApplicationData',
                'baseType': 'PTC.ContentItem',
                'description': 'File attachments uploaded to Windchill',
                'hasStream': True,
                'properties': {
                    'Content': {'type': 'PTC.Hyperlink', 'description': 'Content hyperlink (read-only)'},
                    'FileName': {'type': 'Edm.String', 'description': 'File name'},
                    'FileSize': {'type': 'Edm.Double', 'description': 'File size in bytes'},
                    'Format': {'type': 'Edm.String', 'description': 'File format'},
                    'MimeType': {'type': 'Edm.String', 'description': 'MIME type'},
                    'Role': {'type': 'PTC.EnumType', 'description': 'Content role'}
                },
                'operations': ['READ', 'CREATE', 'UPDATE', 'DELETE']
            },
            'ExternalStoredData': {
                'name': 'ExternalStoredData',
                'type': 'PTC.ExternalStoredData',
                'baseType': 'PTC.ContentItem',
                'description': 'External content references',
                'hasStream': True,
                'properties': {
                    'DisplayName': {'type': 'Edm.String', 'description': 'Display name (required)'},
                    'ExternalLocation': {'type': 'Edm.String', 'description': 'External storage location'}
                }
            },
            'URLData': {
                'name': 'URLData',
                'type': 'PTC.URLData',
                'baseType': 'PTC.ContentItem',
                'description': 'URL attachments',
                'hasStream': True,
                'properties': {
                    'DisplayName': {'type': 'Edm.String', 'description': 'Display name (required)'},
                    'UrlLocation': {'type': 'Edm.String', 'description': 'URL location'}
                }
            },
            'UserRef': {
                'name': 'UserRef',
                'type': 'PTC.UserRef',
                'baseType': 'PTC.WindchillEntity',
                'description': 'User reference for Creator/Modifier navigation',
                'properties': {
                    'DistinguishedName': {'type': 'Edm.String', 'description': 'User distinguished name'},
                    'EMail': {'type': 'Edm.String', 'description': 'Email address'},
                    'FullName': {'type': 'Edm.String', 'description': 'Full display name'},
                    'Identity': {'type': 'Edm.String', 'description': 'User identity'},
                    'LastName': {'type': 'Edm.String', 'description': 'Last name'},
                    'MobilePhoneNumber': {'type': 'Edm.String', 'description': 'Mobile phone'},
                    'Name': {'type': 'Edm.String', 'description': 'Username (login)'},
                    'Status': {'type': 'PTC.EnumType', 'description': 'User status'},
                    'UserDomain': {'type': 'Edm.String', 'description': 'User domain'}
                }
            },
            'ContentInfo': {
                'name': 'ContentInfo',
                'type': 'PTC.ContentInfo',
                'description': 'Content metadata for downloads',
                'properties': {
                    'StreamId': {'type': 'Edm.Int32', 'description': 'Stream ID'},
                    'FileSize': {'type': 'Edm.Int32', 'description': 'File size'},
                    'EncodedInfo': {'type': 'Edm.String', 'description': 'Encoded content info'},
                    'FileName': {'type': 'Edm.String', 'description': 'File name'},
                    'MimeType': {'type': 'Edm.String', 'description': 'MIME type'},
                    'PrimaryContent': {'type': 'Edm.Boolean', 'description': 'Is primary content'},
                    'Category': {'type': 'Edm.String', 'description': 'Content category'},
                    'Role': {'type': 'Edm.String', 'description': 'Content role'}
                }
            },
            'CacheDescriptor': {
                'name': 'CacheDescriptor',
                'type': 'PTC.CacheDescriptor',
                'description': 'Cache management metadata',
                'properties': {
                    'FileNames': {'type': 'Collection(Edm.String)', 'description': 'Cached file names'},
                    'FolderId': {'type': 'Edm.Int64', 'description': 'Folder ID'},
                    'ID': {'type': 'Edm.String', 'description': 'Cache descriptor ID'},
                    'MasterUrl': {'type': 'Edm.String', 'description': 'Master URL'},
                    'ReplicaUrl': {'type': 'Edm.String', 'description': 'Replica URL'},
                    'StreamIds': {'type': 'Collection(Edm.Int64)', 'description': 'Stream IDs'},
                    'VaultId': {'type': 'Edm.Int64', 'description': 'Vault ID'}
                }
            }
        }
        
        return entity_types.get(entity_type, {'error': f'Unknown entity type: {entity_type}'})
    
    def list_entity_types(self) -> List[Dict]:
        '''
        List all entity types in the PTC namespace.
        
        Returns:
            List of entity type info dicts
        '''
        entity_types = [
            'WindchillEntity',
            'ObjectReferenceable', 
            'ContentItem',
            'ApplicationData',
            'ExternalStoredData',
            'URLData',
            'UserRef',
            'ContentInfo',
            'CacheDescriptor'
        ]
        return [self.get_entity_type_info(et) for et in entity_types]
    
    # =========================================================================
    # Complex Type Helpers
    # =========================================================================
    
    def get_complex_type_info(self, type_name: str) -> Dict:
        '''
        Get information about PTC complex types.
        
        Common complex types used across domains:
        - State: Lifecycle state (Value, Display)
        - PersistInfo: Persistence metadata
        - Effectivity: Effectivity configuration
        - VersionInfo: Version control info
        - FolderLocation: Container folder path
        - OrganizationReference: Organization reference
        - ContainerReference: Container reference
        - Icon: Icon representation
        - Hyperlink: URL hyperlink
        
        Args:
            type_name: Complex type name
            
        Returns:
            Dict with complex type information
        '''
        complex_types = {
            'State': {
                'name': 'State',
                'type': 'PTC.State',
                'description': 'Lifecycle state information',
                'properties': {
                    'Value': {'type': 'Edm.String', 'description': 'State enum value (INWORK, RELEASED, etc.)'},
                    'Display': {'type': 'Edm.String', 'description': 'Localized display name'}
                },
                'usage': 'Accessed via State/Value in OData filters'
            },
            'PersistInfo': {
                'name': 'PersistInfo',
                'type': 'PTC.PersistInfo',
                'description': 'Persistence metadata',
                'properties': {
                    'CreateStamp': {'type': 'Edm.DateTimeOffset', 'description': 'Creation timestamp'},
                    'ModifyStamp': {'type': 'Edm.DateTimeOffset', 'description': 'Modification timestamp'},
                    'Classname': {'type': 'Edm.String', 'description': 'Object class name'},
                    'IdA2A2': {'type': 'Edm.Int64', 'description': 'Internal ID'}
                }
            },
            'Effectivity': {
                'name': 'Effectivity',
                'type': 'PTC.Effectivity',
                'description': 'Effectivity configuration',
                'properties': {
                    'ContextId': {'type': 'Edm.String', 'description': 'Effectivity context'},
                    'StartDate': {'type': 'Edm.DateTimeOffset', 'description': 'Start date'},
                    'EndDate': {'type': 'Edm.DateTimeOffset', 'description': 'End date'}
                }
            },
            'VersionInfo': {
                'name': 'VersionInfo',
                'type': 'PTC.VersionInfo',
                'description': 'Version control information',
                'properties': {
                    'Version': {'type': 'Edm.String', 'description': 'Version identifier (A.1, B.2)'},
                    'Iteration': {'type': 'Edm.Int32', 'description': 'Iteration number'},
                    'Series': {'type': 'Edm.String', 'description': 'Version series'}
                }
            },
            'FolderLocation': {
                'name': 'FolderLocation',
                'type': 'PTC.FolderLocation',
                'description': 'Container folder path',
                'properties': {
                    'Path': {'type': 'Edm.String', 'description': 'Full folder path'},
                    'Name': {'type': 'Edm.String', 'description': 'Folder name'}
                }
            },
            'OrganizationReference': {
                'name': 'OrganizationReference',
                'type': 'PTC.OrganizationReference',
                'description': 'Organization reference',
                'properties': {
                    'ID': {'type': 'Edm.String', 'description': 'Organization OID'},
                    'Name': {'type': 'Edm.String', 'description': 'Organization name'}
                }
            },
            'ContainerReference': {
                'name': 'ContainerReference',
                'type': 'PTC.ContainerReference',
                'description': 'Container/context reference',
                'properties': {
                    'ID': {'type': 'Edm.String', 'description': 'Container OID'},
                    'Name': {'type': 'Edm.String', 'description': 'Container name'}
                }
            },
            'Icon': {
                'name': 'Icon',
                'type': 'PTC.Icon',
                'description': 'Icon representation',
                'properties': {
                    'Url': {'type': 'Edm.String', 'description': 'Icon URL'},
                    'Title': {'type': 'Edm.String', 'description': 'Icon title'}
                }
            },
            'Hyperlink': {
                'name': 'Hyperlink',
                'type': 'PTC.Hyperlink',
                'description': 'URL hyperlink',
                'properties': {
                    'Url': {'type': 'Edm.String', 'description': 'Hyperlink URL'},
                    'Title': {'type': 'Edm.String', 'description': 'Link title'}
                }
            }
        }
        
        return complex_types.get(type_name, {'error': f'Unknown complex type: {type_name}'})
    
    def list_complex_types(self) -> List[Dict]:
        '''
        List all complex types in the PTC namespace.
        
        Returns:
            List of complex type info dicts
        '''
        type_names = [
            'State', 'PersistInfo', 'Effectivity', 'VersionInfo',
            'FolderLocation', 'OrganizationReference', 'ContainerReference',
            'Icon', 'Hyperlink'
        ]
        return [self.get_complex_type_info(t) for t in type_names]
    
    # =========================================================================
    # Enum Type Helpers
    # =========================================================================
    
    def get_enum_type_info(self, enum_name: str) -> Dict:
        '''
        Get information about PTC enum types.
        
        Args:
            enum_name: Enum type name
            
        Returns:
            Dict with enum type information
        '''
        enum_types = {
            'AttributeTypeEnum': {
                'name': 'AttributeTypeEnum',
                'type': 'PTC.AttributeTypeEnum',
                'description': 'Attribute type classification',
                'members': {
                    'ModelBased': 'Attribute persisted in database (MBA, Local/Standard)',
                    'InstanceBased': 'Attribute persisted in database (IBA)',
                    'ServerCalculated': 'Calculated on the fly (SCA), not persisted',
                    'NonPersisted': 'Custom attributes with formulas, Alias, NPA',
                    'Unknown': 'Property with no corresponding Windchill attribute'
                }
            }
        }
        
        return enum_types.get(enum_name, {'error': f'Unknown enum type: {enum_name}'})
    
    # =========================================================================
    # OID Helpers
    # =========================================================================
    
    @staticmethod
    def parse_oid(oid: str) -> Dict:
        '''
        Parse a Windchill OID into its components.
        
        OID format: OR:{java.class}:{id}
        
        Args:
            oid: Object identifier string
            
        Returns:
            Dict with 'prefix', 'class', 'id' keys
            
        Example:
            >>> PTCClient.parse_oid('OR:wt.part.WTPart:12345')
            {'prefix': 'OR', 'class': 'wt.part.WTPart', 'id': '12345'}
        '''
        if not oid or not oid.startswith('OR:'):
            return {'error': 'Invalid OID format', 'input': oid}
        
        parts = oid.split(':')
        if len(parts) < 3:
            return {'error': 'Invalid OID format', 'input': oid}
        
        return {
            'prefix': parts[0],
            'class': parts[1],
            'id': parts[2],
            'full_oid': oid
        }
    
    @staticmethod
    def get_domain_for_oid(oid: str) -> str:
        '''
        Determine the Windchill domain for an OID.
        
        Args:
            oid: Object identifier
            
        Returns:
            Domain name (ProdMgmt, DocMgmt, etc.) or 'Unknown'
        '''
        parsed = PTCClient.parse_oid(oid)
        if 'error' in parsed:
            return 'Unknown'
        
        java_class = parsed['class']
        
        # Class to domain mapping
        class_domain_map = {
            'wt.part.WTPart': 'ProdMgmt',
            'wt.part.WTPartMaster': 'ProdMgmt',
            'wt.part.WTPartUsageLink': 'ProdMgmt',
            'wt.doc.WTDocument': 'DocMgmt',
            'wt.doc.WTDocumentMaster': 'DocMgmt',
            'wt.change2.WTChangeOrder2': 'ChangeMgmt',
            'wt.change2.WTChangeRequest2': 'ChangeMgmt',
            'wt.change2.WTChangeActivity2': 'ChangeMgmt',
            'wt.org.WTUser': 'PrincipalMgmt',
            'wt.org.WTGroup': 'PrincipalMgmt',
            'wt.org.WTOrganization': 'PrincipalMgmt',
            'wt.inf.container.WTContainer': 'DataAdmin',
            'wt.folder.CabinetBased': 'DataAdmin',
            'wt.folder.SubFolder': 'DataAdmin',
            'wt.vc.wip.WorkInProgressLink': 'Workflow',
            'wt.workflow.engine.WfProcess': 'Workflow',
            'wt.maturity.PromotionNotice': 'ChangeMgmt',
            'wt.epm.EPMDocument': 'CADDocumentMgmt',
            'wt.mpc.ProcessPlan': 'MfgProcMgmt',
            'wt.mpc.Operation': 'MfgProcMgmt',
            'wt.qms.quality.QualityAction': 'QMS',
            'wt.qms.quality.NonConformance': 'QMS',
            'wt.udi.UDIRecord': 'UDI',
        }
        
        return class_domain_map.get(java_class, 'Unknown')


def create_ptc_client(config_path: str = None, base_url: str = None,
                      username: str = None, password: str = None) -> PTCClient:
    '''
    Factory function to create a PTC client.
    
    Args:
        config_path: Path to config.json
        base_url: Windchill server URL
        username: Username
        password: Password
        
    Returns:
        PTCClient instance
    '''
    return PTCClient(
        config_path=config_path,
        base_url=base_url,
        username=username,
        password=password
    )


def main():
    '''CLI entry point for PTC client.'''
    import argparse
    
    parser = argparse.ArgumentParser(description='Windchill PTC Common Client')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--entity-types', action='store_true', help='List entity types')
    parser.add_argument('--complex-types', action='store_true', help='List complex types')
    parser.add_argument('--entity-type', help='Get specific entity type info')
    parser.add_argument('--complex-type', help='Get specific complex type info')
    parser.add_argument('--parse-oid', help='Parse an OID')
    parser.add_argument('--domain-for-oid', help='Get domain for an OID')
    
    args = parser.parse_args()
    
    client = create_ptc_client(config_path=args.config)
    
    if args.entity_types:
        result = client.list_entity_types()
        print(json.dumps(result, indent=2))
    
    if args.complex_types:
        result = client.list_complex_types()
        print(json.dumps(result, indent=2))
    
    if args.entity_type:
        result = client.get_entity_type_info(args.entity_type)
        print(json.dumps(result, indent=2))
    
    if args.complex_type:
        result = client.get_complex_type_info(args.complex_type)
        print(json.dumps(result, indent=2))
    
    if args.parse_oid:
        result = PTCClient.parse_oid(args.parse_oid)
        print(json.dumps(result, indent=2))
    
    if args.domain_for_oid:
        result = PTCClient.get_domain_for_oid(args.domain_for_oid)
        print(f"Domain: {result}")


if __name__ == '__main__':
    main()
