"""Folders API Handler"""
from typing import Optional, Dict, Any
from .base import BaseHandler


class FoldersHandler(BaseHandler):
    """Handler for Folder-related API endpoints."""
    
    async def get_folder(self, folder_id: str) -> Dict[str, Any]:
        """
        Get a folder.
        
        Args:
            folder_id: Folder ID
            
        Returns:
            Folder data
        """
        return await self.client.get(f"/v2/folder/{folder_id}")
    
    async def update_folder(
        self,
        folder_id: str,
        name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update a folder.
        
        Args:
            folder_id: Folder ID
            name: Folder name
            **kwargs: Additional fields
            
        Returns:
            Updated folder data
        """
        data = {}
        if name is not None:
            data["name"] = name
        
        data.update(kwargs)
        
        return await self.client.put(f"/v2/folder/{folder_id}", json_data=data)
    
    async def delete_folder(self, folder_id: str) -> Dict[str, Any]:
        """
        Delete a folder.
        
        Args:
            folder_id: Folder ID
            
        Returns:
            Deletion response
        """
        return await self.client.delete(f"/v2/folder/{folder_id}")
    
    async def get_folders(self, space_id: str, archived: Optional[bool] = None) -> Dict[str, Any]:
        """
        Get folders in a space.
        
        Args:
            space_id: Space ID
            archived: Include archived folders
            
        Returns:
            Folders data
        """
        params = {}
        if archived is not None:
            params["archived"] = archived
        
        return await self.client.get(f"/v2/space/{space_id}/folder", params=params)
    
    async def create_folder(
        self,
        space_id: str,
        name: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a folder.
        
        Args:
            space_id: Space ID
            name: Folder name
            **kwargs: Additional fields
            
        Returns:
            Created folder data
        """
        data = {"name": name}
        data.update(kwargs)
        
        return await self.client.post(f"/v2/space/{space_id}/folder", json_data=data)

