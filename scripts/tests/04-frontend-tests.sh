#!/bin/bash
#
# 04-frontend-tests.sh - Run frontend unit tests via Docker
#
# Usage: ./scripts/tests/04-frontend-tests.sh [options]
#
# Options:
#   --file <path>       Run tests from specific file (relative to app/)
#   --test <name>       Run specific test by name pattern
#   --watch             Run in watch mode
#   --update            Update snapshots
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

REPO_ROOT=$(get_repo_root)
cd "$REPO_ROOT"

# Set up log file for this phase
LOG_FILE=$(set_log_file "04-frontend-tests")
export CURRENT_LOG_FILE="$LOG_FILE"

# Default options
TEST_FILE=""
TEST_NAME=""
WATCH_MODE=false
UPDATE_SNAPSHOTS=false
EXTRA_ARGS=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --file)
            TEST_FILE="$2"
            shift 2
            ;;
        --test|-t)
            TEST_NAME="$2"
            shift 2
            ;;
        --watch)
            WATCH_MODE=true
            shift
            ;;
        --update|-u)
            UPDATE_SNAPSHOTS=true
            shift
            ;;
        *)
            EXTRA_ARGS="$EXTRA_ARGS $1"
            shift
            ;;
    esac
done

print_header "Frontend Unit Tests (Vitest via Docker)"
echo "  Log: $LOG_FILE"

ensure_daemon_running || exit 1
detect_compose

# Build vitest command
VITEST_CMD="npm run test:unit --"

if [ "$WATCH_MODE" = false ]; then
    VITEST_CMD="$VITEST_CMD --run"
fi

VITEST_CMD="$VITEST_CMD --reporter=verbose"

if [ "$UPDATE_SNAPSHOTS" = true ]; then
    VITEST_CMD="$VITEST_CMD --update"
fi

if [ -n "$TEST_NAME" ]; then
    VITEST_CMD="$VITEST_CMD -t \"$TEST_NAME\""
fi

if [ -n "$TEST_FILE" ]; then
    VITEST_CMD="$VITEST_CMD $TEST_FILE"
fi

VITEST_CMD="$VITEST_CMD $EXTRA_ARGS"

run_with_progress "Building frontend container" $COMPOSE_CMD build frontend

echo "  Running: $VITEST_CMD" | tee -a "$LOG_FILE"

# Run tests and parse output for progress
echo "" >> "$LOG_FILE"
echo "=== Test Run Started: $(date) ===" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

if $COMPOSE_CMD run --rm frontend bash -c "$VITEST_CMD" 2>&1 | parse_vitest_progress; then
    print_success "Frontend unit tests passed"
else
    print_error "Frontend unit tests failed (see log: $LOG_FILE)"
    exit 1
fi
