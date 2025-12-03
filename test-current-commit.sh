#!/bin/bash
#
# test-current-commit.sh
# Run tests on the current commit (useful during interactive rebase)
#
# Usage:
#   ./test-current-commit.sh                    # Run all tests
#   ./test-current-commit.sh --lint             # Just run linting
#   ./test-current-commit.sh --python           # Just run Python tests
#   ./test-current-commit.sh --python --file office/tests/test_morning_prayer.py
#   ./test-current-commit.sh --python --test test_specific_function
#   ./test-current-commit.sh --python --module office
#   ./test-current-commit.sh --e2e --test "morning prayer"
#   ./test-current-commit.sh --frontend
#
# See ./run-tests.sh --help for all available options
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source common functions
source "$SCRIPT_DIR/scripts/tests/common.sh"

REPO_ROOT=$(get_repo_root)
cd "$REPO_ROOT"

# Get current commit info
COMMIT_SHORT=$(git rev-parse --short HEAD)
COMMIT_MSG=$(git log --format=%B -n 1 HEAD | head -1)

print_header "Testing Current Commit"
echo -e "${YELLOW}$COMMIT_SHORT${NC} $COMMIT_MSG"
echo ""

# Check if we're in a rebase/merge
if [ -d ".git/rebase-merge" ] || [ -d ".git/rebase-apply" ]; then
    print_warning "Rebase in progress"
fi

# Run the modular test runner with all passed arguments
if "$SCRIPT_DIR/run-tests.sh" "$@"; then
    echo ""
    print_success "All tests passed for commit $COMMIT_SHORT"
    echo ""
    echo "You can now:"
    echo "  - Continue rebase: git rebase --continue"
    echo "  - Amend commit: git commit --amend"
    exit 0
else
    echo ""
    print_error "Tests failed for commit $COMMIT_SHORT"
    echo ""
    echo "To fix this commit:"
    echo "  1. Make your changes"
    echo "  2. Stage them: git add <files>"
    echo "  3. Amend: git commit --amend"
    echo "  4. Test again: ./test-current-commit.sh"
    echo "  5. Continue: git rebase --continue"
    echo ""
    echo "Tip: Run specific tests to iterate faster:"
    echo "  ./test-current-commit.sh --python --test <test_name>"
    echo "  ./test-current-commit.sh --lint --fix"
    exit 1
fi
