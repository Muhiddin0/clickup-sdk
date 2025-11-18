"""
ClickUp Client - Global client instance with proper initialization.
"""

import logging
from clickup_sdk import ClickUp

from config.settings import get_settings

logger = logging.getLogger(__name__)

# Global ClickUp client instance
_clickup_client: ClickUp | None = None


def get_clickup_client() -> ClickUp:
    """
    Get or create global ClickUp client instance.

    Returns:
        ClickUp client instance
    """
    global _clickup_client
    if _clickup_client is None:
        settings = get_settings()
        _clickup_client = ClickUp(token=settings.CLICKUP_API_TOKEN)
        logger.info("✅ ClickUp client initialized")
    return _clickup_client


# For backward compatibility, create a module-level function
def get_clickup() -> ClickUp:
    """Get ClickUp client (alias for get_clickup_client)."""
    return get_clickup_client()
