"""Custom Fields API Handler"""
from typing import Optional, Dict, Any, List
from .base import BaseHandler


class CustomFieldsHandler(BaseHandler):
    """Handler for Custom Field-related API endpoints."""
    
    async def get_list_fields(self, list_id: str) -> Dict[str, Any]:
        """
        Get custom fields for a list.
        
        Args:
            list_id: List ID
            
        Returns:
            Custom fields data
        """
        return await self.client.get(f"/v2/list/{list_id}/field")
    
    async def get_folder_fields(self, folder_id: str) -> Dict[str, Any]:
        """
        Get custom fields for a folder.
        
        Args:
            folder_id: Folder ID
            
        Returns:
            Custom fields data
        """
        return await self.client.get(f"/v2/folder/{folder_id}/field")
    
    async def get_space_fields(self, space_id: str) -> Dict[str, Any]:
        """
        Get custom fields for a space.
        
        Args:
            space_id: Space ID
            
        Returns:
            Custom fields data
        """
        return await self.client.get(f"/v2/space/{space_id}/field")
    
    async def get_team_fields(self, team_id: int) -> Dict[str, Any]:
        """
        Get custom fields for a team.
        
        Args:
            team_id: Team ID
            
        Returns:
            Custom fields data
        """
        return await self.client.get(f"/v2/team/{team_id}/field")
    
    async def get_task_field(
        self,
        task_id: str,
        field_id: str,
        custom_task_ids: Optional[bool] = None,
        team_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get a custom field value for a task.
        
        Args:
            task_id: Task ID
            field_id: Custom field ID
            custom_task_ids: If true, task_id is a custom task ID
            team_id: Team ID (required if custom_task_ids is true)
            
        Returns:
            Custom field data
        """
        params = {}
        if custom_task_ids is not None:
            params["custom_task_ids"] = custom_task_ids
        if team_id is not None:
            params["team_id"] = team_id
        
        return await self.client.get(f"/v2/task/{task_id}/field/{field_id}", params=params)
    
    async def set_task_field(
        self,
        task_id: str,
        field_id: str,
        value: Any,
        custom_task_ids: Optional[bool] = None,
        team_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Set a custom field value for a task.
        
        Args:
            task_id: Task ID
            field_id: Custom field ID
            value: Field value
            custom_task_ids: If true, task_id is a custom task ID
            team_id: Team ID (required if custom_task_ids is true)
            
        Returns:
            Updated field data
        """
        params = {}
        if custom_task_ids is not None:
            params["custom_task_ids"] = custom_task_ids
        if team_id is not None:
            params["team_id"] = team_id
        
        data = {"value": value}
        return await self.client.post(f"/v2/task/{task_id}/field/{field_id}", json_data=data, params=params)

