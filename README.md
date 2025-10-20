# Django gRPC E-Commerce Project

An intermediate-level Django project demonstrating gRPC integration with a microservices architecture for an e-commerce system.

## Project Overview

This project implements a Django-based e-commerce system with gRPC services for Products and Orders management. It showcases:

- **gRPC Services**: Separate gRPC servers for Products and Orders
- **Django REST API**: HTTP REST endpoints that communicate with gRPC services
- **Microservices Architecture**: Decoupled services communicating via gRPC
- **Protocol Buffers**: Strongly-typed message definitions
- **Django Admin**: Full admin interface for data management

## Architecture

```
┌─────────────────┐
│   REST Client   │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│  Django Views   │
└────────┬────────┘
         │ gRPC
         ▼
┌─────────────────┐     ┌─────────────────┐
│ Product Service │     │  Order Service  │
│   (Port 50051)  │     │   (Port 50052)  │
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
┌──────────────────────────────────┐
│        SQLite Database           │
└──────────────────────────────────┘
```

## Features

### Product Service
- Create, read, update, delete products
- List products with pagination
- Search products by name, category, price range
- Stock management

### Order Service
- Create orders with multiple items
- List orders with pagination and status filtering
- Update order status
- Cancel orders (with stock restoration)
- Get orders by customer email
- Automatic stock deduction

## Project Structure

```
gRPC/
├── ecommerce_grpc/          # Django project settings
│   ├── settings.py
│   └── urls.py
├── products/                # Products Django app
│   ├── models.py           # Product model
│   ├── views.py            # REST API views
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin configuration
│   ├── grpc_server.py      # gRPC server implementation
│   └── grpc_client.py      # gRPC client wrapper
├── orders/                  # Orders Django app
│   ├── models.py           # Order and OrderItem models
│   ├── views.py            # REST API views
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin configuration
│   ├── grpc_server.py      # gRPC server implementation
│   └── grpc_client.py      # gRPC client wrapper
├── protos/                  # Protocol Buffer definitions
│   ├── products.proto
│   └── orders.proto
├── requirements.txt
└── manage.py
```

## Setup Instructions

### 1. Virtual Environment (Already Created)

The virtual environment is already set up in the `venv/` directory.

Activate it:
```bash
source venv/bin/activate
```

### 2. Database Setup

Run migrations to create the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Admin User

```bash
python manage.py createsuperuser
```

### 4. Start the Services

You need to run **three separate processes**:

**Terminal 1 - Product gRPC Server:**
```bash
python products/grpc_server.py
```

**Terminal 2 - Order gRPC Server:**
```bash
python orders/grpc_server.py
```

**Terminal 3 - Django Development Server:**
```bash
python manage.py runserver
```

## API Endpoints

### Products API

- **GET** `/api/products/` - List products (pagination: ?page=1&page_size=10)
- **POST** `/api/products/` - Create product
- **GET** `/api/products/<id>/` - Get product details
- **PUT** `/api/products/<id>/` - Update product
- **DELETE** `/api/products/<id>/` - Delete product
- **GET** `/api/products/search/` - Search products (?query=laptop&category=electronics&min_price=100&max_price=1000)

### Orders API

- **GET** `/api/orders/` - List orders (pagination: ?page=1&page_size=10&status=pending)
- **POST** `/api/orders/` - Create order
- **GET** `/api/orders/<id>/` - Get order details
- **PATCH** `/api/orders/<id>/status/` - Update order status
- **POST** `/api/orders/<id>/cancel/` - Cancel order
- **GET** `/api/orders/customer/<email>/` - Get customer orders

## Example API Requests

### Create a Product

```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 999.99,
    "stock_quantity": 50,
    "category": "electronics"
  }'
```

### Create an Order

```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "shipping_address": "123 Main St, City, Country",
    "items": [
      {
        "product_id": 1,
        "quantity": 2
      }
    ]
  }'
```

### Search Products

```bash
curl "http://localhost:8000/api/products/search/?query=laptop&category=electronics&min_price=500&max_price=2000"
```

### Update Order Status

```bash
curl -X PATCH http://localhost:8000/api/orders/1/status/ \
  -H "Content-Type: application/json" \
  -d '{"status": "shipped"}'
```

## gRPC Service Ports

- **Product Service**: `localhost:50051`
- **Order Service**: `localhost:50052`

## Product Categories

Available categories:
- `electronics`
- `clothing`
- `books`
- `home`
- `sports`
- `toys`
- `other`

## Order Statuses

Available statuses:
- `pending` - Order placed
- `processing` - Order being prepared
- `shipped` - Order shipped
- `delivered` - Order delivered
- `cancelled` - Order cancelled

## Admin Interface

Access the Django admin at: `http://localhost:8000/admin/`

Features:
- Manage products and orders
- View order items inline
- Filter by status, category, dates
- Search functionality

## Development Notes

### Recompiling Proto Files

If you modify the `.proto` files, recompile them:

```bash
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/products.proto
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/orders.proto
```

### Testing gRPC Services Directly

You can test gRPC services using tools like:
- **grpcurl**: Command-line tool for gRPC
- **BloomRPC**: GUI client for gRPC
- **Postman**: Supports gRPC (newer versions)

## Key Learning Points

1. **gRPC Integration**: How to integrate gRPC with Django
2. **Protocol Buffers**: Defining service contracts with .proto files
3. **Microservices**: Separating concerns into independent services
4. **Client-Server Pattern**: gRPC clients communicating with gRPC servers
5. **Transaction Management**: Atomic operations with database transactions
6. **Error Handling**: Proper error handling in gRPC services
7. **REST to gRPC Bridge**: Django views acting as a bridge between REST and gRPC

## Technologies Used

- **Django 4.2.7**: Web framework
- **Django REST Framework 3.14.0**: REST API toolkit
- **gRPC 1.59.3**: RPC framework
- **Protocol Buffers 4.25.1**: Serialization format
- **SQLite**: Database (default Django database)

## Future Enhancements

- Add authentication and authorization
- Implement caching (Redis)
- Add message queues (RabbitMQ/Celery)
- Implement streaming RPCs
- Add comprehensive test suite
- Docker containerization
- API documentation with Swagger/OpenAPI
- Monitoring and logging
- Load balancing for gRPC services

## Troubleshooting

### gRPC Connection Errors

If you get connection errors:
1. Ensure both gRPC servers are running
2. Check ports 50051 and 50052 are not in use
3. Verify firewall settings

### Import Errors

If you get import errors for generated proto files:
1. Ensure you're in the project root directory
2. Recompile proto files
3. Check Python path includes the project root

### Database Errors

If you get database errors:
1. Run migrations: `python manage.py migrate`
2. Check database file permissions
3. Delete `db.sqlite3` and re-run migrations if needed

## License

This is an educational project for learning purposes.
