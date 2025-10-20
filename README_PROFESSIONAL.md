# Django gRPC E-Commerce - Professional Edition

[![CI/CD](https://github.com/yourusername/ecommerce-grpc/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/yourusername/ecommerce-grpc/actions)
[![codecov](https://codecov.io/gh/yourusername/ecommerce-grpc/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/ecommerce-grpc)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Django 4.2](https://img.shields.io/badge/django-4.2-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready, enterprise-grade Django application with gRPC microservices architecture for e-commerce operations.

## 🌟 Professional Features

### Architecture & Design
- ✅ **Microservices Architecture** - Decoupled gRPC services
- ✅ **Clean Architecture** - Separation of concerns with layered design
- ✅ **API Versioning** - `/api/v1/` endpoints for backward compatibility
- ✅ **Event-Driven** - Celery for asynchronous task processing
- ✅ **Caching Strategy** - Redis for performance optimization

### Security
- ✅ **JWT Authentication** - Secure token-based auth with refresh tokens
- ✅ **Permission System** - Role-based access control
- ✅ **Rate Limiting** - API throttling to prevent abuse
- ✅ **Security Headers** - XSS, CSRF, clickjacking protection
- ✅ **Input Validation** - Comprehensive request validation

### Performance
- ✅ **Redis Caching** - Multi-level caching strategy
- ✅ **Database Optimization** - Indexed queries and connection pooling
- ✅ **Async Tasks** - Celery for background processing
- ✅ **Load Balancing** - Nginx reverse proxy configuration
- ✅ **gRPC Streaming** - Efficient data transfer

### Monitoring & Observability
- ✅ **Prometheus Metrics** - Application and system metrics
- ✅ **Structured Logging** - JSON logging for easy parsing
- ✅ **Error Tracking** - Sentry integration
- ✅ **Health Checks** - Kubernetes-ready health endpoints
- ✅ **Request Tracing** - Custom middleware for request tracking

### Development & Testing
- ✅ **Comprehensive Tests** - Unit, integration, and API tests
- ✅ **Code Coverage** - 80%+ test coverage
- ✅ **CI/CD Pipeline** - GitHub Actions workflows
- ✅ **Code Quality** - Black, isort, flake8, pylint
- ✅ **API Documentation** - OpenAPI/Swagger with drf-spectacular

### Deployment
- ✅ **Docker Containers** - Multi-stage builds for optimization
- ✅ **Docker Compose** - Complete stack orchestration
- ✅ **Kubernetes Ready** - Health checks and graceful shutdown
- ✅ **Environment Management** - Separate dev/staging/prod configs
- ✅ **Database Migrations** - Zero-downtime deployment support

## 📋 Table of Contents

- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Development Setup](#development-setup)
- [Docker Deployment](#docker-deployment)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Configuration](#configuration)
- [Monitoring](#monitoring)
- [Contributing](#contributing)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Nginx (Load Balancer)                │
│                    Rate Limiting & SSL/TLS                   │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
┌────────▼────────┐            ┌────────▼────────┐
│  Django Web App │            │  Static Files   │
│  (Gunicorn)     │            │  (Nginx)        │
└────────┬────────┘            └─────────────────┘
         │
         │ gRPC Calls
         │
    ┌────┴────┐
    │         │
┌───▼──┐  ┌──▼───┐
│Product│  │Order │
│ gRPC  │  │ gRPC │
│Server │  │Server│
└───┬───┘  └──┬───┘
    │         │
    └────┬────┘
         │
    ┌────▼────┐     ┌──────────┐     ┌─────────┐
    │PostgreSQL│     │  Redis   │     │ Celery  │
    │ Database │     │  Cache   │     │ Workers │
    └──────────┘     └──────────┘     └─────────┘
```

### Component Breakdown

- **Nginx**: Reverse proxy, load balancing, SSL termination, static file serving
- **Django Web App**: REST API gateway, business logic, authentication
- **gRPC Services**: Microservices for Products and Orders
- **PostgreSQL**: Primary data store with connection pooling
- **Redis**: Caching layer and Celery message broker
- **Celery**: Asynchronous task queue for background jobs
- **Prometheus**: Metrics collection and monitoring

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 13+
- Redis 6+
- Docker & Docker Compose (for containerized deployment)

### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/ecommerce-grpc.git
cd ecommerce-grpc

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
make install
# or: pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# 5. Run migrations
make migrate

# 6. Create superuser
make superuser

# 7. Start services
# Terminal 1: Start gRPC servers
./start_grpc_servers.sh

# Terminal 2: Start Django server
python manage.py runserver

# Terminal 3: Start Celery worker (optional)
make celery-worker

# Terminal 4: Start Celery beat (optional)
make celery-beat
```

### Docker Deployment

```bash
# Build and start all services
make docker-up

# View logs
make docker-logs

# Stop all services
make docker-down
```

## 📚 API Documentation

### Interactive Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### Authentication

All write operations require JWT authentication:

```bash
# 1. Register a new user
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User"
  }'

# 2. Login to get tokens
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "SecurePass123!"
  }'

# 3. Use access token in requests
curl -X POST http://localhost:8000/api/v1/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product Name",
    "description": "Description",
    "price": 99.99,
    "stock_quantity": 100,
    "category": "electronics"
  }'
```

### API Endpoints

#### Authentication
- `POST /api/v1/auth/register/` - Register new user
- `POST /api/v1/auth/login/` - Login and get tokens
- `POST /api/v1/auth/refresh/` - Refresh access token
- `GET /api/v1/user/profile/` - Get user profile
- `PATCH /api/v1/user/profile/` - Update user profile
- `POST /api/v1/user/change-password/` - Change password

#### Products
- `GET /api/v1/products/` - List products (paginated)
- `POST /api/v1/products/` - Create product (auth required)
- `GET /api/v1/products/{id}/` - Get product details
- `PUT /api/v1/products/{id}/` - Update product (auth required)
- `DELETE /api/v1/products/{id}/` - Delete product (auth required)
- `GET /api/v1/products/search/` - Search products

#### Orders
- `GET /api/v1/orders/` - List orders (paginated)
- `POST /api/v1/orders/` - Create order (auth required)
- `GET /api/v1/orders/{id}/` - Get order details
- `PATCH /api/v1/orders/{id}/status/` - Update order status
- `POST /api/v1/orders/{id}/cancel/` - Cancel order
- `GET /api/v1/orders/customer/{email}/` - Get customer orders

#### System
- `GET /api/v1/health/` - Health check endpoint
- `GET /metrics` - Prometheus metrics

## 🧪 Testing

### Run All Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
pytest products/test_api.py

# Run tests with specific marker
pytest -m unit
pytest -m integration
```

### Test Structure

```
tests/
├── unit/           # Unit tests for models and utilities
├── integration/    # Integration tests for services
└── api/           # API endpoint tests
```

### Code Quality

```bash
# Run all quality checks
make lint

# Format code
make format

# Individual checks
black --check .
isort --check-only .
flake8 .
pylint products orders core
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_ENV=production

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Redis
REDIS_URL=redis://localhost:6379/1
CELERY_BROKER_URL=redis://localhost:6379/0

# gRPC
GRPC_PRODUCT_SERVER_HOST=localhost
GRPC_PRODUCT_SERVER_PORT=50051
GRPC_ORDER_SERVER_HOST=localhost
GRPC_ORDER_SERVER_PORT=50052

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Sentry (optional)
SENTRY_DSN=your-sentry-dsn
SENTRY_ENVIRONMENT=production

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Settings Structure

```
ecommerce_grpc/settings/
├── __init__.py      # Auto-loads based on DJANGO_ENV
├── base.py          # Common settings
├── development.py   # Development overrides
├── production.py    # Production settings
└── testing.py       # Test settings
```

## 📊 Monitoring

### Prometheus Metrics

Access metrics at: http://localhost:8000/metrics

Key metrics:
- Request count and latency
- Database query performance
- Cache hit/miss rates
- Celery task execution
- gRPC call statistics

### Logging

Logs are stored in `logs/django.log` with rotation:

```python
# Log levels
DEBUG    # Detailed information for debugging
INFO     # General information
WARNING  # Warning messages
ERROR    # Error messages
CRITICAL # Critical issues
```

### Sentry Integration

Configure Sentry for error tracking:

```env
SENTRY_DSN=https://your-sentry-dsn
SENTRY_ENVIRONMENT=production
```

## 🔒 Security Best Practices

1. **Never commit secrets** - Use environment variables
2. **Use HTTPS in production** - Configure SSL/TLS
3. **Keep dependencies updated** - Regular security updates
4. **Enable rate limiting** - Prevent API abuse
5. **Use strong passwords** - Enforce password policies
6. **Regular backups** - Database and media files
7. **Monitor logs** - Watch for suspicious activity
8. **Security headers** - Already configured in settings

## 📦 Deployment

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set strong `SECRET_KEY`
- [ ] Use PostgreSQL (not SQLite)
- [ ] Configure Redis
- [ ] Set up SSL/TLS certificates
- [ ] Configure email backend
- [ ] Set up Sentry
- [ ] Configure backups
- [ ] Set up monitoring
- [ ] Run security audit
- [ ] Load test the application

### Docker Production Deployment

```bash
# Build production images
docker-compose -f docker-compose.yml build

# Start services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Run `make lint` before committing
- Keep commits atomic and descriptive

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django REST Framework
- gRPC Python
- Celery
- Redis
- PostgreSQL
- All contributors and maintainers

## 📞 Support

- **Documentation**: [Full Docs](https://docs.example.com)
- **Issues**: [GitHub Issues](https://github.com/yourusername/ecommerce-grpc/issues)
- **Email**: support@example.com

---

**Built with ❤️ for production environments**
