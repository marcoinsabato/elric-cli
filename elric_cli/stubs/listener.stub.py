import structlog

logger = structlog.get_logger()


class {{ class_name }}:
    """{{ class_name }} event listener."""

    async def handle(self, event):
        """
        Handle the event.
        
        Args:
            event: The event to handle
        """
        logger.info("listener.handling", listener="{{ snake_name }}", event=event.to_dict())
        
        try:
            # TODO: Implement event handling logic here
            logger.info("listener.handled", listener="{{ snake_name }}")
        except Exception as e:
            logger.error("listener.failed", listener="{{ snake_name }}", error=str(e))
            raise
