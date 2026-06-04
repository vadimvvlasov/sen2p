"""
Example usage of sen2p for downloading Sentinel-2 imagery using native CDSE API
"""

from sen2p.cdse_downloader import CDSEDownloader

# Example 1: Basic download
print("Example 1: Basic download with CDSEDownloader")
print("=" * 60)

# Initialize downloader (loads credentials from environment variables)
downloader = CDSEDownloader()

# Search for products
products = downloader.search(
    location=(172.1, -43.5),  # Christchurch, New Zealand (longitude, latitude)
    start_date="2024-01-01",
    end_date="2024-01-31",
    cloud_max=20,
    producttype="MSIL2A",  # Level-2A (atmospherically corrected)
)

print(f"Found {len(products)} products")

# Download products
results = downloader.download_products(
    products,
    output_dir="sentinel_data",
    max_products=1,  # Just download one for testing
)

print(f"\nDownloaded {len(results)} products:")
for r in results:
    print(f"  Title: {r['title']}")
    print(f"  Cloud cover: {r['cloud_cover']}%")
    print(f"  Date: {r['date']}")
    print(f"  Path: {r['path']}")
    print()


# Example 2: Download with explicit credentials
print("\nExample 2: Using explicit credentials")
print("=" * 60)

# downloader = CDSEDownloader(
#     username="your_email@example.com",
#     password="your_password"
# )
#
# products = downloader.search(
#     location=(172.1, -43.5),
#     start_date="2024-01-01",
#     end_date="2024-01-31",
#     cloud_max=10,
#     producttype="MSIL2A",
# )
#
# results = downloader.download_products(products, max_products=3)


# Example 3: Integration with rasteric (pseudo-code)
print("\nExample 3: Integration with rasteric")
print("=" * 60)
print("""
# After downloading with sen2p, process with rasteric:

from rasteric import raster
from sen2p.cdse_downloader import CDSEDownloader

# Download
downloader = CDSEDownloader()
products = downloader.search(
    location=(172.1, -43.5),
    start_date="2023-06-01",
    end_date="2023-06-30",
    cloud_max=20,
    producttype="MSIL2A",
)
results = downloader.download_products(products, max_products=1)

# Calculate NDVI from downloaded imagery
raster.ndvi(
    results[0]["path"],
    "ndvi.tif",
    red_band=4,  # Band 4 is Red in Sentinel-2
    nir_band=8   # Band 8 is NIR in Sentinel-2
)
""")
