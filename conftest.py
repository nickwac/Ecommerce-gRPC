"""
Pytest configuration and fixtures.
"""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from products.models import Product
from orders.models import Order, OrderItem


@pytest.fixture
def api_client():
    """Return an API client for testing."""
    return APIClient()


@pytest.fixture
def user(db):
    """Create and return a test user."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def admin_user(db):
    """Create and return an admin user."""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Return an authenticated API client."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """Return an admin authenticated API client."""
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def product(db):
    """Create and return a test product."""
    return Product.objects.create(
        name='Test Product',
        description='A test product description',
        price=99.99,
        stock_quantity=100,
        category='electronics'
    )


@pytest.fixture
def products(db):
    """Create and return multiple test products."""
    return [
        Product.objects.create(
            name=f'Product {i}',
            description=f'Description {i}',
            price=10.00 * i,
            stock_quantity=50 + i,
            category='electronics' if i % 2 == 0 else 'books'
        )
        for i in range(1, 6)
    ]


@pytest.fixture
def order(db, product, user):
    """Create and return a test order."""
    order = Order.objects.create(
        customer_name='Test Customer',
        customer_email='customer@example.com',
        shipping_address='123 Test St',
        status='pending'
    )
    
    OrderItem.objects.create(
        order=order,
        product=product,
        product_name=product.name,
        quantity=2,
        price=product.price
    )
    
    order.calculate_total()
    return order
