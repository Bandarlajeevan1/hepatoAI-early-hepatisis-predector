# Docker Deployment Guide

## **Prerequisites**

1. Docker Desktop installed: https://www.docker.com/products/docker-desktop
2. Docker Compose included with Docker Desktop

---

## **Step 1: Build Docker Images**

```powershell
cd "C:\new major\hepatitis-detection"

# Build images
docker compose build
```

---

## **Step 2: Update Environment Variables**

Create or update `docker-compose.yml` with production settings:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      FLASK_ENV: production
      FLASK_DEBUG: False
      MONGO_URI: mongodb+srv://jeevanbandarla1234_db_user:Jeevan12@cluster0.eg83ljt.mongodb.net/hepatitis_db?appName=Cluster0&retryWrites=true&w=majority
      SECRET_KEY: your-secure-secret-key-here
      JWT_SECRET: your-jwt-secret-here
    ports:
      - "5000:5000"

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      REACT_APP_API_URL: http://localhost:5000
    ports:
      - "3000:3000"
```

---

## **Step 3: Start Services**

```powershell
# Start all services in background
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f backend
docker compose logs -f frontend
```

---

## **Step 4: Access Application**

- Frontend: **http://localhost:3000**
- Backend: **http://localhost:5000**
- API Docs: **http://localhost:5000/apidocs**

---

## **Step 5: Deploy to Docker Registry**

### **Push to Docker Hub**

```powershell
# Login to Docker Hub
docker login

# Tag images
docker tag hepatitis-detection-backend your-username/hepatitis-backend:latest
docker tag hepatitis-detection-frontend your-username/hepatitis-frontend:latest

# Push images
docker push your-username/hepatitis-backend:latest
docker push your-username/hepatitis-frontend:latest
```

### **Deploy with Updated Images**

```powershell
# Update docker-compose.yml to use your images
# Then pull and run on production server:

docker compose pull
docker compose up -d
```

---

## **Step 6: Production Checklist**

- [ ] Change `FLASK_DEBUG=False`
- [ ] Update `SECRET_KEY` to random 32+ char string
- [ ] Update `JWT_SECRET`
- [ ] Verify `MONGO_URI` is correct
- [ ] Configure reverse proxy (Nginx)
- [ ] Set up SSL/TLS certificates
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Configure backups

---

## **Useful Commands**

```powershell
# Stop all services
docker compose down

# Remove all containers and volumes
docker compose down -v

# Rebuild images
docker compose build --no-cache

# Scale services
docker compose up -d --scale backend=2

# View container logs
docker logs container-name

# Execute command in container
docker exec container-name ls -la

# Remove unused images
docker image prune
```

