"""Users API Handler"""
from typing import Optional, Dict, Any
from .base import BaseHandler


class UsersHandler(BaseHandler):
    """Handler for User-related API endpoints."""
    
    async def get_user(self) -> Dict[str, Any]:
        """
        Get authorized user information.
        
        Returns:
            User data
        """
        return await self.client.get("/v2/user")
    
    async def get_team_users(self, team_id: int) -> Dict[str, Any]:
        """
        Get users in a team.
        
        Args:
            team_id: Team ID
            
        Returns:
            Users data
        """
        return await self.client.get(f"/v2/team/{team_id}/user")
    
    async def get_team_user(self, team_id: int, user_id: int) -> Dict[str, Any]:
        """
        Get a specific user in a team.
        
        Args:
            team_id: Team ID
            user_id: User ID
            
        Returns:
            User data
        """
        return await self.client.get(f"/v2/team/{team_id}/user/{user_id}")

