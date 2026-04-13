'''
Windchill PLM ProjMgmt (Project Management) Domain Client

Project Management domain client providing:
- Project plans management
- Activities, tasks, milestones
- Activity hierarchy navigation
- Project scheduling and tracking

This domain handles project planning and execution.
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
from typing import Dict, List, Optional, Any
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from windchill_base import WindchillBaseClient, ODataError


class ProjMgmtClient(WindchillBaseClient):
    '''
    Client for Windchill ProjMgmt OData domain.
    
    Provides project management operations including
    project plans, activities, milestones, and deliverables.
    '''
    
    DOMAIN = 'ProjMgmt'
    
    def __init__(self, **kwargs):
        '''Initialize ProjMgmt client with default domain.'''
        kwargs.setdefault('domain', self.DOMAIN)
        super().__init__(**kwargs)
    
    # =========================================================================
    # ProjectPlan Queries
    # =========================================================================
    
    def get_project_plans(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get ProjectPlan records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of ProjectPlans
        '''
        return self.query_entities('ProjectPlans', filter_expr=filter_expr, top=top)
    
    def get_project_plan_by_id(self, plan_id: str, expand: List[str] = None) -> dict:
        '''
        Get ProjectPlan by ID.
        
        Args:
            plan_id: ProjectPlan ID (OID format)
            expand: Navigation properties to expand
        
        Returns:
            ProjectPlan dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('ProjectPlans', plan_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_project_plan_by_name(self, name: str) -> dict:
        '''
        Get ProjectPlan by name.
        
        Args:
            name: Project plan name
        
        Returns:
            ProjectPlan dictionary
        '''
        plans = self.query_entities(
            'ProjectPlans',
            filter_expr=f"Name eq '{name}'",
            top=1
        )
        return plans[0] if plans else None
    
    def get_project_plans_by_status(self, status: str, top: int = 50) -> List[dict]:
        '''
        Get ProjectPlans by status.
        
        Args:
            status: Status value
            top: Maximum results
        
        Returns:
            List of ProjectPlans with specified status
        '''
        return self.query_entities(
            'ProjectPlans',
            filter_expr=f"Status eq '{status}'",
            top=top
        )
    
    # =========================================================================
    # Activity Queries
    # =========================================================================
    
    def get_activities(self, filter_expr: str = None, top: int = 50) -> List[dict]:
        '''
        Get Activity records.
        
        Args:
            filter_expr: OData filter expression
            top: Maximum results
        
        Returns:
            List of Activities
        '''
        return self.query_entities('Activities', filter_expr=filter_expr, top=top)
    
    def get_activity_by_id(self, activity_id: str, expand: List[str] = None) -> dict:
        '''
        Get Activity by ID.
        
        Args:
            activity_id: Activity ID (OID format)
            expand: Navigation properties to expand
        
        Returns:
            Activity dictionary
        '''
        expand_str = ','.join(expand) if expand else None
        return self.get_entity('Activities', activity_id, domain=self.DOMAIN, expand=expand_str)
    
    def get_activities_by_name(self, name: str, top: int = 50) -> List[dict]:
        '''
        Get Activities by name.
        
        Args:
            name: Activity name
            top: Maximum results
        
        Returns:
            List of matching Activities
        '''
        return self.query_entities(
            'Activities',
            filter_expr=f"Name eq '{name}'",
            top=top
        )
    
    def get_activities_by_plan_name(self, plan_name: str, top: int = 50) -> List[dict]:
        '''
        Get Activities by plan name.
        
        Args:
            plan_name: Plan name
            top: Maximum results
        
        Returns:
            List of Activities
        '''
        return self.query_entities(
            'Activities',
            filter_expr=f"PlanName eq '{plan_name}'",
            top=top
        )
    
    def get_activities_by_status(self, status: str, top: int = 50) -> List[dict]:
        '''
        Get Activities by status.
        
        Args:
            status: Status value
            top: Maximum results
        
        Returns:
            List of Activities with specified status
        '''
        return self.query_entities(
            'Activities',
            filter_expr=f"Status eq '{status}'",
            top=top
        )
    
    def get_milestones(self, top: int = 50) -> List[dict]:
        '''
        Get all milestone activities.
        
        Args:
            top: Maximum results
        
        Returns:
            List of milestone Activities
        '''
        return self.query_entities(
            'Activities',
            filter_expr="Milestone eq true",
            top=top
        )
    
    def get_summary_activities(self, top: int = 50) -> List[dict]:
        '''
        Get all summary activities.
        
        Args:
            top: Maximum results
        
        Returns:
            List of summary Activities
        '''
        return self.query_entities(
            'Activities',
            filter_expr="Summary eq true",
            top=top
        )
    
    def get_deliverable_activities(self, top: int = 50) -> List[dict]:
        '''
        Get all deliverable activities.
        
        Args:
            top: Maximum results
        
        Returns:
            List of deliverable Activities
        '''
        return self.query_entities(
            'Activities',
            filter_expr="Deliverable eq true",
            top=top
        )
    
    # =========================================================================
    # Navigation Properties - ProjectPlan
    # =========================================================================
    
    def get_activities_for_plan(self, plan_id: str) -> List[dict]:
        '''
        Get all Activities for a ProjectPlan.
        
        Args:
            plan_id: ProjectPlan ID
        
        Returns:
            List of Activities
        '''
        return self.get_navigation('ProjectPlans', plan_id, 'Activities', domain=self.DOMAIN)
    
    def get_immediate_children(self, plan_id: str) -> List[dict]:
        '''
        Get immediate children (top-level activities) for a ProjectPlan.
        
        Args:
            plan_id: ProjectPlan ID
        
        Returns:
            List of top-level Activities
        '''
        return self.get_navigation('ProjectPlans', plan_id, 'ImmediateChildren', domain=self.DOMAIN)
    
    def get_plan_context(self, plan_id: str) -> dict:
        '''
        Get context for a ProjectPlan.
        
        Args:
            plan_id: ProjectPlan ID
        
        Returns:
            Container dictionary
        '''
        return self.get_navigation('ProjectPlans', plan_id, 'Context', domain=self.DOMAIN)
    
    # =========================================================================
    # Navigation Properties - Activity
    # =========================================================================
    
    def get_activity_children(self, activity_id: str) -> List[dict]:
        '''
        Get child Activities for an Activity.
        
        Args:
            activity_id: Activity ID
        
        Returns:
            List of child Activities
        '''
        return self.get_navigation('Activities', activity_id, 'Children', domain=self.DOMAIN)
    
    def get_activity_owner(self, activity_id: str) -> dict:
        '''
        Get ActivityOwner (User) for an Activity.
        
        Args:
            activity_id: Activity ID
        
        Returns:
            User dictionary
        '''
        return self.get_navigation('Activities', activity_id, 'ActivityOwner', domain=self.DOMAIN)
    
    def get_activity_deliverables(self, activity_id: str) -> List[dict]:
        '''
        Get Deliverables for an Activity.
        
        Args:
            activity_id: Activity ID
        
        Returns:
            List of deliverable entities
        '''
        return self.get_navigation('Activities', activity_id, 'Deliverables', domain=self.DOMAIN)
    
    def get_activity_context(self, activity_id: str) -> dict:
        '''
        Get context for an Activity.
        
        Args:
            activity_id: Activity ID
        
        Returns:
            Container dictionary
        '''
        return self.get_navigation('Activities', activity_id, 'Context', domain=self.DOMAIN)
    
    # =========================================================================
    # ProjectPlan CRUD Operations
    # =========================================================================
    
    def create_project_plan(
        self,
        name: str,
        deadline: str = None,
        estimated_start: str = None,
        estimated_finish: str = None
    ) -> dict:
        '''
        Create a new ProjectPlan.
        
        Args:
            name: Project plan name
            deadline: Deadline date string
            estimated_start: Estimated start date string
            estimated_finish: Estimated finish date string
        
        Returns:
            Created ProjectPlan
        '''
        payload = {'Name': name}
        
        if deadline:
            payload['Deadline'] = deadline
        if estimated_start:
            payload['EstimatedStart'] = estimated_start
        if estimated_finish:
            payload['EstimatedFinish'] = estimated_finish
        
        return self.create_entity('ProjectPlans', payload, domain=self.DOMAIN)
    
    def update_project_plan(
        self,
        plan_id: str,
        name: str = None,
        status: str = None,
        percent_work_complete: float = None
    ) -> dict:
        '''
        Update a ProjectPlan.
        
        Args:
            plan_id: ProjectPlan ID
            name: Updated name
            status: Updated status
            percent_work_complete: Updated progress
        
        Returns:
            Updated ProjectPlan
        '''
        payload = {}
        
        if name is not None:
            payload['Name'] = name
        if status is not None:
            payload['Status'] = status
        if percent_work_complete is not None:
            payload['PercentWorkComplete'] = percent_work_complete
        
        return self.update_entity('ProjectPlans', plan_id, payload, domain=self.DOMAIN)
    
    def delete_project_plan(self, plan_id: str) -> bool:
        '''
        Delete a ProjectPlan.
        
        Args:
            plan_id: ProjectPlan ID
        
        Returns:
            True if successful
        '''
        return self.delete_entity('ProjectPlans', plan_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Activity CRUD Operations
    # =========================================================================
    
    def create_activity(
        self,
        name: str,
        start_date: str = None,
        finish_date: str = None,
        summary: bool = False,
        milestone: bool = False,
        deliverable: bool = False,
        percent_work_complete: float = 0.0
    ) -> dict:
        '''
        Create a new Activity.
        
        Args:
            name: Activity name
            start_date: Start date (ISO format)
            finish_date: Finish date (ISO format)
            summary: Is summary activity
            milestone: Is milestone
            deliverable: Is deliverable
            percent_work_complete: Initial progress
        
        Returns:
            Created Activity
        '''
        payload = {
            'Name': name,
            'Summary': summary,
            'Milestone': milestone,
            'Deliverable': deliverable,
            'PercentWorkComplete': percent_work_complete
        }
        
        if start_date:
            payload['StartDate'] = start_date
        if finish_date:
            payload['FinishDate'] = finish_date
        
        return self.create_entity('Activities', payload, domain=self.DOMAIN)
    
    def update_activity(
        self,
        activity_id: str,
        name: str = None,
        status: str = None,
        percent_work_complete: float = None,
        start_date: str = None,
        finish_date: str = None
    ) -> dict:
        '''
        Update an Activity.
        
        Args:
            activity_id: Activity ID
            name: Updated name
            status: Updated status
            percent_work_complete: Updated progress
            start_date: Updated start date
            finish_date: Updated finish date
        
        Returns:
            Updated Activity
        '''
        payload = {}
        
        if name is not None:
            payload['Name'] = name
        if status is not None:
            payload['Status'] = status
        if percent_work_complete is not None:
            payload['PercentWorkComplete'] = percent_work_complete
        if start_date is not None:
            payload['StartDate'] = start_date
        if finish_date is not None:
            payload['FinishDate'] = finish_date
        
        return self.update_entity('Activities', activity_id, payload, domain=self.DOMAIN)
    
    def delete_activity(self, activity_id: str) -> bool:
        '''
        Delete an Activity.
        
        Args:
            activity_id: Activity ID
        
        Returns:
            True if successful
        '''
        return self.delete_entity('Activities', activity_id, domain=self.DOMAIN)
    
    # =========================================================================
    # Actions
    # =========================================================================
    
    def add_activity_to_plan(self, plan_id: str, activity_id: str) -> dict:
        '''
        Add an Activity to a ProjectPlan.
        
        Args:
            plan_id: ProjectPlan ID
            activity_id: Activity ID
        
        Returns:
            Result of the action
        '''
        self._ensure_csrf_token()
        
        action_url = f"{self._get_base_url()}/ProjectPlans('{plan_id}')/PTC.ProjMgmt.AddToPlan"
        
        payload = {
            "ProjectPlan": plan_id,
            "Activity": activity_id
        }
        
        headers = self._get_headers()
        if self.csrf_token:
            headers['CSRF_NONCE'] = self.csrf_token
        
        response = self.session.post(action_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json() if response.content else {'success': True}
    
    def create_activity_in_plan(
        self,
        plan_id: str,
        name: str,
        start_date: str = None,
        finish_date: str = None,
        summary: bool = False,
        milestone: bool = False,
        deliverable: bool = False
    ) -> dict:
        '''
        Create an Activity and add it to a Plan in one operation.
        
        Args:
            plan_id: ProjectPlan ID
            name: Activity name
            start_date: Start date (ISO format)
            finish_date: Finish date (ISO format)
            summary: Is summary activity
            milestone: Is milestone
            deliverable: Is deliverable
        
        Returns:
            Created and added Activity
        '''
        # Create the activity
        activity = self.create_activity(
            name=name,
            start_date=start_date,
            finish_date=finish_date,
            summary=summary,
            milestone=milestone,
            deliverable=deliverable
        )
        
        # Add to plan
        result = self.add_activity_to_plan(plan_id, activity['ID'])
        
        # Return the activity
        return self.get_activity_by_id(activity['ID'])


def create_proj_mgmt_client(config_path: str = None, **kwargs) -> ProjMgmtClient:
    '''
    Factory function to create ProjMgmt client.
    
    Args:
        config_path: Path to config.json
        **kwargs: Additional client options
    
    Returns:
        ProjMgmtClient instance
    '''
    if config_path:
        with open(config_path, 'r') as f:
            config = json.load(f)
        kwargs.update(config)
    
    return ProjMgmtClient(**kwargs)
