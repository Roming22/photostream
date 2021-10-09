#!/bin/bash -e
#
# Build the image
#
set -o pipefail
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
PROJECT_DIR="$(realpath "${SCRIPT_DIR}/../..")"

IMAGE_REPOSITORY_HOST="k3d-registry.localhost"
if ping -c1 -q "$IMAGE_REPOSITORY_HOST" >/dev/null 2>&1; then
    IMAGE_REPOSITORY_USER="${IMAGE_REPOSITORY_HOST}:5000/skwr/web"
fi
VERSION="latest"
DOCKERFILE="${PROJECT_DIR}/tools/tooling/container/Dockerfile"
TAG="photostream:latest"
TARGET="release"

docker build --file "${DOCKERFILE}" --tag "${TAG}" --target "${TARGET}" "${PROJECT_DIR}"

# Print the tag
if [[ -n "${IMAGE_REPOSITORY_USER}" ]]; then
    docker tag "${TAG}" "${IMAGE_REPOSITORY_USER}/photostream:${VERSION}"
    echo "${IMAGE_REPOSITORY_USER}/photostream:${VERSION}"
else
    echo "[WARNING] IMAGE_REPOSITORY_USER is not set, image can't be pushed without being retagged" >&2;
    echo "$TAG"
fi
