"""
Simple ClickUp Webhook Handler Example
"""
import asyncio
from clickup_sdk.webhook import WebhookDispatcher, WebhookServer, WebhookEvent


# Create dispatcher
dispatcher = WebhookDispatcher()


# Register handlers using decorators
@dispatcher.on("taskCreated")
async def on_task_created(event: WebhookEvent):
    """Handle when a task is created"""
    print(f"✅ New task created: {event.task_id}")
    # Your logic here
    # For example: send notification, log to database, etc.


@dispatcher.on("taskUpdated")
async def on_task_updated(event: WebhookEvent):
    """Handle when a task is updated"""
    print(f"📝 Task updated: {event.task_id}")
    # Your logic here


@dispatcher.on("taskStatusUpdated")
async def on_status_changed(event: WebhookEvent):
    """Handle when task status changes"""
    print(f"📊 Status changed for task: {event.task_id}")
    # Check what changed
    if event.history_items:
        for item in event.history_items:
            old_status = item.get("before", {}).get("status", {}).get("status", "")
            new_status = item.get("after", {}).get("status", {}).get("status", "")
            print(f"  {old_status} → {new_status}")


# Run server
if __name__ == "__main__":
    server = WebhookServer(dispatcher, path="/webhook")
    print("🚀 Webhook server starting on http://0.0.0.0:8000/webhook")
    print("📝 Registered handlers:", dispatcher.get_registered_events())
    server.run(host="0.0.0.0", port=8000)

