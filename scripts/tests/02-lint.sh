#!/bin/bash
#
# 02-lint.sh - Run code formatting and linting
#
# Usage: ./scripts/tests/02-lint.sh [--fix]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

REPO_ROOT=$(get_repo_root)
cd "$REPO_ROOT"

# Set up log file for this phase
LOG_FILE=$(set_log_file "02-lint")
export CURRENT_LOG_FILE="$LOG_FILE"

FIX_MODE=false
for arg in "$@"; do
    case $arg in
        --fix)
            FIX_MODE=true
            shift
            ;;
    esac
done

print_header "Code Formatting & Linting"
echo "  Log: $LOG_FILE"

if command -v pre-commit &> /dev/null; then
    if [ "$FIX_MODE" = true ]; then
        print_progress "  Running pre-commit with auto-fix..."
        if pre-commit run --all-files >> "$LOG_FILE" 2>&1; then
            printf "\r\033[K"
            print_success "Code formatting and linting passed"
        else
            # pre-commit may have fixed files, run again to verify
            printf "\r\033[K"
            print_progress "  Re-running after fixes..."
            if pre-commit run --all-files >> "$LOG_FILE" 2>&1; then
                printf "\r\033[K"
                print_success "Code formatting and linting passed after fixes"
            else
                printf "\r\033[K"
                print_error "Code formatting or linting still has issues (see log: $LOG_FILE)"
                exit 1
            fi
        fi
    else
        print_progress "  Running pre-commit checks..."
        if pre-commit run --all-files >> "$LOG_FILE" 2>&1; then
            printf "\r\033[K"
            print_success "Code formatting and linting passed"
        else
            printf "\r\033[K"
            print_error "Code formatting or linting failed. Run with --fix or see log: $LOG_FILE"
            exit 1
        fi
    fi
else
    print_error "pre-commit not installed. Install with: pip install pre-commit"
    exit 1
fi

print_success "Linting complete"
