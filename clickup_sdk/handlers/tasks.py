"""Tasks API Handler"""
from typing import Optional, Dict, Any, List
from .base import BaseHandler


class TasksHandler(BaseHandler):
    """Handler for Task-related API endpoints."""
    
    async def get_task(
        self,
        task_id: str,
        custom_task_ids: Optional[bool] = None,
        team_id: Optional[int] = None,
        include_subtasks: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Get a task.
        
        Args:
            task_id: Task ID
            custom_task_ids: If true, task_id is a custom task ID
            team_id: Team ID (required if custom_task_ids is true)
            include_subtasks: Include subtasks in response
            
        Returns:
            Task data
        """
        params = {}
        if custom_task_ids is not None:
            params["custom_task_ids"] = custom_task_ids
        if team_id is not None:
            params["team_id"] = team_id
        if include_subtasks is not None:
            params["include_subtasks"] = include_subtasks
            
        return await self.client.get(f"/v2/task/{task_id}", params=params)
    
    async def update_task(
        self,
        task_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[int] = None,
        due_date: Optional[int] = None,
        due_date_time: Optional[bool] = None,
        parent: Optional[str] = None,
        time_estimate: Optional[int] = None,
        start_date: Optional[int] = None,
        start_date_time: Optional[bool] = None,
        assignees: Optional[List[str]] = None,
        archived: Optional[bool] = None,
        custom_task_ids: Optional[bool] = None,
        team_id: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update a task.
        
        Args:
            task_id: Task ID
            name: Task name
            description: Task description
            status: Task status
            priority: Task priority (1-4)
            due_date: Due date (Unix timestamp in milliseconds)
            due_date_time: Whether due date includes time
            parent: Parent task ID
            time_estimate: Time estimate in milliseconds
            start_date: Start date (Unix timestamp in milliseconds)
            start_date_time: Whether start date includes time
            assignees: List of assignee user IDs
            archived: Whether task is archived
            custom_task_ids: If true, task_id is a custom task ID
            team_id: Team ID (required if custom_task_ids is true)
            **kwargs: Additional task fields
            
        Returns:
            Updated task data
        """
        params = {}
        if custom_task_ids is not None:
            params["custom_task_ids"] = custom_task_ids
        if team_id is not None:
            params["team_id"] = team_id
        
        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if status is not None:
            data["status"] = status
        if priority is not None:
            data["priority"] = priority
        if due_date is not None:
            data["due_date"] = due_date
        if due_date_time is not None:
            data["due_date_time"] = due_date_time
        if parent is not None:
            data["parent"] = parent
        if time_estimate is not None:
            data["time_estimate"] = time_estimate
        if start_date is not None:
            data["start_date"] = start_date
        if start_date_time is not None:
            data["start_date_time"] = start_date_time
        if assignees is not None:
            data["assignees"] = assignees
        if archived is not None:
            data["archived"] = archived
        
        data.update(kwargs)
        
        return await self.client.put(f"/v2/task/{task_id}", json_data=data, params=params)
    
    async def delete_task(
        self,
        task_id: str,
        custom_task_ids: Optional[bool] = None,
        team_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Delete a task.
        
        Args:
            task_id: Task ID
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
            
        return await self.client.delete(f"/v2/task/{task_id}", params=params)
    
    async def get_tasks(
        self,
        list_id: Optional[str] = None,
        team_id: Optional[int] = None,
        archived: Optional[bool] = None,
        page: Optional[int] = None,
        order_by: Optional[str] = None,
        reverse: Optional[bool] = None,
        subtasks: Optional[bool] = None,
        statuses: Optional[List[str]] = None,
        include_closed: Optional[bool] = None,
        assignees: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        due_date_gt: Optional[int] = None,
        due_date_lt: Optional[int] = None,
        date_created_gt: Optional[int] = None,
        date_created_lt: Optional[int] = None,
        date_updated_gt: Optional[int] = None,
        date_updated_lt: Optional[int] = None,
        custom_fields: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Get tasks.
        
        Args:
            list_id: List ID (optional)
            team_id: Team ID (required if list_id is not provided)
            archived: Include archived tasks
            page: Page number (0 indexed)
            order_by: Order by field (id, created, updated, due_date)
            reverse: Reverse order
            subtasks: Include subtasks
            statuses: Filter by statuses
            include_closed: Include closed tasks
            assignees: Filter by assignees
            tags: Filter by tags
            due_date_gt: Due date greater than (Unix timestamp)
            due_date_lt: Due date less than (Unix timestamp)
            date_created_gt: Created date greater than (Unix timestamp)
            date_created_lt: Created date less than (Unix timestamp)
            date_updated_gt: Updated date greater than (Unix timestamp)
            date_updated_lt: Updated date less than (Unix timestamp)
            custom_fields: Custom field filters
            
        Returns:
            Tasks data
        """
        if list_id:
            endpoint = f"/v2/list/{list_id}/task"
        elif team_id:
            endpoint = f"/v2/team/{team_id}/task"
        else:
            raise ValueError("Either list_id or team_id must be provided")
        
        params = {}
        if archived is not None:
            params["archived"] = archived
        if page is not None:
            params["page"] = page
        if order_by is not None:
            params["order_by"] = order_by
        if reverse is not None:
            params["reverse"] = reverse
        if subtasks is not None:
            params["subtasks"] = subtasks
        if statuses is not None:
            params["statuses[]"] = statuses
        if include_closed is not None:
            params["include_closed"] = include_closed
        if assignees is not None:
            params["assignees[]"] = assignees
        if tags is not None:
            params["tags[]"] = tags
        if due_date_gt is not None:
            params["due_date_gt"] = due_date_gt
        if due_date_lt is not None:
            params["due_date_lt"] = due_date_lt
        if date_created_gt is not None:
            params["date_created_gt"] = date_created_gt
        if date_created_lt is not None:
            params["date_created_lt"] = date_created_lt
        if date_updated_gt is not None:
            params["date_updated_gt"] = date_updated_gt
        if date_updated_lt is not None:
            params["date_updated_lt"] = date_updated_lt
        if custom_fields is not None:
            params["custom_fields"] = custom_fields
        
        return await self.client.get(endpoint, params=params)
    
    async def create_task(
        self,
        list_id: str,
        name: str,
        description: Optional[str] = None,
        assignees: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        status: Optional[str] = None,
        priority: Optional[int] = None,
        due_date: Optional[int] = None,
        due_date_time: Optional[bool] = None,
        time_estimate: Optional[int] = None,
        start_date: Optional[int] = None,
        start_date_time: Optional[bool] = None,
        notify_all: Optional[bool] = None,
        parent: Optional[str] = None,
        links_to: Optional[str] = None,
        check_required_custom_fields: Optional[bool] = None,
        custom_task_ids: Optional[bool] = None,
        team_id: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a task.
        
        Args:
            list_id: List ID
            name: Task name
            description: Task description
            assignees: List of assignee user IDs
            tags: List of tag names
            status: Task status
            priority: Task priority (1-4)
            due_date: Due date (Unix timestamp in milliseconds)
            due_date_time: Whether due date includes time
            time_estimate: Time estimate in milliseconds
            start_date: Start date (Unix timestamp in milliseconds)
            start_date_time: Whether start date includes time
            notify_all: Notify all assignees
            parent: Parent task ID
            links_to: Task ID to link to
            check_required_custom_fields: Check required custom fields
            custom_task_ids: If true, use custom task IDs
            team_id: Team ID (required if custom_task_ids is true)
            **kwargs: Additional task fields
            
        Returns:
            Created task data
        """
        params = {}
        if custom_task_ids is not None:
            params["custom_task_ids"] = custom_task_ids
        if team_id is not None:
            params["team_id"] = team_id
        
        data = {"name": name}
        if description is not None:
            data["description"] = description
        if assignees is not None:
            data["assignees"] = assignees
        if tags is not None:
            data["tags"] = tags
        if status is not None:
            data["status"] = status
        if priority is not None:
            data["priority"] = priority
        if due_date is not None:
            data["due_date"] = due_date
        if due_date_time is not None:
            data["due_date_time"] = due_date_time
        if time_estimate is not None:
            data["time_estimate"] = time_estimate
        if start_date is not None:
            data["start_date"] = start_date
        if start_date_time is not None:
            data["start_date_time"] = start_date_time
        if notify_all is not None:
            data["notify_all"] = notify_all
        if parent is not None:
            data["parent"] = parent
        if links_to is not None:
            data["links_to"] = links_to
        if check_required_custom_fields is not None:
            data["check_required_custom_fields"] = check_required_custom_fields
        
        data.update(kwargs)
        
        return await self.client.post(f"/v2/list/{list_id}/task", json_data=data, params=params)
    
    async def get_time_in_status(self, task_id: str) -> Dict[str, Any]:
        """Get time in status for a task."""
        return await self.client.get(f"/v2/task/{task_id}/time_in_status")
    
    async def merge_tasks(
        self,
        task_id: str,
        task_ids_to_merge: List[str],
        custom_task_ids: Optional[bool] = None,
        team_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Merge tasks.
        
        Args:
            task_id: Target task ID
            task_ids_to_merge: List of task IDs to merge
            custom_task_ids: If true, use custom task IDs
            team_id: Team ID (required if custom_task_ids is true)
            
        Returns:
            Merge response
        """
        params = {}
        if custom_task_ids is not None:
            params["custom_task_ids"] = custom_task_ids
        if team_id is not None:
            params["team_id"] = team_id
        
        data = {"task_ids_to_merge": task_ids_to_merge}
        return await self.client.post(f"/v2/task/{task_id}/merge", json_data=data, params=params)

