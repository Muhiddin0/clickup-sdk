"""Spaces API Handler"""
from typing import Optional, Dict, Any
from .base import BaseHandler


class SpacesHandler(BaseHandler):
    """Handler for Space-related API endpoints."""
    
    async def get_space(self, space_id: str) -> Dict[str, Any]:
        """
        Get a space.
        
        Args:
            space_id: Space ID
            
        Returns:
            Space data
        """
        return await self.client.get(f"/v2/space/{space_id}")
    
    async def update_space(
        self,
        space_id: str,
        name: Optional[str] = None,
        color: Optional[str] = None,
        avatar: Optional[str] = None,
        features: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update a space.
        
        Args:
            space_id: Space ID
            name: Space name
            color: Space color
            avatar: Space avatar
            features: Space features
            **kwargs: Additional fields
            
        Returns:
            Updated space data
        """
        data = {}
        if name is not None:
            data["name"] = name
        if color is not None:
            data["color"] = color
        if avatar is not None:
            data["avatar"] = avatar
        if features is not None:
            data["features"] = features
        
        data.update(kwargs)
        
        return await self.client.put(f"/v2/space/{space_id}", json_data=data)
    
    async def delete_space(self, space_id: str) -> Dict[str, Any]:
        """
        Delete a space.
        
        Args:
            space_id: Space ID
            
        Returns:
            Deletion response
        """
        return await self.client.delete(f"/v2/space/{space_id}")
    
    async def get_spaces(self, team_id: int, archived: Optional[bool] = None) -> Dict[str, Any]:
        """
        Get spaces in a team.
        
        Args:
            team_id: Team ID
            archived: Include archived spaces
            
        Returns:
            Spaces data
        """
        params = {}
        if archived is not None:
            params["archived"] = archived
        
        return await self.client.get(f"/v2/team/{team_id}/space", params=params)
    
    async def create_space(
        self,
        team_id: int,
        name: str,
        multiple_assignees: Optional[bool] = None,
        features: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a space.
        
        Args:
            team_id: Team ID
            name: Space name
            multiple_assignees: Allow multiple assignees
            features: Space features
            **kwargs: Additional fields
            
        Returns:
            Created space data
        """
        data = {"name": name}
        if multiple_assignees is not None:
            data["multiple_assignees"] = multiple_assignees
        if features is not None:
            data["features"] = features
        
        data.update(kwargs)
        
        return await self.client.post(f"/v2/team/{team_id}/space", json_data=data)

