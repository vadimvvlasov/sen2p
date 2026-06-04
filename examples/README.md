# sen2p Examples

Example scripts demonstrating sen2p usage with the native CDSE API.

## Available Examples

### basic.py ✅ **Recommended**

**Native CDSE implementation** - Shows the working approach.

```bash
uv run python examples/basic.py
```

**What it includes:**
- Using `CDSEDownloader` class
- OAuth2 authentication (automatic)
- Searching for products
- Downloading imagery
- Integration with rasteric (pseudo-code)

**This example works reliably with CDSE.**

---

### demo.py ⚠️ **Legacy**

**Old sentinelsat-based example** - May not work due to CDSE migration.

Uses the old `download()` function which may return 403 Forbidden errors.

For working examples, **use basic.py instead**.

---

## Before Running

⚠️ **Important:** Old portal (`scihub.copernicus.eu`) shut down in October 2023.

### 1. Register at CDSE

**Register** at the NEW portal:  
**https://dataspace.copernicus.eu**

1. Click **REGISTER** and fill the form
2. **Verify your email** (check spam folder!)

### 2. Set Credentials

```bash
export CDSE_USER="your_email@example.com"
export CDSE_PASSWORD="your_password"
```

Or create a `.env` file in the project root:
```
CDSE_USER=your_email@example.com
CDSE_PASSWORD=your_password
```

Alternative variable names (also supported):
```bash
export COPERNICUS_USER="your_email@example.com"
export COPERNICUS_PASSWORD="your_password"
```

### 3. Run Example

```bash
uv run python examples/basic.py
```

---

## Creating Your Own Scripts

### Basic Pattern

```python
from sen2p.cdse_downloader import CDSEDownloader

# Initialize downloader
downloader = CDSEDownloader()

# Search for products
products = downloader.search(
    location=(172.1, -43.5),  # (longitude, latitude)
    start_date="2024-01-01",
    end_date="2024-01-31",
    cloud_max=20,
    producttype="MSIL2A",  # Level-2A (atmospherically corrected)
)

print(f"Found {len(products)} products")

# Download
results = downloader.download_products(
    products,
    output_dir="data",
    max_products=3,  # Download 3 best matches
)

# Use the results
for result in results:
    print(f"Downloaded: {result['title']}")
    print(f"Path: {result['path']}")
    print(f"Clouds: {result['cloud_cover']}%")
```

---

## Common Patterns

### Pattern 1: Time Series

```python
from sen2p.cdse_downloader import CDSEDownloader

downloader = CDSEDownloader()

# Download imagery across a year
products = downloader.search(
    location=(172.1, -43.5),
    start_date="2024-01-01",
    end_date="2024-12-31",
    cloud_max=15,
)

results = downloader.download_products(
    products,
    output_dir="timeseries",
    max_products=12,  # One per month
)
```

### Pattern 2: Multiple Locations

```python
from sen2p.cdse_downloader import CDSEDownloader

downloader = CDSEDownloader()

locations = {
    "christchurch": (172.1, -43.5),
    "wellington": (174.8, -41.3),
}

for name, coords in locations.items():
    products = downloader.search(
        location=coords,
        start_date="2024-01-01",
        end_date="2024-01-31",
        cloud_max=20,
    )
    
    results = downloader.download_products(
        products,
        output_dir=f"data/{name}",
        max_products=3,
    )
    
    print(f"{name}: Downloaded {len(results)} products")
```

### Pattern 3: With rasteric Processing

```python
from sen2p.cdse_downloader import CDSEDownloader
# from rasteric import raster  # Uncomment when rasteric is available

downloader = CDSEDownloader()

# Download
products = downloader.search(
    location=(172.1, -43.5),
    start_date="2024-06-01",
    end_date="2024-06-30",
    cloud_max=20,
)

results = downloader.download_products(products, max_products=5)

# Process each scene (pseudo-code)
# for result in results:
#     raster.ndvi(
#         result["path"],
#         f"ndvi_{result['id']}.tif",
#         red_band=4,  # Red
#         nir_band=8   # NIR
#     )
```

### Pattern 4: Different Product Types

```python
from sen2p.cdse_downloader import CDSEDownloader

downloader = CDSEDownloader()

# Level-2A (atmospherically corrected) - Recommended
products_l2a = downloader.search(
    location=(172.1, -43.5),
    start_date="2024-01-01",
    end_date="2024-01-31",
    producttype="MSIL2A",  # Default
)

# Level-1C (top-of-atmosphere)
products_l1c = downloader.search(
    location=(172.1, -43.5),
    start_date="2024-01-01",
    end_date="2024-01-31",
    producttype="MSIL1C",
)
```

---

## Product Types

### ✅ Correct (CDSE Format)
- `MSIL2A` - Level-2A (atmospherically corrected) - **Recommended**
- `MSIL1C` - Level-1C (top-of-atmosphere)

### ❌ Wrong (Old Format - Don't Use)
- `S2MSI2A` - Not recognized by CDSE
- `S2MSI1C` - Not recognized by CDSE

---

## Need More Help?

- **Documentation:** See `../docs/` directory
- **Quick Start:** `../docs/QUICKSTART.md`
- **CDSE Implementation:** `../CDSE_STATUS.md`
- **API Reference:** `../README.md`
- **FAQ:** `../docs/FAQ.md`

---

## Troubleshooting

### "Invalid credentials"
- Verify you've registered at https://dataspace.copernicus.eu
- Check your email is verified
- Ensure environment variables are set:
  ```bash
  echo $CDSE_USER
  echo $CDSE_PASSWORD
  ```

### "No products found"
- Expand the date range
- Increase `cloud_max` parameter (try 50 or 100)
- Verify coordinates are (longitude, latitude) not (latitude, longitude)
- Check if the location has Sentinel-2 coverage

### "Download failed"
- Check internet connection
- Verify disk space available
- Token may have expired - script will retry automatically
- Try reducing `max_products` to test

### "Import error: No module named 'sen2p'"
- Ensure sen2p is installed: `uv add sen2p`
- Check you're in the correct virtual environment

---

Happy downloading! 🛰️

**Note:** Use `CDSEDownloader` for reliable downloads with the native CDSE API.
