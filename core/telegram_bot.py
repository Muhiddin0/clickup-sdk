"""
Telegram bot utilities for sending messages and documents.
"""

import requests
from typing import Optional, List, Dict, Any, Union

from config.settings import get_settings
from core.logging_config import get_logger

logger = get_logger(__name__)

REQUEST_TIMEOUT = 10


def create_inline_keyboard(buttons: List[List[Dict[str, str]]]) -> Dict[str, Any]:
    """
    Create inline keyboard markup for Telegram.

    Args:
        buttons: List of button rows, each row is a list of button dicts
                 Example: [[{"text": "Open", "url": "https://..."}],
                          [{"text": "Done", "callback_data": "done"}]]

    Returns:
        Inline keyboard markup dict
    """
    return {"inline_keyboard": buttons}


def send_message(
    chat_id: Union[int, str],
    text: str,
    reply_markup: Optional[Dict[str, Any]] = None,
    parse_mode: str = "HTML",
) -> bool:
    """
    Send message to Telegram chat.

    Args:
        chat_id: Telegram chat ID
        text: Message text
        reply_markup: Optional inline keyboard markup
        parse_mode: Parse mode (HTML or Markdown)

    Returns:
        True if message was sent successfully, False otherwise
    """
    if not text:
        logger.warning(f"Attempted to send empty message to chat {chat_id}")
        return False

    settings = get_settings()
    telegram_api_url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"

    payload: Dict[str, Any] = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
    }

    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        resp = requests.post(telegram_api_url, json=payload, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()

        response_data = resp.json()

        if response_data.get("ok"):
            logger.debug(f"✅ Message sent successfully to chat {chat_id}")
            return True
        else:
            error_description = response_data.get("description", "Unknown error")
            logger.error(
                f"❌ Telegram API error for chat {chat_id}: {error_description}"
            )
            return False

    except requests.exceptions.Timeout:
        logger.error(f"⏱️ Timeout while sending message to chat {chat_id}")
        return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Request error while sending message to chat {chat_id}: {e}")
        return False
    except Exception as e:
        logger.error(
            f"❌ Unexpected error while sending message to chat {chat_id}: {e}",
            exc_info=True,
        )
        return False


def send_document_from_url(
    chat_id: Union[int, str],
    file_url: str,
    caption: Optional[str] = None,
    reply_markup: Optional[Dict[str, Any]] = None,
    parse_mode: str = "HTML",
    disable_content_type_detection: bool = False,
) -> bool:
    """
    Send a document (e.g. PDF) to Telegram chat using a direct URL.

    Telegram'ning sendDocument metodi `document` parametriga:
      - HTTP(S) URL
      - yoki allaqachon yuklangan faylning file_id
    qabul qiladi. Biz bu funksiya orqali URL yuboramiz.

    Args:
        chat_id: Telegram chat ID
        file_url: HTTP(S) URL yoki file_id
        caption: Optional caption text
        reply_markup: Optional inline keyboard markup
        parse_mode: Caption parse mode (HTML or Markdown)
        disable_content_type_detection: Telegram'ga kontent turini aniqlamaslikni aytish

    Returns:
        True if document was sent successfully, False otherwise
    """
    if not file_url:
        logger.warning(f"Attempted to send empty file_url to chat {chat_id}")
        return False

    settings = get_settings()
    telegram_api_url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendDocument"

    payload: Dict[str, Any] = {
        "chat_id": chat_id,
        "document": file_url,  # URL yoki file_id
        "parse_mode": parse_mode,
    }

    if caption:
        payload["caption"] = caption

    if reply_markup:
        payload["reply_markup"] = reply_markup

    if disable_content_type_detection:
        payload["disable_content_type_detection"] = True

    try:
        # URL yoki file_id yuborayotganimiz uchun json= kifoya (multipart shart emas)
        resp = requests.post(telegram_api_url, json=payload, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()

        response_data = resp.json()

        if response_data.get("ok"):
            logger.debug(
                f"✅ Document sent successfully to chat {chat_id} from URL: {file_url}"
            )
            return True
        else:
            error_description = response_data.get("description", "Unknown error")
            logger.error(
                f"❌ Telegram API error while sending document to chat {chat_id}: "
                f"{error_description}"
            )
            return False

    except requests.exceptions.Timeout:
        logger.error(f"⏱️ Timeout while sending document to chat {chat_id}")
        return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Request error while sending document to chat {chat_id}: {e}")
        return False
    except Exception as e:
        logger.error(
            f"❌ Unexpected error while sending document to chat {chat_id}: {e}",
            exc_info=True,
        )
        return False
