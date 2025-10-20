# API Testing Guide

Complete guide for testing the Django gRPC E-Commerce API endpoints.

## Prerequisites

Ensure all services are running:
1. Product gRPC Server (port 50051)
2. Order gRPC Server (port 50052)
3. Django Development Server (port 8000)

## Products API Testing

### 1. Create Products

```bash
# Create a laptop
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dell XPS 15",
    "description": "Premium laptop with 11th Gen Intel Core i7",
    "price": 1799.99,
    "stock_quantity": 30,
    "category": "electronics"
  }'

# Create a book
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Design Patterns",
    "description": "Elements of Reusable Object-Oriented Software",
    "price": 54.99,
    "stock_quantity": 100,
    "category": "books"
  }'

# Create sports equipment
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Yoga Mat",
    "description": "Premium non-slip yoga mat",
    "price": 29.99,
    "stock_quantity": 200,
    "category": "sports"
  }'
```

### 2. List All Products

```bash
# Get all products (default pagination)
curl http://localhost:8000/api/products/

# With custom pagination
curl "http://localhost:8000/api/products/?page=1&page_size=5"
```

### 3. Get Single Product

```bash
# Get product with ID 1
curl http://localhost:8000/api/products/1/
```

### 4. Update Product

```bash
# Update product price and stock
curl -X PUT http://localhost:8000/api/products/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dell XPS 15",
    "description": "Premium laptop with 11th Gen Intel Core i7 - Updated",
    "price": 1699.99,
    "stock_quantity": 25,
    "category": "electronics"
  }'

# Partial update (only price)
curl -X PUT http://localhost:8000/api/products/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "price": 1599.99
  }'
```

### 5. Search Products

```bash
# Search by name
curl "http://localhost:8000/api/products/search/?query=laptop"

# Search by category
curl "http://localhost:8000/api/products/search/?category=electronics"

# Search with price range
curl "http://localhost:8000/api/products/search/?min_price=50&max_price=100"

# Combined search
curl "http://localhost:8000/api/products/search/?query=laptop&category=electronics&min_price=1000&max_price=2000"
```

### 6. Delete Product

```bash
# Delete product with ID 1
curl -X DELETE http://localhost:8000/api/products/1/
```

## Orders API Testing

### 1. Create Orders

```bash
# Create order with single item
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "customer_email": "john.doe@example.com",
    "shipping_address": "123 Main Street, New York, NY 10001",
    "items": [
      {
        "product_id": 1,
        "quantity": 1
      }
    ]
  }'

# Create order with multiple items
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Jane Smith",
    "customer_email": "jane.smith@example.com",
    "shipping_address": "456 Oak Avenue, Los Angeles, CA 90001",
    "items": [
      {
        "product_id": 1,
        "quantity": 2
      },
      {
        "product_id": 2,
        "quantity": 1
      },
      {
        "product_id": 3,
        "quantity": 3
      }
    ]
  }'
```

### 2. List Orders

```bash
# Get all orders
curl http://localhost:8000/api/orders/

# With pagination
curl "http://localhost:8000/api/orders/?page=1&page_size=5"

# Filter by status
curl "http://localhost:8000/api/orders/?status=pending"
curl "http://localhost:8000/api/orders/?status=shipped"
```

### 3. Get Single Order

```bash
# Get order with ID 1
curl http://localhost:8000/api/orders/1/
```

### 4. Update Order Status

```bash
# Update to processing
curl -X PATCH http://localhost:8000/api/orders/1/status/ \
  -H "Content-Type: application/json" \
  -d '{"status": "processing"}'

# Update to shipped
curl -X PATCH http://localhost:8000/api/orders/1/status/ \
  -H "Content-Type: application/json" \
  -d '{"status": "shipped"}'

# Update to delivered
curl -X PATCH http://localhost:8000/api/orders/1/status/ \
  -H "Content-Type: application/json" \
  -d '{"status": "delivered"}'
```

### 5. Cancel Order

```bash
# Cancel order (restores product stock)
curl -X POST http://localhost:8000/api/orders/1/cancel/ \
  -H "Content-Type: application/json"
```

### 6. Get Customer Orders

```bash
# Get all orders for a specific customer
curl http://localhost:8000/api/orders/customer/john.doe@example.com/
```

## Testing Workflow Examples

### Complete Product Lifecycle

```bash
# 1. Create a product
PRODUCT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Product",
    "description": "A test product",
    "price": 99.99,
    "stock_quantity": 50,
    "category": "electronics"
  }')

echo $PRODUCT_RESPONSE

# 2. Extract product ID (using jq if available)
# PRODUCT_ID=$(echo $PRODUCT_RESPONSE | jq -r '.product.id')

# 3. Get the product
curl http://localhost:8000/api/products/1/

# 4. Update the product
curl -X PUT http://localhost:8000/api/products/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Test Product",
    "description": "Updated description",
    "price": 89.99,
    "stock_quantity": 45,
    "category": "electronics"
  }'

# 5. Search for the product
curl "http://localhost:8000/api/products/search/?query=Updated"

# 6. Delete the product
curl -X DELETE http://localhost:8000/api/products/1/
```

### Complete Order Lifecycle

```bash
# 1. Create products first
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product A",
    "description": "First product",
    "price": 100.00,
    "stock_quantity": 50,
    "category": "electronics"
  }'

curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product B",
    "description": "Second product",
    "price": 200.00,
    "stock_quantity": 30,
    "category": "electronics"
  }'

# 2. Create an order
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Test Customer",
    "customer_email": "test@example.com",
    "shipping_address": "123 Test St, Test City, TC 12345",
    "items": [
      {"product_id": 1, "quantity": 2},
      {"product_id": 2, "quantity": 1}
    ]
  }'

# 3. Get the order
curl http://localhost:8000/api/orders/1/

# 4. Update order status through lifecycle
curl -X PATCH http://localhost:8000/api/orders/1/status/ \
  -H "Content-Type: application/json" \
  -d '{"status": "processing"}'

curl -X PATCH http://localhost:8000/api/orders/1/status/ \
  -H "Content-Type: application/json" \
  -d '{"status": "shipped"}'

curl -X PATCH http://localhost:8000/api/orders/1/status/ \
  -H "Content-Type: application/json" \
  -d '{"status": "delivered"}'

# 5. Get customer's orders
curl http://localhost:8000/api/orders/customer/test@example.com/
```

### Testing Stock Management

```bash
# 1. Create a product with limited stock
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Limited Stock Item",
    "description": "Only 5 in stock",
    "price": 50.00,
    "stock_quantity": 5,
    "category": "electronics"
  }'

# 2. Check initial stock
curl http://localhost:8000/api/products/1/

# 3. Create order (reduces stock)
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Stock Test",
    "customer_email": "stock@example.com",
    "shipping_address": "123 Stock St",
    "items": [{"product_id": 1, "quantity": 3}]
  }'

# 4. Check stock after order (should be 2)
curl http://localhost:8000/api/products/1/

# 5. Cancel order (restores stock)
curl -X POST http://localhost:8000/api/orders/1/cancel/

# 6. Check stock after cancellation (should be 5 again)
curl http://localhost:8000/api/products/1/
```

## Error Testing

### Test Invalid Requests

```bash
# Missing required fields
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Incomplete Product"
  }'

# Invalid product ID
curl http://localhost:8000/api/products/99999/

# Invalid order status
curl -X PATCH http://localhost:8000/api/orders/1/status/ \
  -H "Content-Type: application/json" \
  -d '{"status": "invalid_status"}'

# Insufficient stock
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Test",
    "customer_email": "test@example.com",
    "shipping_address": "123 Test St",
    "items": [{"product_id": 1, "quantity": 10000}]
  }'
```

## Using Python Requests

If you prefer Python for testing:

```python
import requests
import json

BASE_URL = "http://localhost:8000/api"

# Create product
product_data = {
    "name": "Python Test Product",
    "description": "Created via Python",
    "price": 99.99,
    "stock_quantity": 25,
    "category": "electronics"
}
response = requests.post(f"{BASE_URL}/products/", json=product_data)
print(response.json())

# List products
response = requests.get(f"{BASE_URL}/products/")
print(response.json())

# Create order
order_data = {
    "customer_name": "Python Tester",
    "customer_email": "python@example.com",
    "shipping_address": "123 Python St",
    "items": [{"product_id": 1, "quantity": 2}]
}
response = requests.post(f"{BASE_URL}/orders/", json=order_data)
print(response.json())
```

## Expected Response Formats

### Product Response
```json
{
  "id": 1,
  "name": "Product Name",
  "description": "Product description",
  "price": 99.99,
  "stock_quantity": 50,
  "category": "electronics",
  "created_at": "2025-10-20T14:00:00Z",
  "updated_at": "2025-10-20T14:00:00Z"
}
```

### Order Response
```json
{
  "id": 1,
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "items": [
    {
      "product_id": 1,
      "product_name": "Product Name",
      "quantity": 2,
      "price": 99.99,
      "subtotal": 199.98
    }
  ],
  "total_amount": 199.98,
  "status": "pending",
  "shipping_address": "123 Main St",
  "created_at": "2025-10-20T14:00:00Z",
  "updated_at": "2025-10-20T14:00:00Z"
}
```

## Tips

1. **Use jq for JSON formatting**: `curl ... | jq`
2. **Save responses to files**: `curl ... > response.json`
3. **Use Postman or Insomnia** for a GUI testing experience
4. **Check gRPC server logs** for debugging
5. **Monitor Django server logs** for request details

Happy testing! 🧪
