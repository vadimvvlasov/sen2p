"""
Download Sentinel-2 imagery using native CDSE API
"""

import os
from pathlib import Path

from sen2p.cdse_downloader import CDSEDownloader


# Load credentials from .env file
def load_env():
    """Load variables from .env file"""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()


# Load .env
load_env()

# Parameters
LOCATION = [-51.2, -30.0]  # Porto Alegre, Rio Grande do Sul, Brazil
START_DATE = "2023-06-01"  # Extended period
END_DATE = "2023-12-31"
CLOUD_MAX = 50  # Increased acceptable cloud coverage
MAX_PRODUCTS = 3
OUTPUT_DIR = "sentinel_data_cdse"

print("=" * 70)
print("Downloading Sentinel-2 via CDSE API")
print("=" * 70)
print()
print(f"Location: {LOCATION}")
print(f"Period: {START_DATE} - {END_DATE}")
print(f"Max cloud coverage: {CLOUD_MAX}%")
print(f"Quantity: {MAX_PRODUCTS} best matches")
print()

try:
    # Create downloader
    downloader = CDSEDownloader()
    print("✓ Credentials loaded")

    # Get access token
    print("Getting access token...")
    downloader.get_access_token()
    print("✓ Access token obtained")
    print()

    # Search for products
    print("Searching for imagery...")
    products = downloader.search(
        location=tuple(LOCATION),
        start_date=START_DATE,
        end_date=END_DATE,
        cloud_max=CLOUD_MAX,
        collection="SENTINEL-2",
        producttype="MSIL2A",
    )

    print(f"✓ Found: {len(products)} images")
    print()

    if products:
        # Show first few
        print(f"Top {min(MAX_PRODUCTS, len(products))} images:")
        for i, p in enumerate(products[:MAX_PRODUCTS], 1):
            print(f"  {i}. {p['name']}")
            print(f"     Cloud coverage: {p['cloud_cover']:.1f}%")
            print(f"     Date: {p['date']}")
        print()

        # Download
        print(f"Starting download to {OUTPUT_DIR}/...")
        print()

        results = downloader.download_products(
            products, output_dir=OUTPUT_DIR, max_products=MAX_PRODUCTS
        )

        print()
        print("=" * 70)
        print(f"✓ Successfully downloaded: {len(results)} image(s)")
        print("=" * 70)
        print()

        for i, r in enumerate(results, 1):
            print(f"Image #{i}:")
            print(f"  Name: {r['title']}")
            print(f"  Cloud coverage: {r['cloud_cover']:.1f}%")
            print(f"  Date: {r['date']}")
            print(f"  Path: {r['path']}")
            print()

        print("Next steps:")
        print("  • Unzip the .zip files")
        print("  • Process with rasteric")
        print("  • Calculate NDVI or other indices")

    else:
        print("=" * 70)
        print("✗ No images found")
        print("=" * 70)
        print()
        print("Try:")
        print("  • Expand the date range")
        print("  • Increase cloud_max")
        print("  • Check coordinates")

except ValueError as e:
    print("=" * 70)
    print("✗ Configuration error")
    print("=" * 70)
    print()
    print(str(e))
    print()
    print("Register at: https://dataspace.copernicus.eu")
    print()
    print("Then set:")
    print("  export CDSE_USER='your_email@example.com'")
    print("  export CDSE_PASSWORD='your_password'")

except RuntimeError as e:
    print("=" * 70)
    print("✗ Runtime error")
    print("=" * 70)
    print()
    print(f"Details: {e}")
    print()
    print("Possible causes:")
    print("  • Invalid credentials")
    print("  • Network issues")
    print("  • Server temporarily unavailable")

except Exception as e:
    print("=" * 70)
    print("✗ Unexpected error")
    print("=" * 70)
    print()
    print(f"Error: {e}")
    print()
    print("If the problem persists:")
    print("  • Check internet connection")
    print("  • Verify credentials")
    print("  • Review documentation")

print()
print("=" * 70)
