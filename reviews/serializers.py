"""
Serializers for Reviews app.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Review, ReviewHelpful, ReviewImage


class UserSerializer(serializers.ModelSerializer):
    """Simple user serializer for review author."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class ReviewImageSerializer(serializers.ModelSerializer):
    """Serializer for review images."""
    
    class Meta:
        model = ReviewImage
        fields = ['id', 'image', 'caption', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for product reviews."""
    
    user = UserSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    images = ReviewImageSerializer(many=True, read_only=True)
    helpful_percentage = serializers.FloatField(read_only=True)
    user_vote = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = [
            'id',
            'product_id',
            'user',
            'rating',
            'title',
            'comment',
            'is_verified_purchase',
            'helpful_count',
            'not_helpful_count',
            'helpful_percentage',
            'user_vote',
            'images',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'user',
            'is_verified_purchase',
            'helpful_count',
            'not_helpful_count',
            'created_at',
            'updated_at'
        ]
    
    def get_user_vote(self, obj):
        """Get current user's vote on this review."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                vote = ReviewHelpful.objects.get(review=obj, user=request.user)
                return 'helpful' if vote.is_helpful else 'not_helpful'
            except ReviewHelpful.DoesNotExist:
                return None
        return None
    
    def validate_rating(self, value):
        """Validate rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
    
    def validate_product_id(self, value):
        """Validate that product exists."""
        from products.models import Product
        
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product does not exist.")
        return value
    
    def validate(self, data):
        """Validate that user hasn't already reviewed this product."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            product_id = data.get('product_id')
            if self.instance is None:  # Creating new review
                if Review.objects.filter(
                    product_id=product_id,
                    user=request.user
                ).exists():
                    raise serializers.ValidationError(
                        "You have already reviewed this product."
                    )
        return data
    
    def create(self, validated_data):
        """Create review."""
        from products.models import Product
        
        product_id = validated_data.pop('product_id')
        product = Product.objects.get(id=product_id)
        user = self.context['request'].user
        
        # Check if user has purchased this product (optional)
        # from orders.models import OrderItem
        # is_verified = OrderItem.objects.filter(
        #     order__user=user,
        #     product=product
        # ).exists()
        
        review = Review.objects.create(
            product=product,
            user=user,
            # is_verified_purchase=is_verified,
            **validated_data
        )
        return review


class ReviewSummarySerializer(serializers.Serializer):
    """Serializer for review statistics."""
    
    average_rating = serializers.FloatField()
    total_reviews = serializers.IntegerField()
    rating_distribution = serializers.DictField()
    verified_purchase_count = serializers.IntegerField()


class MarkHelpfulSerializer(serializers.Serializer):
    """Serializer for marking review as helpful/not helpful."""
    
    is_helpful = serializers.BooleanField()
