# Publishing Guide

How to publish sen2p to PyPI.

## Prerequisites

1. PyPI account (https://pypi.org/account/register/)
2. API token from PyPI (https://pypi.org/manage/account/token/)
3. uv installed locally

## Pre-Release Checklist

- [ ] All tests pass (`uv run test_import.py`)
- [ ] Version updated in `pyproject.toml`
- [ ] Version updated in `sen2p/__init__.py`
- [ ] `CHANGELOG.md` updated with release notes
- [ ] Documentation reviewed and updated
- [ ] Examples tested
- [ ] Git working directory is clean

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

Examples:
- `0.1.0` - Initial alpha release
- `0.2.0` - Add new features
- `0.2.1` - Fix bugs
- `1.0.0` - First stable release

## Build Package

```bash
# Clean old builds
rm -rf dist/

# Build wheel and source distribution
uv build

# Verify build
ls dist/
# Should see:
# - sen2p-0.1.0-py3-none-any.whl
# - sen2p-0.1.0.tar.gz
```

## Test Package Locally

```bash
# Install in a test environment
uv pip install dist/sen2p-0.1.0-py3-none-any.whl

# Test import
python -c "from sen2p import download; print('OK')"

# Uninstall
uv pip uninstall sen2p
```

## Publish to TestPyPI (Recommended First)

TestPyPI is a separate instance for testing uploads.

```bash
# Configure TestPyPI token
# Add to ~/.pypirc:
[testpypi]
  username = __token__
  password = pypi-your-testpypi-token-here

# Upload to TestPyPI
uv publish --publish-url https://test.pypi.org/legacy/

# Test installation from TestPyPI
uv pip install --index-url https://test.pypi.org/simple/ sen2p

# Verify
python -c "from sen2p import download; print('OK')"
```

## Publish to PyPI (Production)

**⚠️ Warning:** This cannot be undone for the same version number!

```bash
# Configure PyPI token
# Add to ~/.pypirc:
[pypi]
  username = __token__
  password = pypi-your-real-pypi-token-here

# Upload to PyPI
uv publish

# Or with twine
pip install twine
twine upload dist/*
```

## Post-Release

### 1. Tag Release in Git

```bash
# Create tag
git tag v0.1.0

# Push tag
git push origin v0.1.0
```

### 2. Create GitHub Release

1. Go to repository releases page
2. Click "Create a new release"
3. Select tag `v0.1.0`
4. Title: `v0.1.0`
5. Description: Copy from CHANGELOG.md
6. Attach build artifacts (optional)
7. Publish

### 3. Verify Installation

```bash
# Wait a few minutes for PyPI to propagate
# Then test fresh install
pip install sen2p

# Or with uv
uv add sen2p
```

### 4. Update Documentation

If you have documentation site:
- Update version numbers
- Regenerate API docs
- Deploy updated docs

### 5. Announce Release

- Update README.md if needed
- Post on social media (optional)
- Update any dependent projects

## Troubleshooting

### "File already exists"

You uploaded this version before. PyPI doesn't allow re-uploading:
- Increment version number
- Rebuild and re-upload

### "Invalid distribution"

Check:
- `pyproject.toml` is valid
- All files are included
- Build with `uv build` again

### "Upload failed"

Check:
- API token is correct
- Token has upload permissions
- Internet connection is stable

### Testing Failed After Upload

Issues to check:
- Dependencies correctly specified
- Package structure is correct
- `__init__.py` exports are correct

## Alternative: Manual Upload with Twine

```bash
# Install twine
pip install twine

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## Configuration Files

### ~/.pypirc

```ini
[distutils]
  index-servers =
    pypi
    testpypi

[pypi]
  username = __token__
  password = pypi-your-production-token

[testpypi]
  username = __token__
  password = pypi-your-test-token
  repository = https://test.pypi.org/legacy/
```

## Security Notes

- **Never commit API tokens** to git
- Use environment variables for CI/CD
- Rotate tokens periodically
- Use separate tokens for test vs production
- Restrict token scope to "Upload packages" only

## CI/CD (Future)

Example GitHub Actions workflow:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      - name: Build
        run: uv build
      - name: Publish
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: |
          pip install twine
          twine upload dist/*
```

## Version Management Strategy

### During Development (0.x.x)
- Breaking changes allowed
- Major version stays at 0
- Increment minor for features
- Increment patch for fixes

### After 1.0.0
- Breaking changes → increment major
- New features → increment minor
- Bug fixes → increment patch
- Follow semver strictly

## Release Cadence

Suggested schedule:
- **Patch releases**: As needed for critical bugs
- **Minor releases**: Every 2-4 weeks with new features
- **Major releases**: When breaking changes accumulated

## Questions?

- Check [Python Packaging Guide](https://packaging.python.org/)
- Check [uv documentation](https://docs.astral.sh/uv/)
- Check [PyPI help](https://pypi.org/help/)
