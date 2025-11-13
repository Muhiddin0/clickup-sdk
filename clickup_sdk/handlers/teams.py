"""Teams API Handler"""
from typing import Optional, Dict, Any
from .base import BaseHandler


class TeamsHandler(BaseHandler):
    """Handler for Team (Workspace)-related API endpoints."""
    
    async def get_teams(self) -> Dict[str, Any]:
        """
        Get authorized workspaces (teams).
        
        Returns:
            Teams data
        """
        return await self.client.get("/v2/team")
    
    async def get_team_seats(self, team_id: int) -> Dict[str, Any]:
        """
        Get team seats information.
        
        Args:
            team_id: Team ID
            
        Returns:
            Seats data
        """
        return await self.client.get(f"/v2/team/{team_id}/seats")
    
    async def get_team_plan(self, team_id: int) -> Dict[str, Any]:
        """
        Get team plan information.
        
        Args:
            team_id: Team ID
            
        Returns:
            Plan data
        """
        return await self.client.get(f"/v2/team/{team_id}/plan")

