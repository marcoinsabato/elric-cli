import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = structlog.get_logger()


class {{ class_name }}(BaseHTTPMiddleware):
    """{{ class_name }} middleware."""

    async def dispatch(self, request: Request, call_next):
        """
        Process the request.
        
        Args:
            request: The incoming request
            call_next: The next middleware/route handler
            
        Returns:
            Response from the next handler
        """
        logger.debug("middleware.before", middleware="{{ snake_name }}", path=request.url.path)
        
        # TODO: Add pre-processing logic here
        
        response = await call_next(request)
        
        # TODO: Add post-processing logic here
        
        logger.debug("middleware.after", middleware="{{ snake_name }}", status_code=response.status_code)
        
        return response
