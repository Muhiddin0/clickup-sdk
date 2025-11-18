"""
Components for broker message creation and formatting.
"""

from typing import Optional, Union

from core.logging_config import get_logger

logger = get_logger(__name__)


# Constants
DEFAULT_VALUE = "N/A"
CURRENCY_SUFFIX = " UZS"
NUMBER_SUFFIX = " ta"
DATE_FORMAT = "%d.%m.%Y"
MILLISECONDS_TO_SECONDS = 1000


def format_currency(value: Optional[Union[int, str, float]]) -> str:
    """
    Format currency value with spaces.

    Args:
        value: Currency value to format

    Returns:
        Formatted currency string with spaces and UZS suffix
    """
    if not value:
        return DEFAULT_VALUE
    try:
        num = int(value)
        return f"{num:,}".replace(",", " ") + CURRENCY_SUFFIX
    except (ValueError, TypeError) as e:
        logger.warning(f"Failed to format currency value {value}: {e}")
        return str(value)
