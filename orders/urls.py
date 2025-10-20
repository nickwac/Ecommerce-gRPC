from django.urls import path
from orders.views import (
    OrderListCreateView,
    OrderDetailView,
    OrderStatusUpdateView,
    OrderCancelView,
    CustomerOrdersView
)

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order-list-create'),
    path('<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('<int:order_id>/status/', OrderStatusUpdateView.as_view(), name='order-status-update'),
    path('<int:order_id>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
    path('customer/<str:customer_email>/', CustomerOrdersView.as_view(), name='customer-orders'),
]
