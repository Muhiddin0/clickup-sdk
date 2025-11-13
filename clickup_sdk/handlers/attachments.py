"""Attachments API Handler"""
from typing import Optional, Dict, Any
from .base import BaseHandler
import aiohttp


class AttachmentsHandler(BaseHandler):
    """Handler for Attachment-related API endpoints."""
    
    async def create_task_attachment(
        self,
        task_id: str,
        file_path: str,
        custom_task_ids: Optional[bool] = None,
        team_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Upload a file attachment to a task.
        
        Args:
            task_id: Task ID
            file_path: Path to file to upload
            custom_task_ids: If true, task_id is a custom task ID
            team_id: Team ID (required if custom_task_ids is true)
            
        Returns:
            Attachment data
        """
        params = {}
        if custom_task_ids is not None:
            params["custom_task_ids"] = custom_task_ids
        if team_id is not None:
            params["team_id"] = team_id
        
        url = f"{self.client.BASE_URL}/v2/task/{task_id}/attachment"
        if params:
            from urllib.parse import urlencode
            url += f"?{urlencode(params, doseq=True)}"
        
        session = await self.client._get_session()
        headers = {"Authorization": self.client.token}
        
        form_data = aiohttp.FormData()
        with open(file_path, "rb") as f:
            file_content = f.read()
            filename = file_path.split("/")[-1] if "/" in file_path else file_path.split("\\")[-1]
            form_data.add_field("attachment", file_content, filename=filename, content_type="application/octet-stream")
        
        async with session.post(url, headers=headers, data=form_data) as response:
            response.raise_for_status()
            return await response.json()
    
    async def delete_task_attachment(
        self,
        task_id: str,
        attachment_id: str,
        custom_task_ids: Optional[bool] = None,
        team_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Delete a task attachment.
        
        Args:
            task_id: Task ID
            attachment_id: Attachment ID
            custom_task_ids: If true, task_id is a custom task ID
            team_id: Team ID (required if custom_task_ids is true)
            
        Returns:
            Deletion response
        """
        params = {}
        if custom_task_ids is not None:
            params["custom_task_ids"] = custom_task_ids
        if team_id is not None:
            params["team_id"] = team_id
        
        return await self.client.delete(f"/v2/task/{task_id}/attachment/{attachment_id}", params=params)

