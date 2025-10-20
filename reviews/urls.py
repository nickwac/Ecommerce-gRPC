"""
URL configuration for Reviews app.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Product reviews
    path('product/<int:product_id>/', views.ProductReviewListView.as_view(), name='product-reviews'),
    path('product/<int:product_id>/statistics/', views.get_review_statistics, name='review-statistics'),
    
    # Review CRUD
    path('create/', views.create_review, name='review-create'),
    path('<int:review_id>/', views.update_review, name='review-update'),
    path('<int:review_id>/delete/', views.delete_review, name='review-delete'),
    
    # Review interactions
    path('<int:review_id>/helpful/', views.mark_review_helpful, name='review-helpful'),
    
    # User reviews
    path('my-reviews/', views.get_user_reviews, name='user-reviews'),
]
