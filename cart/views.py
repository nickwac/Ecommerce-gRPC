"""
Views for Shopping Cart app.
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Cart, CartItem
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer
)
from products.models import Product


@extend_schema(
    summary="Get cart",
    description="Retrieve the authenticated user's shopping cart.",
    tags=["Shopping Cart"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    """Get user's shopping cart."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart)
    
    return Response({
        'success': True,
        'cart': serializer.data
    }, status=status.HTTP_200_OK)


@extend_schema(
    summary="Add to cart",
    description="Add a product to the shopping cart.",
    tags=["Shopping Cart"],
    request=AddToCartSerializer
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    """Add a product to cart."""
    serializer = AddToCartSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    product_id = serializer.validated_data['product_id']
    quantity = serializer.validated_data['quantity']
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Product not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Check stock availability
    if product.stock_quantity < quantity:
        return Response({
            'success': False,
            'error': f'Only {product.stock_quantity} units available'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Get or create cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get or create cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        # If item already in cart, update quantity
        new_quantity = cart_item.quantity + quantity
        
        # Check if new quantity exceeds stock
        if product.stock_quantity < new_quantity:
            return Response({
                'success': False,
                'error': f'Cannot add {quantity} more. Only {product.stock_quantity - cart_item.quantity} units available'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item.quantity = new_quantity
        cart_item.save()
    
    cart_item_serializer = CartItemSerializer(cart_item)
    
    return Response({
        'success': True,
        'message': 'Product added to cart',
        'cart_item': cart_item_serializer.data
    }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@extend_schema(
    summary="Update cart item",
    description="Update the quantity of a cart item.",
    tags=["Shopping Cart"],
    request=UpdateCartItemSerializer
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):
    """Update cart item quantity."""
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return Response({
            'success': False,
            'error': 'Cart item not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UpdateCartItemSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    quantity = serializer.validated_data['quantity']
    
    # Check stock availability
    if cart_item.product.stock_quantity < quantity:
        return Response({
            'success': False,
            'error': f'Only {cart_item.product.stock_quantity} units available'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    cart_item.quantity = quantity
    cart_item.save()
    
    cart_item_serializer = CartItemSerializer(cart_item)
    
    return Response({
        'success': True,
        'message': 'Cart item updated',
        'cart_item': cart_item_serializer.data
    }, status=status.HTTP_200_OK)


@extend_schema(
    summary="Remove cart item",
    description="Remove an item from the shopping cart.",
    tags=["Shopping Cart"]
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_cart_item(request, item_id):
    """Remove item from cart."""
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return Response({
            'success': False,
            'error': 'Cart item not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    cart_item.delete()
    
    return Response({
        'success': True,
        'message': 'Item removed from cart'
    }, status=status.HTTP_200_OK)


@extend_schema(
    summary="Clear cart",
    description="Remove all items from the shopping cart.",
    tags=["Shopping Cart"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    """Clear all items from cart."""
    try:
        cart = Cart.objects.get(user=request.user)
        deleted_count = cart.items.count()
        cart.clear()
        
        return Response({
            'success': True,
            'message': f'Removed {deleted_count} items from cart',
            'deleted_count': deleted_count
        }, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({
            'success': True,
            'message': 'Cart is already empty',
            'deleted_count': 0
        }, status=status.HTTP_200_OK)


@extend_schema(
    summary="Get cart summary",
    description="Get a summary of the shopping cart.",
    tags=["Shopping Cart"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_summary(request):
    """Get cart summary."""
    try:
        cart = Cart.objects.get(user=request.user)
        
        return Response({
            'success': True,
            'summary': {
                'total_items': cart.total_items,
                'subtotal': float(cart.subtotal),
                'total': float(cart.total),
                'items_count': cart.items.count()
            }
        }, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({
            'success': True,
            'summary': {
                'total_items': 0,
                'subtotal': 0.0,
                'total': 0.0,
                'items_count': 0
            }
        }, status=status.HTTP_200_OK)
