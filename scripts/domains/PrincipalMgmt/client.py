'''
Windchill PLM PrincipalMgmt Domain Client

Principal Management domain client providing:
- User queries
- Group management
- Role assignments
- Organization queries
'''

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class PrincipalMgmtClient(WindchillBaseClient):
    '''
    Client for Windchill PrincipalMgmt OData domain.
    
    Provides principal management operations.
    '''
    
    DOMAIN = 'PrincipalMgmt'
    
    def __init__(self, **kwargs):
        '''Initialize PrincipalMgmt client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # User Queries
    # =========================================================================
    
    def get_users(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get users.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of users
        '''
        return self.query_entities('Users', filter_expr=filter_expr, top=top)
    
    def get_user_by_id(self, user_id: str) -> dict:
        '''
        Get user by ID.
        
        Args:
            user_id: User ID
        
        Returns:
            User dictionary
        '''
        return self.get_entity('Users', user_id, domain=self.DOMAIN)
    
    def get_user_by_name(self, name: str) -> dict:
        '''
        Get user by name.
        
        Args:
            name: User name
        
        Returns:
            User dictionary
        '''
        users = self.query_entities(
            'Users',
            filter_expr=f"name eq '{name}'",
            top=1
        )
        if not users:
            raise ODataError(404, f"User with name '{name}' not found")
        return users[0]
    
    def get_user_by_email(self, email: str) -> dict:
        '''
        Get user by email.
        
        Args:
            email: User email
        
        Returns:
            User dictionary
        '''
        users = self.query_entities(
            'Users',
            filter_expr=f"email eq '{email}'",
            top=1
        )
        if not users:
            raise ODataError(404, f"User with email '{email}' not found")
        return users[0]
    
    # =========================================================================
    # Group Queries
    # =========================================================================
    
    def get_groups(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get groups.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of groups
        '''
        return self.query_entities('Groups', filter_expr=filter_expr, top=top)
    
    def get_group_by_id(self, group_id: str) -> dict:
        '''
        Get group by ID.
        
        Args:
            group_id: Group ID
        
        Returns:
            Group dictionary
        '''
        return self.get_entity('Groups', group_id, domain=self.DOMAIN)
    
    def get_group_by_name(self, name: str) -> dict:
        '''
        Get group by name.
        
        Args:
            name: Group name
        
        Returns:
            Group dictionary
        '''
        groups = self.query_entities(
            'Groups',
            filter_expr=f"name eq '{name}'",
            top=1
        )
        if not groups:
            raise ODataError(404, f"Group with name '{name}' not found")
        return groups[0]
    
    # =========================================================================
    # Role Queries
    # =========================================================================
    
    def get_roles(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get roles.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of roles
        '''
        return self.query_entities('Roles', filter_expr=filter_expr, top=top)
    
    def get_role_by_id(self, role_id: str) -> dict:
        '''
        Get role by ID.
        
        Args:
            role_id: Role ID
        
        Returns:
            Role dictionary
        '''
        return self.get_entity('Roles', role_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Organization Queries
    # =========================================================================
    
    def get_organizations(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get organizations.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of organizations
        '''
        return self.query_entities('Organizations', filter_expr=filter_expr, top=top)
    
    def get_organization_by_id(self, org_id: str) -> dict:
        '''
        Get organization by ID.
        
        Args:
            org_id: Organization ID
        
        Returns:
            Organization dictionary
        '''
        return self.get_entity('Organizations', org_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Navigation Properties
    # =========================================================================
    
    def get_user_groups(self, user_id: str) -> List[dict]:
        '''
        Get groups for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            List of groups
        '''
        return self.get_navigation('Users', user_id, 'Groups', domain=self.DOMAIN)
    
    def get_user_roles(self, user_id: str) -> List[dict]:
        '''
        Get roles for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            List of roles
        '''
        return self.get_navigation('Users', user_id, 'Roles', domain=self.DOMAIN)
    
    def get_group_members(self, group_id: str) -> List[dict]:
        '''
        Get members of a group.
        
        Args:
            group_id: Group ID
        
        Returns:
            List of users
        '''
        return self.get_navigation('Groups', group_id, 'Members', domain=self.DOMAIN)


def create_principalmgmt_client(config_path: str = None, base_url: str = None,
                                 username: str = None, password: str = None) -> PrincipalMgmtClient:
    '''
    Factory function to create a PrincipalMgmt client.
    
    Args:
        config_path: Path to config.json
        base_url: Windchill server URL
        username: Username
        password: Password
    
    Returns:
        PrincipalMgmtClient instance
    '''
    return PrincipalMgmtClient(
        config_path=config_path,
        base_url=base_url,
        username=username,
        password=password
    )


def main():
    '''CLI entry point for PrincipalMgmt client.'''
    import argparse
    
    parser = argparse.ArgumentParser(description='Windchill PrincipalMgmt Client')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--users', action='store_true', help='List users')
    parser.add_argument('--user-id', help='Get user by ID')
    parser.add_argument('--user-name', help='Get user by name')
    parser.add_argument('--user-email', help='Get user by email')
    parser.add_argument('--groups', action='store_true', help='List groups')
    parser.add_argument('--group-id', help='Get group by ID')
    parser.add_argument('--roles', action='store_true', help='List roles')
    parser.add_argument('--user-groups', help='Get groups for user ID')
    parser.add_argument('--user-roles', help='Get roles for user ID')
    parser.add_argument('--group-members', help='Get members for group ID')
    
    args = parser.parse_args()
    
    client = create_principalmgmt_client(config_path=args.config)
    
    if args.users:
        result = client.get_users()
        print(json.dumps(result, indent=2))
    
    if args.user_id:
        result = client.get_user_by_id(args.user_id)
        print(json.dumps(result, indent=2))
    
    if args.user_name:
        result = client.get_user_by_name(args.user_name)
        print(json.dumps(result, indent=2))
    
    if args.user_email:
        result = client.get_user_by_email(args.user_email)
        print(json.dumps(result, indent=2))
    
    if args.groups:
        result = client.get_groups()
        print(json.dumps(result, indent=2))
    
    if args.group_id:
        result = client.get_group_by_id(args.group_id)
        print(json.dumps(result, indent=2))
    
    if args.roles:
        result = client.get_roles()
        print(json.dumps(result, indent=2))
    
    if args.user_groups:
        result = client.get_user_groups(args.user_groups)
        print(json.dumps(result, indent=2))
    
    if args.user_roles:
        result = client.get_user_roles(args.user_roles)
        print(json.dumps(result, indent=2))
    
    if args.group_members:
        result = client.get_group_members(args.group_members)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
