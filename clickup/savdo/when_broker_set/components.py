"""
Components for broker message creation and formatting.
"""
from typing import Optional, Dict, List, Union
from datetime import datetime

from core.clickup_client import get_clickup_client
from core.logging_config import get_logger
from utils.get_curstom_field_value import get_custom_field_value

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
    status_name = status.get("status", DEFAULT_VALUE) if isinstance(status, dict) else DEFAULT_VALUE
    
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


def create_broker_keyboard(task_url: str, task_id: str) -> Dict[str, List[List[Dict[str, str]]]]:
    """
    Create inline keyboard for broker message.
    
    Args:
        task_url: ClickUp task URL
        task_id: Task ID for callback data
    
    Returns:
        Inline keyboard markup dictionary
    """
    buttons: List[List[Dict[str, str]]] = [
        [
            {"text": "🔗 Taskni ochish", "url": task_url}
        ],
        [
            {"text": "✅ Lot qo'yildi", "callback_data": f"lot_in_{task_id}"},
        ]
    ]
    
    return {
        "inline_keyboard": buttons
    }