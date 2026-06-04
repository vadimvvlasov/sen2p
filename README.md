# sen2p

Lightweight Python library for downloading Sentinel-2 satellite imagery.

## Overview

`sen2p` focuses exclusively on downloading Sentinel-2 imagery from the Copernicus Open Access Hub. It provides a clean, simple API for searching and downloading satellite data with cloud filtering.

**The Companion:** `rasteric` focuses on processing and analysis. Together they create a lightweight workflow for satellite imagery:

```python
from sen2p import download
from rasteric import raster

# Download imagery
results = download(
    start_date="2023-06-01",
    end_date="2023-06-30",
    location=[172.1, -43.5],
    bands=["red", "nir"],
    output_dir="data",
    cloud_max=20,
)

# Process with rasteric
raster.ndvi(results[0]["path"], "ndvi.tif", red_band=1, nir_band=2)
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

Or pass them directly to the `download()` function.

## Usage

### Basic Download

```python
from sen2p import download

results = download(
    start_date="2024-01-01",
    end_date="2024-01-31",
    location=[172.1, -43.5],  # [longitude, latitude]
    output_dir="sentinel_data",
    cloud_max=20,  # Max 20% cloud coverage
)

print(f"Downloaded {len(results)} products")
for r in results:
    print(f"  {r['title']} - {r['cloud_cover']}% clouds")
```

### With Credentials

```python
results = download(
    start_date="2024-01-01",
    end_date="2024-01-31",
    location=[172.1, -43.5],
    output_dir="data",
    username="your_username",
    password="your_password",
)
```

### Limit Downloads

```python
# Download only the 3 best matches
results = download(
    start_date="2024-01-01",
    end_date="2024-12-31",
    location=[172.1, -43.5],
    output_dir="data",
    cloud_max=10,
    max_products=3,
)
```

### Choose Product Type

```python
# Level-2A (atmospherically corrected)
results = download(
    start_date="2024-01-01",
    end_date="2024-01-31",
    location=[172.1, -43.5],
    output_dir="data",
    producttype="S2MSI2A",  # Default
)

# Level-1C (top-of-atmosphere)
results = download(
    start_date="2024-01-01",
    end_date="2024-01-31",
    location=[172.1, -43.5],
    output_dir="data",
    producttype="S2MSI1C",
)
```

## API Reference

### `download()`

Main function for downloading Sentinel-2 imagery.

**Parameters:**
- `start_date` (str): Start date in format "YYYY-MM-DD"
- `end_date` (str): End date in format "YYYY-MM-DD"
- `location` (list or tuple): [longitude, latitude]
- `bands` (list, optional): Band names for reference (extraction done in processing)
- `output_dir` (str): Directory to save files (default: "data")
- `cloud_max` (int): Maximum cloud coverage 0-100% (default: 30)
- `max_products` (int, optional): Limit number of downloads
- `username` (str, optional): Copernicus username
- `password` (str, optional): Copernicus password
- `producttype` (str): "S2MSI2A" (Level-2A, default) or "S2MSI1C" (Level-1C)

**Returns:**
List of dictionaries with:
- `id`: Product ID
- `title`: Product title
- `path`: Path to downloaded file
- `size`: File size
- `cloud_cover`: Cloud coverage percentage
- `date`: Acquisition date
- `requested_bands`: Band names (for reference)

## Design Philosophy

**Single Responsibility:** `sen2p` only downloads. Processing, band extraction, mosaicking, and analysis are handled by `rasteric`.

**Simple API:** One main function with sensible defaults.

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
- **Copernicus Hub:** https://scihub.copernicus.eu/
- **Sentinel-2:** https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-2
