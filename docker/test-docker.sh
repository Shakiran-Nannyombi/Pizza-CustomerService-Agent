#!/bin/bash
# Quick Docker Test Script
# Tests if Docker deployment is working correctly

echo "==============================================="
echo "Pizza Customer Service Agent - Docker Test"
echo "==============================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "Install from: https://docs.docker.com/get-docker/"
    exit 1
fi
echo "✓ Docker is installed"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed"
    exit 1
fi
echo "✓ Docker Compose is installed"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found"
    echo "Run: cp .env.example .env"
    echo "Then add your GROQ_API_KEY"
    exit 1
fi
echo "✓ .env file exists"

# Check if GROQ_API_KEY is set
if ! grep -q "GROQ_API_KEY=.*[a-zA-Z0-9]" .env; then
    echo "⚠ GROQ_API_KEY appears to be empty in .env"
    echo "Please add your API key to .env"
    exit 1
fi
echo "✓ GROQ_API_KEY is configured"

echo ""
echo "Starting Docker services..."
echo "-------------------------------------------"

# Build and start services
docker-compose up -d --build

echo ""
echo "Waiting for services to be healthy..."
sleep 10

# Check if containers are running
if [ $(docker-compose ps -q | wc -l) -eq 0 ]; then
    echo "❌ No containers are running"
    echo "Check logs with: docker-compose logs"
    exit 1
fi
echo "✓ Containers are running"

# Test API health
echo ""
echo "Testing API health..."
API_STATUS=$(curl -s http://localhost:8000/status 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✓ API is responding"
    echo "  Response: $API_STATUS"
else
    echo "❌ API is not responding"
    echo "Check logs with: docker-compose logs api"
fi

# Test Streamlit
echo ""
echo "Testing Streamlit..."
STREAMLIT_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8501 2>/dev/null)
if [ "$STREAMLIT_STATUS" = "200" ] || [ "$STREAMLIT_STATUS" = "302" ]; then
    echo "✓ Streamlit is responding"
else
    echo "❌ Streamlit is not responding (Status: $STREAMLIT_STATUS)"
    echo "Check logs with: docker-compose logs streamlit"
fi

echo ""
echo "==============================================="
echo "Test Complete!"
echo "==============================================="
echo ""
echo "Access your application:"
echo "  Frontend: http://localhost:8501"
echo "  API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "View logs:"
echo "  docker-compose logs -f"
echo ""
echo "Stop services:"
echo "  docker-compose down"
echo ""
