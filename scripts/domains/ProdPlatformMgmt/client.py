'''
Windchill PLM ProdPlatformMgmt (Product Platform Management) Domain Client

Product Platform Management domain client providing:
- Variant specification management
- Option and Option Set handling
- Choice management (Design/Sales)
- Expression alias management
- Module variant information links
- Version control (check-in/check-out/revise)
- Lifecycle state management

This domain handles configurable product platforms and variants.
'''

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class ProdPlatformMgmtClient(WindchillBaseClient):
    '''
    Client for Windchill ProdPlatformMgmt OData domain.
    
    Provides product platform management operations including
    variant specifications, options, choices, and expressions.
    '''
    
    DOMAIN = 'ProdPlatformMgmt'
    
    def __init__(self, **kwargs):
        '''Initialize ProdPlatformMgmt client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Variant Specification Queries
    # =========================================================================
    
    def get_variant_specifications(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get VariantSpecification records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of VariantSpecifications
        '''
        return self.query_entities('VariantSpecifications', filter_expr=filter_expr, top=top)
    
    def get_variant_specification_by_id(self, spec_id: str, expand: List[str] = None) -> dict:
        '''
        Get VariantSpecification by ID.
        
        Args:
            spec_id: VariantSpecification ID (OID format)
            expand: Navigation properties to expand
        
        Returns:
            VariantSpecification dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('VariantSpecifications', spec_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_variant_specification_by_number(self, number: str) -> dict:
        '''
        Get VariantSpecification by number.
        
        Args:
            number: Variant specification number
        
        Returns:
            VariantSpecification dictionary
        '''
        specs = self.query_entities(
            'VariantSpecifications',
            filter_expr=f"Number eq '{number}'",
            top=1
        )
        return specs[0] if specs else None
    
    def get_variant_specifications_by_state(self, state: str, top: int = 50) -> List[dict]:
        '''
        Get VariantSpecifications by lifecycle state.
        
        Args:
            state: Lifecycle state value
            top: Maximum results
        
        Returns:
            List of VariantSpecifications in specified state
        '''
        return self.query_entities(
            'VariantSpecifications',
            filter_expr=f"LifecycleState/Value eq '{state}'",
            top=top
        )
    
    def get_variant_specifications_by_name(self, name: str, top: int = 50) -> List[dict]:
        '''
        Get VariantSpecifications by name.
        
        Args:
            name: Specification name
            top: Maximum results
        
        Returns:
            List of matching VariantSpecifications
        '''
        return self.query_entities(
            'VariantSpecifications',
            filter_expr=f"Name eq '{name}'",
            top=top
        )
    
    # =========================================================================
    # Option Set Queries
    # =========================================================================
    
    def get_option_sets(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get OptionSet records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of OptionSets
        '''
        return self.query_entities('OptionSets', filter_expr=filter_expr, top=top)
    
    def get_option_set_by_id(self, option_set_id: str, expand: List[str] = None) -> dict:
        '''
        Get OptionSet by ID.
        
        Args:
            option_set_id: OptionSet ID (OID format)
            expand: Navigation properties to expand
        
        Returns:
            OptionSet dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('OptionSets', option_set_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_option_set_by_number(self, number: str) -> dict:
        '''
        Get OptionSet by number.
        
        Args:
            number: Option set number
        
        Returns:
            OptionSet dictionary
        '''
        option_sets = self.query_entities(
            'OptionSets',
            filter_expr=f"Number eq '{number}'",
            top=1
        )
        return option_sets[0] if option_sets else None
    
    def get_option_sets_by_state(self, state: str, top: int = 50) -> List[dict]:
        '''
        Get OptionSets by lifecycle state.
        
        Args:
            state: Lifecycle state value
            top: Maximum results
        
        Returns:
            List of OptionSets in specified state
        '''
        return self.query_entities(
            'OptionSets',
            filter_expr=f"LifecycleState/Value eq '{state}'",
            top=top
        )
    
    # =========================================================================
    # Option Queries
    # =========================================================================
    
    def get_options(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Option records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Options
        '''
        return self.query_entities('Options', filter_expr=filter_expr, top=top)
    
    def get_option_by_id(self, option_id: str, expand: List[str] = None) -> dict:
        '''
        Get Option by ID.
        
        Args:
            option_id: Option ID (OID format)
            expand: Navigation properties to expand
        
        Returns:
            Option dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('Options', option_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_option_by_number(self, number: str) -> dict:
        '''
        Get Option by number.
        
        Args:
            number: Option number
        
        Returns:
            Option dictionary
        '''
        options = self.query_entities(
            'Options',
            filter_expr=f"Number eq '{number}'",
            top=1
        )
        return options[0] if options else None
    
    # =========================================================================
    # Choice Queries
    # =========================================================================
    
    def get_choices(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Choice records (both DesignChoice and SalesChoice).
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Choices
        '''
        return self.query_entities('Choices', filter_expr=filter_expr, top=top)
    
    def get_choice_by_id(self, choice_id: str) -> dict:
        '''
        Get Choice by ID.
        
        Args:
            choice_id: Choice ID (OID format)
        
        Returns:
            Choice dictionary
        '''
        return self.get_entity('Choices', choice_id, domain=self.DOMAIN)
    
    def get_choice_by_number(self, number: str) -> dict:
        '''
        Get Choice by number.
        
        Args:
            number: Choice number
        
        Returns:
            Choice dictionary
        '''
        choices = self.query_entities(
            'Choices',
            filter_expr=f"Number eq '{number}'",
            top=1
        )
        return choices[0] if choices else None
    
    # =========================================================================
    # Navigation Properties - VariantSpecification
    # =========================================================================
    
    def get_options_for_variant_spec(self, spec_id: str, top: int = 50) -> List[dict]:
        '''
        Get Options for a VariantSpecification.
        
        Args:
            spec_id: VariantSpecification ID
            top: Maximum results
        
        Returns:
            List of Options
        '''
        return self.get_navigation('VariantSpecifications', spec_id, 'Options', domain=self.DOMAIN, top=top)
    
    def get_option_sets_for_variant_spec(self, spec_id: str, top: int = 50) -> List[dict]:
        '''
        Get OptionSets for a VariantSpecification.
        
        Args:
            spec_id: VariantSpecification ID
            top: Maximum results
        
        Returns:
            List of OptionSets
        '''
        return self.get_navigation('VariantSpecifications', spec_id, 'OptionSets', domain=self.DOMAIN, top=top)
    
    def get_module_variant_links(self, spec_id: str, top: int = 50) -> List[dict]:
        '''
        Get ModuleVariantInformationLinks for a VariantSpecification.
        
        Args:
            spec_id: VariantSpecification ID
            top: Maximum results
        
        Returns:
            List of ModuleVariantInformationLinks
        '''
        return self.get_navigation('VariantSpecifications', spec_id, 'ModuleVariantInformationLinks', domain=self.DOMAIN, top=top)
    
    def get_independent_assigned_expressions(self, spec_id: str, top: int = 50) -> List[dict]:
        '''
        Get IndependentAssignedExpressions for a VariantSpecification.
        
        Args:
            spec_id: VariantSpecification ID
            top: Maximum results
        
        Returns:
            List of IndependentAssignedExpressions
        '''
        return self.get_navigation('VariantSpecifications', spec_id, 'IndependentAssignedExpressions', domain=self.DOMAIN, top=top)
    
    def get_variant_spec_creator(self, spec_id: str) -> dict:
        '''Get VariantSpecification creator.'''
        return self.get_navigation('VariantSpecifications', spec_id, 'Creator', domain=self.DOMAIN)
    
    def get_variant_spec_owner(self, spec_id: str) -> dict:
        '''Get VariantSpecification owner.'''
        return self.get_navigation('VariantSpecifications', spec_id, 'Owner', domain=self.DOMAIN)
    
    def get_variant_spec_container(self, spec_id: str) -> dict:
        '''Get VariantSpecification container.'''
        return self.get_navigation('VariantSpecifications', spec_id, 'Container', domain=self.DOMAIN)
    
    # =========================================================================
    # Navigation Properties - OptionSet
    # =========================================================================
    
    def get_options_for_option_set(self, option_set_id: str, top: int = 50) -> List[dict]:
        '''
        Get Options for an OptionSet.
        
        Args:
            option_set_id: OptionSet ID
            top: Maximum results
        
        Returns:
            List of Options
        '''
        return self.get_navigation('OptionSets', option_set_id, 'Options', domain=self.DOMAIN, top=top)
    
    def get_expression_aliases(self, option_set_id: str, top: int = 50) -> List[dict]:
        '''
        Get ExpressionAliases for an OptionSet.
        
        Args:
            option_set_id: OptionSet ID
            top: Maximum results
        
        Returns:
            List of ExpressionAliases
        '''
        return self.get_navigation('OptionSets', option_set_id, 'ExpressionAliases', domain=self.DOMAIN, top=top)
    
    def get_option_set_creator(self, option_set_id: str) -> dict:
        '''Get OptionSet creator.'''
        return self.get_navigation('OptionSets', option_set_id, 'Creator', domain=self.DOMAIN)
    
    def get_option_set_owner(self, option_set_id: str) -> dict:
        '''Get OptionSet owner.'''
        return self.get_navigation('OptionSets', option_set_id, 'Owner', domain=self.DOMAIN)
    
    # =========================================================================
    # Navigation Properties - Option
    # =========================================================================
    
    def get_design_choices_for_option(self, option_id: str, top: int = 50) -> List[dict]:
        '''
        Get DesignChoices for an Option.
        
        Args:
            option_id: Option ID
            top: Maximum results
        
        Returns:
            List of DesignChoices
        '''
        return self.get_navigation('Options', option_id, 'DesignChoices', domain=self.DOMAIN, top=top)
    
    def get_sales_choices_for_option(self, option_id: str, top: int = 50) -> List[dict]:
        '''
        Get SalesChoices for an Option.
        
        Args:
            option_id: Option ID
            top: Maximum results
        
        Returns:
            List of SalesChoices
        '''
        return self.get_navigation('Options', option_id, 'SalesChoices', domain=self.DOMAIN, top=top)
    
    def get_option_group(self, option_id: str) -> dict:
        '''Get OptionGroup for an Option.'''
        return self.get_navigation('Options', option_id, 'OptionGroup', domain=self.DOMAIN)
    
    def get_option_variant_spec(self, option_id: str) -> dict:
        '''Get VariantSpecification for an Option.'''
        return self.get_navigation('Options', option_id, 'VariantSpecification', domain=self.DOMAIN)
    
    # =========================================================================
    # Navigation Properties - Choice
    # =========================================================================
    
    def get_choice_creator(self, choice_id: str) -> dict:
        '''Get Choice creator.'''
        return self.get_navigation('Choices', choice_id, 'Creator', domain=self.DOMAIN)
    
    def get_choice_modifier(self, choice_id: str) -> dict:
        '''Get Choice modifier.'''
        return self.get_navigation('Choices', choice_id, 'Modifier', domain=self.DOMAIN)
    
    def get_choice_owner(self, choice_id: str) -> dict:
        '''Get Choice owner.'''
        return self.get_navigation('Choices', choice_id, 'Owner', domain=self.DOMAIN)
    
    # =========================================================================
    # Variant Specification CRUD Operations
    # =========================================================================
    
    def create_variant_specification(
        self,
        name: str,
        description: str = None,
        number: str = None,
        effectivity: str = None,
        organization: str = None,
        team: str = None
    ) -> dict:
        '''
        Create a new VariantSpecification.
        
        Args:
            name: Specification name
            description: Description
            number: Specification number (auto-generated if not provided)
            effectivity: Effectivity information
            organization: Organization
            team: Team
        
        Returns:
            Created VariantSpecification
        '''
        payload = {'Name': name}
        
        if description:
            payload['Description'] = description
        if number:
            payload['Number'] = number
        if effectivity:
            payload['Effectivity'] = effectivity
        if organization:
            payload['Organization'] = organization
        if team:
            payload['Team'] = team
        
        return self.create_entity('VariantSpecifications', payload, domain=self.DOMAIN)
    
    def update_variant_specification(
        self,
        spec_id: str,
        name: str = None,
        description: str = None,
        effectivity: str = None,
        organization: str = None,
        team: str = None
    ) -> dict:
        '''
        Update a VariantSpecification.
        
        Args:
            spec_id: VariantSpecification ID
            name: Updated name
            description: Updated description
            effectivity: Updated effectivity
            organization: Updated organization
            team: Updated team
        
        Returns:
            Updated VariantSpecification
        '''
        payload = {}
        
        if name is not None:
            payload['Name'] = name
        if description is not None:
            payload['Description'] = description
        if effectivity is not None:
            payload['Effectivity'] = effectivity
        if organization is not None:
            payload['Organization'] = organization
        if team is not None:
            payload['Team'] = team
        
        return self.update_entity('VariantSpecifications', spec_id, payload, domain=self.DOMAIN)
    
    def delete_variant_specification(self, spec_id: str) -> bool:
        '''
        Delete a VariantSpecification.
        
        Args:
            spec_id: VariantSpecification ID
        
        Returns:
            True if successful
        '''
        return self.delete_entity('VariantSpecifications', spec_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Option Set CRUD Operations
    # =========================================================================
    
    def create_option_set(
        self,
        name: str,
        description: str = None,
        number: str = None,
        expression: str = None,
        is_active: bool = True,
        organization: str = None,
        team: str = None
    ) -> dict:
        '''
        Create a new OptionSet.
        
        Args:
            name: Option set name
            description: Description
            number: Option set number (auto-generated if not provided)
            expression: Expression
            is_active: Active status
            organization: Organization
            team: Team
        
        Returns:
            Created OptionSet
        '''
        payload = {
            'Name': name,
            'IsActive': is_active
        }
        
        if description:
            payload['Description'] = description
        if number:
            payload['Number'] = number
        if expression:
            payload['Expression'] = expression
        if organization:
            payload['Organization'] = organization
        if team:
            payload['Team'] = team
        
        return self.create_entity('OptionSets', payload, domain=self.DOMAIN)
    
    def update_option_set(
        self,
        option_set_id: str,
        name: str = None,
        description: str = None,
        expression: str = None,
        is_active: bool = None
    ) -> dict:
        '''
        Update an OptionSet.
        
        Args:
            option_set_id: OptionSet ID
            name: Updated name
            description: Updated description
            expression: Updated expression
            is_active: Updated active status
        
        Returns:
            Updated OptionSet
        '''
        payload = {}
        
        if name is not None:
            payload['Name'] = name
        if description is not None:
            payload['Description'] = description
        if expression is not None:
            payload['Expression'] = expression
        if is_active is not None:
            payload['IsActive'] = is_active
        
        return self.update_entity('OptionSets', option_set_id, payload, domain=self.DOMAIN)
    
    def delete_option_set(self, option_set_id: str) -> bool:
        '''
        Delete an OptionSet.
        
        Args:
            option_set_id: OptionSet ID
        
        Returns:
            True if successful
        '''
        return self.delete_entity('OptionSets', option_set_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Lifecycle State Actions
    # =========================================================================
    
    def set_variant_specification_state(self, spec_id: str, state: str) -> dict:
        '''
        Set lifecycle state for a VariantSpecification.
        
        Args:
            spec_id: VariantSpecification ID
            state: Target state
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/VariantSpecifications('{spec_id}')/PTC.ProdPlatformMgmt.SetState"
        
        payload = {"State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def set_variant_specifications_state_bulk(self, spec_ids: List[str], state: str) -> dict:
        '''
        Set lifecycle state for multiple VariantSpecifications.
        
        Args:
            spec_ids: List of VariantSpecification IDs
            state: Target state
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/VariantSpecifications/PTC.ProdPlatformMgmt.SetStateVariantSpecifications"
        
        payload = {"VariantSpecifications": spec_ids, "State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def set_option_set_state(self, option_set_id: str, state: str) -> dict:
        '''
        Set lifecycle state for an OptionSet.
        
        Args:
            option_set_id: OptionSet ID
            state: Target state
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/OptionSets('{option_set_id}')/PTC.ProdPlatformMgmt.SetState"
        
        payload = {"State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def set_option_sets_state_bulk(self, option_set_ids: List[str], state: str) -> dict:
        '''
        Set lifecycle state for multiple OptionSets.
        
        Args:
            option_set_ids: List of OptionSet IDs
            state: Target state
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/OptionSets/PTC.ProdPlatformMgmt.SetStateOptionSets"
        
        payload = {"OptionSets": option_set_ids, "State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def set_choice_state(self, choice_id: str, state: str) -> dict:
        '''
        Set lifecycle state for a Choice.
        
        Args:
            choice_id: Choice ID
            state: Target state
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/Choices('{choice_id}')/PTC.ProdPlatformMgmt.SetState"
        
        payload = {"State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def set_choices_state_bulk(self, choice_ids: List[str], state: str) -> dict:
        '''
        Set lifecycle state for multiple Choices.
        
        Args:
            choice_ids: List of Choice IDs
            state: Target state
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/Choices/PTC.ProdPlatformMgmt.SetStateChoices"
        
        payload = {"Choices": choice_ids, "State": state}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    # =========================================================================
    # Version Control Actions (Check In/Check Out)
    # =========================================================================
    
    def check_out_variant_specification(
        self,
        spec_id: str,
        check_out_note: str = None,
        description: str = None
    ) -> dict:
        '''
        Check out a VariantSpecification for editing.
        
        Args:
            spec_id: VariantSpecification ID
            check_out_note: Optional check out note
            description: Optional description
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/VariantSpecifications('{spec_id}')/PTC.ProdPlatformMgmt.CheckOut"
        
        payload = {
            "CheckOutNote": check_out_note or "",
            "Description": description or ""
        }
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def check_in_variant_specification(
        self,
        spec_id: str,
        check_in_note: str = None,
        description: str = None,
        keep_checked_out: bool = False,
        version: str = None
    ) -> dict:
        '''
        Check in a VariantSpecification.
        
        Args:
            spec_id: VariantSpecification ID
            check_in_note: Optional check in note
            description: Optional description
            keep_checked_out: Keep checked out after check in
            version: Version
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/VariantSpecifications('{spec_id}')/PTC.ProdPlatformMgmt.CheckIn"
        
        payload = {
            "CheckInNote": check_in_note or "",
            "Description": description or "",
            "KeepCheckedOut": keep_checked_out,
            "Version": version or ""
        }
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def undo_check_out_variant_specification(self, spec_id: str) -> dict:
        '''
        Undo check out for a VariantSpecification.
        
        Args:
            spec_id: VariantSpecification ID
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/VariantSpecifications('{spec_id}')/PTC.ProdPlatformMgmt.UndoCheckOut"
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def revise_variant_specification(
        self,
        spec_id: str,
        description: str = None,
        option: str = None
    ) -> dict:
        '''
        Revise a VariantSpecification.
        
        Args:
            spec_id: VariantSpecification ID
            description: Optional description
            option: Revision option
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/VariantSpecifications('{spec_id}')/PTC.ProdPlatformMgmt.Revise"
        
        payload = {
            "Description": description or "",
            "Option": option or ""
        }
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def revise_variant_specifications_bulk(self, spec_ids: List[str]) -> dict:
        '''
        Revise multiple VariantSpecifications.
        
        Args:
            spec_ids: List of VariantSpecification IDs
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/VariantSpecifications/PTC.ProdPlatformMgmt.ReviseVariantSpecifications"
        
        payload = {"VariantSpecifications": spec_ids}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def revise_option_set(
        self,
        option_set_id: str,
        description: str = None,
        option: str = None
    ) -> dict:
        '''
        Revise an OptionSet.
        
        Args:
            option_set_id: OptionSet ID
            description: Optional description
            option: Revision option
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/OptionSets('{option_set_id}')/PTC.ProdPlatformMgmt.Revise"
        
        payload = {
            "Description": description or "",
            "Option": option or ""
        }
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def revise_option_sets_bulk(self, option_set_ids: List[str]) -> dict:
        '''
        Revise multiple OptionSets.
        
        Args:
            option_set_ids: List of OptionSet IDs
        
        Returns:
            Action result
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/OptionSets/PTC.ProdPlatformMgmt.ReviseOptionSets"
        
        payload = {"OptionSets": option_set_ids}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    # =========================================================================
    # Expression Management
    # =========================================================================
    
    def get_assigned_expressions_for_entity(self, entity_id: str) -> List[dict]:
        '''
        Get assigned expressions for an entity.
        
        Args:
            entity_id: Entity ID
        
        Returns:
            List of assigned expressions
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/VariantSpecifications/PTC.ProdPlatformMgmt.GetAssignedExpressions"
        
        payload = {"EntityID": entity_id}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json().get('value', []) if response.content else []
    
    def get_assigned_option_sets_for_entity(self, entity_id: str) -> List[dict]:
        '''
        Get assigned option sets for an entity.
        
        Args:
            entity_id: Entity ID
        
        Returns:
            List of assigned option sets
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/VariantSpecifications/PTC.ProdPlatformMgmt.GetAssignedOptionSets"
        
        payload = {"EntityID": entity_id}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json().get('value', []) if response.content else []
    
    def get_variant_specs_linked_from_mvil(self, mvil_id: str) -> List[dict]:
        '''
        Get VariantSpecifications linked from a ModuleVariantInformationLink.
        
        Args:
            mvil_id: ModuleVariantInformationLink ID
        
        Returns:
            List of VariantSpecifications
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/VariantSpecifications/PTC.ProdPlatformMgmt.GetVariantSpecificationsLinkedFromMVIL"
        
        payload = {"MVILID": mvil_id}
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json().get('value', []) if response.content else []


def create_prod_platform_mgmt_client(config_path: str = None, **kwargs) -> ProdPlatformMgmtClient:
    '''
    Factory function to create ProdPlatformMgmt client.
    
    Args:
        config_path: Path to config.json
        **kwargs: Additional client options
    
    Returns:
        ProdPlatformMgmtClient instance
    '''
    if config_path:
        with open(config_path, 'r') as f:
            config = json.load(f)
        kwargs.update(config)
    
    return ProdPlatformMgmtClient(**kwargs)
