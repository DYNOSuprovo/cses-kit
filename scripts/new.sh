#!/usr/bin/env bash
# Scaffold a new CSES problem folder from the template.
#
# Usage:
#   scripts/new.sh <category> <slug> [cses-url]
#   scripts/new.sh introductory weird-algorithm
#   scripts/new.sh introductory missing-number https://cses.fi/problemset/task/1083
#
# Creates problems/<category>/<slug>/ with:
#   sol.cpp         (copy of template.cpp)
#   statement.md    (auto-filled from the URL, or a blank template)
#   tests/*.in/.out (auto-fetched sample cases if a URL is given)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ $# -lt 2 ]]; then
  echo "usage: scripts/new.sh <category> <slug> [cses-url]" >&2
  echo "example: scripts/new.sh introductory missing-number https://cses.fi/problemset/task/1083" >&2
  exit 1
fi

CAT="$1"
SLUG="$2"
URL="${3:-}"
DIR="$ROOT/problems/$CAT/$SLUG"

if [[ -d "$DIR" ]]; then
  echo "error: $DIR already exists" >&2
  exit 1
fi

mkdir -p "$DIR/tests"
cp "$ROOT/template.cpp" "$DIR/sol.cpp"

if [[ -n "$URL" ]]; then
  # Auto-fetch statement + sample tests from CSES.
  if python3 "$ROOT/scripts/fetch.py" "$URL" "$DIR"; then
    :
  else
    echo "warning: fetch failed — falling back to a blank statement" >&2
    URL=""  # trigger the blank-template branch below
  fi
fi

if [[ -z "$URL" ]]; then
  cat > "$DIR/statement.md" <<EOF
# $SLUG

<!-- Paste the CSES problem statement here (link + task + constraints). -->

**Link:**

## Task

## Input

## Output

## Constraints

## Example
EOF
  # Seed one empty test-case pair so run.sh has something to diff.
  : > "$DIR/tests/1.in"
  : > "$DIR/tests/1.out"
fi

echo
echo "created $DIR"
echo "  edit    $DIR/statement.md"
echo "  code    $DIR/sol.cpp"
echo "  tests   $DIR/tests/"
echo
echo "run with:  scripts/run.sh problems/$CAT/$SLUG"
