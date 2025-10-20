#!/usr/bin/env python
"""
Script to create sample data for testing the e-commerce gRPC project.
Run this after starting the gRPC servers.
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_grpc.settings')
django.setup()

from products.models import Product
from orders.models import Order, OrderItem
from decimal import Decimal


def create_products():
    """Create sample products"""
    print("Creating sample products...")
    
    products_data = [
        {
            'name': 'MacBook Pro 16"',
            'description': 'High-performance laptop with M2 chip, 16GB RAM, 512GB SSD',
            'price': Decimal('2499.99'),
            'stock_quantity': 25,
            'category': 'electronics'
        },
        {
            'name': 'iPhone 15 Pro',
            'description': 'Latest iPhone with A17 Pro chip, 256GB storage',
            'price': Decimal('1199.99'),
            'stock_quantity': 50,
            'category': 'electronics'
        },
        {
            'name': 'Sony WH-1000XM5',
            'description': 'Premium noise-cancelling wireless headphones',
            'price': Decimal('399.99'),
            'stock_quantity': 100,
            'category': 'electronics'
        },
        {
            'name': 'Nike Air Max 270',
            'description': 'Comfortable running shoes with Air cushioning',
            'price': Decimal('149.99'),
            'stock_quantity': 75,
            'category': 'sports'
        },
        {
            'name': 'Levi\'s 501 Jeans',
            'description': 'Classic straight-fit jeans, blue denim',
            'price': Decimal('89.99'),
            'stock_quantity': 150,
            'category': 'clothing'
        },
        {
            'name': 'The Pragmatic Programmer',
            'description': 'Essential book for software developers',
            'price': Decimal('39.99'),
            'stock_quantity': 200,
            'category': 'books'
        },
        {
            'name': 'Clean Code',
            'description': 'A Handbook of Agile Software Craftsmanship',
            'price': Decimal('44.99'),
            'stock_quantity': 180,
            'category': 'books'
        },
        {
            'name': 'Dyson V15 Vacuum',
            'description': 'Cordless vacuum cleaner with laser detection',
            'price': Decimal('649.99'),
            'stock_quantity': 30,
            'category': 'home'
        },
        {
            'name': 'LEGO Star Wars Set',
            'description': 'Millennium Falcon building set, 1351 pieces',
            'price': Decimal('159.99'),
            'stock_quantity': 60,
            'category': 'toys'
        },
        {
            'name': 'Wilson Tennis Racket',
            'description': 'Professional-grade tennis racket',
            'price': Decimal('199.99'),
            'stock_quantity': 40,
            'category': 'sports'
        }
    ]
    
    created_products = []
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
        if created:
            print(f"  ✓ Created: {product.name}")
        else:
            print(f"  - Already exists: {product.name}")
        created_products.append(product)
    
    return created_products


def create_orders(products):
    """Create sample orders"""
    print("\nCreating sample orders...")
    
    orders_data = [
        {
            'customer_name': 'Alice Johnson',
            'customer_email': 'alice@example.com',
            'shipping_address': '123 Tech Street, San Francisco, CA 94102',
            'items': [
                {'product': products[0], 'quantity': 1},  # MacBook
                {'product': products[2], 'quantity': 1},  # Headphones
            ]
        },
        {
            'customer_name': 'Bob Smith',
            'customer_email': 'bob@example.com',
            'shipping_address': '456 Main Avenue, New York, NY 10001',
            'items': [
                {'product': products[1], 'quantity': 2},  # iPhone
                {'product': products[5], 'quantity': 3},  # Books
            ]
        },
        {
            'customer_name': 'Carol Williams',
            'customer_email': 'carol@example.com',
            'shipping_address': '789 Oak Road, Austin, TX 78701',
            'items': [
                {'product': products[3], 'quantity': 1},  # Shoes
                {'product': products[4], 'quantity': 2},  # Jeans
            ]
        },
        {
            'customer_name': 'David Brown',
            'customer_email': 'david@example.com',
            'shipping_address': '321 Pine Lane, Seattle, WA 98101',
            'items': [
                {'product': products[7], 'quantity': 1},  # Vacuum
                {'product': products[8], 'quantity': 2},  # LEGO
            ]
        }
    ]
    
    for order_data in orders_data:
        # Check if order already exists for this customer
        existing_order = Order.objects.filter(
            customer_email=order_data['customer_email']
        ).first()
        
        if existing_order:
            print(f"  - Order already exists for: {order_data['customer_name']}")
            continue
        
        # Create order
        order = Order.objects.create(
            customer_name=order_data['customer_name'],
            customer_email=order_data['customer_email'],
            shipping_address=order_data['shipping_address'],
            status='pending'
        )
        
        # Create order items
        for item_data in order_data['items']:
            product = item_data['product']
            quantity = item_data['quantity']
            
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                quantity=quantity,
                price=product.price
            )
        
        # Calculate total
        order.calculate_total()
        
        print(f"  ✓ Created order for: {order.customer_name} (${order.total_amount})")


def main():
    print("=" * 60)
    print("Creating Sample Data for E-Commerce gRPC Project")
    print("=" * 60)
    
    # Create products
    products = create_products()
    
    # Create orders
    create_orders(products)
    
    print("\n" + "=" * 60)
    print("Sample data creation completed!")
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  Products: {Product.objects.count()}")
    print(f"  Orders: {Order.objects.count()}")
    print(f"  Order Items: {OrderItem.objects.count()}")
    print("\nYou can now:")
    print("  1. Access Django admin: http://localhost:8000/admin/")
    print("  2. Test REST API endpoints")
    print("  3. Test gRPC services directly")


if __name__ == '__main__':
    main()
