# Quick Start Guide

Get the Django gRPC E-Commerce project up and running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Virtual environment already created (in `venv/` directory)

## Step-by-Step Setup

### 1. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 2. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 4. Start the gRPC Servers

**Option A: Using the helper script (Recommended)**

```bash
./start_grpc_servers.sh
```

**Option B: Manually in separate terminals**

Terminal 1:
```bash
python products/grpc_server.py
```

Terminal 2:
```bash
python orders/grpc_server.py
```

### 5. Start Django Development Server

In a new terminal (with venv activated):

```bash
python manage.py runserver
```

### 6. Create Sample Data (Optional)

```bash
python create_sample_data.py
```

This will create:
- 10 sample products across different categories
- 4 sample orders with multiple items

## Test the API

### Using curl

**List Products:**
```bash
curl http://localhost:8000/api/products/
```

**Create a Product:**
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Product",
    "description": "A test product",
    "price": 99.99,
    "stock_quantity": 10,
    "category": "electronics"
  }'
```

**List Orders:**
```bash
curl http://localhost:8000/api/orders/
```

### Using Browser

- **Django Admin**: http://localhost:8000/admin/
- **Products API**: http://localhost:8000/api/products/
- **Orders API**: http://localhost:8000/api/orders/

## Stop the Servers

**Stop gRPC Servers:**
```bash
./stop_grpc_servers.sh
```

**Stop Django Server:**
Press `Ctrl+C` in the terminal running the Django server.

## Common Issues

### Port Already in Use

If you get "Address already in use" error:

```bash
# Find and kill processes on ports 50051 and 50052
lsof -ti:50051 | xargs kill -9
lsof -ti:50052 | xargs kill -9
```

### Import Errors

Make sure you're in the project root directory and the virtual environment is activated.

### gRPC Connection Errors

Ensure both gRPC servers are running before starting the Django server.

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Explore the API endpoints
3. Check out the Django admin interface
4. Modify the proto files and recompile
5. Add your own features!

## Quick Reference

### API Endpoints

- `GET /api/products/` - List products
- `POST /api/products/` - Create product
- `GET /api/products/<id>/` - Get product
- `PUT /api/products/<id>/` - Update product
- `DELETE /api/products/<id>/` - Delete product
- `GET /api/products/search/` - Search products

- `GET /api/orders/` - List orders
- `POST /api/orders/` - Create order
- `GET /api/orders/<id>/` - Get order
- `PATCH /api/orders/<id>/status/` - Update status
- `POST /api/orders/<id>/cancel/` - Cancel order
- `GET /api/orders/customer/<email>/` - Customer orders

### gRPC Ports

- Product Service: `localhost:50051`
- Order Service: `localhost:50052`

Happy coding! 🚀
