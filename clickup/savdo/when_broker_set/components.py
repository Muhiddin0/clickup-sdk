"""
Components for broker message creation and formatting.
"""

from typing import Dict, List

from core.clickup_client import get_clickup_client
from core.logging_config import get_logger
from utils.get_curstom_field_value import get_custom_field_value
from utils.format_currency import format_currency
from utils.format_number import format_number
from utils.format_dedline import format_deadline


from clickup.utils.get_relation_name import get_relationship_name

logger = get_logger(__name__)

# Constants
DEFAULT_VALUE = "N/A"
DATE_FORMAT = "%d.%m.%Y"
MILLISECONDS_TO_SECONDS = 1000


async def create_broker_message(task_id: str) -> str:
    """
    Create formatted message from task data.

    Args:
        task_id: ClickUp task ID

    Returns:
        Formatted message string

    Raises:
        Exception: If task cannot be retrieved or processed
    """
    try:
        clickup_client = get_clickup_client()
        task = await clickup_client.tasks.get_task(task_id)
    except Exception as e:
        logger.error(f"Failed to get task {task_id}: {e}")
        raise

    # Basic task info
    name = task.get("name", DEFAULT_VALUE)
    status = task.get("status", {})
    status_name = (
        status.get("status", DEFAULT_VALUE)
        if isinstance(status, dict)
        else DEFAULT_VALUE
    )

    # Get custom field values
    quantity = get_custom_field_value(task, "🔢 miqdori")
    lot_out = get_custom_field_value(task, "💵 lot chiqishi")
    lot_in = get_custom_field_value(task, "💸 lot qo'yilishi")
    firma = get_custom_field_value(task, "Firma")
    xaridor = get_custom_field_value(task, "Xaridor companiya")
    hamkor = get_custom_field_value(task, "Hamkor companiya")
    hamkor_narx = get_custom_field_value(task, "Hamkordan olinish narxi")
    broker_deadline = get_custom_field_value(task, "📅 broker dedline")

    # Format values
    quantity_formatted = format_number(quantity)
    lot_out_formatted = format_currency(lot_out)
    lot_in_formatted = format_currency(lot_in)
    hamkor_narx_formatted = format_currency(hamkor_narx)

    # Get relationship names
    firma_name = get_relationship_name(firma)
    xaridor_name = get_relationship_name(xaridor)
    hamkor_name = get_relationship_name(hamkor)

    # Format deadline
    deadline_text = format_deadline(broker_deadline)

    # Build message
    message = f"""🆕 Yangi ish bor!

📌 Ish nomi: {name}
📊 Status: {status_name}
📦 Soni: {quantity_formatted}
🏢 Firmamiz: {firma_name}
👤 Xaridor: {xaridor_name}
🤝 Hamkor: {hamkor_name}
💰 Hamkordan olinish narxi: {hamkor_narx_formatted}
📤 Lot chiqishi: {lot_out_formatted}
📥 Lot qo'yilishi: {lot_in_formatted}
📅 Broker dedline: {deadline_text}
"""

    return message


def create_broker_keyboard(
    task_id: str, list_id: str
) -> Dict[str, List[List[Dict[str, str]]]]:
    """
    Create inline keyboard for broker message.

    Args:
        task_id: Task ID for callback data
        list_id: List ID for callback data

    Returns:
        Inline keyboard markup dictionary
    """
    buttons: List[List[Dict[str, str]]] = [
        [
            {
                "text": "✅ Lot qo'yildi",
                "callback_data": f"lot_in={task_id}&list_id={list_id}",
            },
        ],
    ]

    return {"inline_keyboard": buttons}
