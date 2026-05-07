#!/usr/bin/env bash
set -euo pipefail
export PATH="$HOME/.bun/bin:$PATH"
export GBRAIN_HOME="/Users/kevin/.hermes"
cd /Users/kevin/.hermes/brain
exec /Users/kevin/.bun/bin/gbrain serve
