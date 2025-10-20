"""
Custom exception handlers for the application.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # If response is None, it's an unhandled exception
    if response is None:
        logger.exception(f"Unhandled exception: {exc}")
        return Response(
            {
                'error': 'Internal server error',
                'detail': str(exc) if hasattr(exc, '__str__') else 'An unexpected error occurred',
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Customize the response format
    custom_response_data = {
        'error': response.data.get('detail', 'An error occurred'),
        'status_code': response.status_code,
    }
    
    # Add field-specific errors if they exist
    if isinstance(response.data, dict):
        errors = {k: v for k, v in response.data.items() if k != 'detail'}
        if errors:
            custom_response_data['errors'] = errors
    
    response.data = custom_response_data
    
    return response


class ServiceUnavailableException(Exception):
    """Exception raised when a gRPC service is unavailable."""
    pass


class InvalidRequestException(Exception):
    """Exception raised when request validation fails."""
    pass
