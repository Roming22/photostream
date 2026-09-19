#!/bin/bash -e
SCRIPT_DIR="$(cd "$(dirname "$0")"; pwd)"
uv run "$SCRIPT_DIR/../website/main.py" "$@"