"""
Example usage of sen2p for downloading Sentinel-2 imagery
"""

from sen2p import download

# Example 1: Basic download
print("Example 1: Basic download")
results = download(
    start_date="2024-01-01",
    end_date="2024-01-31",
    location=[172.1, -43.5],  # Christchurch, New Zealand
    output_dir="sentinel_data",
    cloud_max=20,
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
# results = download(
#     start_date="2024-01-01",
#     end_date="2024-01-31",
#     location=[172.1, -43.5],
#     output_dir="data",
#     username="your_username",
#     password="your_password",
#     cloud_max=10
# )


# Example 3: Integration with rasteric (pseudo-code)
# from rasteric import raster
#
# results = download(
#     start_date="2023-06-01",
#     end_date="2023-06-30",
#     location=[172.1, -43.5],
#     bands=["red", "nir"],
#     output_dir="data",
#     cloud_max=20
# )
#
# # Calculate NDVI from downloaded imagery
# raster.ndvi(
#     results[0]["path"],
#     "ndvi.tif",
#     red_band=4,  # Band 4 is Red in Sentinel-2
#     nir_band=8   # Band 8 is NIR in Sentinel-2
# )
