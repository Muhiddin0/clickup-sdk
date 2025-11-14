"""
ClickUp Webhook Filter Example - Custom Field Filter
"""



import asyncio
import os
import logging
from clickup_sdk.webhook import (
    WebhookDispatcher,
    WebhookServer,
    WebhookEvent,
    CustomFieldFilter,
    custom_field_changed,
    status_changed
)

from webhook_setter import WebhookManager


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

dispatcher = WebhookDispatcher()
webhook_manager = WebhookManager()

# Example 1: Custom field o'zgarganda tutib olish (field_id bilan)
@dispatcher.on("taskUpdated", CustomFieldFilter(field_id="custom_field_123"))
async def handle_custom_field_change_by_id(event: WebhookEvent):
    """Custom field o'zgarganda (field_id bilan)"""
    logger.info(f"🎯 Custom field o'zgardi! Task ID: {event.task_id}")
    
    # Qaysi field o'zgarganini topish
    if event.history_items:
        for item in event.history_items:
            field = item.get("field", "")
            before = item.get("before", {})
            after = item.get("after", {})
            logger.info(f"  Field: {field}")
            logger.info(f"  Old value: {before}")
            logger.info(f"  New value: {after}")
    
    print(f"✅ Custom field o'zgarishi tutildi: {event.task_id}")


# Example 2: Custom field o'zgarganda tutib olish (field_name bilan)
@dispatcher.on("taskUpdated", CustomFieldFilter(field_name="broker dedline"))
async def handle_custom_field_change_by_name(event: WebhookEvent):
    """Custom field o'zgarganda (field_name bilan)"""
    logger.info(f"🎯 'broker dedline' custom field o'zgardi! Task ID: {event.task_id}")
    
    if event.history_items:
        for item in event.history_items:
            field = item.get("field", "")
            before = item.get("before", {})
            after = item.get("after", {})
            logger.info(f"  {field}: {before} → {after}")
    
    print(f"✅ Priority field o'zgarishi tutildi: {event.task_id}")


# Example 3: Convenience function bilan
@dispatcher.on("taskUpdated", custom_field_changed(field_id="abc123"))
async def handle_custom_field_convenience(event: WebhookEvent):
    """Convenience function bilan custom field filter"""
    logger.info(f"🎯 Custom field (convenience) o'zgardi! Task ID: {event.task_id}")
    print(f"✅ Custom field o'zgarishi (convenience): {event.task_id}")


# Example 4: Status o'zgarishini filter qilish
@dispatcher.on("taskStatusUpdated", status_changed(to_status="complete"))
async def handle_status_to_complete(event: WebhookEvent):
    """Task 'complete' statusiga o'tganda"""
    logger.info(f"✅ Task complete bo'ldi! Task ID: {event.task_id}")
    print(f"🎉 Task {event.task_id} complete bo'ldi!")


# Example 5: Bir nechta filterlar bilan (AND logic)
from clickup_sdk.webhook import CombinedFilter

@dispatcher.on(
    "taskUpdated",
    CombinedFilter([
        CustomFieldFilter(field_id="custom_field_123"),
        # Boshqa filterlar ham qo'shish mumkin
    ], logic="AND")
)
async def handle_multiple_filters(event: WebhookEvent):
    """Bir nechta filter bilan"""
    logger.info(f"🎯 Multiple filters bilan event tutildi! Task ID: {event.task_id}")


# Example 6: Filter siz oddiy handler (barcha taskUpdated eventlar uchun)
@dispatcher.on("taskUpdated")
async def handle_all_task_updates(event: WebhookEvent):
    """Barcha task update eventlar uchun (filter yo'q)"""
    logger.debug(f"📝 Task updated (no filter): {event.task_id}")
    
    # Debug: barcha fieldlarni ko'rsatish
    if event.history_items:
        logger.info("🔍 Debug - History items:")
        for idx, item in enumerate(event.history_items):
            logger.info(f"  Item {idx}:")
            logger.info(f"    field: {item.get('field', 'N/A')}")
            logger.info(f"    field_id: {item.get('field_id', 'N/A')}")
            logger.info(f"    id: {item.get('id', 'N/A')}")
            logger.info(f"    before: {item.get('before', {})}")
            logger.info(f"    after: {item.get('after', {})}")
            
            # Custom field structure ni tekshirish
            after = item.get("after", {})
            before = item.get("before", {})
            if isinstance(after, dict):
                logger.info(f"    after.name: {after.get('name', 'N/A')}")
                logger.info(f"    after.type: {after.get('type', 'N/A')}")
            if isinstance(before, dict):
                logger.info(f"    before.name: {before.get('name', 'N/A')}")
                logger.info(f"    before.type: {before.get('type', 'N/A')}")


async def main():
    """Main function"""
    webhook_secret = os.getenv("WEBHOOK_SECRET", None)
    
    server = WebhookServer(
        dispatcher=dispatcher,
        secret=webhook_secret,
        path="/clickup-webhook"
    )
    
    logger.info("🚀 Starting ClickUp Webhook Server with Filters...")
    logger.info(f"📡 Listening on http://0.0.0.0:3000/clickup-webhook")
    logger.info(f"📝 Registered events: {dispatcher.get_registered_events()}")
    
    # Get current directory and clickup_sdk directory for auto-reload
    current_dir = os.path.dirname(os.path.abspath(__file__))
    clickup_sdk_dir = os.path.join(current_dir, "clickup_sdk")
    
    await server.start(
        host="0.0.0.0", 
        port=3000, 
        reload=True,
        reload_dirs=[current_dir, clickup_sdk_dir]
    )


if __name__ == "__main__":
    try:
        webhook_manager.initialize_webhook()
        asyncio.run(main(), debug=True)
    except KeyboardInterrupt:
        logger.info("👋 Shutting down webhook server...")

