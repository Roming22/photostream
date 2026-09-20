#!/bin/bash -e
#
# Deliver the image by uploading it to the image repository
#
set -o pipefail
set -x

SCRIPT_DIR="$(dirname "$(realpath "$0")")"
PROJECT_DIR="$(realpath "${SCRIPT_DIR}/../..")"

# Upload the localdev image to the local registry
if [[ -z "${IMAGE_REPOSITORY_USER}" ]]; then
    IMAGE_REPOSITORY="k3d-registry.localhost"
    if ping -c1 -q "$IMAGE_REPOSITORY" >/dev/null 2>&1; then
        IMAGE="${IMAGE_REPOSITORY}:5000/skwr/web/photostream:localdev"
        echo "Uploading: ${IMAGE}"
        docker push "$IMAGE"
        echo "Done"
        exit 0
    else
        echo "[ERROR] $IMAGE_REPOSITORY is not reachable"
        exit 1
    fi
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

# Get the version
python tools/releasing/version.py
VERSION="$(python "${PROJECT_DIR}/src/website/__version__.py")"
IMAGE_REPOSITORY_USER="${IMAGE_REPOSITORY_USER,,}"
IMAGE="${IMAGE_REPOSITORY_URL}/${IMAGE_REPOSITORY_USER}/photostream:${VERSION}"

# Collect all destination tags; release branches also get `:latest`
TAGS=("${IMAGE}")
case "${GITHUB_REF}" in
    refs/heads/release/*)
        # Tag the release branch with the version
        echo "Tagging ${GITHUB_REF} as ${VERSION}"
        git config --get user.email || git config --global user.email "cicd@example.com"
        git config --get user.name || git config --global user.name "CI/CD GitHub"
        git tag --annotate "${VERSION}" --message "Automatic release triggered by $(basename "$0")"
        git push --follow-tags

        # Add the tags to the build arguments and the list of tags
        TAGS+=("${IMAGE_REPOSITORY_URL}/${IMAGE_REPOSITORY_USER}/photostream:latest")
        ;;
    refs/heads/dev)
        TAGS+=("${IMAGE_REPOSITORY_URL}/${IMAGE_REPOSITORY_USER}/photostream:unstable")
        ;;
esac
TAG_ARGS=()
for tag in "${TAGS[@]}"; do
    TAG_ARGS+=("--tag" "${tag}")
done

# QEMU and buildx are set up by docker/setup-qemu-action and docker/setup-buildx-action
# in the workflow. Login is handled by docker/login-action.

# Build once, push all tags in a single invocation
DOCKERFILE="${PROJECT_DIR}/tools/tooling/container/Dockerfile"
PLATFORM="linux/arm64/v8,linux/amd64"
TARGET="release"
CACHE_REF="${IMAGE_REPOSITORY_URL}/${IMAGE_REPOSITORY_USER}/photostream:buildcache"
echo "Building and uploading '${IMAGE}' for platforms '${PLATFORM}'"
docker buildx build \
    --file "${DOCKERFILE}" \
    --platform "${PLATFORM}" \
    --target "${TARGET}" \
    --cache-from "type=registry,ref=${CACHE_REF}" \
    --cache-to "type=registry,ref=${CACHE_REF},mode=max" \
    --push \
    "${TAG_ARGS[@]}" \
    "${PROJECT_DIR}"
echo "Image pushed to '${TAGS[*]}'"
echo "Done"
