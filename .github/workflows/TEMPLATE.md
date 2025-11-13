# GitHub Actions Workflow Template

Use this template to create new custom workflows that leverage the Docker infrastructure.

## Basic Workflow Structure

```yaml
name: My Custom Workflow

on:
  push:
    branches: ["main", "develop", "**-daily-office"]
    paths:
      - "relevant/path/**"
  pull_request:
    branches: ["main", "develop"]
    paths:
      - "relevant/path/**"

jobs:
  my-job:
    name: Descriptive Job Name
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker
        run: |
          sudo apt-get update
          sudo apt-get install -y docker docker-compose

      - name: Verify Docker installation
        run: |
          docker --version
          docker-compose --version

      - name: Start required services
        run: |
          # Choose services you need:
          # - db: PostgreSQL database
          # - cache: Memcached
          # - backend: Django API
          # - frontend: Vue 3 app
          docker-compose up -d db cache backend

      - name: Wait for database (if using db)
        run: |
          for i in {1..30}; do
            if docker exec dailyoffice2019_db_1 pg_isready -U dailyoffice; then
              echo "PostgreSQL is ready!"
              break
            fi
            echo "Waiting... ($i/30)"
            sleep 2
          done

      - name: Load database dump (if needed)
        run: |
          if [ -f site/dailyoffice_2024_01_30.sql.zip ]; then
            unzip -p site/dailyoffice_2024_01_30.sql.zip dailyoffice_2024_01_30.sql | \
              docker exec -i dailyoffice2019_db_1 psql -U dailyoffice dailyoffice
          fi

      - name: Run your custom command
        run: |
          # Example: Run Django management command
          docker exec dailyoffice2019_backend_1 python manage.py your_command
          
          # Example: Run custom Python script
          docker exec dailyoffice2019_backend_1 python scripts/your_script.py
          
          # Example: Run frontend build
          docker exec dailyoffice2019_frontend_1 npm run build

      - name: Copy results from container (if needed)
        if: always()
        run: |
          docker cp dailyoffice2019_backend_1:/workspace/site/output.txt ./output.txt || true

      - name: Upload artifacts (if needed)
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: my-artifacts
          path: |
            output.txt
            other-files/

      - name: Stop services
        if: always()
        run: |
          docker-compose down -v

      - name: Display summary
        if: always()
        run: |
          echo "## Job Summary" >> $GITHUB_STEP_SUMMARY
          echo "✅ Job completed successfully" >> $GITHUB_STEP_SUMMARY
```

## Common Patterns

### Pattern 1: Backend-Only Job

```yaml
jobs:
  backend-job:
    name: Backend Task
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: sudo apt-get install -y docker docker-compose
      - run: docker-compose up -d db cache backend
      - run: |
          # Wait for DB
          until docker exec dailyoffice2019_db_1 pg_isready -U dailyoffice; do sleep 2; done
      - run: docker exec dailyoffice2019_backend_1 python manage.py your_command
      - run: docker-compose down -v
        if: always()
```

### Pattern 2: Frontend-Only Job

```yaml
jobs:
  frontend-job:
    name: Frontend Task
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: sudo apt-get install -y docker docker-compose
      - run: docker-compose up -d frontend
      - run: sleep 30  # Wait for npm install
      - run: docker exec dailyoffice2019_frontend_1 npm run your_script
      - run: docker-compose down -v
        if: always()
```

### Pattern 3: Full Stack Job (with E2E tests)

```yaml
jobs:
  e2e-job:
    name: End-to-End Task
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: sudo apt-get install -y docker docker-compose
      - run: docker-compose up -d  # Start all services
      - run: sleep 60  # Wait for all services
      - run: |
          # Load database
          unzip -p site/dailyoffice_2024_01_30.sql.zip dailyoffice_2024_01_30.sql | \
            docker exec -i dailyoffice2019_db_1 psql -U dailyoffice dailyoffice
      - run: |
          # Check backend health
          curl -f http://localhost:8000/api/
      - run: |
          # Check frontend health
          curl -f http://localhost:5173/
      - run: docker exec dailyoffice2019_frontend_1 npm run test:e2e
      - run: docker-compose down -v
        if: always()
```

### Pattern 4: Parallel Jobs with Shared Setup

```yaml
jobs:
  setup:
    name: Setup Environment
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: sudo apt-get install -y docker docker-compose
      - uses: actions/cache@v4
        with:
          path: ~/.local/share/containers
          key: docker-images-${{ hashFiles('docker-compose.yml') }}
  
  job1:
    name: First Job
    needs: setup
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: sudo apt-get install -y docker docker-compose
      - run: docker-compose up -d backend
      - run: docker exec dailyoffice2019_backend_1 python manage.py job1_command
      - run: docker-compose down -v
        if: always()
  
  job2:
    name: Second Job
    needs: setup
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: sudo apt-get install -y docker docker-compose
      - run: docker-compose up -d backend
      - run: docker exec dailyoffice2019_backend_1 python manage.py job2_command
      - run: docker-compose down -v
        if: always()
```

## Common Variables and Secrets

### Using Environment Variables

```yaml
- name: Run with environment variables
  run: |
    docker exec \
      -e MY_VAR="value" \
      -e ANOTHER_VAR="${{ secrets.MY_SECRET }}" \
      dailyoffice2019_backend_1 \
      python manage.py command
```

### Using GitHub Secrets

```yaml
- name: Use secret in workflow
  env:
    SECRET_KEY: ${{ secrets.MY_SECRET }}
  run: |
    echo "Secret value: $SECRET_KEY"
```

## Useful Actions

### Upload Test Results

```yaml
- name: Upload test results
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: test-results
    path: |
      pytest-results.xml
      coverage.xml
```

### Publish Test Report

```yaml
- name: Publish test results
  uses: EnricoMi/publish-unit-test-result-action@v2
  if: always()
  with:
    files: |
      pytest-results.xml
    check_name: Test Results
```

### Create Pull Request (for auto-fixes)

```yaml
- name: Create PR with fixes
  uses: peter-evans/create-pull-request@v7
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
    commit-message: "fix: Auto-generated fixes"
    title: "🤖 Automated fixes"
    body: "This PR contains automated fixes"
    branch: auto-fix-${{ github.run_id }}
```

## Tips and Best Practices

### 1. Always Clean Up

```yaml
- name: Stop services
  if: always()  # Run even if previous steps fail
  run: docker-compose down -v
```

### 2. Use Health Checks

```yaml
- name: Wait for service health
  run: |
    for i in {1..30}; do
      if docker exec dailyoffice2019_backend_1 python manage.py check; then
        echo "Service is healthy!"
        break
      fi
      sleep 2
    done
```

### 3. Copy Files Safely

```yaml
- name: Copy results
  if: always()
  run: |
    docker cp container:/path/to/file ./local/path || true
    # The '|| true' prevents failure if file doesn't exist
```

### 4. Use Matrix Strategy for Multiple Versions

```yaml
jobs:
  test:
    strategy:
      matrix:
        python-version: ['3.12', '3.13']
        node-version: ['20', '22']
    # ... rest of job
```

### 5. Cache Docker Images

```yaml
- name: Cache Docker images
  uses: actions/cache@v4
  with:
    path: ~/.local/share/containers
    key: docker-${{ hashFiles('docker-compose.yml', 'site/Dockerfile.dev') }}
```

## Example: Custom Data Import Workflow

```yaml
name: Import Liturgical Data

on:
  workflow_dispatch:  # Manual trigger only
    inputs:
      data_file:
        description: 'Data file to import'
        required: true
        type: string

jobs:
  import:
    name: Import Data
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Docker
        run: sudo apt-get install -y docker docker-compose
      
      - name: Start services
        run: docker-compose up -d db cache backend
      
      - name: Wait for database
        run: |
          until docker exec dailyoffice2019_db_1 pg_isready -U dailyoffice; do sleep 2; done
      
      - name: Import data
        run: |
          docker exec dailyoffice2019_backend_1 \
            python manage.py import_data ${{ github.event.inputs.data_file }}
      
      - name: Verify import
        run: |
          docker exec dailyoffice2019_backend_1 \
            python manage.py verify_data
      
      - name: Stop services
        if: always()
        run: docker-compose down -v
      
      - name: Report status
        run: |
          echo "## Data Import Summary" >> $GITHUB_STEP_SUMMARY
          echo "File: ${{ github.event.inputs.data_file }}" >> $GITHUB_STEP_SUMMARY
          echo "Status: ✅ Completed" >> $GITHUB_STEP_SUMMARY
```

## Container Names Reference

Based on `docker-compose.yml`:

- `dailyoffice2019_db_1` - PostgreSQL database
- `dailyoffice2019_cache_1` - Memcached
- `dailyoffice2019_backend_1` - Django backend
- `dailyoffice2019_frontend_1` - Vue 3 frontend

## Service Ports

- Database: `5432`
- Memcached: `11211`
- Backend API: `8000`
- Frontend: `5173`

## Common Django Commands

```bash
# System check
docker exec dailyoffice2019_backend_1 python manage.py check

# Run migrations
docker exec dailyoffice2019_backend_1 python manage.py migrate

# Collect static files
docker exec dailyoffice2019_backend_1 python manage.py collectstatic --noinput

# Create superuser (interactive)
docker exec -it dailyoffice2019_backend_1 python manage.py createsuperuser

# Run tests
docker exec dailyoffice2019_backend_1 python -m pytest

# Run shell
docker exec -it dailyoffice2019_backend_1 python manage.py shell
```

## Common npm Commands

```bash
# Install dependencies
docker exec dailyoffice2019_frontend_1 npm install

# Build for production
docker exec dailyoffice2019_frontend_1 npm run build

# Run linter
docker exec dailyoffice2019_frontend_1 npm run lint

# Run tests
docker exec dailyoffice2019_frontend_1 npm run test:unit
docker exec dailyoffice2019_frontend_1 npm run test:e2e
```

## Debugging Failed Workflows

### 1. View Container Logs

```bash
# Locally
docker logs dailyoffice2019_backend_1

# In workflow
- name: View logs
  if: failure()
  run: |
    docker logs dailyoffice2019_backend_1
```

### 2. Inspect Container

```bash
# Locally
docker exec -it dailyoffice2019_backend_1 bash

# In workflow (run commands directly)
- name: Debug container
  if: failure()
  run: |
    docker exec dailyoffice2019_backend_1 ls -la /workspace/site
    docker exec dailyoffice2019_backend_1 cat /workspace/site/logs/error.log
```

### 3. Enable Verbose Output

```yaml
- name: Run with verbose output
  run: |
    set -x  # Echo all commands
    docker-compose up -d backend
    docker exec dailyoffice2019_backend_1 python manage.py check --verbosity 2
```

---

For more examples, see existing workflows in `.github/workflows/`:
- `backend-tests.yml`
- `frontend-tests.yml`
- `formatting.yml`
- `ci.yml`
