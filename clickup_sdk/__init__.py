"""
ClickUp SDK - Python library for ClickUp API v2
Similar to aiogram style for easy usage
"""
from .client import ClickUp
from .webhook import WebhookDispatcher, WebhookServer, WebhookEvent

__version__ = "1.0.0"
__all__ = ["ClickUp", "WebhookDispatcher", "WebhookServer", "WebhookEvent"]

