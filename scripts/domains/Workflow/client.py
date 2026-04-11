'''
Windchill PLM Workflow Domain Client

Workflow domain client providing:
- Lifecycle template queries
- State transition information
- Workflow process management
'''

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class WorkflowClient(WindchillBaseClient):
    '''
    Client for Windchill Workflow OData domain.
    
    Provides workflow and lifecycle operations.
    '''
    
    DOMAIN = 'Workflow'
    
    def __init__(self, **kwargs):
        '''Initialize Workflow client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # Lifecycle Templates
    # =========================================================================
    
    def get_lifecycle_template(self, template_id: str) -> dict:
        '''
        Get lifecycle template by ID.
        
        Args:
            template_id: Lifecycle template ID
        
        Returns:
            Lifecycle template dictionary
        '''
        return self.get_entity('LifecycleTemplates', template_id, domain=self.DOMAIN)
    
    def get_lifecycle_templates(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get lifecycle templates.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of lifecycle templates
        '''
        return self.query_entities('LifecycleTemplates', filter_expr=filter_expr, top=top)
    
    # =========================================================================
    # State Transitions
    # =========================================================================
    
    def get_valid_state_transitions(self, lifecycle_id: str) -> List[dict]:
        '''
        Get valid state transitions for a lifecycle.
        
        Args:
            lifecycle_id: Lifecycle template ID or name
        
        Returns:
            List of valid state transitions
        '''
        return self.invoke_action(
            'GetValidStateTransitions',
            entity_id=lifecycle_id,
            entity_type='LifecycleTemplate'
        )
    
    # =========================================================================
    # Workflow Processes
    # =========================================================================
    
    def get_workflow_processes(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get workflow processes.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of workflow processes
        '''
        return self.query_entities('WorkflowProcesses', filter_expr=filter_expr, top=top)
    
    def get_workflow_process_by_id(self, process_id: str) -> dict:
        '''
        Get workflow process by ID.
        
        Args:
            process_id: Workflow process ID
        
        Returns:
            Workflow process dictionary
        '''
        return self.get_entity('WorkflowProcesses', process_id, domain=self.DOMAIN)
    
    def get_workflow_tasks(self, process_id: str) -> List[dict]:
        '''
        Get tasks for a workflow process.
        
        Args:
            process_id: Workflow process ID
        
        Returns:
            List of workflow tasks
        '''
        return self.get_navigation('WorkflowProcesses', process_id, 'Tasks', domain=self.DOMAIN)


def create_workflow_client(config_path: str = None, base_url: str = None,
                            username: str = None, password: str = None) -> WorkflowClient:
    '''
    Factory function to create a Workflow client.
    
    Args:
        config_path: Path to config.json
        base_url: Windchill server URL
        username: Username
        password: Password
    
    Returns:
        WorkflowClient instance
    '''
    return WorkflowClient(
        config_path=config_path,
        base_url=base_url,
        username=username,
        password=password
    )


def main():
    '''CLI entry point for Workflow client.'''
    import argparse
    
    parser = argparse.ArgumentParser(description='Windchill Workflow Client')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--lifecycle-templates', action='store_true', help='List lifecycle templates')
    parser.add_argument('--lifecycle-id', help='Get lifecycle template by ID')
    parser.add_argument('--state-transitions', help='Get valid state transitions for lifecycle')
    parser.add_argument('--processes', action='store_true', help='List workflow processes')
    parser.add_argument('--process-id', help='Get workflow process by ID')
    parser.add_argument('--tasks', help='Get tasks for process ID')
    
    args = parser.parse_args()
    
    client = create_workflow_client(config_path=args.config)
    
    if args.lifecycle_templates:
        result = client.get_lifecycle_templates()
        print(json.dumps(result, indent=2))
    
    if args.lifecycle_id:
        result = client.get_lifecycle_template(args.lifecycle_id)
        print(json.dumps(result, indent=2))
    
    if args.state_transitions:
        result = client.get_valid_state_transitions(args.state_transitions)
        print(json.dumps(result, indent=2))
    
    if args.processes:
        result = client.get_workflow_processes()
        print(json.dumps(result, indent=2))
    
    if args.process_id:
        result = client.get_workflow_process_by_id(args.process_id)
        print(json.dumps(result, indent=2))
    
    if args.tasks:
        result = client.get_workflow_tasks(args.tasks)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
