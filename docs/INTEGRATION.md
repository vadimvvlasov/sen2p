# Integration Guide: sen2p + rasteric

This guide shows how `sen2p` and `rasteric` work together for a complete satellite imagery workflow.

## Philosophy

- **sen2p**: Downloads raw Sentinel-2 imagery from Copernicus
- **rasteric**: Processes downloaded imagery (band extraction, NDVI, mosaicking, etc.)

Two libraries, clear separation of concerns.

## Complete Workflow Example

```python
from sen2p import download
from rasteric import raster

# Step 1: Download Sentinel-2 imagery
results = download(
    start_date="2023-06-01",
    end_date="2023-06-30",
    location=[172.1, -43.5],  # Christchurch, NZ
    output_dir="sentinel_data",
    cloud_max=20,
    producttype="S2MSI2A"  # Level-2A (atmospherically corrected)
)

print(f"Downloaded {len(results)} scenes")

# Step 2: Process with rasteric
# Extract specific bands
for result in results:
    # Sentinel-2 band numbers:
    # Band 4 = Red (665 nm)
    # Band 8 = NIR (842 nm)
    # Band 3 = Green (560 nm)
    # Band 2 = Blue (490 nm)
    
    # Calculate NDVI
    ndvi_path = f"outputs/ndvi_{result['id']}.tif"
    raster.ndvi(
        result["path"],
        ndvi_path,
        red_band=4,
        nir_band=8
    )
    print(f"Created NDVI: {ndvi_path}")

# Step 3: Mosaic multiple scenes (if needed)
if len(results) > 1:
    scene_paths = [r["path"] for r in results]
    raster.mosaic(
        scene_paths,
        "outputs/mosaic.tif",
        bands=[4, 8]  # Red and NIR
    )
```

## Sentinel-2 Band Reference

For use with `rasteric` processing:

### Level-2A Bands (S2MSI2A)
| Band | Name | Resolution | Wavelength | Common Use |
|------|------|------------|------------|------------|
| B01 | Coastal aerosol | 60m | 443 nm | Aerosol detection |
| B02 | Blue | 10m | 490 nm | True color composite |
| B03 | Green | 10m | 560 nm | True color composite |
| B04 | Red | 10m | 665 nm | NDVI, true color |
| B05 | Red Edge 1 | 20m | 705 nm | Vegetation analysis |
| B06 | Red Edge 2 | 20m | 740 nm | Vegetation analysis |
| B07 | Red Edge 3 | 20m | 783 nm | Vegetation analysis |
| B08 | NIR | 10m | 842 nm | NDVI, vegetation |
| B8A | Narrow NIR | 20m | 865 nm | Water vapor |
| B09 | Water vapor | 60m | 945 nm | Cloud detection |
| B11 | SWIR 1 | 20m | 1610 nm | Soil moisture |
| B12 | SWIR 2 | 20m | 2190 nm | Fire detection |

## Common Processing Patterns

### Pattern 1: NDVI Time Series

```python
# Download monthly imagery for a growing season
results = download(
    start_date="2023-04-01",
    end_date="2023-09-30",
    location=[172.1, -43.5],
    output_dir="growing_season",
    cloud_max=15
)

# Calculate NDVI for each date
ndvi_series = []
for result in results:
    ndvi_path = f"ndvi/ndvi_{result['date'].strftime('%Y%m%d')}.tif"
    raster.ndvi(result["path"], ndvi_path, red_band=4, nir_band=8)
    ndvi_series.append({
        'date': result['date'],
        'path': ndvi_path,
        'cloud_cover': result['cloud_cover']
    })
```

### Pattern 2: Multi-spectral Composite

```python
# Download and create false color composite
results = download(
    start_date="2023-07-01",
    end_date="2023-07-31",
    location=[172.1, -43.5],
    output_dir="data",
    cloud_max=10,
    max_products=1
)

# Extract NIR, Red, Green for false color (shows vegetation in red)
raster.composite(
    results[0]["path"],
    "false_color.tif",
    bands=[8, 4, 3],  # NIR, Red, Green
    band_names=["NIR", "Red", "Green"]
)
```

### Pattern 3: Change Detection

```python
# Download imagery from two different dates
before = download(
    start_date="2023-01-01",
    end_date="2023-01-15",
    location=[172.1, -43.5],
    output_dir="data/before",
    cloud_max=10,
    max_products=1
)

after = download(
    start_date="2023-12-01",
    end_date="2023-12-15",
    location=[172.1, -43.5],
    output_dir="data/after",
    cloud_max=10,
    max_products=1
)

# Calculate NDVI for both
raster.ndvi(before[0]["path"], "ndvi_before.tif", red_band=4, nir_band=8)
raster.ndvi(after[0]["path"], "ndvi_after.tif", red_band=4, nir_band=8)

# Detect changes
raster.difference("ndvi_before.tif", "ndvi_after.tif", "ndvi_change.tif")
```

## Data Flow

```
┌─────────────┐
│ sen2p       │
│  download() │  → Raw .SAFE files
└─────────────┘     (Sentinel-2 products)
       ↓
┌─────────────┐
│ rasteric    │
│  extract()  │  → Individual bands as GeoTIFF
└─────────────┘
       ↓
┌─────────────┐
│ rasteric    │
│  ndvi()     │  → Vegetation indices
│  composite()│  → Multi-band composites
│  mosaic()   │  → Combined scenes
└─────────────┘
       ↓
    Analysis
```

## Tips

1. **Storage**: Sentinel-2 L2A products are ~1GB each. Plan storage accordingly.

2. **Cloud filtering**: Use `cloud_max=10` or lower for analysis-ready data. Higher values useful for time series with later filtering.

3. **Product type**: 
   - Use `S2MSI2A` (Level-2A) for analysis - atmospherically corrected
   - Use `S2MSI1C` (Level-1C) only if you need to apply custom atmospheric correction

4. **Location precision**: The `location` parameter searches an area around the point. For larger areas, consider multiple downloads or using a polygon footprint.

5. **Processing order**: 
   - Extract bands first with `rasteric.extract()`
   - Then apply indices or composites
   - Mosaic last if combining multiple scenes

## Error Handling

```python
try:
    results = download(
        start_date="2023-06-01",
        end_date="2023-06-30",
        location=[172.1, -43.5],
        output_dir="data",
        cloud_max=20
    )
    
    if not results:
        print("No imagery found matching criteria")
    else:
        # Process with rasteric
        for result in results:
            try:
                raster.ndvi(
                    result["path"],
                    f"ndvi_{result['id']}.tif",
                    red_band=4,
                    nir_band=8
                )
            except Exception as e:
                print(f"Processing failed for {result['id']}: {e}")
                
except ValueError as e:
    print(f"Configuration error: {e}")
except RuntimeError as e:
    print(f"Download failed: {e}")
```

## Next Steps

- See `rasteric` documentation for full processing capabilities
- Check `example.py` for basic usage
- Review Sentinel-2 documentation for band details and specifications
