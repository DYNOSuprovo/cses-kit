#!/usr/bin/env bash
# Show solved vs remaining CSES problems per category.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ROOT/scripts/cses.py" status "$@"
