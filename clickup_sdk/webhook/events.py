"""Webhook Event Types and Models"""
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class WebhookEventType(str, Enum):
    """ClickUp webhook event types"""
    # Task events
    TASK_CREATED = "taskCreated"
    TASK_UPDATED = "taskUpdated"
    TASK_DELETED = "taskDeleted"
    TASK_PRIORITY_UPDATED = "taskPriorityUpdated"
    TASK_STATUS_UPDATED = "taskStatusUpdated"
    TASK_ASSIGNEE_UPDATED = "taskAssigneeUpdated"
    TASK_DUE_DATE_UPDATED = "taskDueDateUpdated"
    TASK_TAG_UPDATED = "taskTagUpdated"
    TASK_MOVED = "taskMoved"
    TASK_COMMENT_POSTED = "taskCommentPosted"
    TASK_COMMENT_UPDATED = "taskCommentUpdated"
    TASK_TIME_ESTIMATE_UPDATED = "taskTimeEstimateUpdated"
    TASK_TIME_TRACKED_UPDATED = "taskTimeTrackedUpdated"
    
    # List events
    LIST_CREATED = "listCreated"
    LIST_UPDATED = "listUpdated"
    LIST_DELETED = "listDeleted"
    
    # Folder events
    FOLDER_CREATED = "folderCreated"
    FOLDER_UPDATED = "folderUpdated"
    FOLDER_DELETED = "folderDeleted"
    
    # Space events
    SPACE_CREATED = "spaceCreated"
    SPACE_UPDATED = "spaceUpdated"
    SPACE_DELETED = "spaceDeleted"
    
    # Goal events
    GOAL_CREATED = "goalCreated"
    GOAL_UPDATED = "goalUpdated"
    GOAL_DELETED = "goalDeleted"
    
    # Key Result events
    KEY_RESULT_CREATED = "keyResultCreated"
    KEY_RESULT_UPDATED = "keyResultUpdated"
    KEY_RESULT_DELETED = "keyResultDeleted"
    
    # Wildcard
    ALL = "*"


@dataclass
class WebhookEvent:
    """Webhook event data model"""
    event: str
    history_items: Optional[list] = None
    task_id: Optional[str] = None
    webhook_id: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebhookEvent":
        """Create WebhookEvent from dictionary"""
        return cls(
            event=data.get("event", ""),
            history_items=data.get("history_items", []),
            task_id=data.get("task_id"),
            webhook_id=data.get("webhook_id")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "event": self.event,
            "history_items": self.history_items or [],
            "task_id": self.task_id,
            "webhook_id": self.webhook_id
        }


@dataclass
class TaskEvent(WebhookEvent):
    """Task-related webhook event"""
    task: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TaskEvent":
        """Create TaskEvent from dictionary"""
        event = super().from_dict(data)
        return cls(
            event=event.event,
            history_items=event.history_items,
            task_id=event.task_id,
            webhook_id=event.webhook_id,
            task=data.get("task")
        )

