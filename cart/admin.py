from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Inline admin for cart items."""
    model = CartItem
    extra = 0
    readonly_fields = ['price', 'subtotal', 'added_at', 'updated_at']
    fields = ['product', 'quantity', 'price', 'subtotal', 'added_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin interface for Cart."""
    
    list_display = ['id', 'user', 'session_key', 'total_items', 'subtotal', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'session_key']
    readonly_fields = ['created_at', 'updated_at', 'total_items', 'subtotal', 'total']
    inlines = [CartItemInline]
    
    def total_items(self, obj):
        return obj.total_items
    total_items.short_description = 'Total Items'
    
    def subtotal(self, obj):
        return f'${obj.subtotal:.2f}'
    subtotal.short_description = 'Subtotal'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin interface for CartItem."""
    
    list_display = ['id', 'cart', 'product', 'quantity', 'price', 'subtotal', 'is_available', 'added_at']
    list_filter = ['added_at', 'updated_at']
    search_fields = ['product__name', 'cart__user__username']
    readonly_fields = ['price', 'subtotal', 'added_at', 'updated_at']
    
    def is_available(self, obj):
        return obj.is_available
    is_available.boolean = True
    is_available.short_description = 'Available'
