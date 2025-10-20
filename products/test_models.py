"""
Unit tests for Product models.
"""

import pytest
from decimal import Decimal
from products.models import Product


@pytest.mark.django_db
class TestProductModel:
    """Test cases for Product model."""
    
    def test_create_product(self):
        """Test creating a product."""
        product = Product.objects.create(
            name='Test Laptop',
            description='A test laptop',
            price=Decimal('999.99'),
            stock_quantity=50,
            category='electronics'
        )
        
        assert product.id is not None
        assert product.name == 'Test Laptop'
        assert product.price == Decimal('999.99')
        assert product.stock_quantity == 50
        assert product.category == 'electronics'
        assert product.created_at is not None
        assert product.updated_at is not None
    
    def test_product_str(self):
        """Test product string representation."""
        product = Product.objects.create(
            name='Test Product',
            description='Description',
            price=Decimal('50.00'),
            stock_quantity=10,
            category='books'
        )
        
        assert str(product) == 'Test Product'
    
    def test_is_in_stock(self):
        """Test is_in_stock method."""
        product_in_stock = Product.objects.create(
            name='In Stock',
            description='Description',
            price=Decimal('10.00'),
            stock_quantity=5,
            category='books'
        )
        
        product_out_of_stock = Product.objects.create(
            name='Out of Stock',
            description='Description',
            price=Decimal('10.00'),
            stock_quantity=0,
            category='books'
        )
        
        assert product_in_stock.is_in_stock() is True
        assert product_out_of_stock.is_in_stock() is False
    
    def test_product_ordering(self):
        """Test products are ordered by created_at descending."""
        product1 = Product.objects.create(
            name='First',
            description='First product',
            price=Decimal('10.00'),
            stock_quantity=10,
            category='books'
        )
        
        product2 = Product.objects.create(
            name='Second',
            description='Second product',
            price=Decimal('20.00'),
            stock_quantity=20,
            category='books'
        )
        
        products = list(Product.objects.all())
        assert products[0] == product2
        assert products[1] == product1
