"""
sen2p - Sentinel-2 Image Downloader

A lightweight library for downloading Sentinel-2 satellite imagery.
Focuses on simple API for downloading images with cloud filtering.
"""

from .downloader import download

__version__ = "0.1.0"
__all__ = ["download"]
