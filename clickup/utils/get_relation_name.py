"""
Components for broker message creation and formatting.
"""

from typing import Optional, Dict, List, Union

from core.logging_config import get_logger

logger = get_logger(__name__)

# Constants
DEFAULT_VALUE = "N/A"
DATE_FORMAT = "%d.%m.%Y"


def get_relationship_name(custom_field_value: Optional[Union[Dict, List, str]]) -> str:
    """
    Extract name from relationship field value.

    Args:
        custom_field_value: Relationship field value (can be dict, list, or string)

    Returns:
        Name from relationship field or default value
    """
    if not custom_field_value:
        return DEFAULT_VALUE

    if isinstance(custom_field_value, list):
        if len(custom_field_value) > 0:
            first_item = custom_field_value[0]
            if isinstance(first_item, dict):
                return first_item.get("name", DEFAULT_VALUE)
            return str(first_item)
        return DEFAULT_VALUE

    if isinstance(custom_field_value, dict):
        return custom_field_value.get("name", DEFAULT_VALUE)

    return str(custom_field_value)
