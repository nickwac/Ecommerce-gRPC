"""
Wishlist models for saving favorite products.
"""

from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class WishlistItem(models.Model):
    """
    Model representing a product in a user's wishlist.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wishlist_items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='wishlisted_by'
    )
    added_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True, help_text="Optional notes about this item")
    
    class Meta:
        ordering = ['-added_at']
        unique_together = ['user', 'product']
        indexes = [
            models.Index(fields=['user', '-added_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username}'s wishlist - {self.product.name}"
    
    @property
    def is_in_stock(self):
        """Check if the wishlisted product is in stock."""
        return self.product.is_in_stock()
    
    @property
    def product_price(self):
        """Get current product price."""
        return self.product.price
