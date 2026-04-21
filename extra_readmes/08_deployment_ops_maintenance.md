# Deployment, Ops & Maintenance

## 1. Deployment Overview

### 1.1 Deployment Architecture

```mermaid
flowchart TB
    subgraph Development["Development"]
        DEV[Dev Environment]
        TEST[Testing]
    end
    
    subgraph Staging["Staging"]
        STG_API[API]
        STG_DB[(Database)]
    end
    
    subgraph Production["Production"]
        LB[Load Balancer]
        
        subgraph Cluster["Service Cluster"]
            API1[API Instance 1]
            API2[API Instance 2]
            API3[API Instance N]
        end
        
        DB[(Primary DB)]
        DB_R[(Replica DB)]
    end
    
    DEV --> TEST
    TEST --> STG
    STG --> LB
    LB --> API1
    LB --> API2
    LB --> API3
    API1 --> DB
    API2 --> DB_R
    API3 --> DB
```

### 1.2 Deployment Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| Blue-Green | Two identical environments | Zero-downtime updates |
| Canary | Gradual rollout | Test in production |
| Rolling | Incremental updates | Minimal resources |
| Recreate | Stop all, start new | Simple, brief downtime |

## 2. Docker Deployment

### 2.1 Dockerfile

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2.2 Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://cache:6379
      - LOG_LEVEL=INFO
    depends_on:
      - db
      - cache
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    volumes:
      - db_data:/var/lib/postgresql/data
    restart: unless-stopped

  cache:
    image: redis:7-alpine
    restart: unless-stopped

volumes:
  db_data:
```

### 2.3 Docker Commands

```bash
# Build image
docker build -t microservice:latest .

# Run container
docker run -d -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/mydb \
  --name my_service \
  microservice:latest

# View logs
docker logs -f my_service

# Scale service
docker-compose up -d --scale api=3
```

## 3. Proxmox Deployment

### 3.1 VM Configuration

| Resource | Specification |
|----------|---------------|
| CPU | 2-4 cores |
| RAM | 4-8 GB |
| Storage | 40-80 GB SSD |
| Network | Bridged or NAT |

### 3.2 Proxmox LXC Setup

```bash
# Create container
pct create 100 \
  local:vztmpl/debian-12-standard_12.2-1_amd64.tar.zst \
  -rootfs local-lvm:8 \
  -cores 2 \
  -memory 4096 \
  -net0 bridge=vmbr0,name=eth0

# Start container
pct start 100

# Access container
pct exec 100 bash
```

### 3.3 Systemd Service

```ini
[Unit]
Description=My Microservice
After=network.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/myservice
Environment="PATH=/opt/myservice/venv/bin"
Environment="PORT=8000"
ExecStart=/opt/myservice/venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port $PORT
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Install service
sudo cp myservice.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable myservice
sudo systemctl start myservice

# Check status
sudo systemctl status myservice

# View logs
journalctl -u myservice -f
```

## 4. Environment Configuration

### 4.1 Environment Variables

```bash
# .env file (DO NOT COMMIT)
export DATABASE_URL="postgresql://user:password@host:5432/db"
export REDIS_URL="redis://host:6379"
export API_KEY="your-api-key-here"
export JWT_SECRET="your-jwt-secret"
export LOG_LEVEL="INFO"

# Production overrides
export LOG_LEVEL="WARNING"
export DEBUG="false"
```

### 4.2 Configuration Management

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    database_url: str
    
    # Redis
    redis_url: str
    
    # Security
    api_key: str
    jwt_secret: str
    
    # Application
    app_name: str = "microservice"
    debug: bool = False
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
```

## 5. CI/CD Pipeline

### 5.1 GitHub Actions

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest --cov=myservice

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to server
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /opt/myservice
            docker-compose pull
            docker-compose up -d
```

### 5.2 Deployment Script

```bash
#!/bin/bash
# deploy.sh

set -e

# Pull latest changes
git pull origin main

# Build Docker image
docker build -t microservice:latest .

# Run database migrations
docker-compose run api python manage.py migrate

# Restart services
docker-compose up -d --no-deps api

# Health check
sleep 5
curl -f http://localhost:8000/health || exit 1

echo "Deployment successful!"
```

## 6. Monitoring & Observability

### 6.1 Health Checks

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": "microservice",
        "version": "1.0.0"
    }

@app.get("/health/ready")
def readiness_check():
    """Readiness check with dependencies."""
    # Check database
    # Check cache
    # Check external services
    return {"status": "ready"}

@app.get("/health/live")
def liveness_check():
    """Liveness check."""
    return {"status": "alive"}
```

### 6.2 Metrics Export

```python
from prometheus_client import Counter, Histogram, generate_latest

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

@app.get("/metrics")
def metrics():
    """Prometheus metrics endpoint."""
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )
```

### 6.3 Logging

```python
import logging
from loguru import logger

# Configure structured logging
logger.add(
    "logs/{time}.log",
    rotation="1 day",
    retention="30 days",
    level="INFO",
    format="{time} | {level} | {name}:{function}:{line} - {message}"
)

# Add contextual information
logger.configure(
    extra={"service": "microservice", "version": "1.0.0"}
)
```

## 7. Backup & Recovery

### 7.1 Database Backup

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DATABASE_URL="postgresql://user:pass@localhost:5432/mydb"

# Create backup
pg_dump "$DATABASE_URL" > "$BACKUP_DIR/db_$DATE.sql"

# Compress
gzip "$BACKUP_DIR/db_$DATE.sql"

# Keep only last 7 days
find "$BACKUP_DIR" -name "db_*.sql.gz" -mtime +7 -delete

echo "Backup completed: db_$DATE.sql.gz"
```

### 7.2 Restore Procedure

```bash
# Restore from backup
gunzip < backup/db_20240420_120000.sql.gz | psql $DATABASE_URL

# Verify
psql $DATABASE_URL -c "SELECT COUNT(*) FROM users"
```

## 8. Maintenance

### 8.1 Log Rotation

```bash
# /etc/logrotate.d/myservice
/var/log/myservice/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload myservice > /dev/null 2>&1 || true
    endscript
}
```

### 8.2 Database Maintenance

```sql
-- Analyze tables
ANALYZE;

-- Vacuum to reclaim space
VACUUM FULL;

-- Reindex for performance
REINDEX DATABASE mydb;
```

### 8.3 Update Procedure

```bash
# 1. Check current version
docker-compose ps

# 2. Pull latest
docker-compose pull

# 3. Run migrations
docker-compose run api python manage.py migrate

# 4. Restart
docker-compose up -d

# 5. Verify
curl http://localhost:8000/health
```

## 9. Troubleshooting

### 9.1 Common Issues

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| High memory | Check logs, reduce workers | Restart service |
| Slow response | Check metrics | Optimize queries |
| Connection errors | Check network | Restart dependencies |
| 502 Bad Gateway | Check service health | Restart service |

### 9.2 Diagnostic Commands

```bash
# Check service status
systemctl status myservice

# View logs
journalctl -u myservice -n 100 --no-pager

# Check resource usage
docker stats

# Check network
netstat -tulpn | grep LISTEN

# Database connection
psql -c "SELECT 1"

# Redis connection
redis-cli ping
```