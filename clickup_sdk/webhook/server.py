"""Webhook Server - FastAPI based webhook endpoint"""
from typing import Optional, Dict, Any
import logging
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

from .dispatcher import WebhookDispatcher
from .events import WebhookEvent

logger = logging.getLogger(__name__)


class WebhookServer:
    """
    Webhook server for receiving ClickUp webhook events.
    
    Usage:
        dispatcher = WebhookDispatcher()
        
        @dispatcher.on("taskCreated")
        async def handle_task(event: WebhookEvent):
            print(f"Task created: {event.task_id}")
        
        server = WebhookServer(dispatcher, secret="your_webhook_secret")
        await server.start(host="0.0.0.0", port=8000)
    """
    
    def __init__(
        self,
        dispatcher: WebhookDispatcher,
        secret: Optional[str] = None,
        path: str = "/webhook"
    ):
        """
        Initialize webhook server.
        
        Args:
            dispatcher: WebhookDispatcher instance
            secret: Webhook secret for verification (optional)
            path: Webhook endpoint path
        """
        self.dispatcher = dispatcher
        self.secret = secret
        self.path = path
        self.app = FastAPI(title="ClickUp Webhook Server")
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup FastAPI routes"""
        
        @self.app.get("/")
        async def root():
            """Health check endpoint"""
            return {"status": "ok", "message": "ClickUp Webhook Server"}
        
        @self.app.post(self.path)
        async def webhook_endpoint(request: Request):
            """Webhook endpoint"""
            try:
                # Get request body
                body = await request.json()
                
                # Verify secret if provided
                if self.secret:
                    # ClickUp sends secret in headers or body
                    # Adjust based on your webhook configuration
                    received_secret = request.headers.get("X-ClickUp-Secret") or body.get("secret")
                    if received_secret != self.secret:
                        logger.warning("Webhook secret verification failed")
                        raise HTTPException(status_code=401, detail="Invalid secret")
                
                # Process event
                logger.info(f"Received webhook event: {body.get('event', 'unknown')}")
                results = await self.dispatcher.process_event(body)
                
                return JSONResponse(
                    status_code=200,
                    content={"status": "ok", "processed": len(results)}
                )
            except Exception as e:
                logger.error(f"Error processing webhook: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/health")
        async def health():
            """Health check"""
            return {"status": "healthy"}
    
    async def start(
        self,
        host: str = "0.0.0.0",
        port: int = 8000,
        **uvicorn_kwargs
    ):
        """
        Start the webhook server.
        
        Args:
            host: Host to bind to
            port: Port to bind to
            **uvicorn_kwargs: Additional uvicorn configuration
        """
        config = uvicorn.Config(
            self.app,
            host=host,
            port=port,
            log_level="info",
            **uvicorn_kwargs
        )
        server = uvicorn.Server(config)
        logger.info(f"Starting webhook server on {host}:{port}")
        await server.serve()
    
    def run(
        self,
        host: str = "0.0.0.0",
        port: int = 8000,
        **uvicorn_kwargs
    ):
        """
        Run the webhook server (blocking).
        
        Args:
            host: Host to bind to
            port: Port to bind to
            **uvicorn_kwargs: Additional uvicorn configuration
        """
        uvicorn.run(
            self.app,
            host=host,
            port=port,
            **uvicorn_kwargs
        )
    
    def get_app(self) -> FastAPI:
        """Get FastAPI app instance"""
        return self.app

