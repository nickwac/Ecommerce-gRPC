"""
Views for Reviews app.
"""

from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.db.models import Avg, Count, Q
from .models import Review, ReviewHelpful
from .serializers import (
    ReviewSerializer,
    ReviewSummarySerializer,
    MarkHelpfulSerializer
)
from products.models import Product


class ProductReviewListView(generics.ListAPIView):
    """
    Get all reviews for a specific product.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        product_id = self.kwargs['product_id']
        queryset = Review.objects.filter(product_id=product_id).select_related('user')
        
        # Filter by rating if specified
        rating = self.request.query_params.get('rating')
        if rating:
            queryset = queryset.filter(rating=rating)
        
        # Filter verified purchases only
        verified_only = self.request.query_params.get('verified_only')
        if verified_only == 'true':
            queryset = queryset.filter(is_verified_purchase=True)
        
        # Sort options
        sort_by = self.request.query_params.get('sort_by', 'recent')
        if sort_by == 'helpful':
            queryset = queryset.order_by('-helpful_count')
        elif sort_by == 'rating_high':
            queryset = queryset.order_by('-rating', '-created_at')
        elif sort_by == 'rating_low':
            queryset = queryset.order_by('rating', '-created_at')
        else:  # recent
            queryset = queryset.order_by('-created_at')
        
        return queryset
    
    @extend_schema(
        summary="Get product reviews",
        description="Retrieve all reviews for a specific product with filtering and sorting options.",
        tags=["Reviews"],
        parameters=[
            OpenApiParameter('rating', int, description='Filter by rating (1-5)'),
            OpenApiParameter('verified_only', bool, description='Show only verified purchases'),
            OpenApiParameter('sort_by', str, description='Sort by: recent, helpful, rating_high, rating_low'),
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'reviews': serializer.data,
            'count': queryset.count()
        })


@extend_schema(
    summary="Create product review",
    description="Create a new review for a product.",
    tags=["Reviews"],
    request=ReviewSerializer
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request):
    """Create a new review."""
    serializer = ReviewSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Review created successfully',
            'review': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Update review",
    description="Update an existing review.",
    tags=["Reviews"],
    request=ReviewSerializer
)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_review(request, review_id):
    """Update a review."""
    try:
        review = Review.objects.get(id=review_id, user=request.user)
    except Review.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Review not found or you do not have permission to edit it'
        }, status=status.HTTP_404_NOT_FOUND)
    
    partial = request.method == 'PATCH'
    serializer = ReviewSerializer(
        review,
        data=request.data,
        partial=partial,
        context={'request': request}
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Review updated successfully',
            'review': serializer.data
        })
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Delete review",
    description="Delete a review.",
    tags=["Reviews"]
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, review_id):
    """Delete a review."""
    try:
        review = Review.objects.get(id=review_id, user=request.user)
    except Review.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Review not found or you do not have permission to delete it'
        }, status=status.HTTP_404_NOT_FOUND)
    
    review.delete()
    
    return Response({
        'success': True,
        'message': 'Review deleted successfully'
    }, status=status.HTTP_200_OK)


@extend_schema(
    summary="Get review statistics",
    description="Get rating statistics and distribution for a product.",
    tags=["Reviews"]
)
@api_view(['GET'])
def get_review_statistics(request, product_id):
    """Get review statistics for a product."""
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Product not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    reviews = Review.objects.filter(product=product)
    
    # Calculate statistics
    stats = reviews.aggregate(
        average_rating=Avg('rating'),
        total_reviews=Count('id')
    )
    
    # Rating distribution
    rating_distribution = {}
    for i in range(1, 6):
        rating_distribution[f'{i}_star'] = reviews.filter(rating=i).count()
    
    # Verified purchase count
    verified_count = reviews.filter(is_verified_purchase=True).count()
    
    return Response({
        'success': True,
        'statistics': {
            'average_rating': round(stats['average_rating'] or 0, 2),
            'total_reviews': stats['total_reviews'],
            'rating_distribution': rating_distribution,
            'verified_purchase_count': verified_count
        }
    })


@extend_schema(
    summary="Mark review as helpful",
    description="Mark a review as helpful or not helpful.",
    tags=["Reviews"],
    request=MarkHelpfulSerializer
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_review_helpful(request, review_id):
    """Mark a review as helpful or not helpful."""
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Review not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Prevent users from voting on their own reviews
    if review.user == request.user:
        return Response({
            'success': False,
            'error': 'You cannot vote on your own review'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = MarkHelpfulSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    is_helpful = serializer.validated_data['is_helpful']
    
    # Check if user has already voted
    vote, created = ReviewHelpful.objects.get_or_create(
        review=review,
        user=request.user,
        defaults={'is_helpful': is_helpful}
    )
    
    if not created:
        # Update existing vote
        old_vote = vote.is_helpful
        vote.is_helpful = is_helpful
        vote.save()
        
        # Update counts
        if old_vote != is_helpful:
            if old_vote:
                review.helpful_count -= 1
                review.not_helpful_count += 1
            else:
                review.helpful_count += 1
                review.not_helpful_count -= 1
            review.save()
        
        message = 'Vote updated'
    else:
        # New vote
        if is_helpful:
            review.helpful_count += 1
        else:
            review.not_helpful_count += 1
        review.save()
        
        message = 'Vote recorded'
    
    return Response({
        'success': True,
        'message': message,
        'helpful_count': review.helpful_count,
        'not_helpful_count': review.not_helpful_count
    })


@extend_schema(
    summary="Get user's reviews",
    description="Get all reviews written by the authenticated user.",
    tags=["Reviews"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_reviews(request):
    """Get all reviews by the current user."""
    reviews = Review.objects.filter(user=request.user).select_related('product')
    serializer = ReviewSerializer(reviews, many=True, context={'request': request})
    
    return Response({
        'success': True,
        'reviews': serializer.data,
        'count': reviews.count()
    })
