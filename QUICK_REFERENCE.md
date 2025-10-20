# Quick Reference Card

## 🚀 Essential Commands

### Development
```bash
# Start everything
make run-dev                    # Start all dev servers

# Individual services
./start_grpc_servers.sh         # Start gRPC servers
python manage.py runserver      # Start Django
make celery-worker              # Start Celery worker
make celery-beat                # Start Celery beat
```

### Docker
```bash
make docker-up                  # Start all services
make docker-down                # Stop all services
make docker-logs                # View logs
docker-compose exec web bash   # Shell into container
```

### Database
```bash
make migrate                    # Run migrations
python manage.py makemigrations # Create migrations
make superuser                  # Create admin user
python manage.py shell          # Django shell
```

### Testing
```bash
make test                       # Run all tests
make test-cov                   # Tests with coverage
pytest -v                       # Verbose tests
pytest -k test_name             # Run specific test
```

### Code Quality
```bash
make lint                       # Check code quality
make format                     # Auto-format code
black .                         # Format with Black
isort .                         # Sort imports
flake8 .                        # Lint code
```

---

## 🔗 Important URLs

| Service | URL |
|---------|-----|
| API Base | http://localhost:8000/api/v1/ |
| Admin | http://localhost:8000/admin/ |
| Swagger | http://localhost:8000/api/docs/ |
| ReDoc | http://localhost:8000/api/redoc/ |
| Health | http://localhost:8000/api/v1/health/ |
| Metrics | http://localhost:8000/metrics |

---

## 🔐 Authentication Flow

```bash
# 1. Register
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user","email":"user@example.com","password":"Pass123!","password2":"Pass123!","first_name":"First","last_name":"Last"}'

# 2. Login
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"Pass123!"}'

# 3. Use token
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/api/v1/products/
```

---

## 📦 API Endpoints

### Authentication
- `POST /api/v1/auth/register/` - Register
- `POST /api/v1/auth/login/` - Login
- `POST /api/v1/auth/refresh/` - Refresh token
- `GET /api/v1/user/profile/` - Get profile
- `PATCH /api/v1/user/profile/` - Update profile

### Products
- `GET /api/v1/products/` - List
- `POST /api/v1/products/` - Create (auth)
- `GET /api/v1/products/{id}/` - Detail
- `PUT /api/v1/products/{id}/` - Update (auth)
- `DELETE /api/v1/products/{id}/` - Delete (auth)
- `GET /api/v1/products/search/` - Search

### Orders
- `GET /api/v1/orders/` - List
- `POST /api/v1/orders/` - Create (auth)
- `GET /api/v1/orders/{id}/` - Detail
- `PATCH /api/v1/orders/{id}/status/` - Update status
- `POST /api/v1/orders/{id}/cancel/` - Cancel
- `GET /api/v1/orders/customer/{email}/` - By customer

---

## ⚙️ Environment Variables

```env
# Required
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/1
CELERY_BROKER_URL=redis://localhost:6379/0

# Optional
DEBUG=True
DJANGO_ENV=development
SENTRY_DSN=your-sentry-dsn
```

---

## 🐳 Docker Services

| Service | Port | Description |
|---------|------|-------------|
| web | 8000 | Django app |
| product_grpc | 50051 | Product service |
| order_grpc | 50052 | Order service |
| db | 5432 | PostgreSQL |
| redis | 6379 | Redis cache |
| nginx | 80 | Reverse proxy |

---

## 🧪 Test Commands

```bash
# All tests
pytest

# Specific file
pytest products/test_api.py

# By marker
pytest -m unit
pytest -m integration

# With coverage
pytest --cov=. --cov-report=html

# Verbose
pytest -v -s
```

---

## 📝 Common Tasks

### Create New App
```bash
python manage.py startapp myapp
# Add to INSTALLED_APPS in settings/base.py
```

### Add Celery Task
```python
# myapp/tasks.py
from celery import shared_task

@shared_task
def my_task():
    # Task logic
    pass
```

### Add API Endpoint
```python
# myapp/views.py
from rest_framework.views import APIView

class MyView(APIView):
    def get(self, request):
        return Response({'data': 'value'})

# myapp/urls.py
urlpatterns = [
    path('my-endpoint/', MyView.as_view()),
]
```

### Cache Data
```python
from django.core.cache import cache

# Set
cache.set('key', value, timeout=3600)

# Get
value = cache.get('key')
```

---

## 🔍 Debugging

### View Logs
```bash
# Django logs
tail -f logs/django.log

# Docker logs
docker-compose logs -f web
docker-compose logs -f product_grpc
```

### Django Shell
```python
python manage.py shell

# Import models
from products.models import Product
from orders.models import Order

# Query data
Product.objects.all()
Order.objects.filter(status='pending')
```

### Redis CLI
```bash
redis-cli
> KEYS *
> GET key_name
> FLUSHALL  # Clear all cache
```

---

## 🚨 Troubleshooting

### Redis not running
```bash
# Check status
redis-cli ping

# Start Redis
sudo systemctl start redis  # Linux
brew services start redis   # macOS
```

### Port already in use
```bash
# Find process
lsof -ti:8000

# Kill process
kill -9 $(lsof -ti:8000)
```

### Database locked
```bash
# Stop all processes
pkill -f manage.py
pkill -f celery

# Restart
python manage.py runserver
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check virtual env
which python
```

---

## 📊 Monitoring

### Check Health
```bash
curl http://localhost:8000/api/v1/health/
```

### View Metrics
```bash
curl http://localhost:8000/metrics
```

### Celery Status
```bash
celery -A ecommerce_grpc inspect active
celery -A ecommerce_grpc inspect stats
```

---

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| `.env` | Environment variables |
| `pytest.ini` | Pytest configuration |
| `.flake8` | Flake8 rules |
| `pyproject.toml` | Tool configs |
| `Makefile` | Common commands |
| `docker-compose.yml` | Docker stack |

---

## 📚 Documentation

| File | Description |
|------|-------------|
| `README_PROFESSIONAL.md` | Main documentation |
| `UPGRADE_GUIDE.md` | Upgrade instructions |
| `PROFESSIONAL_FEATURES.md` | Feature details |
| `PROFESSIONAL_SUMMARY.md` | Complete summary |
| `API_TESTING_GUIDE.md` | API examples |
| `QUICK_REFERENCE.md` | This file |

---

## 🎯 Quick Tips

1. **Always activate venv:** `source venv/bin/activate`
2. **Use Makefile:** `make test`, `make lint`, etc.
3. **Check docs:** http://localhost:8000/api/docs/
4. **View logs:** `tail -f logs/django.log`
5. **Test first:** Run tests before committing
6. **Format code:** `make format` before pushing
7. **Use Docker:** Easier for full stack testing
8. **Monitor metrics:** Check `/metrics` endpoint
9. **Read errors:** Error messages are helpful
10. **Ask for help:** Check documentation files

---

**Keep this handy for quick reference!** 📌
