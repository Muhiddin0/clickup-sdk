"""Webhook Event Filters - aiogram style filters"""

from typing import Optional, Callable, Dict, Any, List
from abc import ABC, abstractmethod
import logging
import json

from .events import WebhookEvent

logger = logging.getLogger(__name__)


class Filter(ABC):
    """Base filter class"""

    @abstractmethod
    async def check(self, event: WebhookEvent) -> bool:
        """
        Check if event matches filter.

        Args:
            event: Webhook event

        Returns:
            True if event matches, False otherwise
        """
        pass


class CustomFieldFilter(Filter):
    """Filter for custom field changes"""

    def __init__(
        self,
        field_id: Optional[str] = None,
        field_name: Optional[str] = None,
        on_set: bool = True,
        on_remove: bool = True,
        on_update: bool = True,
    ):
        """
        Initialize custom field filter.

        Args:
            field_id: Custom field ID to filter by
            field_name: Custom field name to filter by (alternative to field_id)
            on_set: Filter when value is set (before empty/None, after has value). Default: True
            on_remove: Filter when value is removed (before has value, after empty/None). Default: True
            on_update: Filter when value is updated (both before and after have values). Default: True
        """
        if not field_id and not field_name:
            raise ValueError("Either field_id or field_name must be provided")

        self.field_id = field_id
        self.field_name = field_name
        self.on_set = on_set
        self.on_remove = on_remove
        self.on_update = on_update

    def _is_empty(self, value) -> bool:
        """Check if value is considered empty"""
        if value is None:
            return True
        if isinstance(value, (list, dict, str)):
            return len(value) == 0
        if isinstance(value, (int, float)):
            return False  # Numbers are never empty
        return not bool(value)

    def _is_filled(self, value) -> bool:
        """Check if value is considered filled"""
        return not self._is_empty(value)

    def _check_change_type(self, before, after) -> Optional[str]:
        """
        Determine the type of change: 'set', 'remove', or 'update'

        Returns:
            'set' if value was set (before empty, after filled)
            'remove' if value was removed (before filled, after empty)
            'update' if value was updated (both filled)
            None if no clear change type
        """
        before_empty = self._is_empty(before)
        after_empty = self._is_empty(after)

        if before_empty and self._is_filled(after):
            return "set"
        elif self._is_filled(before) and after_empty:
            return "remove"
        elif self._is_filled(before) and self._is_filled(after):
            return "update"
        return None

    async def check(self, event: WebhookEvent) -> bool:
        """Check if custom field changed"""
        if event.event != "taskUpdated":
            return False

        if not event.history_items:
            return False

        for item in event.history_items:
            field = item.get("field", "")
            field_id = item.get("field_id") or item.get("id")
            before = item.get("before", {})
            after = item.get("after", {})

            # Determine change type
            change_type = self._check_change_type(before, after)

            # Check if this change type should be filtered
            if change_type == "set" and not self.on_set:
                continue
            if change_type == "remove" and not self.on_remove:
                continue
            if change_type == "update" and not self.on_update:
                continue

            # Check by field ID
            if self.field_id:
                target_id = str(self.field_id).strip()

                # Direct field_id match in item root
                if field_id and str(field_id).strip() == target_id:
                    return True
                if item.get("id") and str(item.get("id")).strip() == target_id:
                    return True

                # Check if field_id is in the field string
                if field and target_id in str(field):
                    return True

                # Helper function to recursively search for field_id
                def find_field_id_in_dict(d, target):
                    """Recursively search for field_id in dictionary"""
                    if not isinstance(d, dict):
                        return False

                    # Check direct id fields
                    for key in ["id", "field_id", "custom_field_id"]:
                        if key in d and str(d[key]).strip() == target:
                            return True

                    # Check nested custom_field structure
                    if "custom_field" in d and isinstance(d["custom_field"], dict):
                        cf = d["custom_field"]
                        for key in ["id", "field_id", "custom_field_id"]:
                            if key in cf and str(cf[key]).strip() == target:
                                return True

                    # Recursively check nested dictionaries
                    for value in d.values():
                        if isinstance(value, dict):
                            if find_field_id_in_dict(value, target):
                                return True
                        elif isinstance(value, list):
                            for elem in value:
                                if isinstance(elem, dict):
                                    if find_field_id_in_dict(elem, target):
                                        return True

                    return False

                # Check in after dict
                if isinstance(after, dict):
                    if find_field_id_in_dict(after, target_id):
                        return True

                # Check in before dict
                if isinstance(before, dict):
                    if find_field_id_in_dict(before, target_id):
                        return True

                # Deep search in entire item (as last resort)
                item_str = json.dumps(item, default=str)
                if target_id in item_str:
                    return True

            # Check by field name
            if self.field_name:
                search_name = self.field_name.lower().strip()

                # Direct field name match (case insensitive, substring match)
                if field:
                    field_lower = field.lower().strip()
                    if (
                        search_name == field_lower
                        or search_name in field_lower
                        or field_lower in search_name
                    ):
                        return True

                # Check after dict
                if isinstance(after, dict):
                    # Check name field
                    if after.get("name"):
                        name_lower = str(after.get("name", "")).lower().strip()
                        if (
                            search_name == name_lower
                            or search_name in name_lower
                            or name_lower in search_name
                        ):
                            return True
                    # Check label field (some custom fields use label)
                    if after.get("label"):
                        label_lower = str(after.get("label", "")).lower().strip()
                        if (
                            search_name == label_lower
                            or search_name in label_lower
                            or label_lower in search_name
                        ):
                            return True
                    # Check value field if it contains name
                    if after.get("value"):
                        value_str = str(after.get("value", "")).lower()
                        if search_name in value_str:
                            return True

                # Check before dict
                if isinstance(before, dict):
                    if before.get("name"):
                        name_lower = str(before.get("name", "")).lower().strip()
                        if (
                            search_name == name_lower
                            or search_name in name_lower
                            or name_lower in search_name
                        ):
                            return True
                    if before.get("label"):
                        label_lower = str(before.get("label", "")).lower().strip()
                        if (
                            search_name == label_lower
                            or search_name in label_lower
                            or label_lower in search_name
                        ):
                            return True

                # Check if field name is in the entire item structure (deep search)
                item_str = json.dumps(item, default=str).lower()
                if search_name in item_str:
                    return True

        return False


class TaskStatusFilter(Filter):
    """Filter for specific task status changes"""

    def __init__(
        self, from_status: Optional[str] = None, to_status: Optional[str] = None
    ):
        """
        Initialize task status filter.

        Args:
            from_status: Previous status (optional)
            to_status: New status (optional)
        """
        self.from_status = from_status
        self.to_status = to_status

    @staticmethod
    def _extract_status(value: Any) -> str:
        """
        Normalize status value from ClickUp history items.

        Args:
            value: History item value (dict, str, etc.)

        Returns:
            Status string (lowercase) or empty string
        """
        if not value:
            return ""

        if isinstance(value, dict):
            status_data = value.get("status")
            if isinstance(status_data, dict):
                return str(status_data.get("status", "")).strip()
            if isinstance(status_data, str):
                return status_data.strip()
            # Sometimes ClickUp sends direct value without nested status dict
            return str(value.get("status", "")).strip()

        if isinstance(value, str):
            return value.strip()

        return str(value).strip()

    async def check(self, event: WebhookEvent) -> bool:
        """Check if status changed to/from specified status"""
        if event.event != "taskStatusUpdated":
            return False

        if not event.history_items:
            return False

        for item in event.history_items:
            before = item.get("before")
            after = item.get("after")

            old_status = self._extract_status(before).lower()
            new_status = self._extract_status(after).lower()

            # Check from_status
            if self.from_status and old_status != self.from_status.lower():
                continue

            # Check to_status
            if self.to_status and new_status != self.to_status.lower():
                continue

            return True

        return False


class TaskAssigneeFilter(Filter):
    """Filter for task assignee changes"""

    def __init__(self, user_id: Optional[str] = None):
        """
        Initialize task assignee filter.

        Args:
            user_id: User ID to filter by (optional, if None checks any assignee change)
        """
        self.user_id = user_id

    async def check(self, event: WebhookEvent) -> bool:
        """Check if assignee changed"""
        if event.event != "taskAssigneeUpdated":
            return False

        if not self.user_id:
            return True  # Any assignee change

        if not event.history_items:
            return False

        for item in event.history_items:
            after = item.get("after", {})
            if isinstance(after, dict):
                assignees = after.get("assignees", [])
                if isinstance(assignees, list):
                    for assignee in assignees:
                        if (
                            isinstance(assignee, dict)
                            and assignee.get("id") == self.user_id
                        ):
                            return True
                        if assignee == self.user_id:
                            return True

        return False


class EventTypeFilter(Filter):
    """Filter for specific event types"""

    def __init__(self, event_types: List[str]):
        """
        Initialize event type filter.

        Args:
            event_types: List of event types to match
        """
        self.event_types = [e.lower() for e in event_types]

    async def check(self, event: WebhookEvent) -> bool:
        """Check if event type matches"""
        return event.event.lower() in self.event_types


class CombinedFilter(Filter):
    """Combine multiple filters with AND/OR logic"""

    def __init__(self, filters: List[Filter], logic: str = "AND"):
        """
        Initialize combined filter.

        Args:
            filters: List of filters to combine
            logic: "AND" or "OR" logic
        """
        self.filters = filters
        self.logic = logic.upper()

        if self.logic not in ["AND", "OR"]:
            raise ValueError("Logic must be 'AND' or 'OR'")

    async def check(self, event: WebhookEvent) -> bool:
        """Check if event matches combined filters"""
        if not self.filters:
            return True

        results = []
        for filter_obj in self.filters:
            result = await filter_obj.check(event)
            results.append(result)

        if self.logic == "AND":
            return all(results)
        else:  # OR
            return any(results)


# Convenience functions
def custom_field_changed(
    field_id: Optional[str] = None,
    field_name: Optional[str] = None,
    on_set: bool = True,
    on_remove: bool = True,
    on_update: bool = True,
) -> CustomFieldFilter:
    """Create custom field filter"""
    return CustomFieldFilter(
        field_id=field_id,
        field_name=field_name,
        on_set=on_set,
        on_remove=on_remove,
        on_update=on_update,
    )


def custom_field_set(
    field_id: Optional[str] = None, field_name: Optional[str] = None
) -> CustomFieldFilter:
    """Create filter for when custom field value is set (only on_set=True)"""
    return CustomFieldFilter(
        field_id=field_id,
        field_name=field_name,
        on_set=True,
        on_remove=False,
        on_update=False,
    )


def custom_field_removed(
    field_id: Optional[str] = None, field_name: Optional[str] = None
) -> CustomFieldFilter:
    """Create filter for when custom field value is removed (only on_remove=True)"""
    return CustomFieldFilter(
        field_id=field_id,
        field_name=field_name,
        on_set=False,
        on_remove=True,
        on_update=False,
    )


def custom_field_updated(
    field_id: Optional[str] = None, field_name: Optional[str] = None
) -> CustomFieldFilter:
    """Create filter for when custom field value is updated (only on_update=True)"""
    return CustomFieldFilter(
        field_id=field_id,
        field_name=field_name,
        on_set=False,
        on_remove=False,
        on_update=True,
    )


def status_changed(
    from_status: Optional[str] = None, to_status: Optional[str] = None
) -> TaskStatusFilter:
    """Create status change filter"""
    return TaskStatusFilter(from_status=from_status, to_status=to_status)


def assignee_changed(user_id: Optional[str] = None) -> TaskAssigneeFilter:
    """Create assignee change filter"""
    return TaskAssigneeFilter(user_id=user_id)
