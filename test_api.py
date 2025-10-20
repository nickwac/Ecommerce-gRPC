#!/usr/bin/env python
"""
Simple test script to verify the Django gRPC E-Commerce API is working.
Make sure all servers are running before executing this script.
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000/api"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_response(response, description):
    """Print formatted response"""
    print(f"\n{description}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    return response

def test_products_api():
    """Test Products API endpoints"""
    print_section("Testing Products API")
    
    # 1. Create a product
    print("\n1. Creating a product...")
    product_data = {
        "name": "Test Laptop",
        "description": "High-performance test laptop",
        "price": 1299.99,
        "stock_quantity": 10,
        "category": "electronics"
    }
    response = requests.post(f"{BASE_URL}/products/", json=product_data)
    print_response(response, "Create Product Response:")
    
    if response.status_code != 201:
        print("❌ Failed to create product")
        return False
    
    product_id = response.json().get('product', {}).get('id')
    print(f"✅ Product created with ID: {product_id}")
    
    # 2. List products
    print("\n2. Listing products...")
    response = requests.get(f"{BASE_URL}/products/")
    print_response(response, "List Products Response:")
    
    if response.status_code != 200:
        print("❌ Failed to list products")
        return False
    print("✅ Products listed successfully")
    
    # 3. Get single product
    print(f"\n3. Getting product {product_id}...")
    response = requests.get(f"{BASE_URL}/products/{product_id}/")
    print_response(response, "Get Product Response:")
    
    if response.status_code != 200:
        print("❌ Failed to get product")
        return False
    print("✅ Product retrieved successfully")
    
    # 4. Search products
    print("\n4. Searching products...")
    response = requests.get(f"{BASE_URL}/products/search/?query=laptop")
    print_response(response, "Search Products Response:")
    
    if response.status_code != 200:
        print("❌ Failed to search products")
        return False
    print("✅ Products searched successfully")
    
    # 5. Update product
    print(f"\n5. Updating product {product_id}...")
    update_data = {
        "name": "Test Laptop Updated",
        "description": "Updated description",
        "price": 1199.99,
        "stock_quantity": 8,
        "category": "electronics"
    }
    response = requests.put(f"{BASE_URL}/products/{product_id}/", json=update_data)
    print_response(response, "Update Product Response:")
    
    if response.status_code != 200:
        print("❌ Failed to update product")
        return False
    print("✅ Product updated successfully")
    
    return product_id

def test_orders_api(product_id):
    """Test Orders API endpoints"""
    print_section("Testing Orders API")
    
    # 1. Create an order
    print("\n1. Creating an order...")
    order_data = {
        "customer_name": "Test Customer",
        "customer_email": "test@example.com",
        "shipping_address": "123 Test Street, Test City, TC 12345",
        "items": [
            {
                "product_id": product_id,
                "quantity": 2
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/orders/", json=order_data)
    print_response(response, "Create Order Response:")
    
    if response.status_code != 201:
        print("❌ Failed to create order")
        return False
    
    order_id = response.json().get('order', {}).get('id')
    print(f"✅ Order created with ID: {order_id}")
    
    # 2. List orders
    print("\n2. Listing orders...")
    response = requests.get(f"{BASE_URL}/orders/")
    print_response(response, "List Orders Response:")
    
    if response.status_code != 200:
        print("❌ Failed to list orders")
        return False
    print("✅ Orders listed successfully")
    
    # 3. Get single order
    print(f"\n3. Getting order {order_id}...")
    response = requests.get(f"{BASE_URL}/orders/{order_id}/")
    print_response(response, "Get Order Response:")
    
    if response.status_code != 200:
        print("❌ Failed to get order")
        return False
    print("✅ Order retrieved successfully")
    
    # 4. Update order status
    print(f"\n4. Updating order {order_id} status...")
    status_data = {"status": "processing"}
    response = requests.patch(f"{BASE_URL}/orders/{order_id}/status/", json=status_data)
    print_response(response, "Update Order Status Response:")
    
    if response.status_code != 200:
        print("❌ Failed to update order status")
        return False
    print("✅ Order status updated successfully")
    
    # 5. Get customer orders
    print("\n5. Getting customer orders...")
    response = requests.get(f"{BASE_URL}/orders/customer/test@example.com/")
    print_response(response, "Get Customer Orders Response:")
    
    if response.status_code != 200:
        print("❌ Failed to get customer orders")
        return False
    print("✅ Customer orders retrieved successfully")
    
    # 6. Cancel order
    print(f"\n6. Cancelling order {order_id}...")
    response = requests.post(f"{BASE_URL}/orders/{order_id}/cancel/")
    print_response(response, "Cancel Order Response:")
    
    if response.status_code != 200:
        print("❌ Failed to cancel order")
        return False
    print("✅ Order cancelled successfully")
    
    return True

def cleanup(product_id):
    """Clean up test data"""
    print_section("Cleaning Up Test Data")
    
    print(f"\nDeleting test product {product_id}...")
    response = requests.delete(f"{BASE_URL}/products/{product_id}/")
    
    if response.status_code == 200:
        print("✅ Test product deleted successfully")
    else:
        print("⚠️  Could not delete test product (may have been deleted already)")

def main():
    """Main test function"""
    print("=" * 60)
    print("  Django gRPC E-Commerce API Test Suite")
    print("=" * 60)
    print("\nMake sure all servers are running:")
    print("  1. Product gRPC Server (port 50051)")
    print("  2. Order gRPC Server (port 50052)")
    print("  3. Django Development Server (port 8000)")
    print("\nStarting tests in 3 seconds...")
    
    import time
    time.sleep(3)
    
    try:
        # Test Products API
        product_id = test_products_api()
        if not product_id:
            print("\n❌ Products API tests failed")
            sys.exit(1)
        
        # Test Orders API
        success = test_orders_api(product_id)
        if not success:
            print("\n❌ Orders API tests failed")
            cleanup(product_id)
            sys.exit(1)
        
        # Cleanup
        cleanup(product_id)
        
        # Final summary
        print_section("Test Summary")
        print("\n✅ All tests passed successfully!")
        print("\nThe Django gRPC E-Commerce API is working correctly.")
        print("\nYou can now:")
        print("  - Access the admin panel: http://localhost:8000/admin/")
        print("  - Test the API endpoints manually")
        print("  - Create sample data: python create_sample_data.py")
        print("  - Review the API_TESTING_GUIDE.md for more examples")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error!")
        print("\nCould not connect to the API server.")
        print("Please ensure all servers are running:")
        print("  1. ./start_grpc_servers.sh")
        print("  2. python manage.py runserver")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
