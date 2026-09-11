#!/usr/bin/env bash
# Submit sol.cpp for a problem to CSES and poll until the verdict is ready.
#
# Usage:
#   scripts/submit.sh problems/introductory/missing-number
#   scripts/submit.sh problems/introductory/missing-number/sol.cpp
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ $# -lt 1 ]]; then
  echo "usage: scripts/submit.sh <problem-dir>" >&2
  exit 1
fi
exec python3 "$ROOT/scripts/cses.py" submit "$@"
