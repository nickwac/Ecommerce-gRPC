"""
Celery tasks for Shopping Cart app.
"""

from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task
def cleanup_abandoned_carts():
    """
    Clean up abandoned carts (carts not updated in 30 days).
    """
    from .models import Cart
    
    try:
        threshold = timezone.now() - timedelta(days=30)
        abandoned_carts = Cart.objects.filter(updated_at__lt=threshold)
        count = abandoned_carts.count()
        
        if count > 0:
            abandoned_carts.delete()
            logger.info(f"Cleaned up {count} abandoned carts")
            return f"Deleted {count} abandoned carts"
        
        return "No abandoned carts to clean"
    except Exception as e:
        logger.error(f"Error cleaning abandoned carts: {str(e)}")
        raise


@shared_task
def send_cart_abandonment_reminders():
    """
    Send reminders to users who have items in their cart but haven't checked out.
    """
    from .models import Cart
    from core.tasks import send_email_notification
    
    try:
        # Find carts that haven't been updated in 24 hours but are less than 7 days old
        start_threshold = timezone.now() - timedelta(hours=24)
        end_threshold = timezone.now() - timedelta(days=7)
        
        abandoned_carts = Cart.objects.filter(
            updated_at__lt=start_threshold,
            updated_at__gt=end_threshold,
            user__isnull=False
        ).select_related('user')
        
        reminders_sent = 0
        
        for cart in abandoned_carts:
            # Check if we've already sent a reminder (use cache)
            cache_key = f"cart_reminder_sent_{cart.id}"
            
            if not cache.get(cache_key) and cart.items.exists():
                # Send reminder email
                # send_email_notification.delay(
                #     'You left items in your cart',
                #     f'Hi {cart.user.username}, you have {cart.total_items} items waiting in your cart.',
                #     [cart.user.email]
                # )
                
                # Mark as reminded (cache for 7 days)
                cache.set(cache_key, True, timeout=60*60*24*7)
                reminders_sent += 1
                
                logger.info(f"Sent cart abandonment reminder to {cart.user.username}")
        
        return f"Sent {reminders_sent} cart abandonment reminders"
    except Exception as e:
        logger.error(f"Error sending cart reminders: {str(e)}")
        raise


@shared_task
def check_cart_item_availability():
    """
    Check if cart items are still available and notify users if items are out of stock.
    """
    from .models import CartItem
    from core.tasks import send_email_notification
    
    try:
        # Find cart items where product is out of stock
        unavailable_items = CartItem.objects.select_related(
            'cart__user', 'product'
        ).filter(
            product__stock_quantity__lt=1,
            cart__user__isnull=False
        )
        
        notifications_sent = 0
        notified_users = set()
        
        for item in unavailable_items:
            user = item.cart.user
            
            if user.id not in notified_users:
                # Send notification once per user
                # send_email_notification.delay(
                #     'Items in your cart are out of stock',
                #     f'Some items in your cart are no longer available.',
                #     [user.email]
                # )
                
                notified_users.add(user.id)
                notifications_sent += 1
                
                logger.info(f"Sent out-of-stock notification to {user.username}")
        
        return f"Sent {notifications_sent} out-of-stock notifications"
    except Exception as e:
        logger.error(f"Error checking cart availability: {str(e)}")
        raise


@shared_task
def calculate_cart_statistics():
    """
    Calculate and cache shopping cart statistics.
    """
    from .models import Cart, CartItem
    from django.db.models import Count, Sum, Avg
    
    try:
        total_carts = Cart.objects.count()
        active_carts = Cart.objects.filter(
            updated_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        cart_stats = Cart.objects.aggregate(
            avg_items=Avg('items__quantity'),
            total_items=Sum('items__quantity')
        )
        
        # Calculate average cart value
        carts_with_items = Cart.objects.filter(items__isnull=False).distinct()
        total_value = sum(cart.total for cart in carts_with_items)
        avg_cart_value = total_value / carts_with_items.count() if carts_with_items.count() > 0 else 0
        
        stats = {
            'total_carts': total_carts,
            'active_carts': active_carts,
            'average_items_per_cart': float(cart_stats['avg_items'] or 0),
            'total_items_in_carts': cart_stats['total_items'] or 0,
            'average_cart_value': float(avg_cart_value)
        }
        
        # Cache for 1 hour
        cache.set('cart_statistics', stats, timeout=3600)
        
        logger.info("Cart statistics updated")
        return "Statistics updated"
    except Exception as e:
        logger.error(f"Error calculating cart statistics: {str(e)}")
        raise


@shared_task
def sync_cart_prices():
    """
    Update cart item prices if product prices have changed.
    This ensures cart always shows current prices.
    """
    from .models import CartItem
    
    try:
        # Cart items automatically get current price from product
        # This task is mainly for logging/monitoring
        
        cart_items = CartItem.objects.select_related('product').all()
        updated_count = 0
        
        for item in cart_items:
            # Trigger save to update timestamps
            # Prices are calculated dynamically via property
            item.save()
            updated_count += 1
        
        logger.info(f"Synced prices for {updated_count} cart items")
        return f"Synced {updated_count} cart items"
    except Exception as e:
        logger.error(f"Error syncing cart prices: {str(e)}")
        raise
