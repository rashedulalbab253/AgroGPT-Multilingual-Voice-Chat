---
description: how to dockerize and push AgroGPT to Docker Hub
---

This workflow guides you through Dockerizing the AgroGPT application and pushing the images to Docker Hub.

### Prerequisites
- Docker and Docker Compose installed
- A Docker Hub account (`rashedulalbab1234`)
- Logged into Docker CLI (`docker login`)

### 1. Build and Tag Images Locally
Run the following commands to build and tag your images using your Docker Hub username.

```bash
# Build & Tag Backend
docker build -t rashedulalbab1234/agrogpt-backend:latest ./backend

# Build & Tag Frontend
docker build -t rashedulalbab1234/agrogpt-frontend:latest ./frontend
```

### 2. Push to Docker Hub
Push the tagged images to your repository.

```bash
docker push rashedulalbab1234/agrogpt-backend:latest
docker push rashedulalbab1234/agrogpt-frontend:latest
```

### 3. CI/CD with GitHub Actions (Optional)
To automate this using GitHub Actions (as `rashedulalbab253`), you can use the `.github/workflows/docker-publish.yml` file.

### 4. Running the Dockerized System
Use the `docker-compose.yml` to run everything together:

```bash
docker-compose up -d
```
