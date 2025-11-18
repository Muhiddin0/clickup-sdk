"""
ClickUp API Client - Main client class similar to aiogram style
"""

import aiohttp
from typing import Optional, Dict, Any, List
from urllib.parse import urlencode


class ClickUp:
    """
    Main ClickUp API client class.

    Usage:
        clickup = ClickUp(token="pk_...")
        user = await clickup.get_user()
    """

    BASE_URL = "https://api.clickup.com/api"

    def __init__(self, token: str):
        """
        Initialize ClickUp client.

        Args:
            token: ClickUp API token (Personal API Token or OAuth access token)
        """
        self.token = token
        self._session: Optional[aiohttp.ClientSession] = None

        # Initialize handlers
        from .handlers import (
            TasksHandler,
            ListsHandler,
            SpacesHandler,
            FoldersHandler,
            CommentsHandler,
            AttachmentsHandler,
            CustomFieldsHandler,
            GoalsHandler,
            TimeEntriesHandler,
            WebhooksHandler,
            UsersHandler,
            TeamsHandler,
        )

        self.tasks = TasksHandler(self)
        self.lists = ListsHandler(self)
        self.spaces = SpacesHandler(self)
        self.folders = FoldersHandler(self)
        self.comments = CommentsHandler(self)
        self.attachments = AttachmentsHandler(self)
        self.custom_fields = CustomFieldsHandler(self)
        self.goals = GoalsHandler(self)
        self.time_entries = TimeEntriesHandler(self)
        self.webhooks = WebhooksHandler(self)
        self.users = UsersHandler(self)
        self.teams = TeamsHandler(self)

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None or self._session.closed:
            # Create session with proper timeout configuration
            # Timeout is set to avoid "Timeout context manager should be used inside a task" error
            # Using ClientTimeout with explicit values to avoid context manager issues
            timeout = aiohttp.ClientTimeout(
                total=30, connect=10, sock_read=10, sock_connect=10
            )
            connector = aiohttp.TCPConnector(
                limit=100, limit_per_host=30, ttl_dns_cache=300, force_close=False
            )
            self._session = aiohttp.ClientSession(
                timeout=timeout, connector=connector, raise_for_status=False
            )
        return self._session

    async def close(self):
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication."""
        return {"Authorization": self.token, "Content-Type": "application/json"}

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request to ClickUp API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., "/v2/user")
            params: Query parameters
            json_data: JSON body data
            data: Form data or other body data
            headers: Additional headers

        Returns:
            Response JSON data
        """
        session = await self._get_session()
        url = f"{self.BASE_URL}{endpoint}"

        request_headers = self._get_headers()
        if headers:
            request_headers.update(headers)

        # Build query string
        if params:
            # Filter out None values
            params = {k: v for k, v in params.items() if v is not None}
            url += f"?{urlencode(params, doseq=True)}"

        async with session.request(
            method=method, url=url, headers=request_headers, json=json_data, data=data
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make GET request."""
        return await self._request("GET", endpoint, params=params)

    async def post(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make POST request."""
        return await self._request(
            "POST",
            endpoint,
            json_data=json_data,
            data=data,
            params=params,
            headers=headers,
        )

    async def put(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make PUT request."""
        return await self._request("PUT", endpoint, json_data=json_data, params=params)

    async def delete(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make DELETE request."""
        return await self._request("DELETE", endpoint, params=params)

    # Convenience methods
    async def get_user(self) -> Dict[str, Any]:
        """Get authorized user information."""
        return await self.get("/v2/user")

    async def get_teams(self) -> Dict[str, Any]:
        """Get authorized workspaces (teams)."""
        return await self.get("/v2/team")
