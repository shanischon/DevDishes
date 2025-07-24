#!/usr/bin/env bash
set -euo pipefail

# load credentials from docker.env
if [[ ! -f docker.env ]]; then
  echo "ERROR: docker.env not found"
  exit 1
fi
set -a; source docker.env; set +a

# login to Docker Hub
docker login -u "$DOCKERHUB_USERNAME" -p "$DOCKERHUB_TOKEN"

# build & push each microservice
for svc in frontend backend; do
  image_name="devdishes-${svc}"             # yields devdishes-frontend, devdishes-backend
  full_image="${DOCKERHUB_USERNAME}/${image_name}:latest"
  echo "→ Building $svc as $full_image"
  docker build -t "$full_image" "./$svc"
  echo "→ Pushing $full_image"
  docker push "$full_image"
done
