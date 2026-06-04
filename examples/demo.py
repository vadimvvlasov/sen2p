"""
sen2p - Sentinel-2 Image Downloader Demo
"""

from sen2p import download


def main():
    """
    Demo script for sen2p

    Before running:
    1. Register at https://dataspace.copernicus.eu (NEW portal!)
    2. Set environment variables:
       export CDSE_USER="your_email@example.com"
       export CDSE_PASSWORD="your_password"

    Note: Old portal (scihub.copernicus.eu) shut down in October 2023.
    """

    print("=" * 60)
    print("sen2p - Sentinel-2 Image Downloader")
    print("=" * 60)
    print()

    # Example: Download Sentinel-2 imagery for Christchurch, New Zealand
    print("Downloading Sentinel-2 imagery...")
    print("Location: Christchurch, New Zealand [172.1, -43.5]")
    print("Date range: January 2024")
    print()

    try:
        results = download(
            start_date="2024-01-01",
            end_date="2024-01-31",
            location=[172.1, -43.5],
            output_dir="sentinel_data",
            cloud_max=20,
            max_products=1,  # Download just one for demo
        )

        if results:
            print(f"\n✓ Successfully downloaded {len(results)} product(s)")
            print()
            for r in results:
                print(f"  Product: {r['title']}")
                print(f"  Cloud cover: {r['cloud_cover']}%")
                print(f"  Date: {r['date']}")
                print(f"  Size: {r['size']}")
                print(f"  Path: {r['path']}")
                print()

            print("Next steps:")
            print("  • Use rasteric to process the downloaded imagery")
            print("  • See INTEGRATION.md for complete workflows")
            print("  • See example.py for more usage examples")
        else:
            print("✗ No products found matching criteria")
            print("  Try:")
            print("  • Expanding date range")
            print("  • Increasing cloud_max")
            print("  • Checking location coordinates")

    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        print()
        print("⚠️  IMPORTANT: Old portal shut down in October 2023!")
        print()
        print("Register at NEW portal:")
        print("  https://dataspace.copernicus.eu")
        print()
        print("Then set credentials:")
        print("  export CDSE_USER='your_email@example.com'")
        print("  export CDSE_PASSWORD='your_password'")
        print()
        print("Alternative variable names also work:")
        print("  export COPERNICUS_USER='your_email@example.com'")
        print("  export COPERNICUS_PASSWORD='your_password'")
    except RuntimeError as e:
        print(f"✗ Download error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()
