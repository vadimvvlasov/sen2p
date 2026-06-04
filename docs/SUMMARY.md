# sen2p - Project Summary

## What is sen2p?

**sen2p** is a lightweight Python library for downloading Sentinel-2 satellite imagery from the Copernicus Open Access Hub. It provides a simple, focused API for searching and downloading satellite data with intelligent cloud filtering.

## Key Features

✓ **Simple API** - One main function with sensible defaults  
✓ **Cloud filtering** - Automatically filter images by cloud coverage  
✓ **Clean integration** - Designed to work seamlessly with `rasteric` for processing  
✓ **Free data** - Access to entire Sentinel-2 archive via Copernicus  
✓ **Type hints** - Full type annotation support  
✓ **Easy setup** - Uses `uv` for fast, reliable dependency management

## Quick Example

```python
from sen2p import download

results = download(
    start_date="2024-01-01",
    end_date="2024-01-31",
    location=[172.1, -43.5],
    output_dir="data",
    cloud_max=20
)
```

## Architecture

```
┌─────────────┐
│   sen2p     │  Downloads Sentinel-2 imagery
│  (download) │  • Search by location & date
└─────────────┘  • Filter by cloud coverage
       ↓          • Save raw .SAFE files
┌─────────────┐
│  rasteric   │  Processes imagery
│ (analysis)  │  • Band extraction
└─────────────┘  • NDVI calculation
                 • Mosaicking
```

**Philosophy:** Clear separation of concerns. sen2p downloads, rasteric processes.

## Project Structure

```
sen2p/
├── sen2p/                     # Package code
│   ├── __init__.py            # Public API
│   └── downloader.py          # Core functionality
│
├── Documentation
│   ├── README.md              # Full documentation
│   ├── QUICKSTART.md          # 5-minute guide
│   ├── INTEGRATION.md         # rasteric workflows
│   └── SENTINEL2_REFERENCE.md # Band specifications
│
├── Examples
│   ├── main.py                # Demo script
│   └── example.py             # Usage examples
│
└── Configuration
    ├── pyproject.toml         # Package config
    ├── .env.example           # Credentials template
    └── uv.lock                # Locked dependencies
```

## Installation

```bash
# With uv (recommended)
uv add sen2p

# With pip
pip install sen2p
```

## Requirements

- Python 3.10+
- Free Copernicus account (register at https://scihub.copernicus.eu)
- Dependencies: `sentinelsat`, `requests` (auto-installed)

## Core Function

### `download()`

```python
results = download(
    start_date="YYYY-MM-DD",
    end_date="YYYY-MM-DD",
    location=[lon, lat],
    bands=["red", "nir"],      # Optional, for reference
    output_dir="data",
    cloud_max=30,              # Max cloud % (0-100)
    max_products=None,         # Limit downloads
    username=None,             # Or use env vars
    password=None,
    producttype="S2MSI2A"      # Level-2A (default)
)
```

**Returns:** List of dicts with:
- `id`, `title`, `path`, `size`, `cloud_cover`, `date`, `requested_bands`

## Use Cases

### 1. NDVI Time Series
Download monthly imagery and calculate vegetation indices over time.

### 2. Change Detection
Compare vegetation, water, or land use between two dates.

### 3. Agricultural Monitoring
Track crop health and soil moisture throughout growing season.

### 4. Multi-spectral Analysis
Create false color composites, water indices, burn severity maps.

## Integration with rasteric

```python
from sen2p import download
from rasteric import raster

# 1. Download
results = download(
    start_date="2023-06-01",
    end_date="2023-06-30",
    location=[172.1, -43.5],
    output_dir="data",
    cloud_max=20
)

# 2. Process
raster.ndvi(
    results[0]["path"],
    "ndvi.tif",
    red_band=4,   # Sentinel-2 Band 4 = Red
    nir_band=8    # Sentinel-2 Band 8 = NIR
)
```

## Technology Stack

- **API Client:** sentinelsat
- **Data Source:** Copernicus Open Access Hub
- **Satellite:** Sentinel-2A & 2B (ESA)
- **Package Manager:** uv (recommended) or pip
- **Build System:** hatchling

## Sentinel-2 Quick Reference

**Most Common Bands (10m resolution):**
- B02 (Blue) - 490 nm
- B03 (Green) - 560 nm
- B04 (Red) - 665 nm
- B08 (NIR) - 842 nm

**Product Types:**
- **S2MSI2A** (Level-2A) - Atmospherically corrected ✓ Recommended
- **S2MSI1C** (Level-1C) - Top-of-atmosphere

**Typical File Size:** ~1GB per scene

## Getting Help

1. **Quick Start:** See `QUICKSTART.md` for 5-minute setup
2. **Full Docs:** See `README.md` for complete API reference
3. **Integration:** See `INTEGRATION.md` for workflows with rasteric
4. **Band Info:** See `SENTINEL2_REFERENCE.md` for spectral details
5. **Examples:** Run `uv run example.py` for code samples

## Development Status

- Version: 0.1.0 (Alpha)
- License: MIT
- Python: 3.10+
- Status: Active development

## Contributing

See `CONTRIBUTING.md` for development setup and guidelines.

## Related Links

- [Copernicus Hub](https://scihub.copernicus.eu/)
- [Sentinel-2 Mission](https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-2)
- [sentinelsat Documentation](https://sentinelsat.readthedocs.io/)

## Design Goals

1. **Simplicity:** One function, clear purpose
2. **Reliability:** Use battle-tested sentinelsat library
3. **Compatibility:** Seamless integration with rasteric
4. **Performance:** Efficient search and download
5. **Usability:** Sensible defaults, minimal configuration

## What sen2p Does NOT Do

- ❌ Band extraction (use rasteric)
- ❌ Image processing (use rasteric)
- ❌ NDVI calculation (use rasteric)
- ❌ Mosaicking (use rasteric)
- ❌ Reprojection (use rasteric)

**sen2p downloads. rasteric processes.**

## Next Steps

1. Install: `uv add sen2p`
2. Register at Copernicus Hub
3. Set credentials: `COPERNICUS_USER`, `COPERNICUS_PASSWORD`
4. Read `QUICKSTART.md`
5. Run `uv run main.py`

---

**Built with ❤️ for the remote sensing community**
