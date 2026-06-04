# Changelog

All notable changes to sen2p will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-06-04

### Added
- **Native CDSE Implementation:** Complete native implementation of Copernicus Data Space Ecosystem API
  - `CDSEDownloader` class with OAuth2 authentication
  - Direct OData v1 API queries
  - Efficient attribute expansion (`$expand=Attributes`)
  - Geographic footprint filtering with WKT POLYGON parsing
  - Cloud cover filtering
  - Progress bars for downloads
  - Automatic result sorting by cloud cover and date
- Export `CDSEDownloader` in main `__init__.py`
- Comprehensive CDSE implementation documentation
- Working examples with `CDSEDownloader`
- English translations for all scripts

### Changed
- **BREAKING:** Recommended API changed from `download()` to `CDSEDownloader`
- **BREAKING:** Product types changed from `S2MSI2A`/`S2MSI1C` to `MSIL2A`/`MSIL1C`
- Version bumped to 0.2.0
- All documentation updated to reflect working CDSE implementation
- README.md now shows `CDSEDownloader` examples
- QUICKSTART.md updated with native CDSE approach
- examples/basic.py rewritten to use `CDSEDownloader`
- CDSE_STATUS.md renamed and rewritten to celebrate success
- All Russian comments translated to English

### Fixed
- Authentication issues with CDSE (OAuth2 now working)
- Product type format for CDSE API
- Date filtering now done at API level
- Attribute retrieval optimized with single expanded query

### Deprecated
- `download()` function (sentinelsat-based) - May not work with CDSE
- Old product type format (`S2MSI2A`, `S2MSI1C`)

### Technical Details
- OAuth2 token authentication via `identity.dataspace.copernicus.eu`
- OData catalog queries via `catalogue.dataspace.copernicus.eu`
- Product downloads via `zipper.dataspace.copernicus.eu`
- Server-side date filtering for efficiency
- Single API call for products + attributes
- Bounding box geographic filtering
- Tested with multiple locations and date ranges

## [0.1.0] - 2026-06-04

### Changed
- **BREAKING:** Migrated to Copernicus Data Space Ecosystem (CDSE)
  - Old portal (scihub.copernicus.eu) shut down October 2023
  - New API endpoint: catalogue.dataspace.copernicus.eu
  - Now accepts email as username (required by CDSE)
  - Environment variables: Support both CDSE_* and COPERNICUS_* names
  - See MIGRATION_CDSE.md for migration guide

### Added
- Initial release of sen2p
- Core `download()` function for Sentinel-2 imagery
- Support for Copernicus Open Access Hub (via sentinelsat)
- Cloud coverage filtering
- Product type selection (L1C, L2A)
- Environment variable support for credentials
- Support for CDSE_USER and CDSE_PASSWORD environment variables
- Automatic fallback to COPERNICUS_USER/PASSWORD (backward compatibility)
- Migration guide (docs/MIGRATION_CDSE.md)
- Clear error messages for credential setup
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

### Fixed
- Updated all documentation with new registration URL
- Updated examples with new credentials format

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

[0.2.0]: https://github.com/yourusername/sen2p/releases/tag/v0.2.0
[0.1.0]: https://github.com/yourusername/sen2p/releases/tag/v0.1.0
