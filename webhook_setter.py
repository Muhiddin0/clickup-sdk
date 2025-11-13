import requests

from config.environments import CLICKUP_API_TOKEN, TEAM_ID


def delete_webhook(web_hook_id):
    resp = requests.delete(
        f"https://api.clickup.com/api/v2/webhook/{web_hook_id}",
        headers={
            "Authorization": CLICKUP_API_TOKEN,
            "Content-Type": "application/json",
        },
    )

    print(resp.json())


def get_webhook():
    resp = requests.get(
        f"https://api.clickup.com/api/v2/team/{TEAM_ID}/webhook",
        headers={
            "Authorization": CLICKUP_API_TOKEN,
            "Content-Type": "application/json",
        },
    )

    print(resp.json())

    return resp.json()


def set_webhook():
    webhook_payload = {
        "endpoint": "https://clickup.venu.uz/clickup-webhook",
        "events": [
            "taskCreated",
            "taskUpdated",
            "taskStatusUpdated",
            "taskDeleted"],
        "status": "active",
    }

    resp = requests.post(
        f"https://api.clickup.com/api/v2/team/{TEAM_ID}/webhook",
        headers={
            "Authorization": CLICKUP_API_TOKEN,
            "Content-Type": "application/json",
        },
        json=webhook_payload,
    )

    print(resp.status_code, resp.json())
