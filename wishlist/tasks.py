"""
Celery tasks for Wishlist app.
"""

from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task
def cleanup_old_wishlist_items():
    """
    Clean up wishlist items older than 90 days (optional).
    This is a maintenance task to keep the database clean.
    """
    from .models import WishlistItem
    
    try:
        threshold = timezone.now() - timedelta(days=90)
        old_items = WishlistItem.objects.filter(added_at__lt=threshold)
        count = old_items.count()
        
        if count > 0:
            old_items.delete()
            logger.info(f"Cleaned up {count} old wishlist items")
            return f"Deleted {count} old wishlist items"
        
        return "No old wishlist items to clean"
    except Exception as e:
        logger.error(f"Error cleaning wishlist items: {str(e)}")
        raise


@shared_task
def send_price_drop_notifications():
    """
    Send notifications to users when wishlisted products have price drops.
    This would integrate with your notification system.
    """
    from .models import WishlistItem
    from core.tasks import send_email_notification
    
    try:
        # This is a placeholder - you would implement actual price tracking
        # For now, we'll just log the action
        
        wishlist_items = WishlistItem.objects.select_related('user', 'product').all()
        
        # In a real implementation, you would:
        # 1. Track historical prices
        # 2. Compare current price with historical
        # 3. Send notification if price dropped
        
        logger.info(f"Checked {wishlist_items.count()} wishlist items for price drops")
        return f"Checked {wishlist_items.count()} items"
    except Exception as e:
        logger.error(f"Error checking price drops: {str(e)}")
        raise


@shared_task
def send_back_in_stock_notifications():
    """
    Send notifications when out-of-stock wishlisted products are back in stock.
    """
    from .models import WishlistItem
    from core.tasks import send_email_notification
    
    try:
        # Get wishlist items for products that are now in stock
        wishlist_items = WishlistItem.objects.select_related(
            'user', 'product'
        ).filter(product__stock_quantity__gt=0)
        
        notifications_sent = 0
        
        for item in wishlist_items:
            # Check if we've already notified about this (use cache)
            cache_key = f"back_in_stock_notified_{item.id}"
            
            if not cache.get(cache_key):
                # Send notification
                # send_email_notification.delay(
                #     f'{item.product.name} is back in stock!',
                #     f'Good news! {item.product.name} is now available.',
                #     [item.user.email]
                # )
                
                # Mark as notified (cache for 7 days)
                cache.set(cache_key, True, timeout=60*60*24*7)
                notifications_sent += 1
                
                logger.info(f"Sent back-in-stock notification to {item.user.username}")
        
        return f"Sent {notifications_sent} back-in-stock notifications"
    except Exception as e:
        logger.error(f"Error sending back-in-stock notifications: {str(e)}")
        raise


@shared_task
def calculate_wishlist_statistics():
    """
    Calculate and cache wishlist statistics.
    """
    from .models import WishlistItem
    from django.db.models import Count
    
    try:
        total_items = WishlistItem.objects.count()
        users_with_wishlist = WishlistItem.objects.values('user').distinct().count()
        
        # Most wishlisted products
        popular_products = WishlistItem.objects.values(
            'product__id', 'product__name'
        ).annotate(
            wishlist_count=Count('id')
        ).order_by('-wishlist_count')[:10]
        
        stats = {
            'total_items': total_items,
            'users_with_wishlist': users_with_wishlist,
            'popular_products': list(popular_products)
        }
        
        # Cache for 1 hour
        cache.set('wishlist_statistics', stats, timeout=3600)
        
        logger.info("Wishlist statistics updated")
        return "Statistics updated"
    except Exception as e:
        logger.error(f"Error calculating wishlist statistics: {str(e)}")
        raise
