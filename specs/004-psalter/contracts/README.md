# API Contracts

This directory contains API contract specifications for the Psalter feature.

## Files

- **`psalms-api.yaml`**: OpenAPI 3.0 specification for `/api/v1/psalms` endpoints
  - Lists all psalms with first verse preview
  - Retrieves complete psalm with all verses
  - Lists thematic topics
  - Fully documents request/response schemas

## Usage

### Viewing the API Documentation

1. **Swagger UI** (Interactive API explorer):

   ```bash
   # Start the Django development server
   cd site && python manage.py runsslserver

   # Navigate to:
   # https://127.0.0.1:8000/api/
   ```

2. **ReDoc** (Beautiful API documentation):

   ```bash
   # https://127.0.0.1:8000/api/redoc/
   ```

3. **Raw OpenAPI Spec**:

   ```bash
   # JSON format:
   # https://127.0.0.1:8000/api/openapi.json

   # YAML format:
   # https://127.0.0.1:8000/api/openapi.yaml
   ```

### Validating Against the Contract

The OpenAPI spec in this directory documents the **intended** behavior per the specification.
The **actual** API is auto-generated from Django REST Framework serializers and may differ.

To ensure the implementation matches the spec:

```bash
# Generate current API schema
cd site
python manage.py spectacular --file /tmp/current-schema.yaml

# Compare with contract
diff specs/004-psalter/contracts/psalms-api.yaml /tmp/current-schema.yaml
```

**Any differences should be reconciled** - either update the code to match the spec or update the spec to match reality (with justification).

## API Endpoints Summary

| Endpoint                  | Method | Description         | Requirements                   |
| ------------------------- | ------ | ------------------- | ------------------------------ |
| `/api/v1/psalms`          | GET    | List all 150 psalms | FR-002, US2                    |
| `/api/v1/psalms/{number}` | GET    | Get single psalm    | FR-002, FR-003, FR-004, FR-005 |
| `/api/v1/psalms/topics/`  | GET    | List all topics     | FR-011, US4                    |

## Schema Objects

| Object         | Purpose            | Key Fields                                                                 |
| -------------- | ------------------ | -------------------------------------------------------------------------- |
| `PsalmSummary` | List view          | `id`, `number`, `latin_title`, `verses[0]`, `topics`                       |
| `PsalmDetail`  | Full psalm         | `id`, `number`, `latin_title`, `verses[]`, `topics`                        |
| `PsalmVerse`   | Verse within psalm | `number`, `first_half`, `second_half`, `first_half_tle`, `second_half_tle` |
| `PsalmTopic`   | Thematic category  | `id`, `topic_name`, `order`                                                |

## Important Notes

### Contemporary vs Traditional Language Edition

Both are included in every `PsalmVerse`:

- **Contemporary** (default): `first_half`, `second_half` (always present)
- **Traditional** (optional): `first_half_tle`, `second_half_tle` (may be null)

Client decides which to display based on user preference (FR-013, FR-015).

### Pointing Marks (FR-014)

The asterisk (\*) between first and second half-lines is **NOT stored in the database**.
It's added at display time:

```html
<p>{{ verse.first_half }} * {{ verse.second_half }}</p>
```

This keeps the data model clean and allows for flexible formatting.

### Topics are Managed via Admin Interface

Topics can be created, edited, and reordered through the Django admin interface (FR-016-017).
The API provides **read-only access** to topics for frontend display.

There is **no POST/PUT/PATCH/DELETE** for topics via the public API - management is done through Django admin at `/admin/psalter/psalmtopic/`.

### Performance Requirements

- **SC-001**: Individual psalm must load in <2 seconds
- **SC-006**: Language edition toggle must update in <1 second

Current implementation uses:

- Database indexes on `Psalm.number` (fast lookup)
- Prefetch relationships in `PsalmsViewSet` (avoid N+1 queries)
- Memcached for aggressive caching (optional, dataset is tiny)

## Testing the API

### Using cURL

```bash
# List all psalms
curl https://127.0.0.1:8000/api/v1/psalms

# Get Psalm 23
curl https://127.0.0.1:8000/api/v1/psalms/23

# List all topics
curl https://127.0.0.1:8000/api/v1/psalms/topics/
```

### Using HTTPie

```bash
# More readable output
http https://127.0.0.1:8000/api/v1/psalms/23
```

### From Frontend

```javascript
// Get Psalm 23
const response = await this.$http.get(
  `${import.meta.env.VITE_API_URL}api/v1/psalms/23/`
);
const psalm = response.data;

// Get all topics
const topicsResponse = await this.$http.get(
  `${import.meta.env.VITE_API_URL}api/v1/psalms/topics/`
);
const topics = topicsResponse.data;
```

## Contract Validation in Tests

Integration tests should validate responses against this OpenAPI schema:

```python
# In site/psalter/tests.py or site/tests/integration/test_psalms_api.py
from openapi_spec_validator import validate_spec
import yaml

def test_api_matches_contract():
    # Load the contract
    with open('specs/004-psalter/contracts/psalms-api.yaml') as f:
        spec = yaml.safe_load(f)

    # Validate OpenAPI spec is well-formed
    validate_spec(spec)

    # Test actual API responses match schema
    # (Use openapi-core or similar library)
```

## Maintaining the Contract

When making changes to the API:

1. **Update the contract FIRST** (spec-driven development)
2. **Implement the change** in Django REST Framework
3. **Validate the implementation** matches the contract
4. **Update tests** to cover the new behavior
5. **Document breaking changes** in commit message

This ensures the contract remains the source of truth for API behavior.

## Related Documentation

- **Feature Spec**: `/specs/004-psalter/spec.md`
- **Data Model**: `/specs/004-psalter/data-model.md`
- **Implementation Plan**: `/specs/004-psalter/plan.md`
- **Quickstart Guide**: `/specs/004-psalter/quickstart.md`
