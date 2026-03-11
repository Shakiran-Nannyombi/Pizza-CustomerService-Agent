# Docker Quick Reference

Quick commands for deploying and managing the Pizza Customer Service Agent with Docker.

## Setup (First Time)

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env and add your GROQ_API_KEY
nano .env  # or vim, code, etc.

# 3. Test setup
./test-docker.sh
```

## Common Commands

### Start Services

```bash
# Development
docker-compose up -d

# Production
docker-compose -f docker-compose.prod.yml up -d

# With rebuild
docker-compose up -d --build
```

### Stop Services

```bash
# Stop (keeps data)
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f streamlit

# Last 50 lines
docker-compose logs --tail=50
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific
docker-compose restart api
```

### Check Status

```bash
# Container status
docker-compose ps

# Resource usage
docker stats

# Health check
curl http://localhost:8000/status
```

### Shell Access

```bash
# API container
docker exec -it pizza-agent-api bash

# Streamlit container
docker exec -it pizza-agent-streamlit bash
```

### Rebuild

```bash
# Clean rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Access URLs

- **Frontend**: <http://localhost:8501>
- **API**: <http://localhost:8000>
- **API Docs**: <http://localhost:8000/docs>
- **API ReDoc**: <http://localhost:8000/redoc>

## Makefile Shortcuts

```bash
# Using Makefile (easier)
make docker-up        # Start services
make docker-down      # Stop services
make docker-logs      # View logs
make docker-build     # Rebuild
make prod-up          # Production start
make health           # API health check
```

## Troubleshooting

### Port Already in Use

```bash
# Find what's using the port
lsof -i :8000
lsof -i :8501

# Kill the process
kill -9 <PID>
```

### Services Won't Start

```bash
# View detailed logs
docker-compose logs api
docker-compose logs streamlit

# Check container status
docker-compose ps

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### API Connection Issues

```bash
# Test API from host
curl http://localhost:8000/status

# Test from streamlit container
docker exec pizza-agent-streamlit curl http://api:8000/status

# Check network
docker network inspect pizza-network
```

### Environment Variables Not Working

```bash
# Check if .env exists
cat .env

# Verify vars in container
docker exec pizza-agent-api env | grep GROQ

# Force recreate
docker-compose up --force-recreate
```

## Production Deployment

```bash
# Start production services
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop
docker-compose -f docker-compose.prod.yml down
```

## Maintenance

### Update Application

```bash
git pull
docker-compose up -d --build
```

### Update Base Images

```bash
docker pull python:3.12-slim
docker-compose build --pull
docker-compose up -d
```

### Clean Up

```bash
# Remove stopped containers
docker-compose down

# Remove unused images
docker image prune -a

# Clean everything
docker system prune -a
```

### Backup

```bash
# Backup volumes
docker run --rm \
  -v pizza-agent_api-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz /data
```

## Monitoring

```bash
# Real-time stats
docker stats pizza-agent-api pizza-agent-streamlit

# Check health
docker inspect --format='{{.State.Health.Status}}' pizza-agent-api

# View resource limits
docker inspect --format='{{.HostConfig.Memory}}' pizza-agent-api
```

## Complete Workflow

```bash
# First time setup
cp .env.example .env
# Edit .env and add GROQ_API_KEY
docker-compose up -d
# Wait 10 seconds
curl http://localhost:8000/status
# Open http://localhost:8501

# Daily use
docker-compose up -d    # Start
docker-compose down     # Stop

# After code changes
docker-compose up -d --build

# Troubleshooting
docker-compose logs -f
docker-compose restart
docker-compose down && docker-compose up -d
```

## Quick Test Script

```bash
# Run automated test
./test-docker.sh
```

## Help

For detailed documentation, see [DOCKER.md](DOCKER.md)

For general help, see [README.md](../README.md)

---

**Tip**: Use `make` commands for easier workflow:

```bash
make help  # See all available commands
```
