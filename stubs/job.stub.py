import structlog

logger = structlog.get_logger()


class {{ class_name }}:
    """{{ class_name }} background job."""

    async def execute(self, *args, **kwargs):
        """
        Execute the job logic.
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
        """
        logger.info("job.started", job="{{ snake_name }}")
        
        try:
            # TODO: Implement job logic here
            logger.info("job.completed", job="{{ snake_name }}")
        except Exception as e:
            logger.error("job.failed", job="{{ snake_name }}", error=str(e))
            raise
