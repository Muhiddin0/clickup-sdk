"""
Webhook handlers for broker field changes in ClickUp tasks.
"""

from typing import Optional, Any

from clickup.savdo.when_broker_set.components import (
    create_broker_message,
    create_broker_keyboard,
)
from clickup_sdk.webhook import (
    CustomFieldFilter,
    custom_field_set,
    custom_field_removed,
    WebhookEvent,
)
from core.dispatcher import dispatcher
from core.clickup_client import get_clickup_client
from core.telegram_bot import send_message
from utils.get_curstom_field_value import get_custom_field_value
from core.logging_config import get_logger


logger = get_logger(__name__)


def extract_relation_task_id(after: Any) -> Optional[str]:
    """
    Extract relation task ID from various data structures.

    Args:
        after: Value from history item 'after' field

    Returns:
        Relation task ID string or None if extraction fails
    """
    if isinstance(after, list) and len(after) > 0:
        first_item = after[0]
        if isinstance(first_item, dict) and "id" in first_item:
            return str(first_item["id"])
        return str(first_item)

    if isinstance(after, dict):
        if "id" in after:
            return str(after["id"])
        # Sometimes the ID might be the value itself
        if len(after) == 1:
            return str(list(after.values())[0])

    if isinstance(after, str):
        return after

    return None


# Broker ma'lumot joylanganda
@dispatcher.on("taskUpdated", custom_field_set(field_name="Broker"))
async def handle_broker_set(event: WebhookEvent) -> None:

    print("🚀 ~ file: when_broker_set.py:59 ~ event:", event)

    """
    Handle broker field being set (assigned).

    Args:
        event: Webhook event containing task update information
    """
    logger.info(f"🎯 Broker belgilandi! Task ID: {event.task_id}")

    if not event.history_items:
        logger.warning(f"No history items found for task {event.task_id}")
        return

    for item in event.history_items:
        before = item.get("before", {})
        after = item.get("after", {})

        logger.info(f"  Broker: {before} → {after}")

        # Extract relation task ID
        relation_task_id = extract_relation_task_id(after)
        if not relation_task_id:
            logger.warning(f"Could not extract relation task ID from: {after}")
            continue

        logger.info(f"  Relation Task ID: {relation_task_id}")

        # Get relation task (broker) and send message
        try:
            clickup_client = get_clickup_client()
            relation_task = await clickup_client.tasks.get_task(relation_task_id)
            telegram_id = get_custom_field_value(relation_task, "telegram_id")

            if not telegram_id:
                logger.warning(
                    f"⚠️ No telegram_id found for broker task {relation_task_id}"
                )
                continue

            logger.info(f"  Telegram ID: {telegram_id}")

            # Get main task for URL and list information
            main_task = await clickup_client.tasks.get_task(event.task_id)
            task_url = main_task.get("url", "")

            if not task_url:
                logger.warning(f"⚠️ No URL found for main task {event.task_id}")
                continue

            # Get list information from task
            list_info = main_task.get("list", {})
            list_id = list_info.get("id", "")
            list_name = list_info.get("name", "N/A")

            logger.info(f"📂 Task list: {list_name} (ID: {list_id})")

            # Create formatted message from main task
            message = await create_broker_message(event.task_id)

            # Create inline keyboard with task_id and list_id
            keyboard = create_broker_keyboard(event.task_id, list_id)

            # Send message to broker with inline keyboard
            success = send_message(int(telegram_id), message, reply_markup=keyboard)
            if success:
                logger.info(f"✅ Message sent to broker (Telegram ID: {telegram_id})")
            else:
                logger.error(f"❌ Failed to send message to Telegram ID {telegram_id}")

        except Exception as e:
            logger.error(
                f"❌ Error processing broker task {relation_task_id}: {e}",
                exc_info=True,
            )


# Broker ma'lumot olib tashlanganda
@dispatcher.on("taskUpdated", custom_field_removed(field_name="Broker"))
async def handle_broker_removed(event: WebhookEvent) -> None:
    """
    Handle broker field being removed.

    Args:
        event: Webhook event containing task update information
    """
    logger.info(f"🗑️ Broker olib tashlandi! Task ID: {event.task_id}")

    if event.history_items:
        for item in event.history_items:
            before = item.get("before", {})
            after = item.get("after", {})
            logger.info(f"  Broker: {before} → {after}")

    logger.info(f"✅ Broker olib tashlandi: {event.task_id}")


# Broker ma'lumot yangilanganda (optional - agar kerak bo'lsa)
@dispatcher.on(
    "taskUpdated",
    CustomFieldFilter(
        field_name="Broker", on_set=False, on_remove=False, on_update=True
    ),
)
async def handle_broker_updated(event: WebhookEvent) -> None:
    """
    Handle broker field being updated (not set or removed, just updated).

    Args:
        event: Webhook event containing task update information
    """
    logger.info(f"🔄 Broker yangilandi! Task ID: {event.task_id}")

    if event.history_items:
        for item in event.history_items:
            before = item.get("before", {})
            after = item.get("after", {})
            logger.info(f"  Broker: {before} → {after}")

    logger.info(f"✅ Broker yangilandi: {event.task_id}")
