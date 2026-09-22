#!/bin/bash -e
SCRIPT_DIR="$(cd "$(dirname "$0")"; pwd)"
APP_DIR="$(cd "$SCRIPT_DIR/.."; pwd)"
MAIN="$APP_DIR/website/main.py"

# Flat layout puts the package at $APP_DIR/website; the image syncs deps
# without installing the project, so PYTHONPATH is required.
export PYTHONPATH="$APP_DIR${PYTHONPATH:+:$PYTHONPATH}"
exec "$APP_DIR/.venv/bin/python" "$MAIN" "$@"
