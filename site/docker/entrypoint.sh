#!/usr/bin/env bash
set -euo pipefail

if [[ -n "${POSTGRES_HOST:-}" ]]; then
  echo "Waiting for PostgreSQL at ${POSTGRES_HOST}:${POSTGRES_PORT:-5432}..."
  until pg_isready --host="${POSTGRES_HOST}" --port="${POSTGRES_PORT:-5432}" --username="${POSTGRES_USER:-postgres}" >/dev/null 2>&1; do
    sleep 1
  done
fi

if [[ -n "${SKIP_MIGRATIONS:-}" ]]; then
  echo "Skipping database migrations because SKIP_MIGRATIONS=${SKIP_MIGRATIONS}."
else
  echo "Applying database migrations..."
  python manage.py migrate --noinput
fi

# Ensure calendar cache is populated for past and future years
if [[ -z "${SKIP_CALENDAR_CACHE:-}" ]]; then
  echo "Ensuring calendar cache is populated..."
  python manage.py ensure_calendar_cache
else
  echo "Skipping calendar cache generation because SKIP_CALENDAR_CACHE=${SKIP_CALENDAR_CACHE}."
fi

exec "$@"
