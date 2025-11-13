"""Goals API Handler"""
from typing import Optional, Dict, Any, List
from .base import BaseHandler


class GoalsHandler(BaseHandler):
    """Handler for Goal-related API endpoints."""
    
    async def get_goal(self, goal_id: str) -> Dict[str, Any]:
        """
        Get a goal.
        
        Args:
            goal_id: Goal ID
            
        Returns:
            Goal data
        """
        return await self.client.get(f"/v2/goal/{goal_id}")
    
    async def update_goal(
        self,
        goal_id: str,
        name: Optional[str] = None,
        due_date: Optional[int] = None,
        description: Optional[str] = None,
        multiple_owners: Optional[bool] = None,
        owners: Optional[List[int]] = None,
        color: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update a goal.
        
        Args:
            goal_id: Goal ID
            name: Goal name
            due_date: Due date (Unix timestamp in milliseconds)
            description: Goal description
            multiple_owners: Allow multiple owners
            owners: List of owner user IDs
            color: Goal color
            **kwargs: Additional fields
            
        Returns:
            Updated goal data
        """
        data = {}
        if name is not None:
            data["name"] = name
        if due_date is not None:
            data["due_date"] = due_date
        if description is not None:
            data["description"] = description
        if multiple_owners is not None:
            data["multiple_owners"] = multiple_owners
        if owners is not None:
            data["owners"] = owners
        if color is not None:
            data["color"] = color
        
        data.update(kwargs)
        
        return await self.client.put(f"/v2/goal/{goal_id}", json_data=data)
    
    async def delete_goal(self, goal_id: str) -> Dict[str, Any]:
        """
        Delete a goal.
        
        Args:
            goal_id: Goal ID
            
        Returns:
            Deletion response
        """
        return await self.client.delete(f"/v2/goal/{goal_id}")
    
    async def get_goals(self, team_id: int, include_completed: Optional[bool] = None) -> Dict[str, Any]:
        """
        Get goals for a team.
        
        Args:
            team_id: Team ID
            include_completed: Include completed goals
            
        Returns:
            Goals data
        """
        params = {}
        if include_completed is not None:
            params["include_completed"] = include_completed
        
        return await self.client.get(f"/v2/team/{team_id}/goal", params=params)
    
    async def create_goal(
        self,
        team_id: int,
        name: str,
        due_date: Optional[int] = None,
        description: Optional[str] = None,
        multiple_owners: Optional[bool] = None,
        owners: Optional[List[int]] = None,
        color: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a goal.
        
        Args:
            team_id: Team ID
            name: Goal name
            due_date: Due date (Unix timestamp in milliseconds)
            description: Goal description
            multiple_owners: Allow multiple owners
            owners: List of owner user IDs
            color: Goal color
            **kwargs: Additional fields
            
        Returns:
            Created goal data
        """
        data = {"name": name}
        if due_date is not None:
            data["due_date"] = due_date
        if description is not None:
            data["description"] = description
        if multiple_owners is not None:
            data["multiple_owners"] = multiple_owners
        if owners is not None:
            data["owners"] = owners
        if color is not None:
            data["color"] = color
        
        data.update(kwargs)
        
        return await self.client.post(f"/v2/team/{team_id}/goal", json_data=data)

