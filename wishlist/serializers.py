"""
Serializers for Wishlist app.
"""

from rest_framework import serializers
from .models import WishlistItem
from products.serializers import ProductSerializer


class WishlistItemSerializer(serializers.ModelSerializer):
    """Serializer for wishlist items."""
    
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = WishlistItem
        fields = [
            'id',
            'product',
            'product_id',
            'notes',
            'added_at',
            'is_in_stock',
            'product_price'
        ]
        read_only_fields = ['id', 'added_at']
    
    def validate_product_id(self, value):
        """Validate that product exists."""
        from products.models import Product
        
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product does not exist.")
        return value
    
    def create(self, validated_data):
        """Create wishlist item."""
        from products.models import Product
        
        product_id = validated_data.pop('product_id')
        product = Product.objects.get(id=product_id)
        user = self.context['request'].user
        
        # Check if already in wishlist
        if WishlistItem.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("Product already in wishlist.")
        
        wishlist_item = WishlistItem.objects.create(
            user=user,
            product=product,
            **validated_data
        )
        return wishlist_item


class WishlistSummarySerializer(serializers.Serializer):
    """Serializer for wishlist summary."""
    
    total_items = serializers.IntegerField()
    in_stock_count = serializers.IntegerField()
    out_of_stock_count = serializers.IntegerField()
