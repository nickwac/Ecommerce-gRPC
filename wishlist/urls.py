"""
URL configuration for Wishlist app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.WishlistListView.as_view(), name='wishlist-list'),
    path('add/', views.add_to_wishlist, name='wishlist-add'),
    path('remove/<int:product_id>/', views.remove_from_wishlist, name='wishlist-remove'),
    path('clear/', views.clear_wishlist, name='wishlist-clear'),
    path('move-to-cart/<int:product_id>/', views.move_to_cart, name='wishlist-move-to-cart'),
    path('check/<int:product_id>/', views.check_in_wishlist, name='wishlist-check'),
]
