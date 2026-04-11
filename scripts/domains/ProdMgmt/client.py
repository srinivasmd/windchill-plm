'''
Windchill PLM ProdMgmt Domain Client

Product Management domain client providing:
- Part CRUD operations
- BOM structure queries
- Part lifecycle management (check-in/out, revise, state)
- Multi-level BOM rollup and components report
- Batch operations
'''

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class ProdMgmtClient(WindchillBaseClient):
    '''
    Client for Windchill ProdMgmt OData domain.
    
    Provides product management operations including:
    - Part queries and CRUD
    - BOM structure navigation
    - Part lifecycle management
    - Multi-level BOM operations
    '''
    
    DOMAIN = 'ProdMgmt'
    
    def __init__(self, **kwargs):
        '''Initialize ProdMgmt client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Part Queries
    # =========================================================================
    # Part Queries
    # =========================================================================

    def get_part_by_number(self, number: str, expand: str = None) -> dict:
        '''
        Get part by number.

        Args:
            number: Part number
            expand: Navigation properties to expand

        Returns:
            Part dictionary
        '''
        # NOTE: Windchill OData uses 'Number' (capital N), not 'number'
        parts = self.query_entities(
            'Parts',
            filter_expr=f"Number eq '{number}'",
            expand=expand,
            top=1
        )
        if not parts:
            raise ODataError(404, f"Part with number '{number}' not found")
        return parts[0]
    
    def get_part_by_id(self, part_id: str, expand: str = None) -> dict:
        '''
        Get part by ID.
        
        Args:
            part_id: Part ID (OBID)
            expand: Navigation properties to expand
        
        Returns:
            Part dictionary
        '''
        return self.get_entity('Parts', part_id, domain=self.DOMAIN, expand=expand)
    
    def search_parts(self, search_term: str, top: int = 50) -> List[dict]:
        '''
        Search parts by term.
        
        Args:
            search_term: Search term
            top: Maximum results
        
        Returns:
            List of matching parts
        '''
        return self.search('Parts', search_term, domain=self.DOMAIN, top=top)
    
    def get_part_versions(self, part_id: str) -> List[dict]:
        '''
        Get all versions of a part.
        
        Args:
            part_id: Part ID
        
        Returns:
            List of part versions
        '''
        return self.get_navigation('Parts', part_id, 'Versions', domain=self.DOMAIN)
    
    def get_part_revisions(self, part_id: str) -> List[dict]:
        '''
        Get all revisions of a part.
        
        Args:
            part_id: Part ID
        
        Returns:
            List of part revisions
        '''
        return self.get_navigation('Parts', part_id, 'Revisions', domain=self.DOMAIN)
    
    def get_part_documents(self, part_id: str) -> List[dict]:
        '''
        Get documents associated with a part.
        
        Args:
            part_id: Part ID
        
        Returns:
            List of documents
        '''
        return self.get_navigation('Parts', part_id, 'Documents', domain=self.DOMAIN)
    
    # =========================================================================
    # BOM Structure
    # =========================================================================
    
    def get_bom(self, part_id: str, expand_uses: bool = False) -> List[dict]:
        '''
        Get Bill of Materials for a part.
        
        Args:
            part_id: Part ID
            expand_uses: Expand Uses navigation property
        
        Returns:
            List of BOM lines
        '''
        expand = 'Uses' if expand_uses else None
        return self.get_navigation('Parts', part_id, 'Uses', domain=self.DOMAIN)
    
    def get_part_children(self, part_id: str) -> List[dict]:
        '''
        Get child parts (BOM children).
        
        Args:
            part_id: Parent part ID
        
        Returns:
            List of child parts
        '''
        uses = self.get_bom(part_id)
        children = []
        for use in uses:
            if 'Part' in use:
                children.append(use['Part'])
            else:
                # Fetch the child part
                child_part = self.get_navigation('PartUses', use.get('ID'), 'Part', domain=self.DOMAIN)
                children.append(child_part)
        return children
    
    def get_part_parents(self, part_id: str) -> List[dict]:
        '''
        Get parent parts (where-used).
        
        Args:
            part_id: Part ID
        
        Returns:
            List of parent parts
        '''
        return self.get_where_used(part_id)
    
    def get_part_structure(self, part_id: str, depth: int = None) -> dict:
        '''
        Get complete part structure recursively.
        
        Args:
            part_id: Part ID
            depth: Maximum depth (None for unlimited)
        
        Returns:
            Part structure tree
        '''
        def build_structure(pid: str, current_depth: int) -> dict:
            if depth is not None and current_depth > depth:
                return None
            
            part = self.get_part_by_id(pid)
            uses = self.get_bom(pid)
            
            structure = {
                'Part': part,
                'Uses': []
            }
            
            for use in uses:
                child_id = use.get('PartId') or use.get('Part', {}).get('ID')
                if child_id:
                    child_structure = build_structure(child_id, current_depth + 1)
                    if child_structure:
                        structure['Uses'].append({
                            'Use': use,
                            'Child': child_structure
                        })
            
            return structure
        
        return build_structure(part_id, 0)
    
    def get_where_used(self, part_id: str) -> List[dict]:
        '''
        Get where-used (parent assemblies).
        
        Args:
            part_id: Part ID
        
        Returns:
            List of parent usages
        '''
        return self.get_navigation('Parts', part_id, 'WhereUsed', domain=self.DOMAIN)
    
    # =========================================================================
    # Multi-Level BOM Operations
    # =========================================================================
    
    def get_multi_level_bom_rollup(self, part_id: str,
                                     navigation_criteria: dict = None,
                                     include_bom: bool = True,
                                     rollup_attributes: List[str] = None) -> List[dict]:
        '''
        Get multi-level BOM rollup.
        
        Args:
            part_id: Part ID
            navigation_criteria: Navigation criteria
            include_bom: Include BOM in result
            rollup_attributes: Attributes to roll up
        
        Returns:
            List of BOM rollup items
        '''
        params = {
            'NavigationCriteria': navigation_criteria or {},
            'IncludeBOM': include_bom,
            'RollupAttributes': rollup_attributes or []
        }
        
        return self.invoke_action(
            'GetMultiLevelBOMRollup',
            parameters=params,
            entity_id=part_id,
            entity_type='Part'
        )
    
    def get_multi_level_components_report(self, part_id: str,
                                           navigation_criteria: dict = None,
                                           show_single_level: bool = False) -> List[dict]:
        '''
        Get multi-level components report.
        
        Args:
            part_id: Part ID
            navigation_criteria: Navigation criteria
            show_single_level: Show single-level report only
        
        Returns:
            List of components with quantities
        '''
        return self.invoke_action(
            'GetMultiLevelComponentsReport',
            parameters={
                'NavigationCriteria': navigation_criteria or {},
                'ShowSingleLevelReport': show_single_level
            },
            entity_id=part_id,
            entity_type='Part'
        )
    
    # =========================================================================
    # Part Lifecycle Management
    # =========================================================================
    
    def check_out_part(self, part_id: str) -> dict:
        '''
        Check out a part for editing.
        
        Args:
            part_id: Part ID
        
        Returns:
            Checkout result
        '''
        return self.invoke_action(
            'CheckOut',
            entity_id=part_id,
            entity_type='Part'
        )
    
    def check_in_part(self, part_id: str) -> dict:
        '''
        Check in a part after editing.
        
        Args:
            part_id: Part ID
        
        Returns:
            Checkin result
        '''
        return self.invoke_action(
            'CheckIn',
            entity_id=part_id,
            entity_type='Part'
        )
    
    def undo_check_out_part(self, part_id: str) -> dict:
        '''
        Undo check out of a part.
        
        Args:
            part_id: Part ID
        
        Returns:
            Undo checkout result
        '''
        return self.invoke_action(
            'UndoCheckOut',
            entity_id=part_id,
            entity_type='Part'
        )
    
    def revise_part(self, part_id: str, comment: str = None) -> dict:
        '''
        Revise a part to create a new version.
        
        Args:
            part_id: Part ID
            comment: Revision comment
        
        Returns:
            Revised part
        '''
        params = {}
        if comment:
            params['Comment'] = comment
        
        return self.invoke_action(
            'Revise',
            parameters=params,
            entity_id=part_id,
            entity_type='Part'
        )
    
    def set_part_state(self, part_id: str, state: str, comment: str = None) -> dict:
        '''
        Set lifecycle state of a part.
        
        Args:
            part_id: Part ID
            state: Target state (e.g., 'Released', 'InWork')
            comment: State change comment
        
        Returns:
            State change result
        '''
        params = {'State': state}
        if comment:
            params['Comment'] = comment
        
        return self.invoke_action(
            'SetState',
            parameters=params,
            entity_id=part_id,
            entity_type='Part'
        )
    
    # =========================================================================
    # Batch Operations
    # =========================================================================
    
    def create_parts_batch(self, parts_data: List[dict]) -> List[dict]:
        '''
        Create multiple parts in a batch.
        
        Args:
            parts_data: List of part data dictionaries
        
        Returns:
            List of created parts
        '''
        return self.invoke_action('CreateParts', parameters={'Parts': parts_data})
    
    def update_parts_batch(self, updates: List[dict]) -> List[dict]:
        '''
        Update multiple parts in a batch.
        
        Args:
            updates: List of part updates (each with ID and properties)
        
        Returns:
            List of updated parts
        '''
        return self.invoke_action('UpdateParts', parameters={'Updates': updates})
    
    def delete_parts_batch(self, part_ids: List[str]) -> bool:
        '''
        Delete multiple parts in a batch.
        
        Args:
            part_ids: List of part IDs to delete
        
        Returns:
            True if successful
        '''
        return self.invoke_action('DeleteParts', parameters={'IDs': part_ids})
    
    # =========================================================================
    # Supplier Parts
    # =========================================================================
    
    def set_state_supplier_parts(self, part_id: str, state: str,
                                   comment: str = None) -> dict:
        '''
        Set state for supplier parts.
        
        Args:
            part_id: Supplier part ID
            state: Target state
            comment: State change comment
        
        Returns:
            State change result
        '''
        params = {'State': state}
        if comment:
            params['Comment'] = comment
        
        return self.invoke_action(
            'SetState',
            parameters=params,
            entity_id=part_id,
            entity_type='VendorPart'
        )
    
    # =========================================================================
    # Import/Export Operations
    # =========================================================================
    
    def get_import_mappings(self, bac_delivery_id: str) -> List[dict]:
        '''
        Get import mappings for a BAC delivery.
        
        Args:
            bac_delivery_id: BAC delivery ID
        
        Returns:
            List of import mappings
        '''
        return self.invoke_action(
            'GetImportMappings',
            entity_id=bac_delivery_id,
            entity_type='BACDelivery'
        )
    
    def get_ix_permissions(self, bac_delivery_id: str) -> dict:
        '''
        Get IX permissions for a BAC delivery.
        
        Args:
            bac_delivery_id: BAC delivery ID
        
        Returns:
            IX permissions
        '''
        return self.invoke_action(
            'GetIXPermissions',
            entity_id=bac_delivery_id,
            entity_type='BACDelivery'
        )


def create_prodmgmt_client(config_path: str = None, base_url: str = None,
                            username: str = None, password: str = None) -> ProdMgmtClient:
    '''
    Factory function to create a ProdMgmt client.
    
    Args:
        config_path: Path to config.json
        base_url: Windchill server URL
        username: Username
        password: Password
    
    Returns:
        ProdMgmtClient instance
    '''
    return ProdMgmtClient(
        config_path=config_path,
        base_url=base_url,
        username=username,
        password=password
    )


# =============================================================================
# CLI Entry Point
# =============================================================================

def main():
    '''CLI entry point for ProdMgmt client.'''
    import argparse
    
    parser = argparse.ArgumentParser(description='Windchill ProdMgmt Client')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--part-number', help='Get part by number')
    parser.add_argument('--part-id', help='Get part by ID')
    parser.add_argument('--search', help='Search parts')
    parser.add_argument('--bom', help='Get BOM for part ID')
    parser.add_argument('--check-out', help='Check out part by ID')
    parser.add_argument('--check-in', help='Check in part by ID')
    parser.add_argument('--revise', help='Revise part by ID')
    parser.add_argument('--state', help='Set state for part (requires --part-id)')
    parser.add_argument('--multi-level-bom', help='Get multi-level BOM rollup for part ID')
    parser.add_argument('--components-report', help='Get components report for part ID')
    parser.add_argument('--top', type=int, default=50, help='Max results')
    
    args = parser.parse_args()
    
    client = create_prodmgmt_client(config_path=args.config)
    
    if args.part_number:
        part = client.get_part_by_number(args.part_number)
        print(json.dumps(part, indent=2))
    
    if args.part_id:
        part = client.get_part_by_id(args.part_id)
        print(json.dumps(part, indent=2))
    
    if args.search:
        parts = client.search_parts(args.search, top=args.top)
        print(json.dumps(parts, indent=2))
    
    if args.bom:
        bom = client.get_bom(args.bom)
        print(json.dumps(bom, indent=2))
    
    if args.check_out:
        result = client.check_out_part(args.check_out)
        print(json.dumps(result, indent=2))
    
    if args.check_in:
        result = client.check_in_part(args.check_in)
        print(json.dumps(result, indent=2))
    
    if args.revise:
        result = client.revise_part(args.revise)
        print(json.dumps(result, indent=2))
    
    if args.state and args.part_id:
        result = client.set_part_state(args.part_id, args.state)
        print(json.dumps(result, indent=2))
    
    if args.multi_level_bom:
        result = client.get_multi_level_bom_rollup(args.multi_level_bom)
        print(json.dumps(result, indent=2))
    
    if args.components_report:
        result = client.get_multi_level_components_report(args.components_report)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
