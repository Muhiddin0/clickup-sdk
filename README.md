# ClickUp SDK

Python library for ClickUp API v2, designed with aiogram-style simplicity and ease of use.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
import asyncio
from clickup_sdk import ClickUp

async def main():
    # Initialize client with your API token
    clickup = ClickUp(token="pk_your_token_here")

    # Get user information
    user = await clickup.get_user()
    print(f"Logged in as: {user['user']['username']}")

    # Get teams (workspaces)
    teams = await clickup.get_teams()
    print(f"Teams: {teams}")

    # Work with tasks
    task = await clickup.tasks.get_task("task_id_here")
    print(f"Task: {task['name']}")

    # Create a new task
    new_task = await clickup.tasks.create_task(
        list_id="list_id_here",
        name="New Task",
        description="Task description",
        priority=2
    )

    # Work with lists
    lists = await clickup.lists.get_lists(folder_id="folder_id_here")

    # Work with spaces
    spaces = await clickup.spaces.get_spaces(team_id=123)

    # Work with comments
    comments = await clickup.comments.get_task_comments("task_id_here")

    # Work with time entries
    time_entries = await clickup.time_entries.get_time_entries(team_id=123)

    # Close the session
    await clickup.close()

# Run
asyncio.run(main())
```

## Using Context Manager

```python
async def main():
    async with ClickUp(token="pk_your_token_here") as clickup:
        user = await clickup.get_user()
        print(user)
```

## Available Handlers

The SDK provides organized handlers for different API groups:

- `clickup.tasks` - Task operations (create, update, delete, get)
- `clickup.lists` - List operations
- `clickup.spaces` - Space operations
- `clickup.folders` - Folder operations
- `clickup.comments` - Comment operations
- `clickup.attachments` - Attachment operations
- `clickup.custom_fields` - Custom field operations
- `clickup.goals` - Goal operations
- `clickup.time_entries` - Time entry operations
- `clickup.webhooks` - Webhook operations
- `clickup.users` - User operations
- `clickup.teams` - Team/Workspace operations

## Examples

### Creating a Task

```python
task = await clickup.tasks.create_task(
    list_id="123456",
    name="Complete project",
    description="Finish the project by Friday",
    priority=2,
    due_date=1704067200000,  # Unix timestamp in milliseconds
    assignees=["user_id_1", "user_id_2"]
)
```

### Updating a Task

```python
updated_task = await clickup.tasks.update_task(
    task_id="task_id_here",
    name="Updated task name",
    status="in progress",
    priority=1
)
```

### Getting Tasks with Filters

```python
tasks = await clickup.tasks.get_tasks(
    list_id="123456",
    archived=False,
    statuses=["in progress", "complete"],
    assignees=["user_id_1"],
    tags=["urgent", "important"]
)
```

### Adding Comments

```python
comment = await clickup.comments.create_task_comment(
    task_id="task_id_here",
    comment_text="This looks good!",
    notify_all=True
)
```

### Uploading Attachments

```python
attachment = await clickup.attachments.create_task_attachment(
    task_id="task_id_here",
    file_path="/path/to/file.pdf"
)
```

### Working with Time Entries

```python
# Start a timer
timer = await clickup.time_entries.start_time_entry(
    team_id=123,
    task_id="task_id_here",
    description="Working on feature"
)

# Stop the timer
stopped = await clickup.time_entries.stop_time_entry(
    team_id=123,
    timer_id=timer["data"]["id"]
)
```

## Authentication

The SDK supports both Personal API Tokens and OAuth 2.0 access tokens.

### Personal API Token

```python
clickup = ClickUp(token="pk_your_personal_token")
```

### OAuth 2.0

```python
clickup = ClickUp(token="oauth_access_token")
```

## Webhook Event Handling

The SDK provides aiogram-style webhook event handling for ClickUp events.

### Basic Webhook Server

```python
from clickup_sdk.webhook import WebhookDispatcher, WebhookServer, WebhookEvent

# Create dispatcher
dispatcher = WebhookDispatcher()

# Register event handlers
@dispatcher.on("taskCreated")
async def handle_task_created(event: WebhookEvent):
    print(f"New task created: {event.task_id}")
    # Your custom logic here

@dispatcher.on("taskUpdated")
async def handle_task_updated(event: WebhookEvent):
    print(f"Task updated: {event.task_id}")

@dispatcher.on("taskStatusUpdated")
async def handle_status_change(event: WebhookEvent):
    if event.history_items:
        for item in event.history_items:
            old_status = item.get("before", {}).get("status", {}).get("status", "")
            new_status = item.get("after", {}).get("status", {}).get("status", "")
            print(f"Status: {old_status} → {new_status}")

# Create and run server
server = WebhookServer(dispatcher, secret="your_webhook_secret")
server.run(host="0.0.0.0", port=8000)
```

### Using Middleware

```python
@dispatcher.middleware
async def log_middleware(event: WebhookEvent, handler):
    print(f"Processing event: {event.event}")
    result = await handler(event)
    print(f"Event processed: {event.event}")
    return result
```

### Available Event Types

- **Task Events**: `taskCreated`, `taskUpdated`, `taskDeleted`, `taskStatusUpdated`, `taskAssigneeUpdated`, `taskPriorityUpdated`, `taskDueDateUpdated`, `taskTagUpdated`, `taskMoved`, `taskCommentPosted`, `taskCommentUpdated`, `taskTimeEstimateUpdated`, `taskTimeTrackedUpdated`
- **List Events**: `listCreated`, `listUpdated`, `listDeleted`
- **Folder Events**: `folderCreated`, `folderUpdated`, `folderDeleted`
- **Space Events**: `spaceCreated`, `spaceUpdated`, `spaceDeleted`
- **Goal Events**: `goalCreated`, `goalUpdated`, `goalDeleted`
- **Key Result Events**: `keyResultCreated`, `keyResultUpdated`, `keyResultDeleted`
- **Wildcard**: Use `"*"` to handle all events

### Setting Up Webhooks in ClickUp

1. Create a webhook using the API:

```python
webhook = await clickup.webhooks.create_webhook(
    team_id=123,
    endpoint="https://yourdomain.com/webhook",
    client_id="your_oauth_client_id",
    events=["taskCreated", "taskUpdated", "taskStatusUpdated"]
)
```

2. Run your webhook server (see examples in `webhook_example.py`)

3. ClickUp will send events to your endpoint when changes occur

### Webhook Filters

You can filter events using filters (similar to aiogram filters):

```python
from clickup_sdk.webhook import CustomFieldFilter, custom_field_changed

# Filter by custom field ID
@dispatcher.on("taskUpdated", CustomFieldFilter(field_id="custom_field_123"))
async def handle_custom_field_change(event: WebhookEvent):
    print(f"Custom field changed! Task: {event.task_id}")

# Filter by custom field name
@dispatcher.on("taskUpdated", CustomFieldFilter(field_name="Priority"))
async def handle_priority_change(event: WebhookEvent):
    print(f"Priority field changed! Task: {event.task_id}")

# Using convenience function
@dispatcher.on("taskUpdated", custom_field_changed(field_id="abc123"))
async def handle_field_change(event: WebhookEvent):
    print(f"Field changed: {event.task_id}")

# Filter by status change
from clickup_sdk.webhook import status_changed

@dispatcher.on("taskStatusUpdated", status_changed(to_status="complete"))
async def handle_complete(event: WebhookEvent):
    print(f"Task completed: {event.task_id}")
```

### Available Filters

- **CustomFieldFilter**: Filter by custom field changes (by ID or name)
- **TaskStatusFilter**: Filter by status changes (from/to status)
- **TaskAssigneeFilter**: Filter by assignee changes
- **EventTypeFilter**: Filter by event types
- **CombinedFilter**: Combine multiple filters with AND/OR logic

### Full Webhook Example

See `webhook_example.py` for a complete example with all event handlers.
See `webhook_filter_example.py` for filter usage examples.

## Error Handling

The SDK uses `aiohttp` which raises exceptions on HTTP errors. You should handle them appropriately:

```python
import aiohttp

try:
    task = await clickup.tasks.get_task("invalid_id")
except aiohttp.ClientResponseError as e:
    print(f"Error: {e.status} - {e.message}")
```

## License

MIT
