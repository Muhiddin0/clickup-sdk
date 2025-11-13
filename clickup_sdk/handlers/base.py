"""Base handler class for ClickUp API handlers"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import ClickUp


class BaseHandler:
    """Base class for all ClickUp API handlers."""
    
    def __init__(self, client: "ClickUp"):
        """
        Initialize handler with ClickUp client.
        
        Args:
            client: ClickUp client instance
        """
        self.client = client

