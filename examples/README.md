# sen2p Examples

Example scripts demonstrating how to use sen2p.

## Available Examples

### demo.py
**Quick demo script** - Shows basic download with error handling.

```bash
# Set your credentials first
export COPERNICUS_USER="your_username"
export COPERNICUS_PASSWORD="your_password"

# Run the demo
uv run examples/demo.py
```

**What it does:**
- Downloads one Sentinel-2 image for Christchurch, NZ
- Shows cloud coverage and metadata
- Demonstrates error handling
- Provides next steps

### basic.py
**Multiple usage examples** - Various use cases and patterns.

```bash
uv run examples/basic.py
```

**Includes:**
- Basic download
- Download with explicit credentials
- Integration with rasteric (pseudo-code)

## Before Running

1. **Register** at Copernicus Hub:  
   https://scihub.copernicus.eu/dhus/#/self-registration

2. **Confirm your email** (check spam folder)

3. **Set credentials:**
   ```bash
   export COPERNICUS_USER="your_username"
   export COPERNICUS_PASSWORD="your_password"
   ```

   Or create a `.env` file in the project root:
   ```
   COPERNICUS_USER=your_username
   COPERNICUS_PASSWORD=your_password
   ```

## Creating Your Own Examples

```python
from sen2p import download

# Download imagery
results = download(
    start_date="2024-01-01",
    end_date="2024-01-31",
    location=[172.1, -43.5],  # [longitude, latitude]
    output_dir="data",
    cloud_max=20
)

# Use the results
for result in results:
    print(f"Downloaded: {result['title']}")
    print(f"Path: {result['path']}")
    print(f"Clouds: {result['cloud_cover']}%")
```

## Common Patterns

### Pattern 1: Time Series
```python
# Download monthly imagery
import datetime

start = datetime.date(2024, 1, 1)
end = datetime.date(2024, 12, 31)

results = download(
    start_date=start.isoformat(),
    end_date=end.isoformat(),
    location=[172.1, -43.5],
    output_dir="timeseries",
    cloud_max=15
)
```

### Pattern 2: Multiple Locations
```python
locations = {
    "christchurch": [172.1, -43.5],
    "wellington": [174.8, -41.3],
}

for name, coords in locations.items():
    results = download(
        start_date="2024-01-01",
        end_date="2024-01-31",
        location=coords,
        output_dir=f"data/{name}",
        cloud_max=20
    )
```

### Pattern 3: With rasteric
```python
from sen2p import download
from rasteric import raster

# Download
results = download(
    start_date="2024-06-01",
    end_date="2024-06-30",
    location=[172.1, -43.5],
    output_dir="data",
    cloud_max=20
)

# Process each scene
for result in results:
    raster.ndvi(
        result["path"],
        f"ndvi_{result['id']}.tif",
        red_band=4,
        nir_band=8
    )
```

## Need More Help?

- **Documentation:** See `../docs/` directory
- **Quick Start:** `../docs/QUICKSTART.md`
- **Integration Guide:** `../docs/INTEGRATION.md`
- **FAQ:** `../docs/FAQ.md`

## Troubleshooting

**"No products found"**
- Expand date range
- Increase `cloud_max`
- Verify coordinates

**"Invalid credentials"**
- Check username/password
- Confirm email
- Check environment variables

**"Download failed"**
- Check internet connection
- Verify Copernicus Hub is online
- Try again later (rate limits)

---

Happy downloading! 🛰️
