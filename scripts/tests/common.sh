#!/bin/bash
#
# common.sh - Shared functions and variables for test scripts
#

# Color codes
export RED='\033[0;31m'
export GREEN='\033[0;32m'
export YELLOW='\033[1;33m'
export BLUE='\033[0;34m'
export CYAN='\033[0;36m'
export NC='\033[0m'

# Logging configuration
export LOG_DIR=""
export CURRENT_LOG_FILE=""

# Initialize logging directory
init_logging() {
    local repo_root
    repo_root=$(get_repo_root)
    LOG_DIR="$repo_root/test-logs/$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$LOG_DIR"
    export LOG_DIR
    echo "$LOG_DIR"
}

# Get or create log directory
get_log_dir() {
    if [ -z "$LOG_DIR" ]; then
        # Check if LOG_DIR was passed as environment variable
        if [ -n "$TEST_LOG_DIR" ]; then
            LOG_DIR="$TEST_LOG_DIR"
        else
            LOG_DIR=$(init_logging)
        fi
    fi
    echo "$LOG_DIR"
}

# Set log file for current phase
set_log_file() {
    local phase_name="$1"
    CURRENT_LOG_FILE="$(get_log_dir)/${phase_name}.log"
    export CURRENT_LOG_FILE
    echo "$CURRENT_LOG_FILE"
}

# Log to file (used internally)
log_to_file() {
    if [ -n "$CURRENT_LOG_FILE" ]; then
        cat >> "$CURRENT_LOG_FILE"
    else
        cat > /dev/null
    fi
}

# Progress display helpers
# Clear line and print progress
print_progress() {
    printf "\r\033[K%s" "$1"
}

# Print progress with counts
print_test_progress() {
    local passed=$1
    local failed=$2
    local skipped=$3
    local total=$4
    local current_test=$5
    
    local status=""
    if [ "$failed" -gt 0 ] && [ "$skipped" -gt 0 ]; then
        status="\033[0;32m${passed}P\033[0m \033[0;31m${failed}F\033[0m \033[0;33m${skipped}S\033[0m"
    elif [ "$failed" -gt 0 ]; then
        status="\033[0;32m${passed}P\033[0m \033[0;31m${failed}F\033[0m"
    elif [ "$skipped" -gt 0 ]; then
        status="\033[0;32m${passed}P\033[0m \033[0;33m${skipped}S\033[0m"
    else
        status="\033[0;32m${passed}P\033[0m"
    fi
    
    if [ -n "$total" ] && [ "$total" -gt 0 ]; then
        printf "\r\033[K  [${status} / %d] %s" "$total" "$current_test"
    else
        printf "\r\033[K  [${status}] %s" "$current_test"
    fi
}

# Finalize progress line (move to new line)
finish_progress() {
    echo ""
}

# Parse pytest output for progress
# Usage: command | parse_pytest_progress
parse_pytest_progress() {
    local passed=0
    local failed=0
    local errors=0
    local current_test=""
    local log_file="${CURRENT_LOG_FILE:-/dev/null}"
    
    while IFS= read -r line; do
        # Log full line to file
        echo "$line" >> "$log_file"
        
        # Parse test results
        if [[ "$line" =~ PASSED ]]; then
            ((passed++))
            current_test=$(echo "$line" | sed 's/ PASSED.*//' | sed 's/.*:://')
            print_test_progress $passed $failed 0 0 "${current_test:0:60}"
        elif [[ "$line" =~ FAILED ]]; then
            ((failed++))
            current_test=$(echo "$line" | sed 's/ FAILED.*//' | sed 's/.*:://')
            print_test_progress $passed $failed 0 0 "${current_test:0:60}"
        elif [[ "$line" =~ ERROR ]]; then
            ((errors++))
            print_test_progress $passed $((failed + errors)) 0 0 "ERROR"
        elif [[ "$line" =~ ^"collected" ]]; then
            # Show collection info
            print_progress "  Collecting tests... $line"
        fi
    done
    
    finish_progress
    if [ $failed -gt 0 ]; then
        echo -e "  Total: ${GREEN}${passed} passed${NC}, ${RED}${failed} failed${NC}"
    else
        echo -e "  Total: ${GREEN}${passed} passed${NC}"
    fi
    
    # Return failure if any tests failed
    [ $failed -eq 0 ] && [ $errors -eq 0 ]
}

# Parse vitest output for progress
parse_vitest_progress() {
    local passed=0
    local failed=0
    local current_test=""
    local log_file="${CURRENT_LOG_FILE:-/dev/null}"
    
    while IFS= read -r line; do
        # Log full line to file
        echo "$line" >> "$log_file"
        
        # Parse test results (vitest format: ✓ or ✗)
        if [[ "$line" =~ ^[[:space:]]*✓ ]] || [[ "$line" =~ PASS ]]; then
            ((passed++))
            current_test=$(echo "$line" | sed 's/.*✓//' | sed 's/.*PASS//' | xargs)
            print_test_progress $passed $failed 0 0 "${current_test:0:60}"
        elif [[ "$line" =~ ^[[:space:]]*✗ ]] || [[ "$line" =~ FAIL ]]; then
            ((failed++))
            current_test=$(echo "$line" | sed 's/.*✗//' | sed 's/.*FAIL//' | xargs)
            print_test_progress $passed $failed 0 0 "${current_test:0:60}"
        fi
    done
    
    finish_progress
    if [ $failed -gt 0 ]; then
        echo -e "  Total: ${GREEN}${passed} passed${NC}, ${RED}${failed} failed${NC}"
    else
        echo -e "  Total: ${GREEN}${passed} passed${NC}"
    fi
    
    [ $failed -eq 0 ]
}

# Parse playwright output for progress
parse_playwright_progress() {
    local passed=0
    local failed=0
    local skipped=0
    local flaky=0
    local total=0
    local current_test=""
    local log_file="${CURRENT_LOG_FILE:-/dev/null}"
    local test_run_started=false
    local final_passed=0
    local final_failed=0
    local final_skipped=0
    local final_flaky=0
    local found_summary=false
    
    while IFS= read -r line; do
        # Log full line to file
        echo "$line" >> "$log_file"
        
        # Parse test count (e.g., "Running 45 tests using 4 workers")
        if [[ "$line" =~ Running[[:space:]]([0-9]+)[[:space:]]tests ]]; then
            total="${BASH_REMATCH[1]}"
            test_run_started=true
            print_progress "  Running $total tests..."
        fi
        
        # Parse Playwright's final summary line (e.g., "  7 flaky", "  30 skipped", "  258 passed")
        # These appear at the end of the test run and represent the actual final results
        if [[ "$line" =~ ^[[:space:]]*([0-9]+)[[:space:]]passed ]]; then
            final_passed="${BASH_REMATCH[1]}"
            found_summary=true
        fi
        if [[ "$line" =~ ^[[:space:]]*([0-9]+)[[:space:]]failed ]]; then
            final_failed="${BASH_REMATCH[1]}"
            found_summary=true
        fi
        if [[ "$line" =~ ^[[:space:]]*([0-9]+)[[:space:]]skipped ]]; then
            final_skipped="${BASH_REMATCH[1]}"
            found_summary=true
        fi
        if [[ "$line" =~ ^[[:space:]]*([0-9]+)[[:space:]]flaky ]]; then
            final_flaky="${BASH_REMATCH[1]}"
            found_summary=true
        fi
        
        # Only parse test results after test run has started
        # This avoids counting ✓ from warmup cache output
        if [ "$test_run_started" = true ]; then
            # Parse individual test results - match lines starting with "  ✓  N", "  ✘  N", or "  -  N"
            # The format is: "  ✓  123 [browser] › file.spec.ts:line:col › test name"
            if [[ "$line" =~ ^[[:space:]]*✓[[:space:]]+[0-9]+ ]]; then
                ((passed++))
                current_test=$(echo "$line" | sed 's/.*\] //' | head -c 60)
                print_test_progress $passed $failed $skipped $total "${current_test}"
            elif [[ "$line" =~ ^[[:space:]]*✘[[:space:]]+[0-9]+ ]]; then
                ((failed++))
                current_test=$(echo "$line" | sed 's/.*\] //' | head -c 60)
                print_test_progress $passed $failed $skipped $total "${current_test}"
            elif [[ "$line" =~ ^[[:space:]]*-[[:space:]]+[0-9]+ ]]; then
                ((skipped++))
                current_test=$(echo "$line" | sed 's/.*\] //' | head -c 60)
                print_test_progress $passed $failed $skipped $total "${current_test}"
            elif [[ "$line" =~ ^\[[0-9]+/[0-9]+\] ]]; then
                # Playwright progress format: [1/45] 
                current_test=$(echo "$line" | sed 's/^\[[0-9]*\/[0-9]*\] //' | head -c 60)
                print_test_progress $passed $failed $skipped $total "${current_test}"
            fi
        fi
    done
    
    finish_progress
    
    # Use final summary counts if found, otherwise use running counts
    if [ "$found_summary" = true ]; then
        passed=$final_passed
        failed=$final_failed
        skipped=$final_skipped
        flaky=$final_flaky
    fi
    
    # Build summary string with all non-zero counts
    local summary="${GREEN}${passed} passed${NC}"
    if [ $flaky -gt 0 ]; then
        summary="${summary}, ${YELLOW}${flaky} flaky${NC}"
    fi
    if [ $failed -gt 0 ]; then
        summary="${summary}, ${RED}${failed} failed${NC}"
    fi
    if [ $skipped -gt 0 ]; then
        summary="${summary}, ${YELLOW}${skipped} skipped${NC}"
    fi
    echo -e "  Total: ${summary}"
    
    # Only fail if there are actual failures (flaky tests that passed on retry are OK)
    [ $failed -eq 0 ]
}

# Simple log wrapper - logs to file, shows minimal output
run_with_progress() {
    local description="$1"
    shift
    
    # Use CURRENT_LOG_FILE if set, otherwise /dev/null
    local log_file="${CURRENT_LOG_FILE:-/dev/null}"
    
    print_progress "  $description..."
    
    if "$@" >> "$log_file" 2>&1; then
        printf "\r\033[K"
        print_success "$description"
        return 0
    else
        printf "\r\033[K"
        if [ "$log_file" != "/dev/null" ]; then
            print_error "$description (see log: $log_file)"
        else
            print_error "$description"
        fi
        return 1
    fi
}

# Helper functions
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Get repository root
get_repo_root() {
    git rev-parse --show-toplevel
}

# Detect and set compose command
detect_compose() {
    if command -v docker-compose &> /dev/null; then
        COMPOSE_CMD="docker-compose"
        if docker --version 2>&1 | grep -qi podman; then
            DAEMON_CMD="podman"
        else
            DAEMON_CMD="docker"
        fi
    elif command -v podman-compose &> /dev/null; then
        COMPOSE_CMD="podman-compose"
        DAEMON_CMD="podman"
    else
        print_error "Neither docker-compose nor podman-compose found. Please install one."
        return 1
    fi
    export COMPOSE_CMD
    export DAEMON_CMD
}

# Ensure docker/podman daemon is running
ensure_daemon_running() {
    detect_compose || return 1
    
    if [ "$DAEMON_CMD" = "docker" ]; then
        if ! docker info &> /dev/null; then
            echo -e "${YELLOW}Docker daemon is not running. Attempting to start...${NC}"
            sudo systemctl start docker
            sleep 2
            if ! docker info &> /dev/null; then
                print_error "Failed to start Docker daemon"
                return 1
            fi
            print_success "Docker daemon started"
        fi
    elif [ "$DAEMON_CMD" = "podman" ]; then
        if ! systemctl --user is-active --quiet podman.socket; then
            echo -e "${YELLOW}Podman socket is not running. Attempting to start...${NC}"
            systemctl --user start podman.socket
            sleep 2
            if ! systemctl --user is-active --quiet podman.socket; then
                print_error "Failed to start Podman socket"
                return 1
            fi
            print_success "Podman socket started"
        fi
        
        if ! podman info &> /dev/null; then
            print_error "Podman is not responding"
            return 1
        fi
    fi
}

# Check if Docker services are running
services_running() {
    detect_compose || return 1
    $COMPOSE_CMD ps --services --filter "status=running" 2>/dev/null | grep -q .
}

# Export functions for use in other scripts
export -f print_header print_success print_error print_warning print_info
export -f get_repo_root detect_compose ensure_daemon_running services_running
export -f init_logging get_log_dir set_log_file log_to_file
export -f print_progress print_test_progress finish_progress
export -f parse_pytest_progress parse_vitest_progress parse_playwright_progress
export -f run_with_progress
