# Getting Started with Django gRPC E-Commerce

Welcome! This guide will help you get started with your new Django gRPC project.

## 🎯 What You Have

A complete, intermediate-level Django project featuring:
- ✅ gRPC microservices architecture
- ✅ REST API gateway
- ✅ Product and Order management
- ✅ Automatic stock management
- ✅ Full Django admin interface
- ✅ Comprehensive documentation

## 📋 Prerequisites Checklist

- [x] Python 3.8+ installed
- [x] Virtual environment created (`venv/`)
- [x] All dependencies installed
- [x] Database migrations applied
- [x] Proto files compiled

## 🚀 Start the Project (3 Commands)

### 1. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 2. Start gRPC Servers
```bash
./start_grpc_servers.sh
```
This starts:
- Product gRPC Server on port 50051
- Order gRPC Server on port 50052

### 3. Start Django Server
Open a new terminal and run:
```bash
source venv/bin/activate
python manage.py runserver
```

**That's it!** Your project is now running. 🎉

## 🧪 Verify Everything Works

### Quick Test
```bash
# In a new terminal
curl http://localhost:8000/api/products/
```

You should see an empty products list (or populated if you ran sample data).

### Run Automated Tests
```bash
python test_api.py
```

This will test all API endpoints and verify everything is working.

## 📊 Add Sample Data (Optional)

```bash
python create_sample_data.py
```

This creates:
- 10 sample products (laptops, books, shoes, etc.)
- 4 sample orders with multiple items

## 🎨 Explore the Admin Interface

### 1. Create a Superuser
```bash
python manage.py createsuperuser
```

### 2. Access Admin Panel
Open browser: http://localhost:8000/admin/

Login with your superuser credentials.

## 📚 Available Documentation

| File | Description |
|------|-------------|
| `README.md` | Complete project documentation |
| `QUICKSTART.md` | 5-minute quick start guide |
| `API_TESTING_GUIDE.md` | Comprehensive API testing examples |
| `PROJECT_SUMMARY.md` | Project overview and status |
| `GETTING_STARTED.md` | This file |

## 🔗 Important URLs

- **Django Admin**: http://localhost:8000/admin/
- **Products API**: http://localhost:8000/api/products/
- **Orders API**: http://localhost:8000/api/orders/
- **Product Search**: http://localhost:8000/api/products/search/

## 🛠️ Common Commands

### Start/Stop Servers
```bash
# Start gRPC servers
./start_grpc_servers.sh

# Stop gRPC servers
./stop_grpc_servers.sh

# Start Django server
python manage.py runserver

# Stop Django server (Ctrl+C in terminal)
```

### Database Operations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell
```

### Development
```bash
# Recompile proto files
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/products.proto
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/orders.proto
```

## 📖 Quick API Examples

### Create a Product
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Product",
    "description": "A great product",
    "price": 99.99,
    "stock_quantity": 50,
    "category": "electronics"
  }'
```

### List Products
```bash
curl http://localhost:8000/api/products/
```

### Create an Order
```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "shipping_address": "123 Main St",
    "items": [{"product_id": 1, "quantity": 2}]
  }'
```

### Search Products
```bash
curl "http://localhost:8000/api/products/search/?query=laptop&category=electronics"
```

## 🎓 Learning Path

### Beginner Level
1. ✅ Understand the project structure
2. ✅ Run the project and test APIs
3. ✅ Explore the Django admin
4. ✅ Create products and orders via API

### Intermediate Level
5. ✅ Study the gRPC service implementations
6. ✅ Understand Protocol Buffers
7. ✅ Explore the client-server communication
8. ✅ Modify existing endpoints

### Advanced Level
9. Add authentication (JWT)
10. Implement caching (Redis)
11. Add streaming RPCs
12. Write comprehensive tests
13. Deploy with Docker

## 🐛 Troubleshooting

### "Address already in use"
```bash
# Kill processes on gRPC ports
lsof -ti:50051 | xargs kill -9
lsof -ti:50052 | xargs kill -9
```

### "Connection refused"
Make sure all three servers are running:
1. Product gRPC Server (port 50051)
2. Order gRPC Server (port 50052)
3. Django Server (port 8000)

### Import errors
Ensure you're in the project root directory and virtual environment is activated.

### Database errors
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
```

## 📝 Project Structure Overview

```
Your Django Project
├── REST API Layer (Django Views)
│   └── Handles HTTP requests
│       └── Calls gRPC services
│
├── gRPC Services Layer
│   ├── Product Service (Port 50051)
│   │   └── Manages products
│   └── Order Service (Port 50052)
│       └── Manages orders
│
└── Database Layer (SQLite)
    └── Stores all data
```

## 🎯 Next Steps

1. **Explore the Code**
   - Check out `products/grpc_server.py`
   - Review `orders/views.py`
   - Study the proto files in `protos/`

2. **Test the APIs**
   - Use the examples in `API_TESTING_GUIDE.md`
   - Try creating products and orders
   - Test the search functionality

3. **Customize**
   - Add new fields to models
   - Create new API endpoints
   - Extend gRPC services

4. **Learn More**
   - Read about gRPC: https://grpc.io/
   - Study Protocol Buffers: https://protobuf.dev/
   - Explore Django: https://www.djangoproject.com/

## 💡 Tips

- **Use the Admin Panel**: Great for quick data management
- **Check Server Logs**: Helpful for debugging
- **Read the Proto Files**: Understand the service contracts
- **Test Incrementally**: Start with simple operations
- **Use Postman/Insomnia**: GUI tools for API testing

## 🤝 Need Help?

1. Check the `README.md` for detailed documentation
2. Review the `API_TESTING_GUIDE.md` for examples
3. Look at the `PROJECT_SUMMARY.md` for overview
4. Examine the code comments
5. Check Django and gRPC server logs

## ✅ Success Checklist

- [ ] Virtual environment activated
- [ ] gRPC servers running
- [ ] Django server running
- [ ] Can access http://localhost:8000/api/products/
- [ ] Can access admin panel
- [ ] Sample data created (optional)
- [ ] Test script runs successfully

Once all checked, you're ready to start developing! 🚀

---

**Happy Coding!** 💻

For detailed information, see:
- Full documentation: `README.md`
- Quick start: `QUICKSTART.md`
- API testing: `API_TESTING_GUIDE.md`
