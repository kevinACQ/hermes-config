#!/usr/bin/env bash
set -euo pipefail
export PATH="$HOME/.local/bin:$HOME/.bun/bin:$PATH"
export GBRAIN_HOME=/Users/kevin/.hermes

echo "1. GBrain version"
gbrain --version

echo "2. Doctor"
cd /Users/kevin/.hermes/brain
gbrain doctor --json

echo "3. Stats"
gbrain stats

echo "4. Health"
gbrain health

echo "5. Search smoke test"
gbrain search "Kevin working style" >/tmp/gbrain-search-smoke.txt
head -20 /tmp/gbrain-search-smoke.txt

echo "6. Query smoke test"
gbrain query "What does this brain know about Hermes?" || true

echo "7. Hermes MCP list"
hermes mcp list

echo "8. Hermes MCP test"
hermes mcp test gbrain

echo "Done"
