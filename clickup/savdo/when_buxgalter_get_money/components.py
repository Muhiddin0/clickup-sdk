"""
Components for accountant notification messages.
"""

from typing import Any, Dict, List, Optional

from core.logging_config import get_logger
from utils.format_currency import format_currency
from utils.format_dedline import format_deadline
from utils.get_curstom_field_value import get_custom_field_value

logger = get_logger(__name__)


DEFAULT_VALUE = "N/A"
PAYMENT_AMOUNT_FIELDS: List[str] = [
    "Summa",
    "Summa (UZS)",
    "Summa UZS",
    "💰 summa",
    "💸 summa",
    "💵 lot chiqishi",
    "💸 lot qo'yilishi",
]


def resolve_payment_amount(
    main_task: Dict[str, Any], payment_task: Dict[str, Any]
) -> str:
    """
    Attempt to resolve payment amount from predefined custom fields.

    Args:
        main_task: Original ClickUp task dictionary
        payment_task: Related ClickUp task that stores payment info

    Returns:
        Formatted payment amount or default value string
    """
    for field_name in PAYMENT_AMOUNT_FIELDS:
        value = get_custom_field_value(payment_task, field_name)
        if value:
            return format_currency(value)

        value = get_custom_field_value(main_task, field_name)
        if value:
            return format_currency(value)

    return DEFAULT_VALUE


def create_accountant_message(
    main_task: Dict[str, Any], payment_task: Dict[str, Any]
) -> str:
    """
    Build notification message for accountants.

    Args:
        main_task: Original ClickUp task dictionary
        payment_task: Related ClickUp task that stores payment info

    Returns:
        Formatted message string
    """
    task_name = main_task.get("name", DEFAULT_VALUE)
    status = main_task.get("status", {})
    status_name = (
        status.get("status", DEFAULT_VALUE)
        if isinstance(status, dict)
        else DEFAULT_VALUE
    )
    list_name = main_task.get("list", {}).get("name", DEFAULT_VALUE)

    payment_title = payment_task.get("name", DEFAULT_VALUE)
    payment_amount = resolve_payment_amount(main_task, payment_task)

    payment_deadline = payment_task.get("due_date") or main_task.get("due_date")
    deadline_text = format_deadline(payment_deadline)

    message = f"""💰 Pul tushishi kutilmoqda!

📌 Asosiy ish: {task_name}
📂 List: {list_name}
📊 Status: {status_name}

🧾 Summa yozuvi: {payment_title}
💵 Kutilayotgan summa: {payment_amount}
📅 To'lov muddati: {deadline_text}
"""
    return message


def create_accountant_keyboard(
    task_url: Optional[str], payment_task_url: Optional[str], task_id: str, list_id: str
) -> Dict[str, List[List[Dict[str, str]]]]:
    """
    Create inline keyboard for accountant message.

    Args:
        task_url: Main ClickUp task URL
        payment_task_url: Related payment task URL
        task_id: Main task ID for callback data
        list_id: List ID for callback data

    Returns:
        Inline keyboard markup dictionary
    """
    buttons: List[List[Dict[str, str]]] = []

    buttons.append(
        [
            {
                "text": "✅ Pul qabul qilindi",
                "callback_data": f"payment_received={task_id}&list_id={list_id}",
            }
        ]
    )

    return {"inline_keyboard": buttons}
