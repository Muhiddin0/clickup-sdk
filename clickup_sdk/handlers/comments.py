"""Comments API Handler"""
from typing import Optional, Dict, Any
from .base import BaseHandler


class CommentsHandler(BaseHandler):
    """Handler for Comment-related API endpoints."""
    
    async def get_comment(self, comment_id: str) -> Dict[str, Any]:
        """
        Get a comment.
        
        Args:
            comment_id: Comment ID
            
        Returns:
            Comment data
        """
        return await self.client.get(f"/v2/comment/{comment_id}")
    
    async def update_comment(
        self,
        comment_id: str,
        comment_text: str,
        assignee: Optional[str] = None,
        resolved: Optional[bool] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update a comment.
        
        Args:
            comment_id: Comment ID
            comment_text: Comment text
            assignee: Assignee user ID
            resolved: Whether comment is resolved
            **kwargs: Additional fields
            
        Returns:
            Updated comment data
        """
        data = {"comment_text": comment_text}
        if assignee is not None:
            data["assignee"] = assignee
        if resolved is not None:
            data["resolved"] = resolved
        
        data.update(kwargs)
        
        return await self.client.put(f"/v2/comment/{comment_id}", json_data=data)
    
    async def delete_comment(self, comment_id: str) -> Dict[str, Any]:
        """
        Delete a comment.
        
        Args:
            comment_id: Comment ID
            
        Returns:
            Deletion response
        """
        return await self.client.delete(f"/v2/comment/{comment_id}")
    
    async def get_task_comments(
        self,
        task_id: str,
        custom_task_ids: Optional[bool] = None,
        team_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get comments for a task.
        
        Args:
            task_id: Task ID
            custom_task_ids: If true, task_id is a custom task ID
            team_id: Team ID (required if custom_task_ids is true)
            
        Returns:
            Comments data
        """
        params = {}
        if custom_task_ids is not None:
            params["custom_task_ids"] = custom_task_ids
        if team_id is not None:
            params["team_id"] = team_id
        
        return await self.client.get(f"/v2/task/{task_id}/comment", params=params)
    
    async def create_task_comment(
        self,
        task_id: str,
        comment_text: str,
        assignee: Optional[str] = None,
        notify_all: Optional[bool] = None,
        custom_task_ids: Optional[bool] = None,
        team_id: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a comment on a task.
        
        Args:
            task_id: Task ID
            comment_text: Comment text
            assignee: Assignee user ID
            notify_all: Notify all assignees
            custom_task_ids: If true, task_id is a custom task ID
            team_id: Team ID (required if custom_task_ids is true)
            **kwargs: Additional fields
            
        Returns:
            Created comment data
        """
        params = {}
        if custom_task_ids is not None:
            params["custom_task_ids"] = custom_task_ids
        if team_id is not None:
            params["team_id"] = team_id
        
        data = {"comment_text": comment_text}
        if assignee is not None:
            data["assignee"] = assignee
        if notify_all is not None:
            data["notify_all"] = notify_all
        
        data.update(kwargs)
        
        return await self.client.post(f"/v2/task/{task_id}/comment", json_data=data, params=params)
    
    async def reply_to_comment(
        self,
        comment_id: str,
        comment_text: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Reply to a comment.
        
        Args:
            comment_id: Comment ID to reply to
            comment_text: Reply text
            **kwargs: Additional fields
            
        Returns:
            Reply comment data
        """
        data = {"comment_text": comment_text}
        data.update(kwargs)
        
        return await self.client.post(f"/v2/comment/{comment_id}/reply", json_data=data)

