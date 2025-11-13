"""Time Entries API Handler"""
from typing import Optional, Dict, Any, List
from .base import BaseHandler


class TimeEntriesHandler(BaseHandler):
    """Handler for Time Entry-related API endpoints."""
    
    async def get_time_entries(
        self,
        team_id: int,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        assignee: Optional[str] = None,
        include_task_tags: Optional[bool] = None,
        include_location_names: Optional[bool] = None,
        space_id: Optional[str] = None,
        folder_id: Optional[str] = None,
        list_id: Optional[str] = None,
        task_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get time entries.
        
        Args:
            team_id: Team ID
            start_date: Start date (Unix timestamp in milliseconds)
            end_date: End date (Unix timestamp in milliseconds)
            assignee: Assignee user ID
            include_task_tags: Include task tags
            include_location_names: Include location names
            space_id: Filter by space ID
            folder_id: Filter by folder ID
            list_id: Filter by list ID
            task_id: Filter by task ID
            
        Returns:
            Time entries data
        """
        params = {}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if assignee is not None:
            params["assignee"] = assignee
        if include_task_tags is not None:
            params["include_task_tags"] = include_task_tags
        if include_location_names is not None:
            params["include_location_names"] = include_location_names
        if space_id is not None:
            params["space_id"] = space_id
        if folder_id is not None:
            params["folder_id"] = folder_id
        if list_id is not None:
            params["list_id"] = list_id
        if task_id is not None:
            params["task_id"] = task_id
        
        return await self.client.get(f"/v2/team/{team_id}/time_entries", params=params)
    
    async def create_time_entry(
        self,
        team_id: int,
        task_id: str,
        start: int,
        duration: int,
        billable: Optional[bool] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        assignee: Optional[str] = None,
        tid: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a time entry.
        
        Args:
            team_id: Team ID
            task_id: Task ID
            start: Start time (Unix timestamp in milliseconds)
            duration: Duration in milliseconds
            billable: Whether entry is billable
            description: Entry description
            tags: List of tag names
            assignee: Assignee user ID
            tid: Timer ID
            **kwargs: Additional fields
            
        Returns:
            Created time entry data
        """
        data = {
            "task_id": task_id,
            "start": start,
            "duration": duration
        }
        if billable is not None:
            data["billable"] = billable
        if description is not None:
            data["description"] = description
        if tags is not None:
            data["tags"] = tags
        if assignee is not None:
            data["assignee"] = assignee
        if tid is not None:
            data["tid"] = tid
        
        data.update(kwargs)
        
        return await self.client.post(f"/v2/team/{team_id}/time_entries", json_data=data)
    
    async def get_current_time_entry(self, team_id: int) -> Dict[str, Any]:
        """
        Get current running time entry.
        
        Args:
            team_id: Team ID
            
        Returns:
            Current time entry data
        """
        return await self.client.get(f"/v2/team/{team_id}/time_entries/current")
    
    async def start_time_entry(
        self,
        team_id: int,
        task_id: str,
        billable: Optional[bool] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        tid: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Start a time entry.
        
        Args:
            team_id: Team ID
            task_id: Task ID
            billable: Whether entry is billable
            description: Entry description
            tags: List of tag names
            tid: Timer ID
            **kwargs: Additional fields
            
        Returns:
            Started time entry data
        """
        data = {"task_id": task_id}
        if billable is not None:
            data["billable"] = billable
        if description is not None:
            data["description"] = description
        if tags is not None:
            data["tags"] = tags
        if tid is not None:
            data["tid"] = tid
        
        data.update(kwargs)
        
        return await self.client.post(f"/v2/team/{team_id}/time_entries/start", json_data=data)
    
    async def stop_time_entry(self, team_id: int, timer_id: str) -> Dict[str, Any]:
        """
        Stop a running time entry.
        
        Args:
            team_id: Team ID
            timer_id: Timer ID
            
        Returns:
            Stopped time entry data
        """
        return await self.client.post(f"/v2/team/{team_id}/time_entries/stop", json_data={"timer_id": timer_id})
    
    async def delete_time_entry(self, team_id: int, timer_id: str) -> Dict[str, Any]:
        """
        Delete a time entry.
        
        Args:
            team_id: Team ID
            timer_id: Timer ID
            
        Returns:
            Deletion response
        """
        return await self.client.delete(f"/v2/team/{team_id}/time_entries/{timer_id}")

