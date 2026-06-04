# Changelog

All notable changes to sen2p will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **BREAKING:** Migrated to Copernicus Data Space Ecosystem (CDSE)
  - Old portal (scihub.copernicus.eu) shut down October 2023
  - New API endpoint: catalogue.dataspace.copernicus.eu
  - Now accepts email as username (required by CDSE)
  - Environment variables: Support both CDSE_* and COPERNICUS_* names
  - See MIGRATION_CDSE.md for migration guide

### Added
- Support for CDSE_USER and CDSE_PASSWORD environment variables
- Automatic fallback to COPERNICUS_USER/PASSWORD (backward compatibility)
- Migration guide (docs/MIGRATION_CDSE.md)
- Clear error messages for credential setup

### Fixed
- Updated all documentation with new registration URL
- Updated examples with new credentials format

## [0.1.0] - 2026-06-04

### Added
- Initial release of sen2p
- Core `download()` function for Sentinel-2 imagery
- Support for Copernicus Open Access Hub
- Cloud coverage filtering
- Product type selection (L1C, L2A)
- Environment variable support for credentials
- `Sentinel2Downloader` class for API interaction
- Comprehensive documentation:
  - README.md with full API reference
  - QUICKSTART.md for quick setup
  - INTEGRATION.md for rasteric workflows
  - SENTINEL2_REFERENCE.md for band specifications
  - CONTRIBUTING.md for developers
  - DEVELOPER_GUIDE.md for code contributors
- Example scripts (main.py, example.py)
- Test script for import verification
- MIT License
- uv package manager support

### Dependencies
- sentinelsat >= 1.2.1
- requests >= 2.34.2
- Python >= 3.10

### Features
- Search Sentinel-2 products by location and date range
- Filter by cloud coverage percentage
- Limit number of downloads
- Download to specified output directory
- Return structured metadata compatible with rasteric
- Support for both Level-1C and Level-2A products
- Point-based location search
- MGRS tile support

[0.1.0]: https://github.com/yourusername/sen2p/releases/tag/v0.1.0
