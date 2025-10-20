"""
Views for Wishlist app.
"""

from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.db.models import Q
from .models import WishlistItem
from .serializers import WishlistItemSerializer, WishlistSummarySerializer
from products.models import Product


class WishlistListView(generics.ListAPIView):
    """
    Get user's wishlist.
    """
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user).select_related('product')
    
    @extend_schema(
        summary="Get wishlist",
        description="Retrieve all items in the authenticated user's wishlist.",
        tags=["Wishlist"]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Calculate summary
        total_items = queryset.count()
        in_stock_count = sum(1 for item in queryset if item.is_in_stock)
        out_of_stock_count = total_items - in_stock_count
        
        return Response({
            'success': True,
            'wishlist': serializer.data,
            'summary': {
                'total_items': total_items,
                'in_stock_count': in_stock_count,
                'out_of_stock_count': out_of_stock_count
            }
        })


@extend_schema(
    summary="Add to wishlist",
    description="Add a product to the user's wishlist.",
    tags=["Wishlist"],
    request=WishlistItemSerializer
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request):
    """Add a product to wishlist."""
    serializer = WishlistItemSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Product added to wishlist',
            'item': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Remove from wishlist",
    description="Remove a product from the user's wishlist.",
    tags=["Wishlist"]
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, product_id):
    """Remove a product from wishlist."""
    try:
        wishlist_item = WishlistItem.objects.get(
            user=request.user,
            product_id=product_id
        )
        wishlist_item.delete()
        
        return Response({
            'success': True,
            'message': 'Product removed from wishlist'
        }, status=status.HTTP_200_OK)
    
    except WishlistItem.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Product not in wishlist'
        }, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    summary="Clear wishlist",
    description="Remove all items from the user's wishlist.",
    tags=["Wishlist"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_wishlist(request):
    """Clear all items from wishlist."""
    deleted_count = WishlistItem.objects.filter(user=request.user).delete()[0]
    
    return Response({
        'success': True,
        'message': f'Removed {deleted_count} items from wishlist',
        'deleted_count': deleted_count
    }, status=status.HTTP_200_OK)


@extend_schema(
    summary="Move to cart",
    description="Move a wishlist item to shopping cart.",
    tags=["Wishlist"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def move_to_cart(request, product_id):
    """Move a wishlist item to cart."""
    try:
        wishlist_item = WishlistItem.objects.get(
            user=request.user,
            product_id=product_id
        )
        
        # Check if product is in stock
        if not wishlist_item.is_in_stock:
            return Response({
                'success': False,
                'error': 'Product is out of stock'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Add to cart (import here to avoid circular import)
        from cart.models import Cart, CartItem
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Check if already in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=wishlist_item.product,
            defaults={'quantity': 1}
        )
        
        if not created:
            # If already in cart, increment quantity
            cart_item.quantity += 1
            cart_item.save()
        
        # Remove from wishlist
        wishlist_item.delete()
        
        return Response({
            'success': True,
            'message': 'Product moved to cart',
            'cart_item_id': cart_item.id
        }, status=status.HTTP_200_OK)
    
    except WishlistItem.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Product not in wishlist'
        }, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    summary="Check if in wishlist",
    description="Check if a product is in the user's wishlist.",
    tags=["Wishlist"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_in_wishlist(request, product_id):
    """Check if a product is in wishlist."""
    exists = WishlistItem.objects.filter(
        user=request.user,
        product_id=product_id
    ).exists()
    
    return Response({
        'in_wishlist': exists,
        'product_id': product_id
    }, status=status.HTTP_200_OK)
