#!/usr/bin/env bash
# Scaffold every CSES problem into problems/<category>/<slug>/.
#
# Usage:
#   scripts/sync.sh
#   scripts/sync.sh --category introductory
#   scripts/sync.sh --dry-run
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ROOT/scripts/cses.py" sync "$@"
