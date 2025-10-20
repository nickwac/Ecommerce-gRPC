"""
Shopping cart models for managing user carts.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from products.models import Product


class Cart(models.Model):
    """
    Model representing a user's shopping cart.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        null=True,
        blank=True
    )
    session_key = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Session key for anonymous users"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['session_key']),
        ]
    
    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Anonymous cart {self.session_key}"
    
    @property
    def total_items(self):
        """Get total number of items in cart."""
        return sum(item.quantity for item in self.items.all())
    
    @property
    def subtotal(self):
        """Calculate cart subtotal."""
        return sum(item.subtotal for item in self.items.all())
    
    @property
    def total(self):
        """Calculate cart total (can include tax, shipping later)."""
        return self.subtotal
    
    def clear(self):
        """Remove all items from cart."""
        self.items.all().delete()


class CartItem(models.Model):
    """
    Model representing an item in a shopping cart.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-added_at']
        unique_together = ['cart', 'product']
        indexes = [
            models.Index(fields=['cart', '-added_at']),
        ]
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name} in cart"
    
    @property
    def price(self):
        """Get current product price."""
        return self.product.price
    
    @property
    def subtotal(self):
        """Calculate subtotal for this item."""
        return Decimal(str(self.product.price)) * self.quantity
    
    @property
    def is_available(self):
        """Check if product is available in requested quantity."""
        return self.product.stock_quantity >= self.quantity
    
    def save(self, *args, **kwargs):
        """Override save to update cart's updated_at timestamp."""
        super().save(*args, **kwargs)
        self.cart.save()  # Update cart's updated_at
