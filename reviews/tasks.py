"""
Celery tasks for Reviews app.
"""

from celery import shared_task
from django.core.cache import cache
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task
def calculate_product_ratings():
    """
    Calculate and cache average ratings for all products.
    """
    from products.models import Product
    from .models import Review
    
    try:
        products = Product.objects.all()
        updated_count = 0
        
        for product in products:
            reviews = Review.objects.filter(product=product)
            stats = reviews.aggregate(
                average_rating=Avg('rating'),
                total_reviews=Count('id')
            )
            
            # Cache the rating
            cache_key = f'product_rating_{product.id}'
            cache.set(cache_key, {
                'average_rating': round(stats['average_rating'] or 0, 2),
                'total_reviews': stats['total_reviews']
            }, timeout=3600 * 24)  # Cache for 24 hours
            
            updated_count += 1
        
        logger.info(f"Updated ratings for {updated_count} products")
        return f"Updated {updated_count} product ratings"
    except Exception as e:
        logger.error(f"Error calculating product ratings: {str(e)}")
        raise


@shared_task
def send_review_reminder_emails():
    """
    Send review reminder emails to users who purchased but haven't reviewed.
    """
    from orders.models import OrderItem
    from .models import Review
    from core.tasks import send_email_notification
    
    try:
        # Find orders from 7 days ago
        seven_days_ago = timezone.now() - timedelta(days=7)
        
        # Get order items from completed orders
        order_items = OrderItem.objects.filter(
            order__status='delivered',
            order__created_at__date=seven_days_ago.date()
        ).select_related('order', 'product')
        
        reminders_sent = 0
        
        for item in order_items:
            # Check if user has already reviewed this product
            if not Review.objects.filter(
                product=item.product,
                user=item.order.user if hasattr(item.order, 'user') else None
            ).exists():
                # Send reminder email
                # send_email_notification.delay(
                #     f'Review your purchase: {item.product.name}',
                #     f'How was your experience with {item.product.name}?',
                #     [item.order.customer_email]
                # )
                reminders_sent += 1
                logger.info(f"Sent review reminder for order {item.order.id}")
        
        return f"Sent {reminders_sent} review reminders"
    except Exception as e:
        logger.error(f"Error sending review reminders: {str(e)}")
        raise


@shared_task
def moderate_reviews():
    """
    Auto-moderate reviews for spam or inappropriate content.
    This is a placeholder for future ML-based moderation.
    """
    from .models import Review
    
    try:
        # Get recent reviews (last 24 hours)
        yesterday = timezone.now() - timedelta(days=1)
        recent_reviews = Review.objects.filter(created_at__gte=yesterday)
        
        flagged_count = 0
        
        for review in recent_reviews:
            # Simple spam detection (placeholder)
            spam_keywords = ['spam', 'fake', 'scam']
            comment_lower = review.comment.lower()
            
            if any(keyword in comment_lower for keyword in spam_keywords):
                # Flag for manual review
                logger.warning(f"Review {review.id} flagged for moderation")
                flagged_count += 1
        
        logger.info(f"Moderated {recent_reviews.count()} reviews, flagged {flagged_count}")
        return f"Moderated {recent_reviews.count()} reviews"
    except Exception as e:
        logger.error(f"Error moderating reviews: {str(e)}")
        raise


@shared_task
def calculate_review_statistics():
    """
    Calculate and cache review statistics.
    """
    from .models import Review
    
    try:
        # Overall statistics
        total_reviews = Review.objects.count()
        avg_rating = Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0
        verified_reviews = Review.objects.filter(is_verified_purchase=True).count()
        
        # Rating distribution
        rating_dist = {}
        for i in range(1, 6):
            rating_dist[f'{i}_star'] = Review.objects.filter(rating=i).count()
        
        # Most helpful reviewers
        from django.contrib.auth.models import User
        top_reviewers = User.objects.annotate(
            review_count=Count('reviews'),
            total_helpful=Count('reviews__helpful_votes', filter=models.Q(reviews__helpful_votes__is_helpful=True))
        ).order_by('-total_helpful')[:10]
        
        stats = {
            'total_reviews': total_reviews,
            'average_rating': round(avg_rating, 2),
            'verified_reviews': verified_reviews,
            'rating_distribution': rating_dist,
            'top_reviewers': [
                {'username': r.username, 'review_count': r.review_count, 'helpful_votes': r.total_helpful}
                for r in top_reviewers
            ]
        }
        
        # Cache for 1 hour
        cache.set('review_statistics', stats, timeout=3600)
        
        logger.info("Review statistics updated")
        return "Statistics updated"
    except Exception as e:
        logger.error(f"Error calculating review statistics: {str(e)}")
        raise


@shared_task
def cleanup_old_review_votes():
    """
    Clean up old review helpful votes (optional maintenance).
    """
    from .models import ReviewHelpful
    
    try:
        # Remove votes older than 1 year
        one_year_ago = timezone.now() - timedelta(days=365)
        old_votes = ReviewHelpful.objects.filter(created_at__lt=one_year_ago)
        count = old_votes.count()
        
        if count > 0:
            old_votes.delete()
            logger.info(f"Cleaned up {count} old review votes")
            return f"Deleted {count} old votes"
        
        return "No old votes to clean"
    except Exception as e:
        logger.error(f"Error cleaning review votes: {str(e)}")
        raise
