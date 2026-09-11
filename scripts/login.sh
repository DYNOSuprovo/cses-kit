#!/usr/bin/env bash
# Log in to cses.fi and store a session cookie in .cses/cookies.txt (gitignored).
#
# Credentials are read from .env (CSES_NICK / CSES_PASS), then the environment,
# then an interactive prompt.
#
# Usage:
#   scripts/login.sh
#   CSES_NICK=you CSES_PASS='…' scripts/login.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ROOT/scripts/cses.py" login "$@"
