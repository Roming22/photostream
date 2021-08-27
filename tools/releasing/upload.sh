#!/bin/bash -e
#
# Deliver the Python package by uploading it to the package server
#
set -o pipefail
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
PROJECT_DIR="$(realpath "${SCRIPT_DIR}/../..")"
VERSION="$(python "${PROJECT_DIR}/src/website/__version__.py")"

echo "Uploading: ${VERSION}"

# Make sure that the tokens have been defined
[[ -n "${POETRY_PYPI_TOKEN_PYPI}" ]] || { \
    echo "[ERROR] POETRY_PYPI_TOKEN_PYPI is not set"; \
    exit 1; \
}
[[ -n "${POETRY_PYPI_TOKEN_TESTPYPI}" ]] || { \
    echo "[ERROR] POETRY_PYPI_TOKEN_TESTPYPI is not set"; \
    exit 1; 
}

# Do not tag anything that does not come from a release branch or the dev branch
if [[ "${GITHUB_REF}" = refs/heads/release/* || "${GITHUB_REF}" = "refs/heads/dev" ]]; then
    git config --get user.email ||git config --global user.email "cicd@example.com"
    git config --get user.name || git config --global user.name "CI/CD GitHub"
    git tag --annotate "${VERSION}" --message "Automatic release triggered by $(basename "$0")"
    git push --follow-tags
fi

# Upload anything to test.pypi.org
echo; echo "Uploading to test.pypi"
poetry config repositories.testpypi "https://test.pypi.org/simple"
poetry publish -v --repository testpypi

# Upload to pypi.org only when it comes from a release branch
if [[ "${GITHUB_REF}" = refs/heads/release/* && "${GITHUB_EVENT_NAME}" == "push" ]]; then
    echo "Uploading to pypi"
    poetry publish
fi
