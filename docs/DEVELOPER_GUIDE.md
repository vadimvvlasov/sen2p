# Developer Guide - sen2p

Quick reference for developers working on sen2p.

## Setup

```bash
# Clone and enter directory
cd sen2p

# Install with uv (creates .venv automatically)
uv sync

# Verify installation
uv run test_import.py
```

## Running Examples

```bash
# Set credentials first
export COPERNICUS_USER="your_username"
export COPERNICUS_PASSWORD="your_password"

# Run demo
uv run main.py

# Run examples
uv run example.py
```

## Project Layout

```
sen2p/
├── sen2p/              # Package source
│   ├── __init__.py     # Exports: download
│   └── downloader.py   # Class: Sentinel2Downloader
│
├── *.md                # Documentation files
├── example.py          # Usage examples
├── main.py             # Demo script
├── test_import.py      # Import tests
└── pyproject.toml      # Project config
```

## Key Files

### `sen2p/__init__.py`
- Exports `download` function
- Defines package version
- Public API entry point

### `sen2p/downloader.py`
- `Sentinel2Downloader` class
- `download()` function implementation
- All download logic

### `pyproject.toml`
- Package metadata
- Dependencies
- Build configuration
- Uses hatchling as build backend

## Adding Features

### Adding a Search Parameter

1. Add parameter to `Sentinel2Downloader.search()`:
```python
def search(
    self,
    location: Tuple[float, float],
    start_date: str,
    end_date: str,
    cloud_max: int = 30,
    your_param: str = "default",  # Add here
    ...
)
```

2. Pass to API query:
```python
products = self.api.query(
    footprint,
    date=(start_date, end_date),
    your_param=your_param,  # Use here
    ...
)
```

3. Update `download()` signature to expose it

4. Update docstrings and README

### Adding a Downloader Method

```python
class Sentinel2Downloader:
    def your_method(self, param: str) -> Any:
        """
        Description of what this does.
        
        Args:
            param: Parameter description
            
        Returns:
            What it returns
        """
        # Implementation
        pass
```

### Adding a Helper Function

```python
def _helper_function(data: Any) -> Any:
    """
    Private helper function (starts with _)
    
    Args:
        data: Input data
        
    Returns:
        Processed data
    """
    # Implementation
    pass
```

## Code Style

- Follow PEP 8
- Use type hints everywhere
- Docstrings: Google style
- Private functions: Prefix with `_`
- Line length: 88 characters (Black default)

## Testing Checklist

Before committing:

```bash
# 1. Test imports
uv run test_import.py

# 2. Run demo (requires credentials)
uv run main.py

# 3. Check types (if mypy installed)
uv run mypy sen2p

# 4. Format code (if ruff installed)
uv run ruff format .
```

## Common Tasks

### Update Dependencies

```bash
# Add new dependency
uv add package_name

# Remove dependency
uv remove package_name

# Update all dependencies
uv sync --upgrade
```

### Build Package

```bash
# Build wheel and sdist
uv build

# Check dist/
ls dist/
```

### Test Installation

```bash
# Install locally in editable mode
uv pip install -e .

# Test in Python
python -c "from sen2p import download; print('OK')"
```

## Architecture Decisions

### Why sentinelsat?

- Battle-tested, mature library
- Handles Copernicus API complexity
- Active maintenance
- Good error handling

### Why One Function?

- Simple is better than complex
- Easy to learn and use
- Clear purpose
- Minimize API surface

### Why Separate from rasteric?

- Single Responsibility Principle
- Downloads vs Processing
- Can be used independently
- Clear boundaries

## API Design Guidelines

1. **Minimize public API** - Only export what's needed
2. **Sensible defaults** - Work out of the box
3. **Type hints** - Help users with IDE autocomplete
4. **Clear errors** - Explain what went wrong
5. **Docstrings** - Document all public functions
6. **Compatibility** - Output works with rasteric

## Error Handling Strategy

```python
# ValueError for configuration errors
if not self.username:
    raise ValueError("Credentials required")

# RuntimeError for API/network errors
try:
    products = self.api.query(...)
except SentinelAPIError as e:
    raise RuntimeError(f"Search failed: {e}")

# Let other exceptions propagate
```

## Output Format

The `download()` function returns a list of dicts:

```python
[
    {
        "id": "product_uuid",
        "title": "S2A_MSIL2A_...",
        "path": "/path/to/file.SAFE",
        "size": "1.2 GB",
        "cloud_cover": 15.5,
        "date": datetime(...),
        "requested_bands": ["red", "nir"]
    },
    ...
]
```

This format is designed for:
1. Easy iteration
2. Passing to rasteric
3. Filtering/sorting
4. Logging/reporting

## Debugging Tips

### Enable Verbose Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from sen2p import download
results = download(...)
```

### Test API Connection

```python
from sentinelsat import SentinelAPI

api = SentinelAPI('username', 'password', 
                  'https://scihub.copernicus.eu/dhus')
api.query(...)  # Test query
```

### Check Product Details

```python
results = download(...)
for r in results:
    print(f"Title: {r['title']}")
    print(f"Path: {r['path']}")
    print(f"Clouds: {r['cloud_cover']}%")
```

## Dependencies

**Runtime:**
- `sentinelsat>=1.2.1` - Sentinel API client
- `requests>=2.34.2` - HTTP library (sentinelsat dependency)

**Development (optional):**
- `mypy` - Type checking
- `ruff` - Linting and formatting
- `pytest` - Testing framework

## Release Checklist

1. Update version in `pyproject.toml`
2. Update version in `sen2p/__init__.py`
3. Update `SUMMARY.md` with version
4. Run all tests
5. Build: `uv build`
6. Tag: `git tag v0.1.0`
7. Push: `git push --tags`

## Future Improvements

Ideas for future versions:

1. **Polygon footprints** - Search by polygon instead of point
2. **Batch downloads** - Parallel download support
3. **Resume downloads** - Continue interrupted downloads
4. **Progress callbacks** - Custom progress handlers
5. **Caching** - Avoid re-downloading same products
6. **CLI tool** - Command-line interface

## Questions?

- Check existing documentation first
- Open an issue for bugs
- Open a discussion for features
- Keep changes focused and tested

## Useful Links

- [sentinelsat docs](https://sentinelsat.readthedocs.io/)
- [Copernicus API](https://scihub.copernicus.eu/userguide/)
- [Sentinel-2 specs](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi)
- [uv docs](https://docs.astral.sh/uv/)
