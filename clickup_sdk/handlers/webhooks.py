"""Webhooks API Handler"""
from typing import Optional, Dict, Any, List
from .base import BaseHandler


class WebhooksHandler(BaseHandler):
    """Handler for Webhook-related API endpoints."""
    
    async def get_webhooks(self, team_id: int, space_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get webhooks for a team.
        
        Args:
            team_id: Team ID
            space_id: Filter by space ID (optional)
            
        Returns:
            Webhooks data
        """
        params = {}
        if space_id is not None:
            params["space_id"] = space_id
        
        return await self.client.get(f"/v2/team/{team_id}/webhook", params=params)
    
    async def create_webhook(
        self,
        team_id: int,
        endpoint: str,
        client_id: str,
        events: List[str],
        space_id: Optional[str] = None,
        list_id: Optional[str] = None,
        folder_id: Optional[str] = None,
        task_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a webhook.
        
        Args:
            team_id: Team ID
            endpoint: Webhook endpoint URL
            client_id: OAuth client ID
            events: List of event types to subscribe to
            space_id: Filter by space ID (optional)
            list_id: Filter by list ID (optional)
            folder_id: Filter by folder ID (optional)
            task_id: Filter by task ID (optional)
            
        Returns:
            Created webhook data
        """
        data = {
            "endpoint": endpoint,
            "client_id": client_id,
            "events": events
        }
        if space_id is not None:
            data["space_id"] = space_id
        if list_id is not None:
            data["list_id"] = list_id
        if folder_id is not None:
            data["folder_id"] = folder_id
        if task_id is not None:
            data["task_id"] = task_id
        
        return await self.client.post(f"/v2/team/{team_id}/webhook", json_data=data)
    
    async def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """
        Delete a webhook.
        
        Args:
            webhook_id: Webhook ID
            
        Returns:
            Deletion response
        """
        return await self.client.delete(f"/v2/webhook/{webhook_id}")

