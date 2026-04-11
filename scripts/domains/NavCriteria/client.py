'''
Windchill PLM NavCriteria Domain Client

Navigation Criteria management domain client providing:
- Navigation Criteria query and management
- Cached Navigation Criteria access
- Configuration Specification support
- Filter management for structure navigation

This domain supports complex types for:
- ConfigSpecs (Standard, Baseline, Change, Effectivity, etc.)
- Filters (Attribute, Path, Spatial, Option, Plant)
- Path filters for occurrence/uses/usage navigation
'''

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class NavCriteriaClient(WindchillBaseClient):
    '''
    Client for Windchill NavCriteria OData domain.
    
    Provides navigation criteria operations including configuration
    specifications and filters for product structure navigation.
    '''
    
    DOMAIN = 'NavCriteria'
    
    # ConfigSpec type constants
    CONFIGSPEC_STANDARD = 'PTC.NavCriteria.ConfigSpec'
    CONFIGSPEC_BASELINE = 'PTC.NavCriteria.BaselineConfigSpec'
    CONFIGSPEC_CHANGE = 'PTC.NavCriteria.ChangeConfigSpec'
    
    # WTPart ConfigSpec types
    WTPART_STANDARD = 'PTC.NavCriteria.WTPartStandardConfigSpec'
    WTPART_BASELINE = 'PTC.NavCriteria.WTPartBaselineConfigSpec'
    WTPART_CHANGE = 'PTC.NavCriteria.WTPartChangeConfigSpec'
    WTPART_ASMATURED = 'PTC.NavCriteria.WTPartAsMaturedConfigSpec'
    WTPART_EFFECTIVITY_DATE = 'PTC.NavCriteria.WTPartEffectivityDateConfigSpec'
    WTPART_EFFECTIVITY_UNIT = 'PTC.NavCriteria.WTPartEffectivityUnitConfigSpec'
    WTPART_PROMOTION_NOTICE = 'PTC.NavCriteria.WTPartPromotionNoticeConfigSpec'
    
    # EPMDocument ConfigSpec types
    EPMDOC_STANDARD = 'PTC.NavCriteria.EPMDocStandardConfigSpec'
    EPMDOC_BASELINE = 'PTC.NavCriteria.EPMDocBaselineConfigSpec'
    EPMDOC_CHANGE = 'PTC.NavCriteria.EPMDocChangeConfigSpec'
    EPMDOC_ASSTORED = 'PTC.NavCriteria.EPMDocAsStoredConfigSpec'
    EPMDOC_PROMOTION_NOTICE = 'PTC.NavCriteria.EPMDocPromotionNoticeConfigSpec'
    
    # Plant ConfigSpec types
    PLANT_STANDARD = 'PTC.NavCriteria.PlantStandardConfigSpec'
    PLANT_EFFECTIVITY_DATE = 'PTC.NavCriteria.PlantEffectivityDateConfigSpec'
    PLANT_EFFECTIVITY_UNIT = 'PTC.NavCriteria.PlantEffectivityUnitConfigSpec'
    
    # Filter type constants
    FILTER_ATTRIBUTE = 'PTC.NavCriteria.AttributeFilter'
    FILTER_PATH = 'PTC.NavCriteria.PathFilter'
    FILTER_SPATIAL = 'PTC.NavCriteria.SpatialFilter'
    FILTER_OPTION = 'PTC.NavCriteria.OptionFilter'
    FILTER_PLANT = 'PTC.NavCriteria.PlantFilter'
    FILTER_PART_TAG = 'PTC.NavCriteria.PartTagFilter'
    
    # Path filter types
    PATH_FILTER_OCCURRENCE = 'PTC.NavCriteria.OccurrencePathFilter'
    PATH_FILTER_USES = 'PTC.NavCriteria.UsesPathFilter'
    PATH_FILTER_USAGE = 'PTC.NavCriteria.UsagePathFilter'
    
    # Spatial filter types
    SPATIAL_FILTER_BOX = 'PTC.NavCriteria.BoxSpatialFilter'
    SPATIAL_FILTER_SPHERE = 'PTC.NavCriteria.SphereSpatialFilter'
    SPATIAL_FILTER_PROXIMITY = 'PTC.NavCriteria.ProximitySpatialFilter'
    
    def __init__(self, **kwargs):
        '''Initialize NavCriteria client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Navigation Criteria Queries
    # =========================================================================
    
    def get_navigation_criteria(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Navigation Criteria records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of NavigationCriteria
        '''
        return self.query_entities('NavigationCriterias', filter_expr=filter_expr, top=top)
    
    def get_navigation_criteria_by_id(self, criteria_id: str) -> dict:
        '''
        Get Navigation Criteria by ID.
        
        Args:
            criteria_id: Criteria ID (OID format)
        
        Returns:
            NavigationCriteria dictionary
        '''
        return self.get_entity('NavigationCriterias', criteria_id, domain=self.DOMAIN)
    
    def get_navigation_criteria_by_name(self, name: str) -> dict:
        '''
        Get Navigation Criteria by name.
        
        Args:
            name: Criteria name
        
        Returns:
            NavigationCriteria dictionary
        '''
        criteria = self.query_entities(
            'NavigationCriterias',
            filter_expr=f"Name eq '{name}'",
            top=1
        )
        return criteria[0] if criteria else None
    
    def get_navigation_criteria_by_type(self, applicable_type: str, top: int = 50) -> List[dict]:
        '''
        Get Navigation Criteria by applicable type.
        
        Args:
            applicable_type: Type the criteria applies to (e.g., 'WTPart', 'EPMDocument')
            top: Maximum results
        
        Returns:
            List of NavigationCriteria for the specified type
        '''
        return self.query_entities(
            'NavigationCriterias',
            filter_expr=f"ApplicableType eq '{applicable_type}'",
            top=top
        )
    
    def get_shared_criteria(self, top: int = 50) -> List[dict]:
        '''
        Get Navigation Criteria shared to all users.
        
        Args:
            top: Maximum results
        
        Returns:
            List of shared NavigationCriteria
        '''
        return self.query_entities(
            'NavigationCriterias',
            filter_expr="SharedToAll eq true",
            top=top
        )
    
    # =========================================================================
    # Cached Navigation Criteria Queries
    # =========================================================================
    
    def get_cached_navigation_criteria(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Cached Navigation Criteria records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of CachedNavigationCriteria
        '''
        return self.query_entities('CachedNavigationCriterias', filter_expr=filter_expr, top=top)
    
    def get_cached_criteria_by_id(self, criteria_id: str) -> dict:
        '''
        Get Cached Navigation Criteria by ID.
        
        Args:
            criteria_id: Criteria ID
        
        Returns:
            CachedNavigationCriteria dictionary
        '''
        return self.get_entity('CachedNavigationCriterias', criteria_id, domain=self.DOMAIN)
    
    def get_cached_criteria_by_name(self, name: str) -> dict:
        '''
        Get Cached Navigation Criteria by name.
        
        Args:
            name: Criteria name
        
        Returns:
            CachedNavigationCriteria dictionary
        '''
        criteria = self.query_entities(
            'CachedNavigationCriterias',
            filter_expr=f"Name eq '{name}'",
            top=1
        )
        return criteria[0] if criteria else None
    
    # =========================================================================
    # ConfigSpec Builder Methods
    # =========================================================================
    
    def build_standard_config_spec(self, view: str = None) -> dict:
        '''
        Build a standard configuration specification.
        
        Args:
            view: Optional view name (e.g., 'Manufacturing', 'Design')
        
        Returns:
            ConfigSpec dictionary
        '''
        spec = {
            '@odata.type': self.WTPART_STANDARD
        }
        if view:
            spec['View'] = view
        return spec
    
    def build_baseline_config_spec(self, baseline_oid: str) -> dict:
        '''
        Build a baseline configuration specification.
        
        Args:
            baseline_oid: Baseline OID
        
        Returns:
            BaselineConfigSpec dictionary
        '''
        return {
            '@odata.type': self.WTPART_BASELINE,
            'BaselineOID': baseline_oid
        }
    
    def build_effectivity_date_config_spec(
        self,
        start_date: str = None,
        end_date: str = None,
        effectivity_type: str = 'WTPart'
    ) -> dict:
        '''
        Build an effectivity date configuration specification.
        
        Args:
            start_date: Start date (ISO 8601 format)
            end_date: End date (ISO 8601 format)
            effectivity_type: Type for effectivity ('WTPart' or 'Plant')
        
        Returns:
            EffectivityDateConfigSpec dictionary
        '''
        if effectivity_type == 'Plant':
            odata_type = self.PLANT_EFFECTIVITY_DATE
        else:
            odata_type = self.WTPART_EFFECTIVITY_DATE
        
        spec = {'@odata.type': odata_type}
        if start_date:
            spec['StartDate'] = start_date
        if end_date:
            spec['EndDate'] = end_date
        return spec
    
    def build_effectivity_unit_config_spec(
        self,
        start_unit: int = None,
        end_unit: int = None,
        effectivity_type: str = 'WTPart'
    ) -> dict:
        '''
        Build an effectivity unit configuration specification.
        
        Args:
            start_unit: Start unit number
            end_unit: End unit number
            effectivity_type: Type for effectivity ('WTPart' or 'Plant')
        
        Returns:
            EffectivityUnitConfigSpec dictionary
        '''
        if effectivity_type == 'Plant':
            odata_type = self.PLANT_EFFECTIVITY_UNIT
        else:
            odata_type = self.WTPART_EFFECTIVITY_UNIT
        
        spec = {'@odata.type': odata_type}
        if start_unit is not None:
            spec['StartUnit'] = start_unit
        if end_unit is not None:
            spec['EndUnit'] = end_unit
        return spec
    
    def build_change_config_spec(self, change_oid: str) -> dict:
        '''
        Build a change configuration specification.
        
        Args:
            change_oid: Change notice OID
        
        Returns:
            ChangeConfigSpec dictionary
        '''
        return {
            '@odata.type': self.WTPART_CHANGE,
            'ChangeOID': change_oid
        }
    
    def build_promotion_notice_config_spec(self, promotion_oid: str) -> dict:
        '''
        Build a promotion notice configuration specification.
        
        Args:
            promotion_oid: Promotion notice OID
        
        Returns:
            PromotionNoticeConfigSpec dictionary
        '''
        return {
            '@odata.type': self.WTPART_PROMOTION_NOTICE,
            'PromotionNoticeOID': promotion_oid
        }
    
    # EPMDocument ConfigSpec builders
    
    def build_epmdoc_standard_config_spec(self, view: str = None) -> dict:
        '''
        Build an EPMDocument standard configuration specification.
        
        Args:
            view: Optional view name
        
        Returns:
            EPMDocStandardConfigSpec dictionary
        '''
        spec = {
            '@odata.type': self.EPMDOC_STANDARD
        }
        if view:
            spec['View'] = view
        return spec
    
    def build_epmdoc_baseline_config_spec(self, baseline_oid: str) -> dict:
        '''
        Build an EPMDocument baseline configuration specification.
        
        Args:
            baseline_oid: Baseline OID
        
        Returns:
            EPMDocBaselineConfigSpec dictionary
        '''
        return {
            '@odata.type': self.EPMDOC_BASELINE,
            'BaselineOID': baseline_oid
        }
    
    def build_epmdoc_as_stored_config_spec(self) -> dict:
        '''
        Build an EPMDocument as-stored configuration specification.
        
        Returns:
            EPMDocAsStoredConfigSpec dictionary
        '''
        return {
            '@odata.type': self.EPMDOC_ASSTORED
        }
    
    # =========================================================================
    # Filter Builder Methods
    # =========================================================================
    
    def build_attribute_filter(
        self,
        attribute: str,
        operator: str,
        value: Any,
        expression: str = None
    ) -> dict:
        '''
        Build an attribute filter.
        
        Args:
            attribute: Attribute name to filter on
            operator: Comparison operator (Equals, NotEquals, Contains, etc.)
            value: Filter value
            expression: Optional filter expression
        
        Returns:
            AttributeFilter dictionary
        '''
        return {
            '@odata.type': self.FILTER_ATTRIBUTE,
            'Attribute': attribute,
            'Operator': operator,
            'Value': value,
            'Expression': expression
        }
    
    def build_path_filter(
        self,
        path: str,
        path_type: str = 'occurrence'
    ) -> dict:
        '''
        Build a path filter.
        
        Args:
            path: Path expression
            path_type: Type of path filter ('occurrence', 'uses', 'usage')
        
        Returns:
            PathFilter dictionary
        '''
        if path_type == 'occurrence':
            odata_type = self.PATH_FILTER_OCCURRENCE
        elif path_type == 'uses':
            odata_type = self.PATH_FILTER_USES
        else:
            odata_type = self.PATH_FILTER_USAGE
        
        return {
            '@odata.type': odata_type,
            'Path': path
        }
    
    def build_box_spatial_filter(
        self,
        min_x: float,
        min_y: float,
        min_z: float,
        max_x: float,
        max_y: float,
        max_z: float
    ) -> dict:
        '''
        Build a box-shaped spatial filter for CAD geometry.
        
        Args:
            min_x, min_y, min_z: Minimum corner coordinates
            max_x, max_y, max_z: Maximum corner coordinates
        
        Returns:
            BoxSpatialFilter dictionary
        '''
        return {
            '@odata.type': self.SPATIAL_FILTER_BOX,
            'MinX': min_x,
            'MinY': min_y,
            'MinZ': min_z,
            'MaxX': max_x,
            'MaxY': max_y,
            'MaxZ': max_z
        }
    
    def build_sphere_spatial_filter(
        self,
        center_x: float,
        center_y: float,
        center_z: float,
        radius: float
    ) -> dict:
        '''
        Build a sphere-shaped spatial filter for CAD geometry.
        
        Args:
            center_x, center_y, center_z: Center point coordinates
            radius: Sphere radius
        
        Returns:
            SphereSpatialFilter dictionary
        '''
        return {
            '@odata.type': self.SPATIAL_FILTER_SPHERE,
            'CenterX': center_x,
            'CenterY': center_y,
            'CenterZ': center_z,
            'Radius': radius
        }
    
    def build_proximity_spatial_filter(
        self,
        target_oid: str,
        distance: float
    ) -> dict:
        '''
        Build a proximity-based spatial filter.
        
        Args:
            target_oid: Target object OID
            distance: Proximity distance
        
        Returns:
            ProximitySpatialFilter dictionary
        '''
        return {
            '@odata.type': self.SPATIAL_FILTER_PROXIMITY,
            'TargetOID': target_oid,
            'Distance': distance
        }
    
    def build_option_filter(
        self,
        option_name: str,
        choices: List[str],
        mode: str = 'Selected'
    ) -> dict:
        '''
        Build an option filter.
        
        Args:
            option_name: Option name
            choices: List of selected choice values
            mode: Filter mode ('Selected', 'Available', etc.)
        
        Returns:
            OptionFilter dictionary
        '''
        return {
            '@odata.type': self.FILTER_OPTION,
            'OptionName': option_name,
            'Choices': [{'Value': c} for c in choices],
            'Mode': mode
        }
    
    def build_plant_filter(self, plant_name: str) -> dict:
        '''
        Build a plant filter.
        
        Args:
            plant_name: Plant name
        
        Returns:
            PlantFilter dictionary
        '''
        return {
            '@odata.type': self.FILTER_PLANT,
            'PlantName': plant_name
        }
    
    # =========================================================================
    # Navigation Criteria Management
    # =========================================================================
    
    def create_navigation_criteria(
        self,
        name: str,
        applicable_type: str,
        config_specs: List[dict] = None,
        filters: List[dict] = None,
        apply_to_top_level: bool = False,
        hide_unresolved: bool = False,
        use_default_for_unresolved: bool = False,
        shared_to_all: bool = False,
        application_name: str = None
    ) -> dict:
        '''
        Create navigation criteria with configuration specifications and filters.
        
        Args:
            name: Criteria name
            applicable_type: Type this criteria applies to (e.g., 'WTPart', 'EPMDocument')
            config_specs: List of ConfigSpec objects
            filters: List of Filter objects
            apply_to_top_level: Apply to top-level objects
            hide_unresolved: Hide unresolved dependents
            use_default_for_unresolved: Use default for unresolved items
            shared_to_all: Share criteria with all users
            application_name: Application name
        
        Returns:
            Created NavigationCriteria
        '''
        payload = {
            'Name': name,
            'ApplicableType': applicable_type,
            'ApplyToTopLevelObject': apply_to_top_level,
            'HideUnresolvedDependents': hide_unresolved,
            'UseDefaultForUnresolved': use_default_for_unresolved,
            'SharedToAll': shared_to_all
        }
        
        if config_specs:
            payload['ConfigSpecs'] = config_specs
        
        if filters:
            payload['Filters'] = filters
        
        if application_name:
            payload['ApplicationName'] = application_name
        
        return self.create_entity('NavigationCriterias', payload, domain=self.DOMAIN)
    
    def update_navigation_criteria(
        self,
        criteria_id: str,
        name: str = None,
        config_specs: List[dict] = None,
        filters: List[dict] = None,
        apply_to_top_level: bool = None,
        hide_unresolved: bool = None,
        use_default_for_unresolved: bool = None,
        shared_to_all: bool = None
    ) -> dict:
        '''
        Update navigation criteria.
        
        Args:
            criteria_id: Criteria ID
            name: New name
            config_specs: Updated ConfigSpecs
            filters: Updated Filters
            apply_to_top_level: Updated apply to top level setting
            hide_unresolved: Updated hide unresolved setting
            use_default_for_unresolved: Updated use default setting
            shared_to_all: Updated shared setting
        
        Returns:
            Updated NavigationCriteria
        '''
        payload = {}
        
        if name is not None:
            payload['Name'] = name
        if config_specs is not None:
            payload['ConfigSpecs'] = config_specs
        if filters is not None:
            payload['Filters'] = filters
        if apply_to_top_level is not None:
            payload['ApplyToTopLevelObject'] = apply_to_top_level
        if hide_unresolved is not None:
            payload['HideUnresolvedDependents'] = hide_unresolved
        if use_default_for_unresolved is not None:
            payload['UseDefaultForUnresolved'] = use_default_for_unresolved
        if shared_to_all is not None:
            payload['SharedToAll'] = shared_to_all
        
        return self.update_entity('NavigationCriterias', criteria_id, payload, domain=self.DOMAIN)
    
    def delete_navigation_criteria(self, criteria_id: str) -> bool:
        '''
        Delete navigation criteria.
        
        Args:
            criteria_id: Criteria ID
        
        Returns:
            True if successful
        '''
        return self.delete_entity('NavigationCriterias', criteria_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Utility Methods
    # =========================================================================
    
    def get_criteria_config_specs(self, criteria_id: str) -> List[dict]:
        '''
        Get configuration specifications from a NavigationCriteria.
        
        Args:
            criteria_id: Criteria ID
        
        Returns:
            List of ConfigSpec objects
        '''
        criteria = self.get_navigation_criteria_by_id(criteria_id)
        return criteria.get('ConfigSpecs', [])
    
    def get_criteria_filters(self, criteria_id: str) -> List[dict]:
        '''
        Get filters from a NavigationCriteria.
        
        Args:
            criteria_id: Criteria ID
        
        Returns:
            List of Filter objects
        '''
        criteria = self.get_navigation_criteria_by_id(criteria_id)
        return criteria.get('Filters', [])
    
    def validate_config_spec(self, config_spec: dict) -> bool:
        '''
        Validate a configuration specification structure.
        
        Args:
            config_spec: ConfigSpec dictionary
        
        Returns:
            True if valid
        '''
        if '@odata.type' not in config_spec:
            return False
        
        # Check required fields based on type
        odata_type = config_spec.get('@odata.type', '')
        
        if 'BaselineConfigSpec' in odata_type:
            return 'BaselineOID' in config_spec or 'Baseline' in config_spec
        elif 'ChangeConfigSpec' in odata_type:
            return 'ChangeOID' in config_spec or 'Change' in config_spec
        elif 'EffectivityDateConfigSpec' in odata_type:
            return True  # Start/End dates optional
        elif 'EffectivityUnitConfigSpec' in odata_type:
            return True  # Start/End units optional
        
        return True


def create_navcriteria_client(config_path: str = None, **kwargs) -> NavCriteriaClient:
    '''
    Factory function to create NavCriteria client.
    
    Args:
        config_path: Path to config.json
        **kwargs: Additional client options
    
    Returns:
        NavCriteriaClient instance
    '''
    if config_path:
        with open(config_path, 'r') as f:
            config = json.load(f)
        kwargs.update(config)
    
    return NavCriteriaClient(**kwargs)
