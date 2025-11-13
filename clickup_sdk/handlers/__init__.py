"""ClickUp API Handlers"""
from .tasks import TasksHandler
from .lists import ListsHandler
from .spaces import SpacesHandler
from .folders import FoldersHandler
from .comments import CommentsHandler
from .attachments import AttachmentsHandler
from .custom_fields import CustomFieldsHandler
from .goals import GoalsHandler
from .time_entries import TimeEntriesHandler
from .webhooks import WebhooksHandler
from .users import UsersHandler
from .teams import TeamsHandler

__all__ = [
    "TasksHandler",
    "ListsHandler",
    "SpacesHandler",
    "FoldersHandler",
    "CommentsHandler",
    "AttachmentsHandler",
    "CustomFieldsHandler",
    "GoalsHandler",
    "TimeEntriesHandler",
    "WebhooksHandler",
    "UsersHandler",
    "TeamsHandler",
]

