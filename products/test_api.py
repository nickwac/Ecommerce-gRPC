"""
API tests for Products endpoints.
"""

import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from products.models import Product


@pytest.mark.django_db
class TestProductAPI:
    """Test cases for Product API endpoints."""
    
    def test_list_products(self, api_client, products):
        """Test listing products."""
        url = reverse('product-list-create')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'products' in response.data
        assert len(response.data['products']) == 5
    
    def test_create_product_unauthenticated(self, api_client):
        """Test creating product without authentication."""
        url = reverse('product-list-create')
        data = {
            'name': 'New Product',
            'description': 'Description',
            'price': 99.99,
            'stock_quantity': 50,
            'category': 'electronics'
        }
        response = api_client.post(url, data, format='json')
        
        # Should fail without authentication
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
    
    def test_create_product_authenticated(self, authenticated_client):
        """Test creating product with authentication."""
        url = reverse('product-list-create')
        data = {
            'name': 'New Product',
            'description': 'A new product',
            'price': 149.99,
            'stock_quantity': 25,
            'category': 'electronics'
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['success'] is True
        assert response.data['product']['name'] == 'New Product'
    
    def test_get_product(self, api_client, product):
        """Test retrieving a single product."""
        url = reverse('product-detail', kwargs={'product_id': product.id})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == product.name
        assert Decimal(str(response.data['price'])) == product.price
    
    def test_get_nonexistent_product(self, api_client):
        """Test retrieving a non-existent product."""
        url = reverse('product-detail', kwargs={'product_id': 99999})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_product(self, authenticated_client, product):
        """Test updating a product."""
        url = reverse('product-detail', kwargs={'product_id': product.id})
        data = {
            'name': 'Updated Product',
            'description': 'Updated description',
            'price': 199.99,
            'stock_quantity': 75,
            'category': 'electronics'
        }
        response = authenticated_client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['product']['name'] == 'Updated Product'
        
        # Verify in database
        product.refresh_from_db()
        assert product.name == 'Updated Product'
    
    def test_delete_product(self, authenticated_client, product):
        """Test deleting a product."""
        url = reverse('product-detail', kwargs={'product_id': product.id})
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        
        # Verify product is deleted
        assert not Product.objects.filter(id=product.id).exists()
    
    def test_search_products(self, api_client, products):
        """Test searching products."""
        url = reverse('product-search')
        response = api_client.get(url, {'query': 'Product 1'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['products']) >= 1
    
    def test_search_by_category(self, api_client, products):
        """Test searching products by category."""
        url = reverse('product-search')
        response = api_client.get(url, {'category': 'electronics'})
        
        assert response.status_code == status.HTTP_200_OK
        assert all(p['category'] == 'electronics' for p in response.data['products'])
    
    def test_search_by_price_range(self, api_client, products):
        """Test searching products by price range."""
        url = reverse('product-search')
        response = api_client.get(url, {'min_price': 20, 'max_price': 40})
        
        assert response.status_code == status.HTTP_200_OK
        for product in response.data['products']:
            assert 20 <= float(product['price']) <= 40
