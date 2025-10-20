"""
Settings package for ecommerce_grpc project.
Automatically loads the appropriate settings based on DJANGO_ENV environment variable.
"""

import os

# Determine which settings to use
env = os.environ.get('DJANGO_ENV', 'development')

if env == 'production':
    from .production import *
elif env == 'testing':
    from .testing import *
else:
    from .development import *
