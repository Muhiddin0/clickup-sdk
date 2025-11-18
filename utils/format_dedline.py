"""
Components for broker message creation and formatting.
"""

from typing import Optional, Union
from datetime import datetime

from core.logging_config import get_logger

logger = get_logger(__name__)

# Constants
DEFAULT_VALUE = "N/A"
DATE_FORMAT = "%d.%m.%Y"
MILLISECONDS_TO_SECONDS = 1000


def format_deadline(deadline: Optional[Union[int, str, float]]) -> str:
    """
    Format deadline timestamp to readable date string.

    Args:
        deadline: Deadline value (timestamp in milliseconds or string)

    Returns:
        Formatted date string or default value
    """
    if not deadline:
        return DEFAULT_VALUE

    try:
        if isinstance(deadline, (int, str)):
            timestamp = int(deadline) / MILLISECONDS_TO_SECONDS
            return datetime.fromtimestamp(timestamp).strftime(DATE_FORMAT)
        return str(deadline)
    except (ValueError, TypeError, OSError) as e:
        logger.warning(f"Failed to format deadline {deadline}: {e}")
        return str(deadline)
