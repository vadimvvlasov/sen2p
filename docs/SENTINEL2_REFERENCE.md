# Sentinel-2 Reference Guide

Quick reference for working with Sentinel-2 data in sen2p and rasteric.

## Product Types

### S2MSI1C (Level-1C)
- Top-of-atmosphere reflectance
- Orthorectified
- No atmospheric correction
- Use when: You need to apply custom atmospheric correction

### S2MSI2A (Level-2A) - **Recommended**
- Bottom-of-atmosphere reflectance
- Atmospherically corrected
- Scene classification included
- Use when: Most analysis tasks (NDVI, composites, etc.)

## Band Information

### All Bands (Level-2A)

| Band | Name | Resolution | Center Wavelength | Bandwidth | Use Case |
|------|------|------------|-------------------|-----------|----------|
| B01 | Coastal aerosol | 60m | 443 nm | 20 nm | Aerosol detection, coastal waters |
| B02 | Blue | 10m | 490 nm | 65 nm | True color, water bodies |
| B03 | Green | 10m | 560 nm | 35 nm | True color, vegetation |
| B04 | Red | 10m | 665 nm | 30 nm | True color, NDVI, vegetation |
| B05 | Vegetation Red Edge 1 | 20m | 705 nm | 15 nm | Vegetation stress, LAI |
| B06 | Vegetation Red Edge 2 | 20m | 740 nm | 15 nm | Vegetation analysis |
| B07 | Vegetation Red Edge 3 | 20m | 783 nm | 20 nm | Vegetation analysis |
| B08 | NIR | 10m | 842 nm | 115 nm | NDVI, vegetation, biomass |
| B8A | Vegetation Red Edge 4 | 20m | 865 nm | 20 nm | Water vapor reference |
| B09 | Water vapor | 60m | 945 nm | 20 nm | Atmospheric correction |
| B10 | SWIR - Cirrus | 60m | 1375 nm | 30 nm | Cirrus cloud detection |
| B11 | SWIR 1 | 20m | 1610 nm | 90 nm | Soil moisture, fire detection |
| B12 | SWIR 2 | 20m | 2190 nm | 180 nm | Fire detection, geology |

### Most Commonly Used Bands

For typical remote sensing workflows:

- **B02 (Blue)** - 10m - Water bodies, true color
- **B03 (Green)** - 10m - Vegetation, true color
- **B04 (Red)** - 10m - Vegetation, true color, NDVI
- **B08 (NIR)** - 10m - Vegetation indices, water detection
- **B11 (SWIR 1)** - 20m - Soil moisture, burn scars
- **B12 (SWIR 2)** - 20m - Fire, geology

## Common Band Combinations

### True Color (RGB)
```python
bands = [4, 3, 2]  # Red, Green, Blue
# Natural colors as seen by human eye
```

### False Color (CIR)
```python
bands = [8, 4, 3]  # NIR, Red, Green
# Vegetation appears red, useful for vegetation analysis
```

### Agriculture
```python
bands = [11, 8, 2]  # SWIR1, NIR, Blue
# Agricultural land use, soil moisture
```

### Atmospheric Penetration
```python
bands = [12, 11, 8]  # SWIR2, SWIR1, NIR
# Penetrates atmospheric conditions, useful for geology
```

### Healthy Vegetation
```python
bands = [8, 11, 2]  # NIR, SWIR1, Blue
# Emphasizes healthy vegetation
```

### Urban
```python
bands = [12, 11, 4]  # SWIR2, SWIR1, Red
# Urban areas, built environment
```

## Vegetation Indices

### NDVI (Normalized Difference Vegetation Index)
```python
NDVI = (NIR - Red) / (NIR + Red)
# Bands: (B08 - B04) / (B08 + B04)
# Range: -1 to +1
# Values:
#   < 0    : Water, clouds
#   0-0.2  : Bare soil, rock
#   0.2-0.5: Sparse vegetation
#   0.5-0.8: Dense vegetation
#   > 0.8  : Very dense vegetation
```

### EVI (Enhanced Vegetation Index)
```python
EVI = 2.5 * (NIR - Red) / (NIR + 6*Red - 7.5*Blue + 1)
# Bands: B08, B04, B02
# Better for high biomass areas
```

### NDWI (Normalized Difference Water Index)
```python
NDWI = (Green - NIR) / (Green + NIR)
# Bands: (B03 - B08) / (B03 + B08)
# Water detection
```

### NDMI (Normalized Difference Moisture Index)
```python
NDMI = (NIR - SWIR1) / (NIR + SWIR1)
# Bands: (B08 - B11) / (B08 + B11)
# Soil/vegetation moisture
```

## File Structure

Sentinel-2 products are delivered in .SAFE format:

```
S2A_MSIL2A_20230601T012345_N0500_R123_T59HPB_20230601T012345.SAFE/
├── GRANULE/
│   └── L2A_T59HPB_A012345_20230601T012345/
│       └── IMG_DATA/
│           ├── R10m/          # 10m resolution bands
│           │   ├── *_B02.jp2  # Blue
│           │   ├── *_B03.jp2  # Green
│           │   ├── *_B04.jp2  # Red
│           │   └── *_B08.jp2  # NIR
│           ├── R20m/          # 20m resolution bands
│           │   ├── *_B05.jp2
│           │   ├── *_B06.jp2
│           │   ├── *_B07.jp2
│           │   ├── *_B8A.jp2
│           │   ├── *_B11.jp2
│           │   └── *_B12.jp2
│           └── R60m/          # 60m resolution bands
│               ├── *_B01.jp2
│               └── *_B09.jp2
├── MTD_MSIL2A.xml            # Metadata
└── ...
```

## Product Naming Convention

```
S2A_MSIL2A_20230601T012345_N0500_R123_T59HPB_20230601T012345
│   │      │              │     │    │                │
│   │      │              │     │    │                └─ Product generation time
│   │      │              │     │    └─ Tile ID (MGRS)
│   │      │              │     └─ Relative orbit number
│   │      │              └─ Processing baseline
│   │      └─ Sensing start time
│   └─ Product level (L1C or L2A)
└─ Mission ID (S2A or S2B)
```

## Cloud Coverage

Cloud coverage percentage in metadata:
- **< 10%**: Ideal for most analysis
- **10-30%**: Usable, may need cloud masking
- **30-50%**: Limited use, significant masking needed
- **> 50%**: Generally unsuitable

sen2p allows filtering by `cloud_max` parameter.

## Temporal Resolution

- Sentinel-2A + 2B: ~5 day revisit at equator
- Single satellite: ~10 day revisit
- Higher latitudes: More frequent coverage due to orbit overlap

## Spatial Coverage

- Global coverage between 56°S and 84°N
- Tiles: 100x100 km (UTM projection)
- MGRS (Military Grid Reference System) tiling

## Data Volume

Typical sizes:
- Level-1C: ~600 MB compressed
- Level-2A: ~900 MB compressed
- Uncompressed: 1-2 GB

Plan storage accordingly when using sen2p!

## Usage with sen2p

```python
from sen2p import download

# Download Level-2A (recommended)
results = download(
    start_date="2023-06-01",
    end_date="2023-06-30",
    location=[172.1, -43.5],
    output_dir="data",
    cloud_max=20,
    producttype="S2MSI2A"  # Level-2A
)

# Access bands with rasteric
from rasteric import raster

# Extract specific bands
raster.extract_bands(
    results[0]["path"],
    bands=[4, 8],  # Red and NIR
    output_dir="bands"
)

# Calculate NDVI
raster.ndvi(
    results[0]["path"],
    "ndvi.tif",
    red_band=4,  # B04
    nir_band=8   # B08
)
```

## Resources

- [Official Sentinel-2 User Guide](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi)
- [Copernicus Open Access Hub](https://scihub.copernicus.eu/)
- [Sentinel-2 Spectral Response Functions](https://earth.esa.int/web/sentinel/user-guides/sentinel-2-msi/document-library)

## Tips

1. **Always use Level-2A** unless you have specific reasons for Level-1C
2. **10m bands are best** for most applications (B02, B03, B04, B08)
3. **Set cloud_max low** (10-20%) for better quality
4. **Check date coverage** - some areas have seasonal cloud issues
5. **MGRS tiles** - large areas may span multiple tiles, requiring mosaicking
