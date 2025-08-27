#!/usr/bin/env bash
set -euo pipefail

# Determine the base to diff against (default: origin/main)
BASE_REF="${BASE_REF:-origin/main}"
if ! git rev-parse --verify "$BASE_REF" >/dev/null 2>&1; then
  echo "Fetching $BASE_REF..."
  git fetch origin main:main || true
  BASE_REF="origin/main"
fi

echo "Using BASE_REF=$BASE_REF"
CHANGED_TARGETS=$(./pants --changed-since="$BASE_REF" list :: || true)

echo "Changed targets:"
echo "$CHANGED_TARGETS"

# If nothing changed, still run a quick sanity lint
if [ -z "$CHANGED_TARGETS" ]; then
  echo "No code changes detected. Running lightweight checks."
  ./pants tailor --check update :: || true
  ./pants lint :: 
  exit 0
fi

./pants fmt --changed-since="$BASE_REF" ::
./pants lint --changed-since="$BASE_REF" ::
./pants test --changed-since="$BASE_REF" ::

echo "Done."
