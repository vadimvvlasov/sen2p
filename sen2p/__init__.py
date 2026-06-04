"""
sen2p - Sentinel-2 Image Downloader

A lightweight library for downloading Sentinel-2 satellite imagery
from the Copernicus Data Space Ecosystem (CDSE).

Uses native CDSE API with OAuth2 authentication for reliable downloads.
"""

from .cdse_downloader import CDSEDownloader
from .downloader import download  # Legacy sentinelsat-based (may not work)

__version__ = "0.2.0"
__all__ = ["CDSEDownloader", "download"]
