#!/usr/bin/env bash
# Connector wrapper for Hermes Desktop -> Retell outbound Hermes voice call.
# Keeps credentials in the existing voice-onboarding project .env and avoids
# requiring broad macOS Documents/Desktop permissions.
set -euo pipefail

PROJECT_DIR="/Users/kevin/projects/voice-onboarding-mvp"
PYTHON="/Users/kevin/.hermes/hermes-agent/venv/bin/python"

cd "$PROJECT_DIR"
set -a
source "$PROJECT_DIR/.env"
set +a

exec "$PYTHON" "$PROJECT_DIR/hermes-v3/memory_bridge.py" --call
