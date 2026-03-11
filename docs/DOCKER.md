# Docker Deployment Guide

Complete guide for deploying the Pizza Customer Service Agent using Docker and Docker Compose.

## Quick Start

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- `.env` file with your `GROQ_API_KEY`

### Deploy in 3 Steps

```bash
# 1. Ensure your .env file exists
echo "GROQ_API_KEY=your_key_here" > .env

# 2. Build and start all services
docker-compose up -d

# 3. Access the application
# Frontend: http://localhost:8501
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Architecture

```bash
┌─────────────────────────────────────────┐
│          Docker Network                 │
│                                         │
│  ┌──────────────┐  ┌─────────────────┐ │
│  │  Streamlit   │  │   FastAPI       │ │
│  │  Frontend    │─▶│   Backend       │ │
│  │  :8501       │  │   :8000         │ │
│  └──────────────┘  └─────────────────┘ │
│         │                    │          │
└─────────┼────────────────────┼──────────┘
          │                    │
          ▼                    ▼
    pizza_agent package (shared)
```

## Docker Files

### Development Setup

**docker-compose.yml** - Development environment

- Hot reload disabled
- Health checks enabled
- Auto-restart on failure
- Basic resource limits

### Production Setup

**docker-compose.prod.yml** - Production environment

- Optimized resource limits
- Log rotation configured
- Nginx reverse proxy
- Enhanced health checks
- Auto-restart always

## Commands

### Development

```bash
# Start services
docker-compose up

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f api
docker-compose logs -f streamlit

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up --build

# Remove volumes
docker-compose down -v
```

### Production

```bash
# Start production services
docker-compose -f docker-compose.prod.yml up -d

# View status
docker-compose -f docker-compose.prod.yml ps

# Scale services (if needed)
docker-compose -f docker-compose.prod.yml up -d --scale api=2

# Update after changes
docker-compose -f docker-compose.prod.yml up -d --build

# Stop production
docker-compose -f docker-compose.prod.yml down
```

## Service Details

### API Service (FastAPI Backend)

**Container:** `pizza-agent-api`
**Port:** 8000
**Image:** Built from `Dockerfile.api`

**Features:**

- Python 3.12 slim base
- Uvicorn ASGI server
- Health check endpoint
- Auto-restart on failure

**Endpoints:**

- Health: <http://localhost:8000/status>
- Docs: <http://localhost:8000/docs>
- Chat: POST <http://localhost:8000/chat>

### Streamlit Service (Frontend)

**Container:** `pizza-agent-streamlit`
**Port:** 8501
**Image:** Built from `Dockerfile.streamlit`

**Features:**

- Python 3.12 slim base
- Streamlit server
- Connects to API via Docker network
- Auto-restart on failure

**Access:** <http://localhost:8501>

### Nginx Service (Production Only)

**Container:** `pizza-agent-nginx`
**Port:** 80 (HTTP), 443 (HTTPS)
**Image:** nginx:alpine

**Features:**

- Reverse proxy for both services
- WebSocket support for Streamlit
- Load balancing ready
- Log rotation

## Environment Variables

Create `.env` file in project root:

```bash
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional (defaults shown)
GROQ_MODEL=llama-3.1-70b-versatile
GROQ_API_URL=https://api.groq.com/openai/v1

# Docker-specific (auto-configured)
API_BASE_URL=http://api:8000
```

## Networking

Services communicate via Docker bridge network `pizza-network`:

- **streamlit → api**: Internal DNS resolution via service name
- **External → api**: Host port 8000
- **External → streamlit**: Host port 8501
- **Production**: Nginx on port 80/443 routes to both

## Health Checks

Both services have health checks configured:

**API:**

```bash
# Check from host
curl http://localhost:8000/status

# Check from container
docker exec pizza-agent-api python -c "import requests; print(requests.get('http://localhost:8000/status').json())"
```

**Streamlit:**

```bash
# Check from host
curl http://localhost:8501/_stcore/health

# Check from container
docker exec pizza-agent-streamlit curl -f http://localhost:8501/_stcore/health
```

## Resource Limits

### Development

- No strict limits
- Best effort allocation

### Production

**Per Service:**

- CPU Limit: 1.0 cores
- CPU Reservation: 0.5 cores
- Memory Limit: 1GB
- Memory Reservation: 512MB

## Volumes

Optional persistent volumes for data:

- `api-data` - API persistent storage
- `streamlit-data` - Streamlit cache/storage

*Currently unused but available for future features*

## Logs

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f streamlit

# Last 100 lines
docker-compose logs --tail=100 api

# Timestamps
docker-compose logs -t -f
```

### Log Rotation (Production)

Configured in docker-compose.prod.yml:

- Max size: 10MB per file
- Max files: 3
- Driver: json-file

## Troubleshooting

### Container Won't Start

```bash
# Check container status
docker-compose ps

# View container logs
docker-compose logs api
docker-compose logs streamlit

# Check if ports are in use
lsof -i :8000
lsof -i :8501

# Restart services
docker-compose restart
```

### Build Failures

```bash
# Clean rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up

# Check Docker daemon
docker info

# Check disk space
df -h
```

### API Connection Issues

```bash
# Test API from host
curl http://localhost:8000/status

# Test API from streamlit container
docker exec pizza-agent-streamlit curl http://api:8000/status

# Check network
docker network inspect pizza-network

# Restart with new network
docker-compose down
docker-compose up
```

### Environment Variables Not Loading

```bash
# Verify .env file exists
cat .env

# Check if variables are set in container
docker exec pizza-agent-api env | grep GROQ
docker exec pizza-agent-streamlit env | grep GROQ

# Rebuild with new env
docker-compose up --build --force-recreate
```

## Performance Optimization

### Build Optimization

1. **Use .dockerignore**
   - Excludes unnecessary files
   - Faster builds
   - Smaller images

2. **Layer Caching**
   - requirements.txt copied first
   - Dependencies cached separately
   - Code changes don't rebuild deps

3. **Multi-stage Builds (Optional)**

   ```dockerfile
   # Add to Dockerfile for smaller images
   FROM python:3.12-slim as builder
   # ... build steps
   
   FROM python:3.12-slim
   COPY --from=builder /app /app
   ```

### Runtime Optimization

1. **Resource Limits**
   - Set in docker-compose.prod.yml
   - Prevents resource hogging
   - Ensures fair allocation

2. **Health Checks**
   - Auto-restart unhealthy containers
   - Early problem detection
   - Better uptime

## Deployment Strategies

### Local Development

```bash
docker-compose up
```

- Fast iteration
- Live debugging
- Easy testing

### Staging/Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```

- Resource limits
- Log rotation
- Nginx proxy
- Always restart

### Cloud Deployment

**AWS ECS:**

```bash
# Use docker-compose.prod.yml as base
# Convert to ECS task definition
ecs-cli compose -f docker-compose.prod.yml up
```

**Azure Container Instances:**

```bash
az container create --resource-group myResourceGroup \
  --file docker-compose.prod.yml
```

**Google Cloud Run:**

```bash
# Deploy API
gcloud run deploy pizza-agent-api --source .

# Deploy Streamlit
gcloud run deploy pizza-agent-streamlit --source .
```

## Security Best Practices

1. **Never commit .env file**

   ```bash
   echo ".env" >> .gitignore
   ```

2. **Use secrets management in production**

   ```yaml
   secrets:
     groq_api_key:
       external: true
   ```

3. **Enable HTTPS in production**
   - Add SSL certificates
   - Configure nginx for HTTPS
   - Redirect HTTP to HTTPS

4. **Scan images for vulnerabilities**

   ```bash
   docker scan pizza-agent-api
   docker scan pizza-agent-streamlit
   ```

## Monitoring

### Docker Stats

```bash
# Real-time resource usage
docker stats

# Specific containers
docker stats pizza-agent-api pizza-agent-streamlit
```

### Health Status

```bash
# Check health
docker-compose ps

# Auto-restart unhealthy containers (already configured)
```

### Logging to External Service

Add to docker-compose.prod.yml:

```yaml
logging:
  driver: "syslog"
  options:
    syslog-address: "tcp://logs.example.com:514"
```

## Backup and Restore

### Backup

```bash
# Backup volumes
docker run --rm \
  -v pizza-agent_api-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/api-backup.tar.gz /data

# Backup environment
cp .env .env.backup
```

### Restore

```bash
# Restore volumes
docker run --rm \
  -v pizza-agent_api-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/api-backup.tar.gz -C /

# Restore environment
cp .env.backup .env
```

## Updates and Maintenance

### Update Application

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose up -d --build

# Or for production
docker-compose -f docker-compose.prod.yml up -d --build
```

### Update Base Images

```bash
# Pull latest Python image
docker pull python:3.12-slim

# Rebuild
docker-compose build --pull
docker-compose up -d
```

### Clean Up

```bash
# Remove stopped containers
docker-compose down

# Remove volumes
docker-compose down -v

# Remove all unused Docker resources
docker system prune -a
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Push
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build images
        run: docker-compose build
      - name: Push to registry
        run: docker-compose push
```

## Support

For issues:

1. Check logs: `docker-compose logs -f`
2. Verify .env file has correct API key
3. Ensure ports 8000 and 8501 are available
4. Review main documentation in `docs/` folder

## Quick Reference

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f

# Rebuild
docker-compose up --build

# Status
docker-compose ps

# Shell access
docker exec -it pizza-agent-api bash
docker exec -it pizza-agent-streamlit bash
```

---

For more information, see the main [README.md](../README.md) and [Architecture docs](ARCHITECTURE.md).
