#!/bin/bash
#
# run-tests.sh - Modular test runner for Daily Office 2019
#
# Run all tests or specific test phases.
#
# Usage:
#   ./run-tests.sh                      # Run all tests
#   ./run-tests.sh --phase <phase>      # Run specific phase(s)
#   ./run-tests.sh --python --file <f>  # Run specific Python tests
#   ./run-tests.sh --e2e --test <name>  # Run specific E2E tests
#
# Phases:
#   setup     - Docker environment setup (phase 1)
#   lint      - Code formatting & linting (phase 2)
#   python    - Python unit/integration tests (phase 3)
#   frontend  - Frontend unit tests (phase 4)
#   e2e       - E2E Playwright tests (phase 5)
#   cleanup   - Stop Docker services
#
# Examples:
#   ./run-tests.sh --lint                           # Just run linting
#   ./run-tests.sh --python                         # Just run Python tests
#   ./run-tests.sh --python --file office/tests/test_morning_prayer.py
#   ./run-tests.sh --python --test test_specific_function
#   ./run-tests.sh --python --module office         # Tests for office module only
#   ./run-tests.sh --e2e --test "morning prayer"    # E2E tests matching pattern
#   ./run-tests.sh --e2e --project chromium         # E2E with specific browser
#   ./run-tests.sh --e2e --skip-warmup              # Skip cache warmup (faster but tests may be slower)
#   ./run-tests.sh --no-build                       # Skip rebuilding Docker images
#   ./run-tests.sh --phase setup,python             # Setup + Python tests only
#   ./run-tests.sh --no-cleanup                     # Don't stop Docker after tests
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TESTS_DIR="$SCRIPT_DIR/scripts/tests"

# Source common functions
source "$TESTS_DIR/common.sh"

# Default settings
RUN_ALL=true
RUN_SETUP=false
RUN_LINT=false
RUN_PYTHON=false
RUN_FRONTEND=false
RUN_E2E=false
RUN_CLEANUP=true
NO_BUILD=false

# Pass-through args for specific phases
PYTHON_ARGS=""
FRONTEND_ARGS=""
E2E_ARGS=""
LINT_ARGS=""
SETUP_ARGS=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --phase)
            RUN_ALL=false
            IFS=',' read -ra PHASES <<< "$2"
            for phase in "${PHASES[@]}"; do
                case $phase in
                    setup) RUN_SETUP=true ;;
                    lint) RUN_LINT=true ;;
                    python) RUN_PYTHON=true ;;
                    frontend) RUN_FRONTEND=true ;;
                    e2e) RUN_E2E=true ;;
                    cleanup) ;; # cleanup is handled separately
                    *) print_error "Unknown phase: $phase"; exit 1 ;;
                esac
            done
            shift 2
            ;;
        --setup)
            RUN_ALL=false
            RUN_SETUP=true
            shift
            ;;
        --lint)
            RUN_ALL=false
            RUN_LINT=true
            shift
            ;;
        --python)
            RUN_ALL=false
            RUN_PYTHON=true
            RUN_SETUP=true  # Python tests need Docker
            shift
            ;;
        --frontend)
            RUN_ALL=false
            RUN_FRONTEND=true
            RUN_SETUP=true  # Frontend tests need Docker
            shift
            ;;
        --e2e)
            RUN_ALL=false
            RUN_E2E=true
            RUN_SETUP=true  # E2E tests need Docker
            shift
            ;;
        --no-cleanup)
            RUN_CLEANUP=false
            shift
            ;;
        --no-build)
            NO_BUILD=true
            SETUP_ARGS="$SETUP_ARGS --no-build"
            shift
            ;;
        --cleanup-only)
            RUN_ALL=false
            RUN_CLEANUP=true
            "$TESTS_DIR/cleanup.sh" --volumes
            exit 0
            ;;
        # Pass-through args for specific test runners
        --file)
            if [ "$RUN_PYTHON" = true ]; then
                PYTHON_ARGS="$PYTHON_ARGS --file $2"
            elif [ "$RUN_FRONTEND" = true ]; then
                FRONTEND_ARGS="$FRONTEND_ARGS --file $2"
            elif [ "$RUN_E2E" = true ]; then
                E2E_ARGS="$E2E_ARGS --file $2"
            fi
            shift 2
            ;;
        --test|-k|-t|-g|--grep)
            if [ "$RUN_PYTHON" = true ]; then
                PYTHON_ARGS="$PYTHON_ARGS --test $2"
            elif [ "$RUN_FRONTEND" = true ]; then
                FRONTEND_ARGS="$FRONTEND_ARGS --test $2"
            elif [ "$RUN_E2E" = true ]; then
                E2E_ARGS="$E2E_ARGS --test $2"
            fi
            shift 2
            ;;
        --module|-m)
            PYTHON_ARGS="$PYTHON_ARGS --module $2"
            shift 2
            ;;
        --project)
            E2E_ARGS="$E2E_ARGS --project $2"
            shift 2
            ;;
        --headed)
            E2E_ARGS="$E2E_ARGS --headed"
            shift
            ;;
        --debug)
            E2E_ARGS="$E2E_ARGS --debug"
            shift
            ;;
        --no-cov)
            PYTHON_ARGS="$PYTHON_ARGS --no-cov"
            shift
            ;;
        --verbose|-v)
            PYTHON_ARGS="$PYTHON_ARGS --verbose"
            shift
            ;;
        --last-failed|--lf)
            PYTHON_ARGS="$PYTHON_ARGS --last-failed"
            shift
            ;;
        --fix)
            LINT_ARGS="$LINT_ARGS --fix"
            shift
            ;;
        --skip-warmup)
            E2E_ARGS="$E2E_ARGS --skip-warmup"
            shift
            ;;
        --help|-h)
            head -50 "$0" | tail -n +2 | sed 's/^# //' | sed 's/^#//'
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Cleanup function
cleanup() {
    if [ "$RUN_CLEANUP" = true ]; then
        echo ""
        print_info "Cleaning up Docker services..."
        "$TESTS_DIR/cleanup.sh" --volumes 2>/dev/null || true
    fi
}

# Set trap to cleanup on exit
trap cleanup EXIT INT TERM

REPO_ROOT=$(get_repo_root)
cd "$REPO_ROOT"

# Initialize logging
LOG_DIR=$(init_logging)
export TEST_LOG_DIR="$LOG_DIR"

print_header "Daily Office 2019 Test Runner"
print_info "Logs will be saved to: $LOG_DIR"

FAILED=false

# Run all phases if no specific phases selected
if [ "$RUN_ALL" = true ]; then
    RUN_SETUP=true
    RUN_LINT=true
    RUN_PYTHON=true
    RUN_FRONTEND=true
    RUN_E2E=true
fi

# Phase 1: Docker Setup
if [ "$RUN_SETUP" = true ]; then
    if ! "$TESTS_DIR/01-docker-setup.sh" $SETUP_ARGS; then
        print_error "Docker setup failed"
        exit 1
    fi
fi

# Phase 2: Linting
if [ "$RUN_LINT" = true ]; then
    if ! "$TESTS_DIR/02-lint.sh" $LINT_ARGS; then
        FAILED=true
        if [ "$RUN_ALL" = true ]; then
            print_error "Linting failed - stopping"
            exit 1
        fi
    fi
fi

# Phase 3: Python Tests
if [ "$RUN_PYTHON" = true ]; then
    if ! "$TESTS_DIR/03-python-tests.sh" $PYTHON_ARGS; then
        FAILED=true
        if [ "$RUN_ALL" = true ]; then
            print_error "Python tests failed - stopping"
            exit 1
        fi
    fi
fi

# Phase 4: Frontend Tests
if [ "$RUN_FRONTEND" = true ]; then
    if ! "$TESTS_DIR/04-frontend-tests.sh" $FRONTEND_ARGS; then
        FAILED=true
        if [ "$RUN_ALL" = true ]; then
            print_error "Frontend tests failed - stopping"
            exit 1
        fi
    fi
fi

# Phase 5: E2E Tests
if [ "$RUN_E2E" = true ]; then
    if ! "$TESTS_DIR/05-e2e-tests.sh" $E2E_ARGS; then
        FAILED=true
        if [ "$RUN_ALL" = true ]; then
            print_error "E2E tests failed - stopping"
            exit 1
        fi
    fi
fi

# Summary
echo ""
if [ "$FAILED" = true ]; then
    print_error "Some tests failed"
    echo ""
    print_info "Log files saved to: $LOG_DIR"
    ls -la "$LOG_DIR"/*.log 2>/dev/null | awk '{print "  " $NF}'
    exit 1
else
    print_success "All requested tests passed!"
    
    if [ "$RUN_ALL" = true ]; then
        echo ""
        echo "Tests completed:"
        echo "  ✓ Docker environment setup"
        echo "  ✓ Code formatting and linting"
        echo "  ✓ Python unit and integration tests"
        echo "  ✓ Frontend unit tests"
        echo "  ✓ E2E tests (Playwright)"
    fi
    
    echo ""
    print_info "Log files saved to: $LOG_DIR"
    ls -la "$LOG_DIR"/*.log 2>/dev/null | awk '{print "  " $NF}'
fi
