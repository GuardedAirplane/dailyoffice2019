#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d node_modules || -z "$(ls -A node_modules 2>/dev/null)" ]]; then
  echo "Installing frontend dependencies..."
  npm install
fi

exec "$@"
