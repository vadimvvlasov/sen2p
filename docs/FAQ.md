# Frequently Asked Questions

## General Questions

### What is sen2p?

sen2p is a lightweight Python library for downloading Sentinel-2 satellite imagery from the Copernicus Open Access Hub. It focuses solely on downloading - processing is handled by its companion library, rasteric.

### Is sen2p free?

Yes! sen2p is open source (MIT license) and the Sentinel-2 data is free from Copernicus.

### Do I need a Copernicus account?

Yes, you need a free account to download data. Register at: https://scihub.copernicus.eu/dhus/#/self-registration

### What's the difference between sen2p and sentinelsat?

- **sentinelsat**: Low-level library for Copernicus API
- **sen2p**: High-level, simple API built on sentinelsat, designed for use with rasteric

sen2p provides a simpler interface and better integration with rasteric workflows.

## Installation & Setup

### How do I install sen2p?

```bash
# With uv (recommended)
uv add sen2p

# With pip
pip install sen2p
```

### What Python version do I need?

Python 3.10 or higher.

### How do I set up credentials?

```bash
export COPERNICUS_USER="your_username"
export COPERNICUS_PASSWORD="your_password"
```

Or pass them directly to `download()`:
```python
download(..., username="user", password="pass")
```

### Can I use a .env file?

Yes! Create a `.env` file:
```bash
COPERNICUS_USER=your_username
COPERNICUS_PASSWORD=your_password
```

Then load it in your code:
```python
from dotenv import load_dotenv
load_dotenv()

from sen2p import download
results = download(...)  # Will use env vars
```

## Using sen2p

### How do I download imagery for a location?

```python
from sen2p import download

results = download(
    start_date="2024-01-01",
    end_date="2024-01-31",
    location=[172.1, -43.5],  # [longitude, latitude]
    output_dir="data"
)
```

### No products found - what's wrong?

Try:
1. **Expand date range** - Maybe no imagery in that period
2. **Increase cloud_max** - Default is 30%, try 50-100%
3. **Check coordinates** - Make sure [lon, lat] not [lat, lon]
4. **Check location** - Some areas have limited coverage

### How do I filter by cloud coverage?

```python
results = download(
    ...,
    cloud_max=20  # Maximum 20% clouds
)
```

Values from 0-100. Lower = fewer clouds = better quality.

### What's the difference between Level-1C and Level-2A?

- **Level-1C (S2MSI1C)**: Top-of-atmosphere, no atmospheric correction
- **Level-2A (S2MSI2A)**: Bottom-of-atmosphere, atmospherically corrected ✓ Recommended

Use Level-2A unless you need to apply custom atmospheric correction.

```python
# Level-2A (default, recommended)
results = download(..., producttype="S2MSI2A")

# Level-1C
results = download(..., producttype="S2MSI1C")
```

### How do I limit downloads?

```python
results = download(
    ...,
    max_products=3  # Download only 3 best matches
)
```

### What format are the downloaded files?

Sentinel-2 products are in .SAFE format (a directory structure with JP2 images and XML metadata). Typical size: ~1GB per scene.

### How do I access specific bands?

sen2p downloads the full product. Use rasteric to extract bands:

```python
from sen2p import download
from rasteric import raster

results = download(...)

# Extract bands with rasteric
raster.extract_bands(
    results[0]["path"],
    bands=[4, 8],  # Red and NIR
    output_dir="bands"
)
```

## Integration with rasteric

### How do I calculate NDVI?

```python
from sen2p import download
from rasteric import raster

results = download(...)

raster.ndvi(
    results[0]["path"],
    "ndvi.tif",
    red_band=4,   # Band 4 = Red
    nir_band=8    # Band 8 = NIR
)
```

### Which bands should I use?

See `SENTINEL2_REFERENCE.md` for full details. Most common:

- **B02** (Blue) - Band 2 - 490nm - 10m
- **B03** (Green) - Band 3 - 560nm - 10m
- **B04** (Red) - Band 4 - 665nm - 10m
- **B08** (NIR) - Band 8 - 842nm - 10m

### Can I download and process in one script?

Yes! That's the intended workflow:

```python
from sen2p import download
from rasteric import raster

# Download
results = download(
    start_date="2024-01-01",
    end_date="2024-01-31",
    location=[172.1, -43.5],
    output_dir="data",
    cloud_max=20
)

# Process immediately
for result in results:
    raster.ndvi(
        result["path"],
        f"ndvi_{result['id']}.tif",
        red_band=4,
        nir_band=8
    )
```

## Errors & Troubleshooting

### "No products found matching criteria"

Solutions:
- Expand date range
- Increase `cloud_max` parameter
- Verify coordinates are correct
- Check if area has Sentinel-2 coverage

### "Invalid credentials"

Check:
- Username and password are correct
- Email is confirmed (check spam folder)
- Environment variables are set correctly
- No typos in credentials

### "Download failed"

Possible causes:
- Network connection issues
- Copernicus Hub is down (check https://scihub.copernicus.eu/)
- API rate limit reached (wait and retry)
- Disk space full

### Download is very slow

Sentinel-2 products are large (~1GB). Download speed depends on:
- Your internet connection
- Copernicus Hub load
- Geographic location

Tips:
- Download during off-peak hours
- Use `max_products` to limit downloads
- Download only what you need

### "Module not found: sen2p"

Make sure you installed it:
```bash
uv add sen2p
# or
pip install sen2p
```

And you're using the correct Python environment.

## Data & Storage

### How much disk space do I need?

- One Sentinel-2 scene: ~1GB compressed
- Plan accordingly for multiple downloads
- Use `max_products` to limit storage

### Can I delete the .SAFE files after processing?

Yes, once you've extracted what you need with rasteric, you can delete the .SAFE directories.

### How long is data retained on Copernicus?

Sentinel-2 data is archived indefinitely. All historical data since 2015 is available.

### What's the temporal resolution?

- With both Sentinel-2A and 2B: ~5 days
- Single satellite: ~10 days
- Higher latitudes: More frequent (orbit overlap)

## Advanced Usage

### Can I search by polygon instead of point?

Current version uses point-based search. Polygon support is planned for future releases.

For now, you can:
1. Download larger area
2. Crop with rasteric

### Can I download multiple locations at once?

Use a loop:

```python
locations = [
    [172.1, -43.5],  # Location 1
    [174.0, -41.3],  # Location 2
]

for loc in locations:
    results = download(
        start_date="2024-01-01",
        end_date="2024-01-31",
        location=loc,
        output_dir=f"data_{loc[0]}_{loc[1]}"
    )
```

### Can I download in parallel?

Not currently supported. Use sequential downloads or implement your own threading.

### How do I resume interrupted downloads?

Current version doesn't support resume. Future feature.

Workaround: Keep track of downloaded products and skip them:

```python
import os

results = download(...)

for result in results:
    output_file = result["path"]
    if os.path.exists(output_file):
        print(f"Skipping {output_file}")
        continue
    # Download...
```

## Development

### How can I contribute?

See `CONTRIBUTING.md` for guidelines.

### How do I report bugs?

Open an issue on GitHub with:
- What you tried to do
- What happened
- Error messages
- Python version
- sen2p version

### Is there a roadmap?

Planned features:
- Polygon footprint support
- Parallel downloads
- Download resume
- CLI tool
- Progress callbacks

## Comparison with Other Tools

### sen2p vs sentinelsat?

- **sentinelsat**: Full-featured API client, all Sentinel missions
- **sen2p**: Simplified, Sentinel-2 focused, rasteric integration

Use sen2p if you want simplicity. Use sentinelsat for advanced features.

### sen2p vs Google Earth Engine?

- **GEE**: Cloud-based, no downloads, built-in processing
- **sen2p**: Local downloads, local processing with rasteric

Use GEE for web-based apps. Use sen2p for offline/local workflows.

### Do I need both sen2p and rasteric?

- **sen2p alone**: Just downloading
- **rasteric alone**: If you already have imagery
- **Both together**: Complete workflow (recommended)

## Getting Help

### Where can I find examples?

- `QUICKSTART.md` - Quick start guide
- `INTEGRATION.md` - Full workflows
- `example.py` - Code examples
- `README.md` - Complete documentation

### Still have questions?

1. Check documentation files
2. Run `uv run example.py`
3. Check Sentinel-2 documentation
4. Open a GitHub issue
5. Check sentinelsat documentation (for API details)

## Useful Resources

- [Copernicus Hub](https://scihub.copernicus.eu/)
- [Sentinel-2 User Guide](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi)
- [sentinelsat docs](https://sentinelsat.readthedocs.io/)
- [SENTINEL2_REFERENCE.md](SENTINEL2_REFERENCE.md) - Band information
