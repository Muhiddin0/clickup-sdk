"""
ClickUp Webhook Handler Example - aiogram style
"""
import asyncio
import os
import logging
from clickup_sdk import ClickUp
from clickup_sdk.webhook import WebhookDispatcher, WebhookServer, WebhookEvent

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize ClickUp client (optional, for making API calls in handlers)
CLICKUP_TOKEN = os.getenv("CLICKUP_TOKEN", "pk_your_token_here")
clickup_client = ClickUp(token=CLICKUP_TOKEN)

# Initialize webhook dispatcher
dispatcher = WebhookDispatcher()


# Middleware - har bir eventdan oldin ishlaydi
@dispatcher.middleware
async def log_middleware(event: WebhookEvent, handler):
    """Log every event before processing"""
    logger.info(f"📥 Received event: {event.event} (Task ID: {event.task_id})")
    result = await handler(event)
    logger.info(f"✅ Processed event: {event.event}")
    return result


# Task event handlers
@dispatcher.on("taskCreated")
async def handle_task_created(event: WebhookEvent):
    """Handle task creation event"""
    logger.info(f"🎉 New task created! Task ID: {event.task_id}")
    
    # You can make API calls here
    # task = await clickup_client.tasks.get_task(event.task_id)
    # logger.info(f"Task name: {task.get('name')}")
    
    # Your custom logic here
    # For example: send notification, update database, etc.
    print(f"✨ Task {event.task_id} was created!")


@dispatcher.on("taskUpdated")
async def handle_task_updated(event: WebhookEvent):
    """Handle task update event"""
    logger.info(f"📝 Task updated! Task ID: {event.task_id}")
    
    # Check what changed
    if event.history_items:
        for item in event.history_items:
            field = item.get("field", "")
            logger.info(f"  Changed field: {field}")
    
    print(f"🔄 Task {event.task_id} was updated!")


@dispatcher.on("taskDeleted")
async def handle_task_deleted(event: WebhookEvent):
    """Handle task deletion event"""
    logger.info(f"🗑️ Task deleted! Task ID: {event.task_id}")
    print(f"❌ Task {event.task_id} was deleted!")


@dispatcher.on("taskStatusUpdated")
async def handle_task_status_updated(event: WebhookEvent):
    """Handle task status change"""
    logger.info(f"📊 Task status updated! Task ID: {event.task_id}")
    
    if event.history_items:
        for item in event.history_items:
            old_value = item.get("before", {}).get("status", {}).get("status", "")
            new_value = item.get("after", {}).get("status", {}).get("status", "")
            logger.info(f"  Status changed: {old_value} → {new_value}")
            print(f"📈 Status changed from '{old_value}' to '{new_value}'")


@dispatcher.on("taskAssigneeUpdated")
async def handle_task_assignee_updated(event: WebhookEvent):
    """Handle task assignee change"""
    logger.info(f"👤 Task assignee updated! Task ID: {event.task_id}")
    
    if event.history_items:
        for item in event.history_items:
            old_assignees = item.get("before", {}).get("assignees", [])
            new_assignees = item.get("after", {}).get("assignees", [])
            logger.info(f"  Assignees changed")
            print(f"👥 Assignees updated for task {event.task_id}")


@dispatcher.on("taskCommentPosted")
async def handle_task_comment(event: WebhookEvent):
    """Handle new comment on task"""
    logger.info(f"💬 New comment on task! Task ID: {event.task_id}")
    
    if event.history_items:
        for item in event.history_items:
            comment = item.get("comment", {})
            comment_text = comment.get("comment_text", "")
            logger.info(f"  Comment: {comment_text[:50]}...")
            print(f"💭 New comment: {comment_text[:100]}")


# List event handlers
@dispatcher.on("listCreated")
async def handle_list_created(event: WebhookEvent):
    """Handle list creation"""
    logger.info(f"📋 New list created!")
    print("📋 A new list was created!")


@dispatcher.on("listUpdated")
async def handle_list_updated(event: WebhookEvent):
    """Handle list update"""
    logger.info(f"📝 List updated!")
    print("📝 A list was updated!")


# Space event handlers
@dispatcher.on("spaceCreated")
async def handle_space_created(event: WebhookEvent):
    """Handle space creation"""
    logger.info(f"🚀 New space created!")
    print("🚀 A new space was created!")


# Wildcard handler - barcha eventlar uchun
@dispatcher.on("*")
async def handle_all_events(event: WebhookEvent):
    """Handle all events (fallback)"""
    logger.debug(f"🌐 Generic handler for event: {event.event}")


async def main():
    """Main function to run webhook server"""
    # Webhook secret (optional, but recommended)
    # Get this from your webhook configuration in ClickUp
    webhook_secret = os.getenv("WEBHOOK_SECRET", None)
    
    # Create webhook server
    server = WebhookServer(
        dispatcher=dispatcher,
        secret=webhook_secret,
        path="/webhook"
    )
    
    logger.info("🚀 Starting ClickUp Webhook Server...")
    logger.info(f"📡 Listening on http://0.0.0.0:8000/webhook")
    logger.info(f"📝 Registered events: {dispatcher.get_registered_events()}")
    
    # Start server
    await server.start(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Shutting down webhook server...")
        asyncio.run(clickup_client.close())

