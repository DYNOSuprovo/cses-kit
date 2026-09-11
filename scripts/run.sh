#!/usr/bin/env bash
# Compile a CSES solution and run it against every test case in its tests/ dir.
#
# Usage:
#   scripts/run.sh <problem-dir>        # compile + run all tests
#   scripts/run.sh <problem-dir> -i     # compile, then read from stdin (interactive)
#
# A "problem-dir" is a folder containing sol.cpp and a tests/ subfolder with
# matching pairs like tests/1.in and tests/1.out.
set -euo pipefail

# Resolve repo root (this script lives in <root>/scripts).
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ $# -lt 1 ]]; then
  echo "usage: scripts/run.sh <problem-dir> [-i]" >&2
  exit 1
fi

PROB="$1"
MODE="${2:-test}"

SRC="$PROB/sol.cpp"
if [[ ! -f "$SRC" ]]; then
  echo "error: $SRC not found" >&2
  exit 1
fi

BIN="$PROB/sol"

# Colors (fall back to empty strings if not a TTY).
if [[ -t 1 ]]; then
  RED=$'\033[31m'; GRN=$'\033[32m'; YEL=$'\033[33m'; DIM=$'\033[2m'; RST=$'\033[0m'
else
  RED=""; GRN=""; YEL=""; DIM=""; RST=""
fi

echo "${DIM}compiling $SRC ...${RST}"
g++ -std=gnu++17 -O2 -Wall -Wextra -Wshadow \
    -D_GLIBCXX_ASSERTIONS -fsanitize=address,undefined \
    -I "$ROOT/include" "$SRC" -o "$BIN"

# Interactive mode: just run the binary with your keyboard as input.
if [[ "$MODE" == "-i" ]]; then
  echo "${DIM}running (type input, Ctrl-D to end):${RST}"
  "$BIN"
  exit $?
fi

shopt -s nullglob
INPUTS=("$PROB"/tests/*.in)
if [[ ${#INPUTS[@]} -eq 0 ]]; then
  echo "${YEL}no test cases in $PROB/tests/ — running once with no input:${RST}"
  "$BIN" || true
  exit 0
fi

pass=0; fail=0
for in in "${INPUTS[@]}"; do
  name="$(basename "$in" .in)"
  exp="$PROB/tests/$name.out"

  # Time the run (seconds, portable).
  start=$(date +%s.%N)
  got="$("$BIN" < "$in" 2>/tmp/cses_stderr || true)"
  end=$(date +%s.%N)
  ms=$(printf "%.0f" "$(echo "($end - $start) * 1000" | bc)")

  if [[ ! -f "$exp" ]]; then
    echo "${YEL}? $name${RST}  (no expected output; got, ${ms}ms):"
    echo "$got" | sed 's/^/    /'
    continue
  fi

  # Compare ignoring trailing whitespace / trailing blank lines.
  if diff -q <(printf '%s' "$got" | sed -e 's/[[:space:]]*$//') \
             <(printf '%s' "$(cat "$exp")" | sed -e 's/[[:space:]]*$//') >/dev/null; then
    echo "${GRN}✓ $name${RST}  ${DIM}(${ms}ms)${RST}"
    ((pass++)) || true
  else
    echo "${RED}✗ $name${RST}  ${DIM}(${ms}ms)${RST}"
    echo "    ${DIM}--- expected ---${RST}"
    sed 's/^/    /' "$exp"
    echo "    ${DIM}--- got ---${RST}"
    echo "$got" | sed 's/^/    /'
    if [[ -s /tmp/cses_stderr ]]; then
      echo "    ${DIM}--- stderr ---${RST}"
      sed 's/^/    /' /tmp/cses_stderr
    fi
    ((fail++)) || true
  fi
done

echo
echo "${GRN}$pass passed${RST}, ${RED}$fail failed${RST}"
[[ $fail -eq 0 ]]
