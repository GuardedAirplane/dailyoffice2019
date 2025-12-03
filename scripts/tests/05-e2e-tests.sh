#!/bin/bash
#
# 05-e2e-tests.sh - Run E2E tests with Playwright via Docker
#
# Usage: ./scripts/tests/05-e2e-tests.sh [options]
#
# Options:
#   --file <path>       Run tests from specific file (relative to app/)
#   --test <name>       Run specific test by name/grep pattern
#   --project <name>    Run specific project (chromium, firefox, webkit)
#   --headed            Run in headed mode (requires display)
#   --debug             Run in debug mode
#   --ui                Open Playwright UI mode
#   --retries <n>       Number of retries for flaky tests
#   --skip-warmup       Skip backend cache warmup
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

REPO_ROOT=$(get_repo_root)
cd "$REPO_ROOT"

# Set up log file for this phase
LOG_FILE=$(set_log_file "05-e2e-tests")
export CURRENT_LOG_FILE="$LOG_FILE"

# Default options
TEST_FILE=""
TEST_NAME=""
PROJECT=""
HEADED=false
DEBUG=false
UI_MODE=false
RETRIES=""
SKIP_WARMUP=false
EXTRA_ARGS=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --file)
            TEST_FILE="$2"
            shift 2
            ;;
        --test|-g|--grep)
            TEST_NAME="$2"
            shift 2
            ;;
        --project)
            PROJECT="$2"
            shift 2
            ;;
        --headed)
            HEADED=true
            shift
            ;;
        --debug)
            DEBUG=true
            shift
            ;;
        --ui)
            UI_MODE=true
            shift
            ;;
        --retries)
            RETRIES="$2"
            shift 2
            ;;
        --skip-warmup)
            SKIP_WARMUP=true
            shift
            ;;
        *)
            EXTRA_ARGS="$EXTRA_ARGS $1"
            shift
            ;;
    esac
done

print_header "E2E Tests (Playwright via Docker)"
echo "  Log: $LOG_FILE"

ensure_daemon_running || exit 1
detect_compose

# Start backend and frontend if not already running
print_progress "  Starting backend and frontend services..."
if $COMPOSE_CMD up -d backend frontend >> "$LOG_FILE" 2>&1; then
    printf "\r\033[K"
    print_success "Application services started"
else
    printf "\r\033[K"
    print_error "Failed to start application services (see log: $LOG_FILE)"
    exit 1
fi

# Wait for backend to be ready
print_progress "  Waiting for backend to start..."
for i in {1..60}; do
    if curl -s --max-time 5 http://localhost:8000/api/v1/ >> "$LOG_FILE" 2>&1; then
        printf "\r\033[K"
        print_success "Backend is ready"
        break
    fi
    if [ $i -eq 60 ]; then
        printf "\r\033[K"
        print_error "Backend failed to start within 60 seconds"
        exit 1
    fi
    print_progress "  Waiting for backend to start... ($i/60)"
    sleep 1
done

# Warm up caches for E2E tests
if [ "$SKIP_WARMUP" = false ]; then
    print_progress "  Warming up backend caches for E2E tests..."
    
    # Run the warmup_cache management command via Docker
    # First try to load from persistent cache (fast), fall back to full generation
    # Uses verbose mode for debugging, sequential processing for reliability
    if $COMPOSE_CMD run --rm -e POSTGRES_HOST=db -e MEMCACHED_HOST=cache backend \
        python manage.py warmup_cache --load-persistent --verbose 2>&1 | tee -a "$LOG_FILE"; then
        printf "\r\033[K"
        print_success "Backend caches loaded from persistent storage"
    else
        # If persistent load fails, do a full warmup and save to persistent cache
        printf "\r\033[K"
        print_progress "  Generating and caching E2E test data..."
        if $COMPOSE_CMD run --rm -e POSTGRES_HOST=db -e MEMCACHED_HOST=cache backend \
            python manage.py warmup_cache --verbose 2>&1 | tee -a "$LOG_FILE"; then
            printf "\r\033[K"
            print_success "Backend caches warmed up and persisted for E2E tests"
        else
            printf "\r\033[K"
            print_warning "Cache warmup had errors (tests may be slower, see log: $LOG_FILE)"
            # Don't fail - tests can still run, just slower
        fi
    fi
fi

# Wait for frontend
print_progress "  Waiting for frontend..."
for i in {1..30}; do
    if curl -s http://localhost:5173 >> "$LOG_FILE" 2>&1; then
        printf "\r\033[K"
        print_success "Frontend is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        printf "\r\033[K"
        print_error "Frontend failed to start within 30 seconds"
        exit 1
    fi
    sleep 1
done

# Warm up frontend routes to ensure Vite has compiled everything
# This is critical for avoiding cold-start failures on the first browser (Chromium)
if [ "$SKIP_WARMUP" = false ]; then
    print_progress "  Warming up frontend routes..."
    echo "=== Frontend Warmup Started: $(date) ===" >> "$LOG_FILE"
    
    # Key routes that E2E tests access - hit these to warm up the entire stack
    # Include various dates used by tests to ensure API caching
    WARMUP_URLS=(
        # Root and standard offices (most common test date)
        "http://localhost:5173/"
        "http://localhost:5173/office/morning_prayer/2024/01/30"
        "http://localhost:5173/office/evening_prayer/2024/01/30"
        "http://localhost:5173/office/compline/2024/01/30"
        "http://localhost:5173/office/midday_prayer/2024/01/30"
        # Family offices with various test dates
        "http://localhost:5173/family/morning_prayer/2024/01/30"
        "http://localhost:5173/family/morning_prayer/2024/03/15"
        "http://localhost:5173/family/midday_prayer/2024/05/10"
        "http://localhost:5173/family/early_evening_prayer/2024/06/20"
        "http://localhost:5173/family/close_of_day_prayer/2024/07/04"
        # Calendar
        "http://localhost:5173/calendar"
        # Month boundary dates (for date-navigation tests)
        "http://localhost:5173/office/evening_prayer/2024/01/31"
        "http://localhost:5173/office/midday_prayer/2024/02/01"
        # Year boundary dates
        "http://localhost:5173/office/morning_prayer/2024/12/31"
        "http://localhost:5173/office/morning_prayer/2025/01/01"
        # Major feasts dates
        "http://localhost:5173/office/morning_prayer/2024/12/25"
        "http://localhost:5173/office/evening_prayer/2024/05/26"
    )
    
    warmup_failed=0
    for url in "${WARMUP_URLS[@]}"; do
        # Extract just the path for cleaner logging
        path="${url#http://localhost:5173}"
        print_progress "  Warming up: ${path}..."
        if curl -s --max-time 30 "$url" >> "$LOG_FILE" 2>&1; then
            echo "  ✓ Warmed up: $url" >> "$LOG_FILE"
        else
            echo "  ✗ Failed to warm up: $url" >> "$LOG_FILE"
            warmup_failed=1
        fi
    done
    
    printf "\r\033[K"
    if [ $warmup_failed -eq 0 ]; then
        print_success "Frontend routes warmed up"
    else
        print_warning "Some frontend routes failed to warm up (tests may be slower)"
    fi
    
    # Small delay to let any background processing complete
    sleep 2
fi

# Build playwright command
PW_CMD="npx playwright test"

if [ -n "$PROJECT" ]; then
    PW_CMD="$PW_CMD --project=$PROJECT"
fi

if [ "$HEADED" = true ]; then
    PW_CMD="$PW_CMD --headed"
fi

if [ "$DEBUG" = true ]; then
    PW_CMD="$PW_CMD --debug"
fi

if [ "$UI_MODE" = true ]; then
    PW_CMD="$PW_CMD --ui"
fi

if [ -n "$RETRIES" ]; then
    PW_CMD="$PW_CMD --retries=$RETRIES"
fi

if [ -n "$TEST_NAME" ]; then
    PW_CMD="$PW_CMD --grep \"$TEST_NAME\""
fi

if [ -n "$TEST_FILE" ]; then
    PW_CMD="$PW_CMD $TEST_FILE"
fi

PW_CMD="$PW_CMD --reporter=list $EXTRA_ARGS"

echo "  Running: $PW_CMD" | tee -a "$LOG_FILE"

# Run tests and parse output for progress
echo "" >> "$LOG_FILE"
echo "=== Test Run Started: $(date) ===" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

if $COMPOSE_CMD run --rm e2e bash -c "$PW_CMD" 2>&1 | parse_playwright_progress; then
    print_success "E2E tests passed"
else
    print_error "E2E tests failed (see log: $LOG_FILE)"
    echo "  View report: cd app && npm run test:e2e:report"
    exit 1
fi
