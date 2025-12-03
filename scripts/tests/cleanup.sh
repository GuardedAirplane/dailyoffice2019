#!/bin/bash
#
# cleanup.sh - Stop and clean up Docker services
#
# Usage: ./scripts/tests/cleanup.sh [--volumes]
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

REPO_ROOT=$(get_repo_root)
cd "$REPO_ROOT"

# Set up log file if logging is enabled
if [ -n "$TEST_LOG_DIR" ]; then
    LOG_FILE=$(set_log_file "cleanup")
fi

REMOVE_VOLUMES=false
for arg in "$@"; do
    case $arg in
        --volumes|-v)
            REMOVE_VOLUMES=true
            shift
            ;;
    esac
done

detect_compose || exit 1

print_progress "  Stopping Docker services..."

if [ "$REMOVE_VOLUMES" = true ]; then
    if [ -n "$LOG_FILE" ]; then
        $COMPOSE_CMD down -v >> "$LOG_FILE" 2>&1
    else
        $COMPOSE_CMD down -v > /dev/null 2>&1
    fi
else
    if [ -n "$LOG_FILE" ]; then
        $COMPOSE_CMD down >> "$LOG_FILE" 2>&1
    else
        $COMPOSE_CMD down > /dev/null 2>&1
    fi
fi

printf "\r\033[K"
print_success "Docker services stopped"
