"""
Development settings for ecommerce_grpc project.
"""

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Development-specific apps
# INSTALLED_APPS += [
#     'django_extensions',  # Optional: install with pip install django-extensions
# ]

# CORS - Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True

# Disable some security features for development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Simplified logging for development
LOGGING['handlers']['console']['level'] = 'DEBUG'
LOGGING['loggers']['django']['level'] = 'DEBUG'

# Cache timeout - shorter for development
CACHES['default']['TIMEOUT'] = 60  # 1 minute

# Show SQL queries in console (optional)
# LOGGING['loggers']['django.db.backends'] = {
#     'level': 'DEBUG',
#     'handlers': ['console'],
# }
