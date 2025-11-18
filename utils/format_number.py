"""
Components for broker message creation and formatting.
"""

from typing import Optional, Union

from core.logging_config import get_logger

logger = get_logger(__name__)

# Constants
DEFAULT_VALUE = "N/A"
NUMBER_SUFFIX = " ta"


def format_number(value: Optional[Union[int, str, float]]) -> str:
    """
    Format number value with suffix.

    Args:
        value: Number value to format

    Returns:
        Formatted number string with suffix
    """
    if not value:
        return DEFAULT_VALUE
    try:
        return f"{int(value)}{NUMBER_SUFFIX}"
    except (ValueError, TypeError) as e:
        logger.warning(f"Failed to format number value {value}: {e}")
        return str(value)
