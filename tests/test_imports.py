"""
Simple import test to verify package structure
"""


def test_imports():
    """Test that all imports work correctly"""

    print("Testing sen2p imports...")

    try:
        from sen2p import download

        print("✓ Successfully imported: download")
    except ImportError as e:
        print(f"✗ Failed to import download: {e}")
        return False

    try:
        from sen2p.downloader import Sentinel2Downloader

        print("✓ Successfully imported: Sentinel2Downloader")
    except ImportError as e:
        print(f"✗ Failed to import Sentinel2Downloader: {e}")
        return False

    try:
        import sentinelsat

        print(f"✓ sentinelsat version: {sentinelsat.__version__}")
    except ImportError as e:
        print(f"✗ sentinelsat not installed: {e}")
        return False

    print("\n✓ All imports successful!")
    print("\nPackage is ready to use.")
    print("\nNext steps:")
    print("  1. Set COPERNICUS_USER and COPERNICUS_PASSWORD")
    print("  2. Run: uv run examples/demo.py")
    print("  3. Check docs/QUICKSTART.md for usage guide")

    return True


if __name__ == "__main__":
    success = test_imports()
    exit(0 if success else 1)
