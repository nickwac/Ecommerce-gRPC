"""
Celery tasks for products app.
"""

from celery import shared_task
from django.core.cache import cache
from django.db.models import Count, Avg
import logging

logger = logging.getLogger(__name__)


@shared_task
def update_product_analytics():
    """Update product analytics and cache statistics."""
    from products.models import Product
    
    try:
        # Calculate analytics
        total_products = Product.objects.count()
        avg_price = Product.objects.aggregate(Avg('price'))['price__avg']
        low_stock_count = Product.objects.filter(stock_quantity__lt=10).count()
        
        # Cache the results
        cache.set('product_analytics', {
            'total_products': total_products,
            'average_price': float(avg_price) if avg_price else 0,
            'low_stock_count': low_stock_count,
        }, timeout=3600 * 6)  # Cache for 6 hours
        
        logger.info("Product analytics updated successfully")
        return "Analytics updated"
    except Exception as e:
        logger.error(f"Error updating product analytics: {str(e)}")
        raise


@shared_task
def update_product_stock(product_id, quantity_change):
    """
    Update product stock asynchronously.
    
    Args:
        product_id: ID of the product
        quantity_change: Amount to change stock by (positive or negative)
    """
    from products.models import Product
    
    try:
        product = Product.objects.get(id=product_id)
        product.stock_quantity += quantity_change
        product.save()
        
        logger.info(f"Updated stock for product {product_id}: {quantity_change}")
        return f"Stock updated for product {product_id}"
    except Product.DoesNotExist:
        logger.error(f"Product {product_id} not found")
        raise
    except Exception as e:
        logger.error(f"Error updating product stock: {str(e)}")
        raise


@shared_task
def check_low_stock_products():
    """Check for low stock products and send notifications."""
    from products.models import Product
    from core.tasks import send_email_notification
    
    try:
        low_stock_products = Product.objects.filter(stock_quantity__lt=10)
        
        if low_stock_products.exists():
            product_list = '\n'.join([
                f"- {p.name}: {p.stock_quantity} units remaining"
                for p in low_stock_products
            ])
            
            message = f"The following products are low on stock:\n\n{product_list}"
            
            # Send notification (implement recipient list from settings)
            # send_email_notification.delay(
            #     'Low Stock Alert',
            #     message,
            #     ['admin@example.com']
            # )
            
            logger.info(f"Low stock alert for {low_stock_products.count()} products")
            return f"Checked {low_stock_products.count()} low stock products"
        
        return "No low stock products"
    except Exception as e:
        logger.error(f"Error checking low stock: {str(e)}")
        raise
