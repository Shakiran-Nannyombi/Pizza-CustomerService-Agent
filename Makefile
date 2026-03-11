# Makefile for Pizza Customer Service Agent
.PHONY: help install dev docker-up docker-down docker-logs docker-build test clean

# Default target
help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make dev          - Run in development mode (local)"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make docker-logs  - View Docker logs"
	@echo "  make docker-build - Rebuild Docker containers"
	@echo "  make prod-up      - Start production Docker setup"
	@echo "  make prod-down    - Stop production Docker setup"
	@echo "  make clean        - Clean up cache and temp files"
	@echo "  make test         - Run tests"

# Install dependencies
install:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
	@echo "✓ Dependencies installed"
	@echo "Don't forget to create .env file with GROQ_API_KEY"

# Run in development mode
dev:
	. .venv/bin/activate && python launch.py

# Docker commands
docker-up:
	docker-compose -f docker/docker-compose.yml up -d
	@echo "✓ Services started"
	@echo "Frontend: http://localhost:8501"
	@echo "API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

docker-down:
	docker-compose -f docker/docker-compose.yml down

docker-logs:
	docker-compose -f docker/docker-compose.yml logs -f

docker-build:
	docker-compose -f docker/docker-compose.yml build --no-cache

docker-restart:
	docker-compose -f docker/docker-compose.yml restart

docker-ps:
	docker-compose -f docker/docker-compose.yml ps

# Production commands
prod-up:
	docker-compose -f docker/docker-compose.prod.yml up -d
	@echo "✓ Production services started"

prod-down:
	docker-compose -f docker/docker-compose.prod.yml down

prod-logs:
	docker-compose -f docker/docker-compose.prod.yml logs -f

prod-build:
	docker-compose -f docker/docker-compose.prod.yml build --no-cache

# Testing
test:
	. .venv/bin/activate && python -m pytest tests/

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	@echo "✓ Cleaned up"

# Setup environment
setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✓ Created .env file from .env.example"; \
		echo "⚠ Please edit .env and add your GROQ_API_KEY"; \
	else \
		echo ".env file already exists"; \
	fi

# Check environment
check-env:
	@if [ ! -f .env ]; then \
		echo ".env file not found!"; \
		echo "Run 'make setup' to create it"; \
		exit 1; \
	else \
		echo "✓ .env file exists"; \
	fi

# API health check
health:
	@curl -s http://localhost:8000/status | python -m json.tool

# Full setup
full-setup: setup install
	@echo "✓ Full setup complete"
	@echo "Next steps:"
	@echo "  1. Edit .env and add your GROQ_API_KEY"
	@echo "  2. Run 'make dev' or 'make docker-up'"
