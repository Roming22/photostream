#!/bin/bash -e
#
# Deliver the image by uploading it to the image repository
#
set -o pipefail
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
PROJECT_DIR="$(realpath "${SCRIPT_DIR}/../..")"
python tools/releasing/version.py
VERSION="$(python "${PROJECT_DIR}/src/website/__version__.py")"

if [[ -z "${IMAGE_REPOSITORY_USER}" ]]; then
    IMAGE_REPOSITORY="k3d-registry.localhost"
    if ping -c1 -q "$IMAGE_REPOSITORY" >/dev/null 2>&1; then
        IMAGE="${IMAGE_REPOSITORY}:5000/skwr/web/photostream:latest"
        echo "Uploading: ${IMAGE}"
        docker push "$IMAGE"
        exit 0
    else
        echo "[ERROR] IMAGE_REPOSITORY_USER is not set"
        exit 1
    fi
else
    IMAGE="${IMAGE_REPOSITORY_USER}/photostream:${VERSION}"
fi

# Make sure that the credentials have been defined
[[ -n "${IMAGE_REPOSITORY_TOKEN}" ]] || { \
    echo "[ERROR] IMAGE_REPOSITORY_TOKEN is not set"; \
    exit 1; \
}
[[ -n "${IMAGE_REPOSITORY_URL}" ]] || { \
    echo "[ERROR] IMAGE_REPOSITORY_URL is not set"; \
    exit 1; \
}

# Do not tag anything that does not come from a release branch or the dev branch
if [[ "${GITHUB_REF}" = refs/heads/release/* || "${GITHUB_REF}" = "refs/heads/dev" ]]; then
    echo "Tagging ${GITHUB_REF} as ${VERSION}"
    git config --get user.email ||git config --global user.email "cicd@example.com"
    git config --get user.name || git config --global user.name "CI/CD GitHub"
    git tag --annotate "${VERSION}" --message "Automatic release triggered by $(basename "$0")"
    git push --follow-tags
fi

# Upload image only when it comes from a release branch
if [[ "${GITHUB_REF}" = refs/heads/release/* && "${GITHUB_EVENT_NAME}" == "push" ]]; then
    echo "Building and uploading ${IMAGE}"

    # Not sure why that bit is needed, but multi-arch build is failing if it's not there.
    docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

    if docker buildx inspect builder >/dev/null; then
        docker buildx rm builder
    fi
    docker buildx create --name builder --driver docker-container --use

    # Build the image
    DOCKERFILE="${PROJECT_DIR}/tools/tooling/container/Dockerfile"
    PLATFORM="linux/arm64/v8,linux/amd64"
    TARGET="release"
    docker login --password "${IMAGE_REPOSITORY_TOKEN}" --username "${IMAGE_REPOSITORY_USER}" "${IMAGE_REPOSITORY_URL}"
    for TAG in ${IMAGE} "${IMAGE_REPOSITORY_USER}/photostream:latest"; do
        docker buildx build --file "${DOCKERFILE}" --platform "${PLATFORM}" --push --tag "${TAG}" --target "${TARGET}" "${PROJECT_DIR}"
    done
    echo "Uploaded ${TAG}"
fi
