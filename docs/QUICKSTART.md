# Quick Start Guide

Get started with sen2p in 5 minutes.

## 1. Installation

```bash
uv add sen2p
```

Or with pip:
```bash
pip install sen2p
```

## 2. Get Copernicus Credentials

⚠️ **Important Update:** The old portal (`scihub.copernicus.eu`) shut down in October 2023.

1. **Register** (free) at the new portal: **https://dataspace.copernicus.eu**
2. Click **REGISTER** in the top right
3. Fill in: name, email, password
4. Accept terms and click **REGISTER**
5. **Verify your email** (check spam folder!)
6. Set environment variables:

```bash
export CDSE_USER="your_email@example.com"
export CDSE_PASSWORD="your_password"
```

Alternative variable names (also supported):
```bash
export COPERNICUS_USER="your_email@example.com"
export COPERNICUS_PASSWORD="your_password"
```

## 3. Download Your First Image

```python
from sen2p.cdse_downloader import CDSEDownloader

# Initialize downloader (loads credentials from environment)
downloader = CDSEDownloader()

# Search for products
products = downloader.search(
    location=(172.1, -43.5),  # (longitude, latitude)
    start_date="2024-01-01",
    end_date="2024-01-31",
    cloud_max=20,
)

print(f"Found {len(products)} products")

# Download products
results = downloader.download_products(
    products,
    output_dir="data",
    max_products=3,  # Download 3 best matches
)

print(f"Downloaded {len(results)} images")
```

## 4. Process with rasteric

```python
from rasteric import raster

# Calculate NDVI
raster.ndvi(
    results[0]["path"],
    "ndvi.tif",
    red_band=4,  # Band 4 = Red
    nir_band=8,  # Band 8 = NIR
)
```

## Done! 🎉

**Next steps:**
- See [README.md](README.md) for full API documentation
- Check [INTEGRATION.md](INTEGRATION.md) for complete workflows
- Review [SENTINEL2_REFERENCE.md](SENTINEL2_REFERENCE.md) for band details
- Run `uv run example.py` for more examples

## Common Issues

### "No products found"
- Expand date range
- Increase `cloud_max`
- Check coordinates (longitude first!)

### "Invalid credentials"
- Verify email is confirmed
- Check username/password
- Set environment variables correctly

### "Download failed"
- Check internet connection
- Copernicus Hub might be down (check status)
- Try again later (API has rate limits)
