"""Lists API Handler"""
from typing import Optional, Dict, Any
from .base import BaseHandler


class ListsHandler(BaseHandler):
    """Handler for List-related API endpoints."""
    
    async def get_list(self, list_id: str) -> Dict[str, Any]:
        """
        Get a list.
        
        Args:
            list_id: List ID
            
        Returns:
            List data
        """
        return await self.client.get(f"/v2/list/{list_id}")
    
    async def update_list(
        self,
        list_id: str,
        name: Optional[str] = None,
        content: Optional[str] = None,
        due_date: Optional[int] = None,
        due_date_time: Optional[bool] = None,
        priority: Optional[int] = None,
        assignee: Optional[str] = None,
        status: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update a list.
        
        Args:
            list_id: List ID
            name: List name
            content: List content/description
            due_date: Due date (Unix timestamp in milliseconds)
            due_date_time: Whether due date includes time
            priority: Priority (1-4)
            assignee: Assignee user ID
            status: Status
            **kwargs: Additional fields
            
        Returns:
            Updated list data
        """
        data = {}
        if name is not None:
            data["name"] = name
        if content is not None:
            data["content"] = content
        if due_date is not None:
            data["due_date"] = due_date
        if due_date_time is not None:
            data["due_date_time"] = due_date_time
        if priority is not None:
            data["priority"] = priority
        if assignee is not None:
            data["assignee"] = assignee
        if status is not None:
            data["status"] = status
        
        data.update(kwargs)
        
        return await self.client.put(f"/v2/list/{list_id}", json_data=data)
    
    async def delete_list(self, list_id: str) -> Dict[str, Any]:
        """
        Delete a list.
        
        Args:
            list_id: List ID
            
        Returns:
            Deletion response
        """
        return await self.client.delete(f"/v2/list/{list_id}")
    
    async def get_lists(self, folder_id: str, archived: Optional[bool] = None) -> Dict[str, Any]:
        """
        Get lists in a folder.
        
        Args:
            folder_id: Folder ID
            archived: Include archived lists
            
        Returns:
            Lists data
        """
        params = {}
        if archived is not None:
            params["archived"] = archived
        
        return await self.client.get(f"/v2/folder/{folder_id}/list", params=params)
    
    async def create_list(
        self,
        folder_id: Optional[str] = None,
        space_id: Optional[str] = None,
        name: str = None,
        content: Optional[str] = None,
        due_date: Optional[int] = None,
        due_date_time: Optional[bool] = None,
        priority: Optional[int] = None,
        assignee: Optional[str] = None,
        status: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a list.
        
        Args:
            folder_id: Folder ID (optional if space_id is provided)
            space_id: Space ID (optional if folder_id is provided)
            name: List name
            content: List content/description
            due_date: Due date (Unix timestamp in milliseconds)
            due_date_time: Whether due date includes time
            priority: Priority (1-4)
            assignee: Assignee user ID
            status: Status
            **kwargs: Additional fields
            
        Returns:
            Created list data
        """
        if folder_id:
            endpoint = f"/v2/folder/{folder_id}/list"
        elif space_id:
            endpoint = f"/v2/space/{space_id}/list"
        else:
            raise ValueError("Either folder_id or space_id must be provided")
        
        data = {}
        if name is not None:
            data["name"] = name
        if content is not None:
            data["content"] = content
        if due_date is not None:
            data["due_date"] = due_date
        if due_date_time is not None:
            data["due_date_time"] = due_date_time
        if priority is not None:
            data["priority"] = priority
        if assignee is not None:
            data["assignee"] = assignee
        if status is not None:
            data["status"] = status
        
        data.update(kwargs)
        
        return await self.client.post(endpoint, json_data=data)

