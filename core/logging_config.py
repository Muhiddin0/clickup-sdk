"""
Logging configuration and setup.
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from config.settings import get_settings


def setup_logging(log_dir: Optional[str] = None) -> None:
    """
    Setup application-wide logging configuration.
    
    Args:
        log_dir: Directory for log files. If None, uses settings LOG_DIR.
    """
    settings = get_settings()
    log_directory = Path(log_dir or settings.LOG_DIR)
    
    # Create logs directory if it doesn't exist
    log_directory.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler with colored output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    root_logger.addHandler(console_handler)
    
    # File handler with rotation for general logs
    general_log_file = log_directory / "app.log"
    file_handler = RotatingFileHandler(
        general_log_file,
        maxBytes=settings.LOG_FILE_MAX_BYTES,
        backupCount=settings.LOG_FILE_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    root_logger.addHandler(file_handler)
    
    # Error log file handler
    error_log_file = log_directory / "errors.log"
    error_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=settings.LOG_FILE_MAX_BYTES,
        backupCount=settings.LOG_FILE_BACKUP_COUNT,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_format)
    root_logger.addHandler(error_handler)
    
    # Webhook-specific logger
    webhook_logger = logging.getLogger("webhook")
    webhook_log_file = log_directory / "webhook.log"
    webhook_handler = RotatingFileHandler(
        webhook_log_file,
        maxBytes=settings.LOG_FILE_MAX_BYTES,
        backupCount=settings.LOG_FILE_BACKUP_COUNT,
        encoding='utf-8'
    )
    webhook_handler.setLevel(logging.DEBUG)
    webhook_handler.setFormatter(file_format)
    webhook_logger.addHandler(webhook_handler)
    webhook_logger.addHandler(console_handler)
    webhook_logger.setLevel(logging.DEBUG)
    
    # Telegram-specific logger
    telegram_logger = logging.getLogger("telegram")
    telegram_log_file = log_directory / "telegram.log"
    telegram_handler = RotatingFileHandler(
        telegram_log_file,
        maxBytes=settings.LOG_FILE_MAX_BYTES,
        backupCount=settings.LOG_FILE_BACKUP_COUNT,
        encoding='utf-8'
    )
    telegram_handler.setLevel(logging.DEBUG)
    telegram_handler.setFormatter(file_format)
    telegram_logger.addHandler(telegram_handler)
    telegram_logger.addHandler(console_handler)
    telegram_logger.setLevel(logging.DEBUG)
    
    logging.info(f"✅ Logging configured. Logs directory: {log_directory.absolute()}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

