"""
Celery configuration for ecommerce_grpc project.
"""

import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_grpc.settings')

app = Celery('ecommerce_grpc')

# Load configuration from Django settings with CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    'cleanup-expired-sessions': {
        'task': 'core.tasks.cleanup_expired_sessions',
        'schedule': crontab(hour=2, minute=0),  # Run daily at 2 AM
    },
    'update-product-analytics': {
        'task': 'products.tasks.update_product_analytics',
        'schedule': crontab(hour='*/6'),  # Run every 6 hours
    },
    'process-pending-orders': {
        'task': 'orders.tasks.process_pending_orders',
        'schedule': crontab(minute='*/30'),  # Run every 30 minutes
    },
    'send-order-status-notifications': {
        'task': 'orders.tasks.send_order_status_notifications',
        'schedule': crontab(minute='*/15'),  # Run every 15 minutes
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task for testing Celery."""
    print(f'Request: {self.request!r}')
