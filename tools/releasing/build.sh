#!/bin/bash -e
#
# Build the image
#
set -o pipefail
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
PROJECT_DIR="$(realpath "${SCRIPT_DIR}/../..")"

# Generate a new version
python tools/releasing/version.py
VERSION="$(python "${PROJECT_DIR}/src/website/__version__.py")"

# Build the image
echo "Release: ${VERSION}"
DOCKERFILE="${PROJECT_DIR}/tools/tooling/container/Dockerfile"
TAG="photostream:latest"
TARGET="release"
docker build --file "${DOCKERFILE}" --tag "${TAG}" --target "${TARGET}" "${PROJECT_DIR}"

if [[ -n "${IMAGE_REPOSITORY_USER}" ]]; then
    docker tag "${TAG}" "${IMAGE_REPOSITORY_USER}/photostream:${VERSION}"
else
    echo "[WARNING] IMAGE_REPOSITORY_USER is not set, image can't be pushed without being retagged"; \
fi