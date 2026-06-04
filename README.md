# sen2p

Lightweight Python library for downloading Sentinel-2 satellite imagery.

## Overview

`sen2p` focuses exclusively on downloading Sentinel-2 imagery from the Copernicus Data Space Ecosystem (CDSE). It provides a clean, native API implementation for searching and downloading satellite data with cloud filtering.

**The Companion:** `rasteric` focuses on processing and analysis. Together they create a lightweight workflow for satellite imagery:

```python
from sen2p.cdse_downloader import CDSEDownloader
from rasteric import raster

# Download imagery
downloader = CDSEDownloader()
products = downloader.search(
    location=(172.1, -43.5),
    start_date="2023-06-01",
    end_date="2023-06-30",
    cloud_max=20,
    producttype="MSIL2A",
)
results = downloader.download_products(products, output_dir="data", max_products=3)

# Process with rasteric
raster.ndvi(results[0]["path"], "ndvi.tif", red_band=4, nir_band=8)
```

Two libraries. Clean separation. Full workflow.

## 📚 Documentation

- **[Quick Start](docs/QUICKSTART.md)** - Get started in 5 minutes
- **[Integration Guide](docs/INTEGRATION.md)** - Using with rasteric
- **[Sentinel-2 Reference](docs/SENTINEL2_REFERENCE.md)** - Band specifications
- **[FAQ](docs/FAQ.md)** - Frequently asked questions
- **[Contributing](docs/CONTRIBUTING.md)** - How to contribute
- **[Full Documentation Index](docs/INDEX.md)** - All documentation

## Installation

```bash
uv add sen2p
```

Or with pip:

```bash
pip install sen2p
```

## Setup

⚠️ **Important:** The old Copernicus Open Access Hub (`scihub.copernicus.eu`) was shut down in October 2023.

You need a free **Copernicus Data Space Ecosystem (CDSE)** account:

1. Register at **[https://dataspace.copernicus.eu](https://dataspace.copernicus.eu)**
2. Click **REGISTER** and fill in the form
3. **Verify your email** (check spam folder)
4. Set your credentials:

```bash
export CDSE_USER="your_email@example.com"
export CDSE_PASSWORD="your_password"
```

Or use the old variable names (also supported):
```bash
export COPERNICUS_USER="your_email@example.com"
export COPERNICUS_PASSWORD="your_password"
```

sen2p uses **native CDSE API** with OAuth2 authentication - credentials are loaded automatically from environment variables.

## Usage

### Basic Download

```python
from sen2p.cdse_downloader import CDSEDownloader

# Initialize downloader (credentials loaded from environment)
downloader = CDSEDownloader()

# Search for products
products = downloader.search(
    location=(172.1, -43.5),  # (longitude, latitude)
    start_date="2024-01-01",
    end_date="2024-01-31",
    cloud_max=20,  # Max 20% cloud coverage
    producttype="MSIL2A",  # Level-2A (atmospherically corrected)
)

print(f"Found {len(products)} products")

# Download products
results = downloader.download_products(
    products,
    output_dir="sentinel_data",
    max_products=3,  # Download only 3 best matches
)

print(f"Downloaded {len(results)} products")
for r in results:
    print(f"  {r['title']} - {r['cloud_cover']}% clouds")
```

### With Explicit Credentials

```python
from sen2p.cdse_downloader import CDSEDownloader

downloader = CDSEDownloader(username="your_email@example.com", password="your_password")

products = downloader.search(
    location=(172.1, -43.5),
    start_date="2024-01-01",
    end_date="2024-01-31",
    cloud_max=20,
)

results = downloader.download_products(products, output_dir="data")
```

### Choose Product Type

```python
# Level-2A (atmospherically corrected) - Recommended
products = downloader.search(
    location=(172.1, -43.5),
    start_date="2024-01-01",
    end_date="2024-01-31",
    producttype="MSIL2A",  # Default
)

# Level-1C (top-of-atmosphere)
products = downloader.search(
    location=(172.1, -43.5),
    start_date="2024-01-01",
    end_date="2024-01-31",
    producttype="MSIL1C",
)
```

## API Reference

### `CDSEDownloader`

Native implementation for Copernicus Data Space Ecosystem API.

#### `__init__(username=None, password=None)`

Initialize the downloader.

**Parameters:**
- `username` (str, optional): CDSE email (or set CDSE_USER/COPERNICUS_USER env var)
- `password` (str, optional): CDSE password (or set CDSE_PASSWORD/COPERNICUS_PASSWORD env var)

**Example:**
```python
# From environment variables
downloader = CDSEDownloader()

# Explicit credentials
downloader = CDSEDownloader(username="email@example.com", password="pass")
```

#### `search(location, start_date, end_date, cloud_max=30, collection="SENTINEL-2", producttype="MSIL2A")`

Search for Sentinel-2 products.

**Parameters:**
- `location` (tuple): (longitude, latitude)
- `start_date` (str): Start date "YYYY-MM-DD"
- `end_date` (str): End date "YYYY-MM-DD"
- `cloud_max` (int): Maximum cloud coverage 0-100% (default: 30)
- `collection` (str): Collection name (default: "SENTINEL-2")
- `producttype` (str): "MSIL2A" (Level-2A, default) or "MSIL1C" (Level-1C)

**Returns:**
List of product dictionaries with:
- `id`: Product ID (UUID)
- `name`: Product name
- `size`: File size in bytes
- `cloud_cover`: Cloud coverage percentage
- `date`: Acquisition date (ISO 8601)
- `download_url`: Download URL (internal use)

**Example:**
```python
products = downloader.search(
    location=(172.1, -43.5),
    start_date="2024-01-01",
    end_date="2024-01-31",
    cloud_max=20,
    producttype="MSIL2A",
)
```

#### `download_products(products, output_dir="data", max_products=None)`

Download multiple products.

**Parameters:**
- `products` (list): List of products from search()
- `output_dir` (str): Directory to save files (default: "data")
- `max_products` (int, optional): Maximum number to download (downloads all if None)

**Returns:**
List of download results with:
- `id`: Product ID
- `title`: Product title
- `path`: Path to downloaded file
- `size`: File size
- `cloud_cover`: Cloud coverage percentage
- `date`: Acquisition date

**Example:**
```python
results = downloader.download_products(
    products,
    output_dir="sentinel_data",
    max_products=3,
)
```

#### `download_product(product_id, output_dir="data")`

Download a single product by ID.

**Parameters:**
- `product_id` (str): Product UUID from search results
- `output_dir` (str): Directory to save the file

**Returns:**
Dictionary with download information.

**Example:**
```python
result = downloader.download_product(
    "82fa3297-4865-4e9b-b532-29686b51bf4d",
    output_dir="data",
)
```

## Design Philosophy

**Native CDSE Implementation:** Direct OAuth2 and OData API integration for reliable downloads without third-party dependencies.

**Single Responsibility:** `sen2p` only downloads. Processing, band extraction, mosaicking, and analysis are handled by `rasteric`.

**Simple API:** Clean class-based interface with sensible defaults.

**Clean Integration:** Output format designed to work seamlessly with `rasteric`.

## License

MIT

---

## Project Structure

```
sen2p/
├── sen2p/              # Core package
├── docs/               # Documentation
├── examples/           # Usage examples
├── tests/              # Test suite
├── README.md           # This file
├── CHANGELOG.md        # Version history
└── LICENSE             # MIT License
```

## Resources

- **Documentation:** [docs/](docs/)
- **Examples:** [examples/](examples/)
- **Copernicus Data Space:** https://dataspace.copernicus.eu/
- **CDSE Documentation:** https://documentation.dataspace.copernicus.eu/
- **Sentinel-2:** https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-2
