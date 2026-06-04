"""
Native CDSE downloader using direct API access
Based on Copernicus Data Space Ecosystem documentation
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Any

import requests


class CDSEDownloader:
    """Direct downloader for Copernicus Data Space Ecosystem"""

    TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
    CATALOG_URL = "https://catalogue.dataspace.copernicus.eu/odata/v1"
    ZIPPER_URL = "https://zipper.dataspace.copernicus.eu/odata/v1"

    def __init__(self, username: str | None = None, password: str | None = None):
        """
        Initialize CDSE downloader.

        Args:
            username: CDSE email (or set CDSE_USER/COPERNICUS_USER env var)
            password: CDSE password (or set CDSE_PASSWORD/COPERNICUS_PASSWORD env var)
        """
        self.username = (
            username or os.getenv("CDSE_USER") or os.getenv("COPERNICUS_USER")
        )
        self.password = (
            password or os.getenv("CDSE_PASSWORD") or os.getenv("COPERNICUS_PASSWORD")
        )

        if not self.username or not self.password:
            raise ValueError(
                "CDSE credentials required. Register at https://dataspace.copernicus.eu"
            )

        self.access_token = None
        self.session = requests.Session()

    def get_access_token(self) -> str:
        """
        Get OAuth2 access token from CDSE.

        Returns:
            Access token string
        """
        data = {
            "client_id": "cdse-public",
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
        }

        try:
            response = self.session.post(self.TOKEN_URL, data=data, timeout=30)

            # Debug: print response if error
            if response.status_code != 200:
                print(f"DEBUG: Status code: {response.status_code}")
                print(f"DEBUG: Response: {response.text[:500]}")

            response.raise_for_status()
            self.access_token = response.json()["access_token"]
            return self.access_token
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to get access token: {e}")

    def search(
        self,
        location: tuple[float, float],
        start_date: str,
        end_date: str,
        cloud_max: int = 30,
        collection: str = "SENTINEL-2",
        producttype: str = "MSIL2A",
    ) -> list[dict[str, Any]]:
        """
        Search for Sentinel-2 products using CDSE OData API.

        Args:
            location: (longitude, latitude) tuple
            start_date: Start date "YYYY-MM-DD"
            end_date: End date "YYYY-MM-DD"
            cloud_max: Maximum cloud coverage (0-100)
            collection: Collection name
            producttype: Product type (MSIL2A or MSIL1C)

        Returns:
            List of product dictionaries
        """
        if not self.access_token:
            self.get_access_token()

        lon, lat = location

        # Format dates for OData (ISO 8601 format without quotes)
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")

        # Build filters - now including date filters in OData query
        filters = [
            f"Collection/Name eq '{collection}'",
            f"contains(Name,'{producttype}')" if producttype else None,
            f"ContentDate/Start gt {start_dt.isoformat()}Z",
            f"ContentDate/Start lt {end_dt.isoformat()}Z",
        ]

        # Remove None values
        filters = [f for f in filters if f]
        filter_query = " and ".join(filters)

        # Build full URL - use $expand to get attributes in one request
        url = f"{self.CATALOG_URL}/Products?$filter={filter_query}&$top=1000&$expand=Attributes"

        print(f"DEBUG: Filter query:\n{filter_query}")

        headers = {"Authorization": f"Bearer {self.access_token}"}

        try:
            response = self.session.get(url, headers=headers, timeout=60)

            # Debug output
            print(f"DEBUG: Response status: {response.status_code}")

            response.raise_for_status()
            data = response.json()

            print(f"DEBUG: Total results from API: {len(data.get('value', []))}")

            # Get product IDs and attributes from expanded response
            products = []
            for item in data.get("value", []):
                # Extract attributes that came with $expand=Attributes
                attrs = {}
                for attr in item.get("Attributes", []):
                    attrs[attr.get("Name")] = attr.get("Value")

                products.append({
                    "id": item.get("Id"),
                    "name": item.get("Name", ""),
                    "size": item.get("ContentLength"),
                    "date": item.get("ContentDate", {}).get("Start", ""),
                    "attrs": attrs,  # Include attributes directly
                })

            print(f"DEBUG: Processing {len(products)} products with attributes...")

            # Filter by cloud cover and location
            filtered_products = []
            for i, product in enumerate(products[:200]):  # Limit to first 200
                attrs = product["attrs"]
                cloud_cover = attrs.get("cloudCover", 100)

                # Filter by cloud cover
                if cloud_cover <= cloud_max:
                    # Get footprint for geographic filtering
                    footprint = attrs.get("footprint", "")

                    # Simple check: if lon,lat in footprint bounds
                    if self._point_in_footprint(lon, lat, footprint):
                        filtered_products.append({
                            "id": product["id"],
                            "name": product["name"],
                            "size": product["size"],
                            "cloud_cover": cloud_cover,
                            "date": product["date"],
                            "download_url": None,  # Will use product ID for download
                        })

                if (i + 1) % 50 == 0:
                    print(f"DEBUG: Checked {i + 1}/{len(products)} products...")

            print(
                f"DEBUG: After cloud and location filtering: {len(filtered_products)} products"
            )

            # Sort by cloud cover (ascending) and date (descending)
            filtered_products.sort(
                key=lambda x: (
                    x.get("cloud_cover", 100),
                    -datetime.fromisoformat(x["date"].rstrip("Z")).timestamp(),
                )
            )

            return filtered_products

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Search failed: {e}")

    def _point_in_footprint(self, lon: float, lat: float, footprint_wkt: str) -> bool:
        """
        Rough check if point is within footprint bounds.

        Args:
            lon: Longitude
            lat: Latitude
            footprint_wkt: WKT POLYGON string

        Returns:
            True if point might be in footprint
        """
        if not footprint_wkt:
            return True  # No footprint info, include it

        # Extract coordinates from WKT
        # Format: POLYGON((lon1 lat1, lon2 lat2, ...))
        try:
            coords_str = footprint_wkt.split("((")[1].split("))")[0]
            coords = []
            for pair in coords_str.split(","):
                parts = pair.strip().split()
                if len(parts) == 2:
                    coords.append((float(parts[0]), float(parts[1])))

            if not coords:
                return True

            # Get bounding box
            lons = [c[0] for c in coords]
            lats = [c[1] for c in coords]

            min_lon, max_lon = min(lons), max(lons)
            min_lat, max_lat = min(lats), max(lats)

            # Check if point is in bounding box
            return min_lon <= lon <= max_lon and min_lat <= lat <= max_lat

        except Exception:
            return True  # If parsing fails, include it

    def download_product(
        self, product_id: str, output_dir: str = "data"
    ) -> dict[str, Any]:
        """
        Download a single product.

        Args:
            product_id: Product ID from search results
            output_dir: Directory to save the file

        Returns:
            Dictionary with download information
        """
        if not self.access_token:
            self.get_access_token()

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Build download URL
        download_url = f"{self.ZIPPER_URL}/Products({product_id})/$value"

        headers = {"Authorization": f"Bearer {self.access_token}"}

        try:
            print(f"Downloading product {product_id}...")

            response = self.session.get(
                download_url, headers=headers, stream=True, timeout=300
            )
            response.raise_for_status()

            # Get filename from Content-Disposition header
            content_disp = response.headers.get("Content-Disposition", "")
            if "filename=" in content_disp:
                filename = content_disp.split("filename=")[1].strip('"')
            else:
                filename = f"product_{product_id}.zip"

            filepath = output_path / filename

            # Download with progress
            total_size = int(response.headers.get("Content-Length", 0))
            downloaded = 0

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size:
                            progress = (downloaded / total_size) * 100
                            print(f"\rProgress: {progress:.1f}%", end="", flush=True)

            print(f"\n✓ Downloaded: {filepath}")

            return {
                "id": product_id,
                "path": str(filepath),
                "size": total_size,
            }

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Download failed: {e}")

    def download_products(
        self,
        products: list[dict[str, Any]],
        output_dir: str = "data",
        max_products: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Download multiple products.

        Args:
            products: List of products from search()
            output_dir: Directory to save files
            max_products: Maximum number to download

        Returns:
            List of download results
        """
        if max_products:
            products = products[:max_products]

        results = []
        for product in products:
            try:
                result = self.download_product(product["id"], output_dir)
                result.update({
                    "title": product["name"],
                    "cloud_cover": product["cloud_cover"],
                    "date": product["date"],
                })
                results.append(result)
            except Exception as e:
                print(f"Failed to download {product['name']}: {e}")
                continue

        return results
