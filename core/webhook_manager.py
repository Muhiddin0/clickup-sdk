"""
Webhook Manager - Handles ClickUp webhook creation and management.
"""
import logging
import requests
from typing import List, Optional

from config.settings import get_settings
from core.logging_config import get_logger

logger = get_logger(__name__)


class WebhookManager:
    """Manages ClickUp webhook lifecycle."""
    
    def __init__(self, api_token: Optional[str] = None, team_id: Optional[str] = None):
        """
        Initialize WebhookManager.
        
        Args:
            api_token: ClickUp API token. If None, uses settings.
            team_id: ClickUp team ID. If None, uses settings.
        """
        settings = get_settings()
        self.api_token = api_token or settings.CLICKUP_API_TOKEN
        self.team_id = team_id or settings.TEAM_ID
        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": self.api_token,
            "Content-Type": "application/json",
        }
    
    def delete_webhook(self, webhook_id: str) -> dict:
        """
        Delete a webhook by ID.
        
        Args:
            webhook_id: Webhook ID to delete
            
        Returns:
            API response dictionary
        """
        try:
            resp = requests.delete(
                f"{self.base_url}/webhook/{webhook_id}",
                headers=self.headers,
                timeout=10
            )
            resp.raise_for_status()
            result = resp.json()
            logger.info(f"✅ Webhook deleted: {webhook_id}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error deleting webhook {webhook_id}: {e}")
            raise
    
    def get_webhooks(self) -> dict:
        """
        Get all webhooks for the team.
        
        Returns:
            API response dictionary with webhooks list
        """
        try:
            resp = requests.get(
                f"{self.base_url}/team/{self.team_id}/webhook",
                headers=self.headers,
                timeout=10
            )
            resp.raise_for_status()
            result = resp.json()
            logger.debug(f"Retrieved {len(result.get('webhooks', []))} webhooks")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error getting webhooks: {e}")
            raise
    
    def create_webhook(
        self, 
        endpoint: Optional[str] = None, 
        events: Optional[List[str]] = None, 
        status: str = "active"
    ) -> dict:
        """
        Create a new webhook.
        
        Args:
            endpoint: Webhook endpoint URL. If None, uses settings.
            events: List of events to subscribe to. If None, uses default events.
            status: Webhook status (active/inactive)
            
        Returns:
            API response dictionary
        """
        settings = get_settings()
        
        if endpoint is None:
            endpoint = settings.WEBHOOK_ENDPOINT
        
        if events is None:
            events = [
                "taskCreated",
                "taskUpdated",
                "taskStatusUpdated",
                "taskDeleted"
            ]
        
        webhook_payload = {
            "endpoint": endpoint,
            "events": events,
            "status": status,
        }
        
        try:
            resp = requests.post(
                f"{self.base_url}/team/{self.team_id}/webhook",
                headers=self.headers,
                json=webhook_payload,
                timeout=10
            )
            resp.raise_for_status()
            result = resp.json()
            logger.info(f"✅ Webhook created: {result.get('id', 'unknown')}")
            logger.debug(f"Webhook endpoint: {endpoint}, Events: {events}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error creating webhook: {e}")
            raise
    
    def initialize_webhook(self) -> None:
        """
        Initialize webhook by deleting existing webhooks and creating a new one.
        This ensures only one active webhook exists.
        """
        try:
            logger.info("🔄 Initializing webhook...")
            
            # Get existing webhooks
            webhooks_data = self.get_webhooks()
            existing_webhooks = webhooks_data.get("webhooks", [])
            
            # Delete all existing webhooks
            if existing_webhooks:
                logger.info(f"🗑️ Deleting {len(existing_webhooks)} existing webhook(s)...")
                for webhook in existing_webhooks:
                    try:
                        self.delete_webhook(webhook["id"])
                    except Exception as e:
                        logger.warning(f"⚠️ Could not delete webhook {webhook['id']}: {e}")
            
            # Create new webhook
            logger.info("➕ Creating new webhook...")
            self.create_webhook()
            
            # Verify webhook creation
            final_webhooks = self.get_webhooks()
            logger.info(f"✅ Webhook initialization complete. Active webhooks: {len(final_webhooks.get('webhooks', []))}")
            
        except Exception as e:
            logger.error(f"❌ Error initializing webhook: {e}", exc_info=True)
            raise

