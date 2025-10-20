"""
Production settings for ecommerce_grpc project.
"""

from .base import *

DEBUG = False

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Production database (PostgreSQL recommended)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': env.str('DB_NAME'),
#         'USER': env.str('DB_USER'),
#         'PASSWORD': env.str('DB_PASSWORD'),
#         'HOST': env.str('DB_HOST'),
#         'PORT': env.int('DB_PORT', 5432),
#         'CONN_MAX_AGE': 600,
#         'OPTIONS': {
#             'connect_timeout': 10,
#         }
#     }
# }

# Email backend for production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.str('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', 587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL', 'noreply@example.com')

# Static files (use WhiteNoise or S3)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Increase cache timeout for production
CACHES['default']['TIMEOUT'] = 3600  # 1 hour

# Stricter CORS settings
CORS_ALLOW_ALL_ORIGINS = False

# Admin URL (change for security)
ADMIN_URL = env.str('ADMIN_URL', 'admin/')
