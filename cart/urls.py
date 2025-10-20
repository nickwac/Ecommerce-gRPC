"""
URL configuration for Shopping Cart app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_cart, name='cart-detail'),
    path('add/', views.add_to_cart, name='cart-add'),
    path('item/<int:item_id>/', views.update_cart_item, name='cart-item-update'),
    path('item/<int:item_id>/remove/', views.remove_cart_item, name='cart-item-remove'),
    path('clear/', views.clear_cart, name='cart-clear'),
    path('summary/', views.cart_summary, name='cart-summary'),
]
