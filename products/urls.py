from django.urls import path
from products.views import (
    ProductListCreateView,
    ProductDetailView,
    ProductSearchView
)

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('search/', ProductSearchView.as_view(), name='product-search'),
]
