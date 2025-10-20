# Upgrade Guide: Intermediate to Professional Level

This guide explains the upgrades made to transform the intermediate Django gRPC project into a production-ready, professional-grade application.

## 🎯 Overview of Upgrades

### 1. Architecture Improvements
- ✅ Multi-environment settings (dev/staging/prod)
- ✅ Celery for asynchronous task processing
- ✅ Redis caching layer
- ✅ API versioning (`/api/v1/`)
- ✅ Structured logging with rotation

### 2. Security Enhancements
- ✅ JWT authentication with refresh tokens
- ✅ Custom permissions system
- ✅ Rate limiting and throttling
- ✅ Security headers (XSS, CSRF, etc.)
- ✅ Environment-based configuration

### 3. Testing & Quality
- ✅ Comprehensive test suite (pytest)
- ✅ Code coverage reporting
- ✅ CI/CD pipelines (GitHub Actions)
- ✅ Code quality tools (black, isort, flake8, pylint)
- ✅ Pre-commit hooks support

### 4. Monitoring & Observability
- ✅ Prometheus metrics integration
- ✅ Sentry error tracking
- ✅ Custom middleware for request logging
- ✅ Health check endpoints
- ✅ Structured JSON logging

### 5. Deployment & DevOps
- ✅ Docker multi-stage builds
- ✅ Docker Compose orchestration
- ✅ Nginx reverse proxy configuration
- ✅ Kubernetes-ready setup
- ✅ Automated deployment workflows

### 6. API Documentation
- ✅ OpenAPI/Swagger integration
- ✅ ReDoc documentation
- ✅ Interactive API explorer
- ✅ Comprehensive endpoint documentation

## 📦 New Dependencies

### Core Additions
```
djangorestframework-simplejwt==5.3.0  # JWT authentication
redis==5.0.1                          # Redis client
django-redis==5.4.0                   # Django Redis cache backend
celery==5.3.4                         # Async task queue
django-celery-beat==2.5.0             # Periodic tasks
django-celery-results==2.5.1          # Task result storage
```

### Monitoring & Documentation
```
django-prometheus==2.3.1              # Prometheus metrics
sentry-sdk==1.39.1                    # Error tracking
drf-spectacular==0.27.0               # API documentation
```

### Testing & Quality
```
pytest==7.4.3                         # Testing framework
pytest-django==4.7.0                  # Django pytest plugin
pytest-cov==4.1.0                     # Coverage reporting
factory-boy==3.3.0                    # Test fixtures
black==23.12.1                        # Code formatter
flake8==6.1.0                         # Linter
isort==5.13.2                         # Import sorter
```

### Database & Performance
```
psycopg2-binary==2.9.9                # PostgreSQL adapter
dj-database-url==2.1.0                # Database URL parsing
hiredis==2.2.3                        # Redis parser
```

## 🔄 Migration Steps

### Step 1: Install New Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Install new packages
pip install -r requirements.txt
```

### Step 2: Update Settings

The settings have been restructured into multiple files:

```
ecommerce_grpc/settings/
├── __init__.py       # Auto-loads based on DJANGO_ENV
├── base.py           # Common settings
├── development.py    # Development overrides
├── production.py     # Production settings
└── testing.py        # Test settings
```

**Old way:**
```python
# Single settings.py file
```

**New way:**
```bash
# Set environment variable
export DJANGO_ENV=development  # or production, testing
```

### Step 3: Set Up Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit with your values
nano .env
```

Required variables:
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - Database connection string
- `REDIS_URL` - Redis connection string
- `CELERY_BROKER_URL` - Celery broker URL

### Step 4: Update URL Configuration

URLs have been versioned and reorganized:

**Old:**
```python
path('api/products/', include('products.urls')),
path('api/orders/', include('orders.urls')),
```

**New:**
```python
path('api/v1/products/', include('products.urls')),
path('api/v1/orders/', include('orders.urls')),
path('api/v1/', include('core.urls')),  # Auth endpoints
```

### Step 5: Run New Migrations

```bash
# Create migrations for new apps
python manage.py makemigrations core

# Run all migrations
python manage.py migrate
```

### Step 6: Set Up Redis (Required)

**Option 1: Local Installation**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# macOS
brew install redis
brew services start redis
```

**Option 2: Docker**
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

### Step 7: Set Up Celery Workers

```bash
# Terminal 1: Start Celery worker
celery -A ecommerce_grpc worker -l info

# Terminal 2: Start Celery beat (for periodic tasks)
celery -A ecommerce_grpc beat -l info
```

Or use the Makefile:
```bash
make celery-worker
make celery-beat
```

### Step 8: Update API Calls

If you have existing clients, update the base URL:

**Old:**
```
http://localhost:8000/api/products/
```

**New:**
```
http://localhost:8000/api/v1/products/
```

### Step 9: Authentication Updates

The project now uses JWT authentication:

**Register:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user",
    "email": "user@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "First",
    "last_name": "Last"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user",
    "password": "SecurePass123!"
  }'
```

**Use Token:**
```bash
curl -X POST http://localhost:8000/api/v1/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Product", ...}'
```

## 🆕 New Features

### 1. Authentication System

```python
# New endpoints
POST /api/v1/auth/register/          # Register user
POST /api/v1/auth/login/             # Login (get tokens)
POST /api/v1/auth/refresh/           # Refresh access token
GET  /api/v1/user/profile/           # Get user profile
PATCH /api/v1/user/profile/          # Update profile
POST /api/v1/user/change-password/   # Change password
```

### 2. Celery Tasks

```python
# Example: Send order confirmation asynchronously
from orders.tasks import send_order_confirmation

send_order_confirmation.delay(order_id=123)
```

Available tasks:
- `cleanup_expired_sessions` - Clean old sessions
- `update_product_analytics` - Update product stats
- `process_pending_orders` - Auto-process old orders
- `send_order_status_notifications` - Email notifications

### 3. Caching

```python
from django.core.cache import cache

# Cache product data
cache.set('product_123', product_data, timeout=3600)

# Get cached data
product = cache.get('product_123')
```

### 4. API Documentation

Access interactive documentation:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- OpenAPI Schema: http://localhost:8000/api/schema/

### 5. Monitoring

- Prometheus metrics: http://localhost:8000/metrics
- Health check: http://localhost:8000/api/v1/health/

### 6. Custom Permissions

```python
from core.permissions import IsAuthenticatedForWrite

class MyView(APIView):
    permission_classes = [IsAuthenticatedForWrite]
```

## 🐳 Docker Deployment

### Quick Start

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### Services Included

- `web` - Django application (Gunicorn)
- `product_grpc` - Product gRPC server
- `order_grpc` - Order gRPC server
- `db` - PostgreSQL database
- `redis` - Redis cache
- `celery_worker` - Celery worker
- `celery_beat` - Celery beat scheduler
- `nginx` - Reverse proxy

## 🧪 Testing

### Run Tests

```bash
# All tests
make test

# With coverage
make test-cov

# Specific tests
pytest products/test_api.py
pytest -m unit
```

### Code Quality

```bash
# Run all checks
make lint

# Format code
make format
```

## 📊 Monitoring Setup

### Prometheus

Add to `prometheus.yml`:
```yaml
scrape_configs:
  - job_name: 'django'
    static_configs:
      - targets: ['localhost:8000']
```

### Sentry

Set in `.env`:
```env
SENTRY_DSN=your-sentry-dsn
SENTRY_ENVIRONMENT=production
```

## 🔒 Security Checklist

- [ ] Change `SECRET_KEY` in production
- [ ] Set `DEBUG=False` in production
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL (not SQLite)
- [ ] Enable HTTPS/SSL
- [ ] Set up firewall rules
- [ ] Configure rate limiting
- [ ] Enable Sentry monitoring
- [ ] Regular security updates
- [ ] Backup database regularly

## 📝 Breaking Changes

### URL Changes
- All API endpoints now under `/api/v1/`
- Authentication endpoints moved to `/api/v1/auth/`

### Authentication
- Session authentication replaced with JWT
- All write operations require authentication
- Token refresh required after expiry

### Settings
- Single `settings.py` split into multiple files
- Environment variables required
- Redis now mandatory for caching

### Dependencies
- Python 3.10+ required
- PostgreSQL recommended for production
- Redis required

## 🆘 Troubleshooting

### Redis Connection Error
```bash
# Check if Redis is running
redis-cli ping

# Start Redis
sudo systemctl start redis  # Linux
brew services start redis   # macOS
```

### Celery Not Working
```bash
# Check broker connection
celery -A ecommerce_grpc inspect ping

# Restart worker
pkill -f celery
make celery-worker
```

### Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Database Migration Issues
```bash
# Reset migrations (development only!)
python manage.py migrate --fake
python manage.py migrate
```

## 📚 Additional Resources

- [Django Best Practices](https://docs.djangoproject.com/en/4.2/misc/design-philosophies/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Redis Documentation](https://redis.io/documentation)
- [Docker Documentation](https://docs.docker.com/)
- [Prometheus Documentation](https://prometheus.io/docs/)

## 🎉 What's Next?

Consider these additional improvements:
1. Kubernetes deployment configuration
2. GraphQL API layer
3. WebSocket support for real-time updates
4. Advanced caching strategies
5. Machine learning integration
6. Multi-tenancy support
7. Advanced analytics dashboard
8. Mobile app backend

---

**Congratulations!** Your project is now production-ready with enterprise-grade features. 🚀
