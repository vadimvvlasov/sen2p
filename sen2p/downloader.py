"""
Core download functionality for Sentinel-2 imagery
"""

import os
from pathlib import Path
from typing import Any

from sentinelsat import SentinelAPI
from sentinelsat.sentinel import SentinelAPIError


class Sentinel2Downloader:
    """Handler for downloading Sentinel-2 imagery from Copernicus Data Space Ecosystem"""

    def __init__(self, username: str | None = None, password: str | None = None):
        """
        Initialize the downloader with Copernicus Data Space credentials.

        Args:
            username: CDSE username/email (or set COPERNICUS_USER or CDSE_USER env var)
            password: CDSE password (or set COPERNICUS_PASSWORD or CDSE_PASSWORD env var)

        Note:
            The old Copernicus Open Access Hub (scihub.copernicus.eu) was shut down
            in October 2023. This library now uses the new Copernicus Data Space
            Ecosystem (CDSE). Register at: https://dataspace.copernicus.eu
        """
        # Try new CDSE environment variables first, fall back to old names
        self.username = (
            username or os.getenv("CDSE_USER") or os.getenv("COPERNICUS_USER")
        )
        self.password = (
            password or os.getenv("CDSE_PASSWORD") or os.getenv("COPERNICUS_PASSWORD")
        )

        if not self.username or not self.password:
            raise ValueError(
                "Copernicus Data Space credentials required. "
                "Register at https://dataspace.copernicus.eu and set:\n"
                "  CDSE_USER (or COPERNICUS_USER) = your email\n"
                "  CDSE_PASSWORD (or COPERNICUS_PASSWORD) = your password\n"
                "Or pass username/password directly to download()."
            )

        # Use new Copernicus Data Space Ecosystem endpoint
        self.api = SentinelAPI(
            self.username,
            self.password,
            "https://catalogue.dataspace.copernicus.eu/odata/v1",
        )

    def search(
        self,
        location: tuple[float, float],
        start_date: str,
        end_date: str,
        cloud_max: int = 30,
        platform: str = "Sentinel-2",
        producttype: str = "S2MSI1C",
    ) -> dict[str, Any]:
        """
        Search for Sentinel-2 products.

        Args:
            location: (longitude, latitude) tuple
            start_date: Start date in format "YYYY-MM-DD"
            end_date: End date in format "YYYY-MM-DD"
            cloud_max: Maximum cloud coverage percentage (0-100)
            platform: Satellite platform name
            producttype: Product type (S2MSI1C for Level-1C, S2MSI2A for Level-2A)

        Returns:
            Dictionary of products found
        """
        lon, lat = location

        # Create a small footprint around the point (approximately 0.1 degree box)
        footprint = f"POINT({lon} {lat})"

        try:
            products = self.api.query(
                footprint,
                date=(start_date, end_date),
                platformname=platform,
                producttype=producttype,
                cloudcoverpercentage=(0, cloud_max),
            )
            return products
        except SentinelAPIError as e:
            raise RuntimeError(f"Search failed: {e}")

    def download_products(
        self,
        products: dict[str, Any],
        output_dir: str,
        max_products: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Download the specified products.

        Args:
            products: Dictionary of products from search()
            output_dir: Directory to save downloaded files
            max_products: Maximum number of products to download (downloads all if None)

        Returns:
            List of dictionaries with download information
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        results = []
        product_items = list(products.items())

        if max_products:
            product_items = product_items[:max_products]

        for product_id, product_info in product_items:
            try:
                # Download the product
                product_path = self.api.download(
                    product_id, directory_path=str(output_path)
                )

                results.append({
                    "id": product_id,
                    "title": product_info["title"],
                    "path": product_path["path"],
                    "size": product_info.get("size"),
                    "cloud_cover": product_info.get("cloudcoverpercentage"),
                    "date": product_info.get("beginposition"),
                })
            except Exception as e:
                print(f"Failed to download {product_id}: {e}")
                continue

        return results


def download(
    start_date: str,
    end_date: str,
    location: tuple[float, float],
    bands: list[str] | None = None,
    output_dir: str = "data",
    cloud_max: int = 30,
    max_products: int | None = None,
    username: str | None = None,
    password: str | None = None,
    producttype: str = "S2MSI2A",
) -> list[dict[str, Any]]:
    """
    Download Sentinel-2 imagery for a specified location and date range.

    Note:
        This library uses the new Copernicus Data Space Ecosystem (CDSE).
        Register at https://dataspace.copernicus.eu

        The old Copernicus Open Access Hub (scihub.copernicus.eu) shut down in October 2023.

    Args:
        start_date: Start date in format "YYYY-MM-DD"
        end_date: End date in format "YYYY-MM-DD"
        location: [longitude, latitude] or (longitude, latitude)
        bands: List of band names to extract (e.g., ["red", "nir", "blue"])
               Note: Band extraction happens in post-processing with rasteric
        output_dir: Directory to save downloaded files
        cloud_max: Maximum cloud coverage percentage (0-100)
        max_products: Maximum number of products to download
        username: CDSE username/email (optional if env var set)
        password: CDSE password (optional if env var set)
        producttype: Product type - "S2MSI1C" (Level-1C) or "S2MSI2A" (Level-2A, default)

    Returns:
        List of dictionaries containing download results with keys:
        - id: Product ID
        - title: Product title
        - path: Path to downloaded file
        - size: File size
        - cloud_cover: Cloud coverage percentage
        - date: Acquisition date
        - requested_bands: Band names (for reference)

    Example:
        >>> results = download(
        ...     start_date="2023-06-01",
        ...     end_date="2023-06-30",
        ...     location=[172.1, -43.5],
        ...     bands=["red", "nir"],
        ...     output_dir="data",
        ...     cloud_max=20,
        ... )
        >>> print(f"Downloaded {len(results)} products")
    """
    # Convert list to tuple if needed
    if isinstance(location, list):
        location = tuple(location)

    # Initialize downloader
    downloader = Sentinel2Downloader(username=username, password=password)

    # Search for products
    print(f"Searching for Sentinel-2 products from {start_date} to {end_date}")
    print(f"Location: {location}, Max cloud cover: {cloud_max}%")

    products = downloader.search(
        location=location,
        start_date=start_date,
        end_date=end_date,
        cloud_max=cloud_max,
        producttype=producttype,
    )

    print(f"Found {len(products)} products")

    if not products:
        print("No products found matching criteria")
        return []

    # Download products
    print(f"Downloading products to {output_dir}")
    results = downloader.download_products(
        products=products, output_dir=output_dir, max_products=max_products
    )

    print(f"Successfully downloaded {len(results)} products")

    # Add band information to results (for reference)
    for result in results:
        result["requested_bands"] = bands

    return results
