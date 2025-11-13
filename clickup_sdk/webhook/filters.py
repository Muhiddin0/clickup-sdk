"""Webhook Event Filters - aiogram style filters"""
from typing import Optional, Callable, Dict, Any, List
from abc import ABC, abstractmethod
import logging

from .events import WebhookEvent

logger = logging.getLogger(__name__)


class Filter(ABC):
    """Base filter class"""
    
    @abstractmethod
    async def check(self, event: WebhookEvent) -> bool:
        """
        Check if event matches filter.
        
        Args:
            event: Webhook event
            
        Returns:
            True if event matches, False otherwise
        """
        pass


class CustomFieldFilter(Filter):
    """Filter for custom field changes"""
    
    def __init__(self, field_id: Optional[str] = None, field_name: Optional[str] = None):
        """
        Initialize custom field filter.
        
        Args:
            field_id: Custom field ID to filter by
            field_name: Custom field name to filter by (alternative to field_id)
        """
        if not field_id and not field_name:
            raise ValueError("Either field_id or field_name must be provided")
        
        self.field_id = field_id
        self.field_name = field_name
    
    async def check(self, event: WebhookEvent) -> bool:
        """Check if custom field changed"""
        if event.event != "taskUpdated":
            return False
        
        if not event.history_items:
            return False
        
        for item in event.history_items:
            field = item.get("field", "")
            field_id = item.get("field_id") or item.get("id")
            
            # Check by field ID
            if self.field_id:
                # Direct field_id match
                if field_id and str(field_id) == str(self.field_id):
                    return True
                # Check if field_id is in the field string
                if field and str(self.field_id) in str(field):
                    return True
                # Check in custom field structure
                after = item.get("after", {})
                before = item.get("before", {})
                if isinstance(after, dict):
                    # Custom fields might have id field
                    if after.get("id") == self.field_id or after.get("field_id") == self.field_id:
                        return True
                if isinstance(before, dict):
                    if before.get("id") == self.field_id or before.get("field_id") == self.field_id:
                        return True
            
            # Check by field name
            if self.field_name:
                # Direct field name match (case insensitive)
                if field and self.field_name.lower() in field.lower():
                    return True
                # Check in custom field name
                after = item.get("after", {})
                before = item.get("before", {})
                if isinstance(after, dict):
                    # Check name field in custom field structure
                    if after.get("name") and self.field_name.lower() in after.get("name", "").lower():
                        return True
                if isinstance(before, dict):
                    if before.get("name") and self.field_name.lower() in before.get("name", "").lower():
                        return True
        
        return False


class TaskStatusFilter(Filter):
    """Filter for specific task status changes"""
    
    def __init__(self, from_status: Optional[str] = None, to_status: Optional[str] = None):
        """
        Initialize task status filter.
        
        Args:
            from_status: Previous status (optional)
            to_status: New status (optional)
        """
        self.from_status = from_status
        self.to_status = to_status
    
    async def check(self, event: WebhookEvent) -> bool:
        """Check if status changed to/from specified status"""
        if event.event != "taskStatusUpdated":
            return False
        
        if not event.history_items:
            return False
        
        for item in event.history_items:
            before = item.get("before", {})
            after = item.get("after", {})
            
            old_status = before.get("status", {}).get("status", "") if isinstance(before, dict) else ""
            new_status = after.get("status", {}).get("status", "") if isinstance(after, dict) else ""
            
            # Check from_status
            if self.from_status and old_status.lower() != self.from_status.lower():
                continue
            
            # Check to_status
            if self.to_status and new_status.lower() != self.to_status.lower():
                continue
            
            return True
        
        return False


class TaskAssigneeFilter(Filter):
    """Filter for task assignee changes"""
    
    def __init__(self, user_id: Optional[str] = None):
        """
        Initialize task assignee filter.
        
        Args:
            user_id: User ID to filter by (optional, if None checks any assignee change)
        """
        self.user_id = user_id
    
    async def check(self, event: WebhookEvent) -> bool:
        """Check if assignee changed"""
        if event.event != "taskAssigneeUpdated":
            return False
        
        if not self.user_id:
            return True  # Any assignee change
        
        if not event.history_items:
            return False
        
        for item in event.history_items:
            after = item.get("after", {})
            if isinstance(after, dict):
                assignees = after.get("assignees", [])
                if isinstance(assignees, list):
                    for assignee in assignees:
                        if isinstance(assignee, dict) and assignee.get("id") == self.user_id:
                            return True
                        if assignee == self.user_id:
                            return True
        
        return False


class EventTypeFilter(Filter):
    """Filter for specific event types"""
    
    def __init__(self, event_types: List[str]):
        """
        Initialize event type filter.
        
        Args:
            event_types: List of event types to match
        """
        self.event_types = [e.lower() for e in event_types]
    
    async def check(self, event: WebhookEvent) -> bool:
        """Check if event type matches"""
        return event.event.lower() in self.event_types


class CombinedFilter(Filter):
    """Combine multiple filters with AND/OR logic"""
    
    def __init__(self, filters: List[Filter], logic: str = "AND"):
        """
        Initialize combined filter.
        
        Args:
            filters: List of filters to combine
            logic: "AND" or "OR" logic
        """
        self.filters = filters
        self.logic = logic.upper()
        
        if self.logic not in ["AND", "OR"]:
            raise ValueError("Logic must be 'AND' or 'OR'")
    
    async def check(self, event: WebhookEvent) -> bool:
        """Check if event matches combined filters"""
        if not self.filters:
            return True
        
        results = []
        for filter_obj in self.filters:
            result = await filter_obj.check(event)
            results.append(result)
        
        if self.logic == "AND":
            return all(results)
        else:  # OR
            return any(results)


# Convenience functions
def custom_field_changed(field_id: Optional[str] = None, field_name: Optional[str] = None) -> CustomFieldFilter:
    """Create custom field filter"""
    return CustomFieldFilter(field_id=field_id, field_name=field_name)


def status_changed(from_status: Optional[str] = None, to_status: Optional[str] = None) -> TaskStatusFilter:
    """Create status change filter"""
    return TaskStatusFilter(from_status=from_status, to_status=to_status)


def assignee_changed(user_id: Optional[str] = None) -> TaskAssigneeFilter:
    """Create assignee change filter"""
    return TaskAssigneeFilter(user_id=user_id)

