#!/bin/bash
#
# 01-docker-setup.sh - Set up Docker environment and seed database
#
# Usage: ./scripts/tests/01-docker-setup.sh [--skip-seed] [--build] [--no-build]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

REPO_ROOT=$(get_repo_root)
cd "$REPO_ROOT"

# Set up log file for this phase
LOG_DIR=$(get_log_dir)
LOG_FILE="$LOG_DIR/01-docker-setup.log"
export CURRENT_LOG_FILE="$LOG_FILE"

SKIP_SEED=false
FORCE_BUILD=false
NO_BUILD=false
for arg in "$@"; do
    case $arg in
        --skip-seed)
            SKIP_SEED=true
            shift
            ;;
        --build)
            FORCE_BUILD=true
            shift
            ;;
        --no-build)
            NO_BUILD=true
            shift
            ;;
    esac
done

print_header "Docker Environment Setup"
echo "  Log: $LOG_FILE"

ensure_daemon_running || exit 1
detect_compose

echo "  Using: $COMPOSE_CMD" | tee -a "$LOG_FILE"

# Clean up any existing containers and volumes to ensure a fresh start
print_progress "  Cleaning up existing containers and volumes..."
$COMPOSE_CMD down -v >> "$LOG_FILE" 2>&1 || true
printf "\r\033[K"
print_success "Cleaned up existing containers and volumes"

# Rebuild images if --build flag is passed or if Dockerfiles have changed
BUILD_ARGS=""
if [ "$NO_BUILD" = false ]; then
    if [ "$FORCE_BUILD" = true ]; then
        print_progress "  Rebuilding Docker images (--build flag)..."
        BUILD_ARGS="--build"
    else
        # Always rebuild to ensure we have the latest images
        print_progress "  Rebuilding Docker images..."
        BUILD_ARGS="--build"
    fi
    if $COMPOSE_CMD build >> "$LOG_FILE" 2>&1; then
        printf "\r\033[K"
        print_success "Docker images rebuilt"
    else
        printf "\r\033[K"
        print_error "Failed to rebuild Docker images (see log: $LOG_FILE)"
        exit 1
    fi
fi

# Start Docker services
print_progress "  Starting Docker services..."
if $COMPOSE_CMD up -d db cache >> "$LOG_FILE" 2>&1; then
    printf "\r\033[K"
    print_success "Database and cache services started"
else
    printf "\r\033[K"
    print_error "Failed to start Docker services (see log: $LOG_FILE)"
    exit 1
fi

# Wait for services to be healthy
print_progress "  Waiting for services to be ready..."
sleep 5

# Verify database is ready
if $COMPOSE_CMD exec -T db pg_isready -U dailyoffice >> "$LOG_FILE" 2>&1; then
    printf "\r\033[K"
    print_success "Database is ready"
else
    printf "\r\033[K"
    print_error "Database failed to start properly"
    exit 1
fi

# Check if database needs seeding
if [ "$SKIP_SEED" = false ]; then
    print_progress "  Checking if database needs seeding..."
    DB_SEEDED=false
    if $COMPOSE_CMD exec -T db psql -U dailyoffice -d dailyoffice -c "SELECT 1 FROM django_migrations LIMIT 1;" >> "$LOG_FILE" 2>&1; then
        if $COMPOSE_CMD exec -T db psql -U dailyoffice -d dailyoffice -c "SELECT 1 FROM churchcal_calendar WHERE abbreviation='ACNA_BCP2019' LIMIT 1;" >> "$LOG_FILE" 2>&1; then
            DB_SEEDED=true
            printf "\r\033[K"
            print_success "Database already seeded with required data"
        fi
    fi

    if [ "$DB_SEEDED" = false ]; then
        print_progress "  Seeding database from dump..."
        # Prefer the unzipped SQL file (contains data), fall back to zip (schema-only)
        if [ -f "site/dailyoffice_2024_01_30.sql" ]; then
            # Copy file to container to avoid pipe issues
            $COMPOSE_CMD cp site/dailyoffice_2024_01_30.sql db:/tmp/dump.sql
            $COMPOSE_CMD exec -T db psql -U dailyoffice -d dailyoffice -f /tmp/dump.sql >> "$LOG_FILE" 2>&1
            
            # Verify seeding
            if $COMPOSE_CMD exec -T db psql -U dailyoffice -d dailyoffice -c "SELECT 1 FROM churchcal_calendar WHERE abbreviation='ACNA_BCP2019' LIMIT 1;" >> "$LOG_FILE" 2>&1; then
                 printf "\r\033[K"
                 print_success "Database seeded successfully"
            else
                 printf "\r\033[K"
                 print_error "Database seeding failed: ACNA_BCP2019 not found"
                 exit 1
            fi
        elif [ -f "site/dailyoffice_2024_01_30.sql.zip" ]; then
            if command -v unzip > /dev/null; then
                unzip -p site/dailyoffice_2024_01_30.sql.zip dailyoffice_2024_01_30.sql > site/dailyoffice_temp.sql
                $COMPOSE_CMD cp site/dailyoffice_temp.sql db:/tmp/dump.sql
                rm site/dailyoffice_temp.sql
                $COMPOSE_CMD exec -T db psql -U dailyoffice -d dailyoffice -f /tmp/dump.sql >> "$LOG_FILE" 2>&1
                
                # Verify seeding
                if $COMPOSE_CMD exec -T db psql -U dailyoffice -d dailyoffice -c "SELECT 1 FROM churchcal_calendar WHERE abbreviation='ACNA_BCP2019' LIMIT 1;" >> "$LOG_FILE" 2>&1; then
                     printf "\r\033[K"
                     print_success "Database seeded successfully"
                else
                     printf "\r\033[K"
                     print_error "Database seeding failed: ACNA_BCP2019 not found"
                     exit 1
                fi
            else
                printf "\r\033[K"
                print_error "unzip command not found, cannot seed database"
                exit 1
            fi
        else
            printf "\r\033[K"
            print_error "Database dump not found at site/dailyoffice_2024_01_30.sql or site/dailyoffice_2024_01_30.sql.zip"
            exit 1
        fi
    fi
fi

# Reset sequence for django_migrations
print_progress "  Resetting django_migrations sequence..."
$COMPOSE_CMD exec -T db psql -U dailyoffice -d dailyoffice -c "SELECT setval('django_migrations_id_seq', (SELECT MAX(id) FROM django_migrations) + 1);" >> "$LOG_FILE" 2>&1 || true
printf "\r\033[K"

# Run migrations
print_progress "  Running database migrations..."
if $COMPOSE_CMD run --rm -e SKIP_MIGRATIONS="" -e SKIP_CALENDAR_CACHE=1 backend python manage.py migrate --noinput >> "$LOG_FILE" 2>&1; then
    printf "\r\033[K"
    print_success "Database migrations applied"
else
    printf "\r\033[K"
    print_warning "Database migrations failed (some might have applied)"
fi

print_success "Docker environment setup complete"
