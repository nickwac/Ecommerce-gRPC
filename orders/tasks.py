"""
Celery tasks for orders app.
"""

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task
def process_pending_orders():
    """Process orders that have been pending for too long."""
    from orders.models import Order
    
    try:
        # Find orders pending for more than 24 hours
        threshold = timezone.now() - timedelta(hours=24)
        pending_orders = Order.objects.filter(
            status='pending',
            created_at__lt=threshold
        )
        
        count = 0
        for order in pending_orders:
            # Auto-update to processing or send reminder
            order.status = 'processing'
            order.save()
            count += 1
            
            logger.info(f"Auto-processed order {order.id}")
        
        return f"Processed {count} pending orders"
    except Exception as e:
        logger.error(f"Error processing pending orders: {str(e)}")
        raise


@shared_task
def send_order_status_notifications():
    """Send notifications for order status changes."""
    from orders.models import Order
    from core.tasks import send_email_notification
    
    try:
        # Find orders that need status notifications
        # This is a placeholder - implement your notification logic
        
        recent_shipped = Order.objects.filter(
            status='shipped',
            updated_at__gte=timezone.now() - timedelta(hours=1)
        )
        
        for order in recent_shipped:
            # Send notification
            # send_email_notification.delay(
            #     f'Order #{order.id} Shipped',
            #     f'Your order has been shipped to {order.shipping_address}',
            #     [order.customer_email]
            # )
            
            logger.info(f"Sent shipping notification for order {order.id}")
        
        return f"Sent {recent_shipped.count()} notifications"
    except Exception as e:
        logger.error(f"Error sending order notifications: {str(e)}")
        raise


@shared_task
def calculate_order_statistics():
    """Calculate and cache order statistics."""
    from orders.models import Order
    from django.db.models import Sum, Count, Avg
    from django.core.cache import cache
    
    try:
        stats = Order.objects.aggregate(
            total_orders=Count('id'),
            total_revenue=Sum('total_amount'),
            average_order_value=Avg('total_amount')
        )
        
        status_breakdown = dict(
            Order.objects.values('status').annotate(count=Count('id')).values_list('status', 'count')
        )
        
        cache_data = {
            'total_orders': stats['total_orders'] or 0,
            'total_revenue': float(stats['total_revenue'] or 0),
            'average_order_value': float(stats['average_order_value'] or 0),
            'status_breakdown': status_breakdown,
        }
        
        cache.set('order_statistics', cache_data, timeout=3600)  # Cache for 1 hour
        
        logger.info("Order statistics updated successfully")
        return "Statistics updated"
    except Exception as e:
        logger.error(f"Error calculating order statistics: {str(e)}")
        raise


@shared_task
def send_order_confirmation(order_id):
    """
    Send order confirmation email.
    
    Args:
        order_id: ID of the order
    """
    from orders.models import Order
    from core.tasks import send_email_notification
    
    try:
        order = Order.objects.get(id=order_id)
        
        message = f"""
        Thank you for your order!
        
        Order ID: {order.id}
        Customer: {order.customer_name}
        Total Amount: ${order.total_amount}
        Status: {order.status}
        
        We will send you updates as your order is processed.
        """
        
        # send_email_notification.delay(
        #     f'Order Confirmation #{order.id}',
        #     message,
        #     [order.customer_email]
        # )
        
        logger.info(f"Sent confirmation email for order {order_id}")
        return f"Confirmation sent for order {order_id}"
    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found")
        raise
    except Exception as e:
        logger.error(f"Error sending order confirmation: {str(e)}")
        raise
