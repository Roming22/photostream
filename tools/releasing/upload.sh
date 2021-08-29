#!/bin/bash -e
#
# Deliver the image by uploading it to the image repository
#
set -o pipefail
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
PROJECT_DIR="$(realpath "${SCRIPT_DIR}/../..")"
VERSION="$(python "${PROJECT_DIR}/src/website/__version__.py")"
IMAGE="${IMAGE_REPOSITORY_USER}/photostream:${VERSION}"
echo "Uploading: ${IMAGE}"

# Make sure that the credentials have been defined
[[ -n "${IMAGE_REPOSITORY_TOKEN}" ]] || { \
    echo "[ERROR] IMAGE_REPOSITORY_TOKEN is not set"; \
    exit 1; \
}
[[ -n "${IMAGE_REPOSITORY_URL}" ]] || { \
    echo "[ERROR] IMAGE_REPOSITORY_URL is not set"; \
    exit 1; \
}
[[ -n "${IMAGE_REPOSITORY_USER}" ]] || { \
    echo "[ERROR] IMAGE_REPOSITORY_USER is not set"; \
    exit 1; \
}

# Do not tag anything that does not come from a release branch or the dev branch
if [[ "${GITHUB_REF}" = refs/heads/release/* || "${GITHUB_REF}" = "refs/heads/dev" ]]; then
    git config --get user.email ||git config --global user.email "cicd@example.com"
    git config --get user.name || git config --global user.name "CI/CD GitHub"
    git tag --annotate "${VERSION}" --message "Automatic release triggered by $(basename "$0")"
    git push --follow-tags
fi

# Upload image only when it comes from a release branch
if [[ "${GITHUB_REF}" = refs/heads/release/* && "${GITHUB_EVENT_NAME}" == "push" ]]; then
    echo "Uploading to ${IMAGE_REPOSITORY_URL}"
    docker login --password "${IMAGE_REPOSITORY_TOKEN}" --username "${IMAGE_REPOSITORY_USER}" "${IMAGE_REPOSITORY_URL}"
    docker push "${IMAGE}"
fi
