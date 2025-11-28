"""
Webhook handlers for accountant notifications when payment status changes.
"""

from typing import Any, Optional

from clickup_sdk.webhook import WebhookEvent, status_changed

from clickup.savdo.when_buxgalter_get_money.components import (
    create_accountant_keyboard,
    create_accountant_message,
)
from core.dispatcher import dispatcher
from core.clickup_client import get_clickup_client
from core.logging_config import get_logger
from core.telegram_bot import send_message
from utils.get_curstom_field_value import get_custom_field_value

logger = get_logger(__name__)

ACCOUNTANT_RELATION_FIELD = "Bug'galter | Summa"
TELEGRAM_FIELD = "telegram_id"


def extract_relation_task_id(value: Any) -> Optional[str]:
    """
    Extract relation task ID from field value.

    Args:
        value: Value returned by get_custom_field_value for relationship field

    Returns:
        Relation task ID string or None if extraction fails
    """
    if isinstance(value, list) and value:
        first_item = value[0]
        if isinstance(first_item, dict) and "id" in first_item:
            return str(first_item["id"])
        return str(first_item)

    if isinstance(value, dict):
        if "id" in value:
            return str(value["id"])
        if len(value) == 1:
            return str(list(value.values())[0])

    if isinstance(value, str):
        return value

    return None


def normalize_chat_id(raw_chat_id: Any) -> Any:
    """
    Normalize chat ID to int when possible.
    """
    if raw_chat_id is None:
        return None

    try:
        return int(str(raw_chat_id).strip())
    except (ValueError, TypeError):
        return str(raw_chat_id).strip()


@dispatcher.on("taskStatusUpdated", status_changed(to_status="pul tushishi kutilmoqda"))
async def notify_accountant_on_payment_pending(event: WebhookEvent) -> None:
    """
    Notify accountant when task status switches to "pul tushishi kutilmoqda".
    """
    logger.info(f"💰 Payment pending status detected. Task ID: {event.task_id}")

    clickup_client = get_clickup_client()

    try:
        task = await clickup_client.tasks.get_task(event.task_id)
    except Exception as exc:
        logger.error(f"❌ Failed to fetch task {event.task_id}: {exc}", exc_info=True)
        return

    relation_value = get_custom_field_value(task, ACCOUNTANT_RELATION_FIELD)
    relation_task_id = extract_relation_task_id(relation_value)

    if not relation_task_id:
        logger.warning(
            "⚠️ Could not determine accountant relation task "
            f"for task {event.task_id}"
        )
        return

    try:
        accountant_task = await clickup_client.tasks.get_task(relation_task_id)
    except Exception as exc:
        logger.error(
            f"❌ Failed to fetch accountant task {relation_task_id}: {exc}",
            exc_info=True,
        )
        return

    telegram_id = get_custom_field_value(accountant_task, TELEGRAM_FIELD)
    if not telegram_id:
        logger.warning(
            f"⚠️ No {TELEGRAM_FIELD} found for accountant task {relation_task_id}"
        )
        return

    # Get list information from task
    list_info = task.get("list", {})
    list_id = list_info.get("id", "")
    list_name = list_info.get("name", "N/A")
    
    logger.info(f"📂 Task list: {list_name} (ID: {list_id})")

    message = create_accountant_message(task, accountant_task)
    keyboard = create_accountant_keyboard(
        task.get("url"),
        accountant_task.get("url"),
        event.task_id,
        list_id,
    )

    chat_id = normalize_chat_id(telegram_id)
    if chat_id is None:
        logger.warning(
            f"⚠️ Telegram chat ID invalid for accountant task {relation_task_id}"
        )
        return

    success = send_message(chat_id, message, reply_markup=keyboard)
    if success:
        logger.info(f"✅ Accountant notified for task {event.task_id}")
    else:
        logger.error(f"❌ Failed to notify accountant chat_id={chat_id}")
