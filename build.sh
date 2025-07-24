#!/usr/bin/env bash
set -euo pipefail

# load credentials
if [[ -f docker.env ]]; then
  # export every VAR=VAL line
  set -a
  source docker.env
  set +a
else
  echo "ERROR: docker.env not found"
  exit 1
fi

# rest of script...
docker login -u "$DOCKERHUB_USERNAME" -p "$DOCKERHUB_TOKEN"
services=(frontend backend)
for svc in "${services[@]}"; do
  image="${DOCKERHUB_USERNAME}/${svc}:latest"
  docker build -t "$image" "./$svc"
  docker push "$image"
done
