"""
Webhook handlers for Dogovor field changes in ClickUp tasks.
"""

from typing import Optional, Any

from .components import (
    create_message,
    create_keyboard,
)
from clickup_sdk.webhook import (
    CustomFieldFilter,
    custom_field_set,
    custom_field_removed,
    WebhookEvent,
)
from core.dispatcher import dispatcher
from core.clickup_client import get_clickup_client
from core.telegram_bot import send_document_from_url
from utils.get_curstom_field_value import get_custom_field_value
from core.logging_config import get_logger
from config.config import Config

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


# Dogovor ma'lumot joylanganda
@dispatcher.on("taskUpdated", custom_field_set(field_name="Dogovor"))
async def handle_dogovor_set(event: WebhookEvent) -> None:
    """
    Handle Dogovor field being set (assigned).

    Args:
        event: Webhook event containing task update information
    """
    logger.info(f"🎯 Dogovor belgilandi! Task ID: {event.task_id}")

    if not event.history_items:
        logger.warning(f"No history items found for task {event.task_id}")
        return

    for item in event.history_items:
        before = item.get("before", {})
        after = item.get("after", {})

        logger.info(f"  Dogovor: {before} → {after}")

        # Extract relation task ID
        dogovor_url = after
        if not dogovor_url:
            logger.warning(f"Could not extract dogovor url from: {after}")
            continue

        logger.info(f"  Dogovor url: {dogovor_url}")

        # Get relation task (Dogovor) and send message
        clickup_client = get_clickup_client()

        task = await clickup_client.tasks.get_task(event.task_id)
        buxgalter_relation = get_custom_field_value(task, "Bug'galter | Document")
        buxgalter = await clickup_client.tasks.get_task(buxgalter_relation[0]["id"])
        telegram_id = get_custom_field_value(buxgalter, "telegram_id")

        if not telegram_id:
            logger.warning(f"⚠️ No telegram_id found for Dogovor task {task}")
            continue

        logger.info(f"  Telegram ID: {telegram_id}")

        # Get list information from task
        list_info = task.get("list", {})
        list_id = list_info.get("id", "")
        list_name = list_info.get("name", "N/A")

        logger.info(f"📂 Task list: {list_name} (ID: {list_id})")

        # Create formatted message from main task
        message = await create_message(event.task_id)

        # Create inline keyboard with task_id and list_id
        keyboard = create_keyboard(event.task_id, list_id)

        print(
            f"🔍 ~ handle_dogovor_set ~ clickup/savdo/when_broker_set_dogovor/when_broker_set_dogovor.py:107 ~ {event}:"
        )

        # Send message to Dogovor with inline keyboard
        success = send_document_from_url(
            caption=message,
            chat_id=telegram_id,
            file_url="https://www.eta.gov.eg/sites/default/files/2020-12/pdf-test.pdf",
            reply_markup=keyboard,
        )
        if success:
            logger.info(f"✅ Message sent to Dogovor (Telegram ID: {telegram_id})")
        else:
            logger.error(f"❌ Failed to send message to Telegram ID {telegram_id}")


# Dogovor ma'lumot olib tashlanganda
@dispatcher.on("taskUpdated", custom_field_removed(field_name="Dogovor"))
async def handle_dogovor_removed(event: WebhookEvent) -> None:
    """
    Handle Dogovor field being removed.

    Args:
        event: Webhook event containing task update information
    """
    logger.info(f"🗑️ Dogovor olib tashlandi! Task ID: {event.task_id}")

    if event.history_items:
        for item in event.history_items:
            before = item.get("before", {})
            after = item.get("after", {})
            logger.info(f"  Dogovor: {before} → {after}")

    logger.info(f"✅ Dogovor olib tashlandi: {event.task_id}")


# Dogovor ma'lumot yangilanganda (optional - agar kerak bo'lsa)
@dispatcher.on(
    "taskUpdated",
    CustomFieldFilter(
        field_name="Dogovor", on_set=False, on_remove=False, on_update=True
    ),
)
async def handle_dogovor_update(event: WebhookEvent) -> None:
    """
    Handle Dogovor field being updated (not set or removed, just updated).

    Args:
        event: Webhook event containing task update information
    """
    logger.info(f"🔄 Dogovor yangilandi! Task ID: {event.task_id}")

    if event.history_items:
        for item in event.history_items:
            before = item.get("before", {})
            after = item.get("after", {})
            logger.info(f"  Dogovor: {before} → {after}")

    logger.info(f"✅ Dogovor yangilandi: {event.task_id}")
