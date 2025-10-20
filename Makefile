.PHONY: help install migrate test lint format clean docker-build docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make migrate       - Run database migrations"
	@echo "  make test          - Run tests"
	@echo "  make test-cov      - Run tests with coverage"
	@echo "  make lint          - Run code quality checks"
	@echo "  make format        - Format code with black and isort"
	@echo "  make clean         - Clean up generated files"
	@echo "  make docker-build  - Build Docker images"
	@echo "  make docker-up     - Start Docker containers"
	@echo "  make docker-down   - Stop Docker containers"
	@echo "  make run-dev       - Run development servers"
	@echo "  make celery-worker - Start Celery worker"
	@echo "  make celery-beat   - Start Celery beat"

install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations
	python manage.py migrate

test:
	pytest

test-cov:
	pytest --cov=. --cov-report=html --cov-report=term-missing

lint:
	black --check .
	isort --check-only .
	flake8 .
	pylint products orders core || true

format:
	black .
	isort .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov .coverage .pytest_cache
	rm -rf build dist

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

run-dev:
	@echo "Starting gRPC servers..."
	@./start_grpc_servers.sh &
	@echo "Starting Django server..."
	@python manage.py runserver

celery-worker:
	celery -A ecommerce_grpc worker -l info

celery-beat:
	celery -A ecommerce_grpc beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

superuser:
	python manage.py createsuperuser

shell:
	python manage.py shell

compile-protos:
	python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/products.proto
	python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/orders.proto

collectstatic:
	python manage.py collectstatic --noinput

requirements:
	pip freeze > requirements.txt
