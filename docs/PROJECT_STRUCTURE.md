# sen2p Project Structure

```
sen2p/
├── sen2p/                      # Main package directory
│   ├── __init__.py             # Public API exports
│   └── downloader.py           # Core download functionality
│
├── docs/                       # Documentation
│   ├── README.md               # Main documentation
│   ├── QUICKSTART.md           # 5-minute getting started guide
│   ├── INTEGRATION.md          # Integration with rasteric
│   ├── SENTINEL2_REFERENCE.md  # Sentinel-2 band reference
│   └── CONTRIBUTING.md         # Contribution guidelines
│
├── examples/
│   ├── main.py                 # Demo script
│   └── example.py              # Usage examples
│
├── config/
│   ├── pyproject.toml          # Project configuration (uv/pip)
│   ├── .env.example            # Environment variable template
│   ├── .gitignore              # Git ignore rules
│   └── .python-version         # Python version specification
│
├── LICENSE                     # MIT License
└── uv.lock                     # Dependency lock file
```

## Key Files

### Core Package

- **`sen2p/__init__.py`**: Exports the main `download()` function
- **`sen2p/downloader.py`**: 
  - `Sentinel2Downloader` class for API interaction
  - `download()` function - main entry point
  - Handles authentication, search, and download

### Documentation

- **`README.md`**: Complete documentation with API reference
- **`QUICKSTART.md`**: Fast 5-minute setup guide
- **`INTEGRATION.md`**: How to use with rasteric, workflows, examples
- **`SENTINEL2_REFERENCE.md`**: Band information, indices, combinations
- **`CONTRIBUTING.md`**: Development setup and guidelines

### Examples

- **`main.py`**: Demo script showing basic usage
- **`example.py`**: Multiple usage examples

### Configuration

- **`pyproject.toml`**: Package metadata, dependencies, build config
- **`.env.example`**: Template for Copernicus credentials
- **`uv.lock`**: Locked dependency versions

## Module Overview

### `sen2p.downloader`

**Classes:**
- `Sentinel2Downloader`: Handles communication with Copernicus API

**Functions:**
- `download()`: Main function - search and download Sentinel-2 imagery

**Key Parameters:**
- Location (lon, lat)
- Date range (start_date, end_date)
- Cloud coverage filter (cloud_max)
- Product type (S2MSI1C or S2MSI2A)

**Returns:**
- List of dictionaries with download metadata
- Compatible with rasteric processing pipeline

## Design Pattern

```
User Code
    ↓
download() function (sen2p/__init__.py)
    ↓
Sentinel2Downloader class (sen2p/downloader.py)
    ↓
SentinelAPI (sentinelsat library)
    ↓
Copernicus Open Access Hub
```

## Dependencies

**Runtime:**
- `sentinelsat`: Sentinel API client
- `requests`: HTTP library

**Development:**
- `uv`: Package manager (recommended)
- Python 3.9+

## Data Flow

```
1. User calls download()
   └─ Validates credentials
   └─ Creates Sentinel2Downloader instance

2. Downloader.search()
   └─ Queries Copernicus Hub
   └─ Filters by cloud coverage
   └─ Returns matching products

3. Downloader.download_products()
   └─ Downloads .SAFE files
   └─ Saves to output_dir
   └─ Returns metadata list

4. Results returned to user
   └─ Compatible with rasteric
```

## Extension Points

If you want to extend sen2p:

1. **Add search filters**: Modify `Sentinel2Downloader.search()`
2. **Support other satellites**: Create new downloader classes
3. **Add preprocessing**: Extend `download_products()` 
4. **Custom output formats**: Modify return structure (keep rasteric compatibility!)

## Philosophy

**Single Responsibility**: Downloads only. Processing is rasteric's job.

**Simple API**: One function. Sensible defaults. Easy to use.

**Clean Separation**: Clear boundary between download and processing.

## Related Projects

- **rasteric**: Processing companion library
- **sentinelsat**: Underlying API client
- **Sentinel-2**: ESA satellite mission
