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
  543```sh
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

## Ingress & TLS (HTTPS)
- The frontend is exposed externally via Kubernetes Ingress, secured with TLS (HTTPS).
- A self-signed certificate is used for development/testing:
  1. Generate a self-signed cert for `devdishes.com`:
     ```sh
     openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
       -keyout tls.key -out tls.crt \
       -subj "/CN=devdishes.com/O=DevDishes"
     base64 < tls.crt | tr -d '\n' > tls.crt.b64
     base64 < tls.key | tr -d '\n' > tls.key.b64
     ```
  2. Copy the contents of `tls.crt.b64` and `tls.key.b64` into `devops/frontend/devdishes-tls.secret.yaml` under `tls.crt:` and `tls.key:`.
  3. The Ingress manifest (`devops/frontend/frontend.ingress.yaml`) is preconfigured for `devdishes.com` and references the TLS secret.
  4. For local testing, add `127.0.0.1 devdishes.com` to your `/etc/hosts` file.

## Recipe Format
- Recipes are public and require only:
  - `name` (string, required)
  - `content` (string, required)
  - `image` (string, optional, base64 or URL)
- Example JSON for POST `/recipes`:
  ```json
  {
    "name": "Pancake",
    "content": "Mix flour, eggs, milk... Fry on pan...",
    "image": "data:image/png;base64,iVBORw0KGgo..." // optional
  }
  ```

## Notes
- The backend and db services are internal (ClusterIP), frontend is exposed via Ingress with TLS (not LoadBalancer).
- Make sure to update image names/tags as needed for your registry.
- For local development, Docker Desktop's Kubernetes will use local disk for PVCs. In the cloud, the default StorageClass will be used. 