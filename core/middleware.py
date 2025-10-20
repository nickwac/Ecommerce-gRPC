"""
Custom middleware for the application.
"""

import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log request details and response time.
    """
    
    def process_request(self, request):
        """Store the start time when request comes in."""
        request.start_time = time.time()
        return None
    
    def process_response(self, request, response):
        """Log request details and calculate response time."""
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            log_data = {
                'method': request.method,
                'path': request.path,
                'status_code': response.status_code,
                'duration_ms': round(duration * 1000, 2),
                'user': str(request.user) if request.user.is_authenticated else 'Anonymous',
            }
            
            # Log based on status code
            if response.status_code >= 500:
                logger.error(f"Server Error: {log_data}")
            elif response.status_code >= 400:
                logger.warning(f"Client Error: {log_data}")
            else:
                logger.info(f"Request: {log_data}")
        
        return response
