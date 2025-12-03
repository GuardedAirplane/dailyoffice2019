#!/bin/bash
#
# verify-commits.sh
# Verify all commits in the current branch by running tests on each commit
#
# Usage: ./verify-commits.sh [base-branch]
#   base-branch: The branch to compare against (default: master)
#

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m'

print_header() {
    echo -e "\n${MAGENTA}========================================${NC}"
    echo -e "${MAGENTA}$1${NC}"
    echo -e "${MAGENTA}========================================${NC}\n"
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

# Cleanup function to ensure Docker is stopped
cleanup() {
    if [ -n "$COMPOSE_CMD" ]; then
        echo ""
        print_info "Cleaning up Docker services..."
        $COMPOSE_CMD down -v 2>/dev/null || true
    fi
}

# Set trap to cleanup on exit
trap cleanup EXIT INT TERM

# Get repository root
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

# Detect docker-compose or podman-compose
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif command -v podman-compose &> /dev/null; then
    COMPOSE_CMD="podman-compose"
else
    print_error "Neither docker-compose nor podman-compose found. Please install one."
    exit 1
fi

print_info "Using container orchestration: $COMPOSE_CMD"

# Get base branch (default to master)
BASE_BRANCH=${1:-master}

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Handle detached HEAD state (e.g., during rebase)
if [ "$CURRENT_BRANCH" = "HEAD" ]; then
    # Try to get the branch being rebased
    if [ -f ".git/rebase-merge/head-name" ]; then
        CURRENT_BRANCH=$(cat .git/rebase-merge/head-name | sed 's|refs/heads/||')
        print_warning "Detected rebase in progress for branch: $CURRENT_BRANCH"
    elif [ -f ".git/rebase-apply/head-name" ]; then
        CURRENT_BRANCH=$(cat .git/rebase-apply/head-name | sed 's|refs/heads/||')
        print_warning "Detected rebase in progress for branch: $CURRENT_BRANCH"
    else
        print_error "Cannot determine current branch (detached HEAD state)"
        echo "Please run this script from a named branch or complete the rebase first"
        exit 1
    fi
fi

print_header "Commit Verification for Branch: $CURRENT_BRANCH"
print_info "Base branch: $BASE_BRANCH"

# Check if there are any commits to verify
if ! git rev-list $BASE_BRANCH..$CURRENT_BRANCH &> /dev/null; then
    print_error "Cannot find commits between $BASE_BRANCH and $CURRENT_BRANCH"
    echo "Make sure both branches exist and there are commits to verify"
    exit 1
fi

# Get list of commits
COMMITS=$(git rev-list --reverse $BASE_BRANCH..$CURRENT_BRANCH)
COMMIT_COUNT=$(echo "$COMMITS" | wc -l)

print_info "Found $COMMIT_COUNT commits to verify"
echo ""

# Store original HEAD
ORIGINAL_HEAD=$(git rev-parse HEAD)

# Track results
FAILED_COMMITS=()
PASSED_COMMITS=()
SKIPPED_COMMITS=()

# Counter
CURRENT=0

# Verify each commit
for commit in $COMMITS; do
    CURRENT=$((CURRENT + 1))
    
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Commit $CURRENT/$COMMIT_COUNT${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    # Get commit details
    COMMIT_SHORT=$(git rev-parse --short $commit)
    COMMIT_MSG=$(git log --format=%B -n 1 $commit | head -1)
    
    echo -e "${YELLOW}$COMMIT_SHORT${NC} $COMMIT_MSG"
    
    # Checkout the commit
    if ! git checkout --quiet $commit 2>/dev/null; then
        print_error "Failed to checkout commit $COMMIT_SHORT"
        FAILED_COMMITS+=("$COMMIT_SHORT: Failed to checkout")
        continue
    fi
    
    # Run the pre-commit hook tests
    if [ -x ".git/hooks/pre-commit" ]; then
        echo ""
        if .git/hooks/pre-commit; then
            print_success "All tests passed for commit $COMMIT_SHORT"
            PASSED_COMMITS+=("$COMMIT_SHORT: $COMMIT_MSG")
        else
            print_error "Tests failed for commit $COMMIT_SHORT"
            FAILED_COMMITS+=("$COMMIT_SHORT: $COMMIT_MSG")
            
            # Ask user what to do
            echo ""
            echo -e "${YELLOW}Options:${NC}"
            echo "  [c] Continue with next commit"
            echo "  [s] Stop verification"
            echo "  [i] Interactive rebase to fix this commit"
            read -p "Choose option (c/s/i): " choice
            
            case $choice in
                i|I)
                    print_info "Starting interactive rebase..."
                    git checkout $CURRENT_BRANCH
                    git rebase -i $commit^
                    exit 0
                    ;;
                s|S)
                    print_warning "Stopping verification"
                    git checkout $ORIGINAL_HEAD
                    exit 1
                    ;;
                *)
                    print_info "Continuing with next commit..."
                    ;;
            esac
        fi
    else
        print_warning "Pre-commit hook not found or not executable"
        SKIPPED_COMMITS+=("$COMMIT_SHORT: $COMMIT_MSG")
    fi
done

# Return to original HEAD
print_info "Returning to original HEAD..."
git checkout --quiet $ORIGINAL_HEAD

# Print summary
print_header "Verification Summary"

echo -e "${GREEN}Passed: ${#PASSED_COMMITS[@]}${NC}"
for commit in "${PASSED_COMMITS[@]}"; do
    echo -e "  ${GREEN}✓${NC} $commit"
done

if [ ${#FAILED_COMMITS[@]} -gt 0 ]; then
    echo -e "\n${RED}Failed: ${#FAILED_COMMITS[@]}${NC}"
    for commit in "${FAILED_COMMITS[@]}"; do
        echo -e "  ${RED}✗${NC} $commit"
    done
fi

if [ ${#SKIPPED_COMMITS[@]} -gt 0 ]; then
    echo -e "\n${YELLOW}Skipped: ${#SKIPPED_COMMITS[@]}${NC}"
    for commit in "${SKIPPED_COMMITS[@]}"; do
        echo -e "  ${YELLOW}⊘${NC} $commit"
    done
fi

echo ""

# Exit with appropriate code
if [ ${#FAILED_COMMITS[@]} -gt 0 ]; then
    print_error "Some commits failed verification"
    echo ""
    echo "To fix failed commits, you can:"
    echo "  1. Run: git rebase -i $BASE_BRANCH"
    echo "  2. Mark failed commits for 'edit' or 'reword'"
    echo "  3. Fix the issues and run: git commit --amend"
    echo "  4. Continue with: git rebase --continue"
    exit 1
else
    print_success "All commits passed verification!"
    exit 0
fi
