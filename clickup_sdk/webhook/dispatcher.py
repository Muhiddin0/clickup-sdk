"""Webhook Dispatcher - aiogram style event handling"""
from typing import Callable, Dict, List, Any, Optional, Awaitable, Union, Tuple
from collections import defaultdict
import asyncio
import logging

from .events import WebhookEvent, WebhookEventType
from .filters import Filter

logger = logging.getLogger(__name__)


class WebhookDispatcher:
    """
    Webhook event dispatcher - similar to aiogram Dispatcher.
    
    Usage:
        dispatcher = WebhookDispatcher()
        
        @dispatcher.on("taskCreated")
        async def handle_task_created(event: WebhookEvent):
            print(f"Task created: {event.task_id}")
        
        await dispatcher.process_event(event_data)
    """
    
    def __init__(self):
        """Initialize webhook dispatcher"""
        self._handlers: Dict[str, List[Tuple[Callable, Optional[Filter]]]] = defaultdict(list)
        self._middlewares: List[Callable] = []
    
    def on(
        self,
        event_type: str,
        *filters: Filter
    ) -> Callable:
        """
        Decorator to register event handler with optional filters.
        
        Args:
            event_type: Event type (e.g., "taskCreated", "taskUpdated", "*" for all)
            *filters: Optional filters to apply
        
        Usage:
            @dispatcher.on("taskCreated")
            async def handle_task(event: WebhookEvent):
                pass
            
            @dispatcher.on("taskUpdated", CustomFieldFilter(field_id="custom_field_123"))
            async def handle_custom_field_change(event: WebhookEvent):
                pass
        """
        def decorator(func: Callable) -> Callable:
            # Combine filters if multiple provided
            if filters:
                if len(filters) == 1:
                    filter_obj = filters[0]
                else:
                    from .filters import CombinedFilter
                    filter_obj = CombinedFilter(list(filters), logic="AND")
            else:
                filter_obj = None
            
            self.register_handler(event_type, func, filter_obj)
            return func
        return decorator
    
    def register_handler(
        self,
        event_type: str,
        handler: Callable,
        filter_obj: Optional[Filter] = None
    ):
        """
        Register an event handler with optional filter.
        
        Args:
            event_type: Event type
            handler: Handler function (async or sync)
            filter_obj: Optional filter to apply
        """
        if not callable(handler):
            raise ValueError("Handler must be callable")
        
        self._handlers[event_type].append((handler, filter_obj))
        filter_info = f" with filter {filter_obj.__class__.__name__}" if filter_obj else ""
        logger.debug(f"Registered handler for event: {event_type}{filter_info}")
    
    def middleware(self, func: Callable) -> Callable:
        """
        Decorator to register middleware.
        
        Usage:
            @dispatcher.middleware
            async def log_middleware(event: WebhookEvent, handler: Callable):
                print(f"Processing event: {event.event}")
                result = await handler(event)
                return result
        """
        self._middlewares.append(func)
        return func
    
    async def process_event(self, event_data: Dict[str, Any]) -> List[Any]:
        """
        Process a webhook event.
        
        Args:
            event_data: Event data from ClickUp webhook
        
        Returns:
            List of handler results
        """
        event = WebhookEvent.from_dict(event_data)
        event_type = event.event
        
        # Get handlers for this specific event and wildcard handlers
        handler_tuples = []
        handler_tuples.extend(self._handlers.get(event_type, []))
        handler_tuples.extend(self._handlers.get("*", []))
        
        if not handler_tuples:
            logger.warning(f"No handlers registered for event: {event_type}")
            return []
        
        results = []
        for handler, filter_obj in handler_tuples:
            try:
                # Check filter if present
                if filter_obj:
                    filter_passed = await filter_obj.check(event)
                    if not filter_passed:
                        logger.debug(f"Filter {filter_obj.__class__.__name__} did not pass for event {event_type}")
                        continue
                
                # Apply middlewares
                handler_to_call = handler
                for middleware in reversed(self._middlewares):
                    handler_to_call = self._wrap_middleware(middleware, handler_to_call)
                
                # Call handler
                if asyncio.iscoroutinefunction(handler_to_call):
                    result = await handler_to_call(event)
                else:
                    result = handler_to_call(event)
                
                results.append(result)
            except Exception as e:
                handler_name = handler.__name__ if hasattr(handler, '__name__') else str(handler)
                logger.error(f"Error processing event {event_type} with handler {handler_name}: {e}", exc_info=True)
        
        return results
    
    def _wrap_middleware(self, middleware: Callable, handler: Callable) -> Callable:
        """Wrap handler with middleware"""
        if asyncio.iscoroutinefunction(middleware):
            async def wrapped_async(event: WebhookEvent):
                return await middleware(event, handler)
            return wrapped_async
        else:
            async def wrapped_sync(event: WebhookEvent):
                return middleware(event, handler)
            return wrapped_sync
    
    def get_registered_events(self) -> List[str]:
        """Get list of registered event types"""
        return list(self._handlers.keys())
    
    def clear_handlers(self):
        """Clear all registered handlers"""
        self._handlers.clear()
        logger.info("All handlers cleared")

