"""
Utility function to extract custom field values from ClickUp tasks.
"""

from typing import Optional, Any, Dict, List


def get_custom_field_value(task: Dict[str, Any], field_name: str) -> Optional[Any]:
    """
    Get custom field value from task by field name.

    Args:
        task: ClickUp task dictionary
        field_name: Name of the custom field to retrieve

    Returns:
        Custom field value if found, None otherwise
    """
    if not task or not field_name:
        return None

    custom_fields = task.get("custom_fields", [])
    if not isinstance(custom_fields, list):
        return None

    for cf in custom_fields:
        if not isinstance(cf, dict):
            continue
        if cf.get("name") == field_name:
            return cf.get("value")

    return None
