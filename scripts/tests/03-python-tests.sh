#!/bin/bash
#
# 03-python-tests.sh - Run Python unit and integration tests via Docker
#
# Usage: ./scripts/tests/03-python-tests.sh [options]
#
# Options:
#   --file <path>       Run tests from specific file (relative to site/)
#   --test <name>       Run specific test by name pattern
#   --module <name>     Run tests from specific module (office, churchcal, bible, psalter)
#   --no-cov            Disable coverage reporting
#   --verbose           More verbose output
#   --last-failed       Only run tests that failed last time
#   -x                  Stop on first failure (default)
#   --no-fail-fast      Don't stop on first failure
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

REPO_ROOT=$(get_repo_root)
cd "$REPO_ROOT"

# Set up log file for this phase
LOG_FILE=$(set_log_file "03-python-tests")
export CURRENT_LOG_FILE="$LOG_FILE"

# Default options
TEST_FILE=""
TEST_NAME=""
TEST_MODULE=""
NO_COV=false
VERBOSE=false
LAST_FAILED=false
FAIL_FAST=true
EXTRA_ARGS=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --file)
            TEST_FILE="$2"
            shift 2
            ;;
        --test|-k)
            TEST_NAME="$2"
            shift 2
            ;;
        --module|-m)
            TEST_MODULE="$2"
            shift 2
            ;;
        --no-cov)
            NO_COV=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --last-failed|--lf)
            LAST_FAILED=true
            shift
            ;;
        -x)
            FAIL_FAST=true
            shift
            ;;
        --no-fail-fast)
            FAIL_FAST=false
            shift
            ;;
        *)
            EXTRA_ARGS="$EXTRA_ARGS $1"
            shift
            ;;
    esac
done

print_header "Python Tests (pytest via Docker)"
echo "  Log: $LOG_FILE"

ensure_daemon_running || exit 1
detect_compose

# Build pytest command
PYTEST_CMD="pytest"

if [ "$VERBOSE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD --verbose -vv"
else
    PYTEST_CMD="$PYTEST_CMD --verbose"
fi

# Add parallel execution
PYTEST_CMD="$PYTEST_CMD -n auto"

# Add coverage unless disabled
if [ "$NO_COV" = false ]; then
    PYTEST_CMD="$PYTEST_CMD --cov=office --cov=churchcal --cov=bible --cov=psalter --cov-report=term-missing --cov-fail-under=0"
fi

# Add fail fast
if [ "$FAIL_FAST" = true ]; then
    PYTEST_CMD="$PYTEST_CMD -x"
fi

# Add last failed
if [ "$LAST_FAILED" = true ]; then
    PYTEST_CMD="$PYTEST_CMD --lf"
fi

# Add test name filter
if [ -n "$TEST_NAME" ]; then
    PYTEST_CMD="$PYTEST_CMD -k \"$TEST_NAME\""
fi

# Add specific file or module
if [ -n "$TEST_FILE" ]; then
    PYTEST_CMD="$PYTEST_CMD $TEST_FILE"
elif [ -n "$TEST_MODULE" ]; then
    case $TEST_MODULE in
        office|churchcal|bible|psalter)
            PYTEST_CMD="$PYTEST_CMD $TEST_MODULE/"
            ;;
        *)
            print_error "Unknown module: $TEST_MODULE. Use: office, churchcal, bible, or psalter"
            exit 1
            ;;
    esac
fi

# Add extra args
PYTEST_CMD="$PYTEST_CMD $EXTRA_ARGS"

run_with_progress "Building backend container" $COMPOSE_CMD build backend

echo "  Running: $PYTEST_CMD" | tee -a "$LOG_FILE"

# Run tests and parse output for progress
echo "" >> "$LOG_FILE"
echo "=== Test Run Started: $(date) ===" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

if $COMPOSE_CMD run --rm -e POSTGRES_HOST=db -e MEMCACHED_HOST=cache -e SKIP_CALENDAR_CACHE=1 backend \
    bash -c "$PYTEST_CMD" 2>&1 | parse_pytest_progress; then
    print_success "Python tests passed"
else
    print_error "Python tests failed (see log: $LOG_FILE)"
    exit 1
fi
