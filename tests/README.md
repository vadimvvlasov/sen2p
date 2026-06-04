# sen2p Tests

Test suite for sen2p library.

## Running Tests

### Import Tests
Verify that the package is correctly installed and imports work:

```bash
uv run tests/test_imports.py
```

This checks:
- `sen2p.download` can be imported
- `sen2p.downloader.Sentinel2Downloader` can be imported
- `sentinelsat` dependency is available

## Test Structure

Currently tests include:
- **test_imports.py** - Import verification

## Future Tests

Planned test coverage:
- Unit tests for `Sentinel2Downloader` class
- Mock API tests (no real downloads)
- Integration tests (with real API, optional)
- Error handling tests
- Parameter validation tests

## Contributing Tests

When adding tests:

1. **Use pytest framework**
   ```bash
   uv add --dev pytest
   ```

2. **Name test files** `test_*.py`

3. **Mock external calls** - Don't hit real Copernicus API in unit tests
   ```python
   from unittest.mock import Mock, patch
   
   @patch('sen2p.downloader.SentinelAPI')
   def test_search(mock_api):
       # Your test here
       pass
   ```

4. **Test edge cases**
   - Invalid credentials
   - No products found
   - Network errors
   - Invalid parameters

5. **Keep tests fast** - Use mocks for external services

## Running Full Test Suite (Future)

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=sen2p

# Run specific test file
uv run pytest tests/test_imports.py

# Run verbose
uv run pytest -v
```

## Test Categories

### Unit Tests
Test individual functions and classes in isolation.

```python
def test_sentinel2_downloader_init():
    downloader = Sentinel2Downloader(username="test", password="test")
    assert downloader.username == "test"
```

### Integration Tests
Test real API interactions (optional, requires credentials).

```python
@pytest.mark.integration
def test_real_download():
    # Requires COPERNICUS_USER and COPERNICUS_PASSWORD
    results = download(...)
    assert len(results) > 0
```

### Mock Tests
Test without hitting real services.

```python
@patch('sen2p.downloader.SentinelAPI')
def test_search_with_mock(mock_api):
    mock_api.return_value.query.return_value = {...}
    # Test logic
```

## Test Data

For tests requiring sample data:
- Use small test fixtures
- Store in `tests/fixtures/`
- Document test data sources

## Continuous Integration

Future CI setup will run tests on:
- Every commit
- Pull requests
- Multiple Python versions (3.10, 3.11, 3.12, 3.13)
- Different operating systems

## Test Coverage Goals

Target coverage:
- **Core functionality:** 90%+
- **Error handling:** 80%+
- **Edge cases:** 70%+

## Need Help?

- pytest documentation: https://docs.pytest.org/
- unittest.mock guide: https://docs.python.org/3/library/unittest.mock.html
- See `../docs/DEVELOPER_GUIDE.md` for development setup
