"""
Models for Payment Processing.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from orders.models import Order


class PaymentMethod(models.Model):
    """
    Model representing a saved payment method.
    """
    PAYMENT_TYPE_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payment_methods'
    )
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    stripe_payment_method_id = models.CharField(max_length=255, blank=True, null=True)
    
    # Card details (last 4 digits, brand, expiry)
    card_last4 = models.CharField(max_length=4, blank=True)
    card_brand = models.CharField(max_length=20, blank=True)
    card_exp_month = models.IntegerField(null=True, blank=True)
    card_exp_year = models.IntegerField(null=True, blank=True)
    
    # PayPal details
    paypal_email = models.EmailField(blank=True)
    
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_default', '-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        if self.payment_type == 'card':
            return f"{self.card_brand} ****{self.card_last4}"
        elif self.payment_type == 'paypal':
            return f"PayPal ({self.paypal_email})"
        return f"{self.get_payment_type_display()}"
    
    def save(self, *args, **kwargs):
        # If this is set as default, unset other defaults
        if self.is_default:
            PaymentMethod.objects.filter(
                user=self.user,
                is_default=True
            ).exclude(id=self.id).update(is_default=False)
        super().save(*args, **kwargs)


class Payment(models.Model):
    """
    Model representing a payment transaction.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('canceled', 'Canceled'),
        ('refunded', 'Refunded'),
        ('partially_refunded', 'Partially Refunded'),
    ]
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='payments'
    )
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments'
    )
    
    # Payment details
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Stripe details
    stripe_payment_intent_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    stripe_charge_id = models.CharField(max_length=255, blank=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    
    # Transaction details
    description = models.TextField(blank=True)
    failure_message = models.TextField(blank=True)
    receipt_url = models.URLField(blank=True)
    
    # Refund details
    refund_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    refund_reason = models.TextField(blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order', '-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['stripe_payment_intent_id']),
        ]
    
    def __str__(self):
        return f"Payment {self.id} - {self.status} - ${self.amount}"
    
    @property
    def is_successful(self):
        """Check if payment was successful."""
        return self.status == 'succeeded'
    
    @property
    def can_be_refunded(self):
        """Check if payment can be refunded."""
        return self.status == 'succeeded' and self.refund_amount < self.amount


class Refund(models.Model):
    """
    Model representing a refund transaction.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('canceled', 'Canceled'),
    ]
    
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='refunds'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Stripe details
    stripe_refund_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['payment', '-created_at']),
        ]
    
    def __str__(self):
        return f"Refund {self.id} - ${self.amount} - {self.status}"
