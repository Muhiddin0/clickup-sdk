"""
ClickUp Webhook Server - Main Application
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from clickup_sdk.webhook import WebhookServer
from core.logging_config import setup_logging, get_logger
from core.dispatcher import dispatcher
from core.webhook_manager import WebhookManager
from config.settings import get_settings

# Setup logging first
setup_logging()
logger = get_logger(__name__)

# Import clickup module - this will automatically register all handlers
# because handlers are imported in clickup/__init__.py
import clickup  # noqa: F401


async def main():
    """Main application entry point."""
    settings = get_settings()
    webhook_manager = WebhookManager()

    # Initialize webhook
    try:
        logger.info("🔄 Initializing ClickUp webhook...")
        webhook_manager.initialize_webhook()
    except Exception as e:
        logger.error(f"❌ Failed to initialize webhook: {e}", exc_info=True)
        logger.warning("⚠️ Continuing without webhook initialization...")

    # Create webhook server
    server = WebhookServer(
        dispatcher=dispatcher,
        secret=settings.WEBHOOK_SECRET,
        path=settings.WEBHOOK_PATH,
    )

    logger.info("🚀 Starting ClickUp Webhook Server...")
    logger.info(
        f"📡 Listening on http://{settings.SERVER_HOST}:{settings.SERVER_PORT}{settings.WEBHOOK_PATH}"
    )
    logger.info(f"📝 Registered events: {dispatcher.get_registered_events()}")
    logger.info(f"🔧 Debug mode: {settings.DEBUG}")
    logger.info(f"🔄 Auto-reload: {settings.RELOAD}")

    # Get directories for auto-reload
    current_dir = os.path.dirname(os.path.abspath(__file__))
    clickup_sdk_dir = os.path.join(current_dir, "clickup_sdk")
    clickup_dir = os.path.join(current_dir, "clickup")
    config_dir = os.path.join(current_dir, "config")
    core_dir = os.path.join(current_dir, "core")

    try:
        await server.start(
            host=settings.SERVER_HOST,
            port=settings.SERVER_PORT,
            reload=settings.RELOAD,
            reload_dirs=[
                current_dir,
                clickup_sdk_dir,
                clickup_dir,
                config_dir,
                core_dir,
            ],
        )
    except Exception as e:
        logger.error(f"❌ Server error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    try:
        # Validate settings
        settings = get_settings()
        settings.validate()

        # Run main application
        asyncio.run(main(), debug=settings.DEBUG)
    except KeyboardInterrupt:
        logger.info("👋 Shutting down webhook server...")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)
