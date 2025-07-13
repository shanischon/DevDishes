# DevDishes - Modern Architecture

## Structure
- `frontend/`: React SPA frontend
- `backend/`: Flask API for recipes
- `db/`: PostgreSQL database (Kubernetes managed)
- `devops/`: Kubernetes manifests and Helm chart

## How to Use

### Frontend
- Place your frontend code in the `frontend/` folder.
- Build Docker image:
  ```sh
  docker build -t frontend:latest ./frontend
  ```
- Deploy to Kubernetes:
  ```sh
  kubectl apply -f devops/frontend/frontend.deployment.yaml
  kubectl apply -f devops/frontend/frontend.service.yaml
  # Or use Helm for the full stack
  ```

### Backend
- Flask app receives recipes as JSON and stores them in PostgreSQL.
- Build Docker image:
  ```sh
  docker build -t backend:latest ./backend
  ```
- Deploy to Kubernetes:
  ```sh
  kubectl apply -f devops/backend/backend.deployment.yaml
  kubectl apply -f devops/backend/backend.service.yaml
  # Or use Helm for the full stack
  ```

### Database (PostgreSQL)
- PostgreSQL runs in a container with a persistent volume claim.
- The database password is stored in a Kubernetes Secret (`postgres-secret`).
- Deploy to Kubernetes:
  ```sh
  kubectl apply -f devops/db/postgres.secret.yaml
  kubectl apply -f devops/db/postgres.pvc.yaml
  kubectl apply -f devops/db/postgres.deployment.yaml
  kubectl apply -f devops/db/postgres.service.yaml
  # Or use Helm for the full stack
  ```

### DevOps & CI/CD
- CI/CD is managed with GitHub Actions (`.github/workflows/ci-cd.yaml`).
- On each push/PR:
  - Only changed microservices are built, tested, versioned, and deployed.
  - Docker images are tagged with the microservice version and pushed to Docker Hub.
  - Helm is used to deploy the stack to Kubernetes, using image tags and secrets.
- Sensitive data (DB password, registry credentials, kubeconfig) is managed with GitHub and Kubernetes Secrets.

## Notes
- The backend and db services are internal (ClusterIP), frontend is exposed via LoadBalancer.
- Make sure to update image names/tags as needed for your registry.
- For local development, Docker Desktop's Kubernetes will use local disk for PVCs. In the cloud, the default StorageClass will be used. 