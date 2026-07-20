#!/usr/bin/env bash
# Run a browser task via ~/browser-use. Used by the /browser-loop skill
# and can be invoked directly. Output: JSON to stdout, logs to stderr.
set -euo pipefail

cd ~/browser-use
source .venv/bin/activate

TASK="${1:-}"
if [[ -z "$TASK" ]]; then
  echo '{"error":"no task provided"}' >&2
  exit 2
fi

# Pass through any extra flags the user gave
shift || true
python run.py "$TASK" "$@"
