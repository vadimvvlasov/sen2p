# GitHub Setup Guide

How to publish sen2p to GitHub.

## Quick Setup

### 1. Create GitHub Repository

Go to https://github.com/new and create a new repository:

- **Name:** `sen2p`
- **Description:** `Lightweight Python library for downloading Sentinel-2 satellite imagery`
- **Visibility:** Public (or Private)
- **Do NOT initialize** with README, .gitignore, or license (we already have them)

### 2. Add Remote

```bash
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/sen2p.git

# Verify
git remote -v
```

### 3. Push Code

```bash
# Push main branch
git push -u origin main

# Push tags
git push --tags
```

### 4. Verify

Visit `https://github.com/YOUR_USERNAME/sen2p` to see your repository.

## Repository Settings

### About Section

Add to repository description:

```
Description: Lightweight Python library for downloading Sentinel-2 satellite imagery
Website: https://pypi.org/project/sen2p/ (after publishing)
Topics: sentinel-2, satellite-imagery, remote-sensing, copernicus, python, earth-observation
```

### README Preview

GitHub will automatically display `README.md` from the root.

### Documentation

Consider enabling GitHub Pages for documentation:
1. Go to Settings → Pages
2. Source: Deploy from branch
3. Branch: main, folder: /docs
4. Visit: `https://YOUR_USERNAME.github.io/sen2p/`

## Creating Releases

### Manual Release

1. Go to Releases → Create a new release
2. Choose tag: `v0.1.0` (or create new)
3. Release title: `v0.1.0`
4. Description: Copy from `CHANGELOG.md`
5. Attach files: None needed (code is in repo)
6. Publish release

### Release Template

```markdown
# sen2p v0.1.0

Initial release of sen2p - Sentinel-2 imagery downloader.

## Features

- Download Sentinel-2 imagery from Copernicus Hub
- Cloud coverage filtering
- Simple `download()` API
- Support for Level-1C and Level-2A products
- Comprehensive documentation
- Working examples

## Installation

```bash
pip install sen2p
```

## Quick Start

```python
from sen2p import download

results = download(
    start_date="2024-01-01",
    end_date="2024-01-31",
    location=[172.1, -43.5],
    output_dir="data",
    cloud_max=20,
)
```

## Documentation

See [README.md](README.md) and [docs/](docs/) for full documentation.

## What's Changed

First release! 🎉

**Full Changelog**: https://github.com/YOUR_USERNAME/sen2p/commits/v0.1.0
```

## Branch Protection (Optional)

For collaborative development:

1. Go to Settings → Branches
2. Add rule for `main`:
   - Require pull request reviews
   - Require status checks
   - Require conversation resolution

## Issues and Pull Requests

### Issue Templates

Create `.github/ISSUE_TEMPLATE/`:

**bug_report.md:**
```markdown
---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
---

**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. ...
2. ...

**Expected behavior**
What you expected to happen.

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11]
- sen2p version: [e.g., 0.1.0]

**Additional context**
Any other context about the problem.
```

**feature_request.md:**
```markdown
---
name: Feature request
about: Suggest an idea for sen2p
title: '[FEATURE] '
labels: enhancement
---

**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives you've considered**
Other solutions you've considered.

**Additional context**
Any other context or screenshots.
```

### Pull Request Template

Create `.github/pull_request_template.md`:

```markdown
## Description

Describe your changes.

## Type of change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Checklist

- [ ] Code follows project style
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] Tests pass
- [ ] No new warnings

## Related Issues

Closes #(issue number)
```

## GitHub Actions (CI/CD)

### Basic Test Workflow

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12', '3.13']

    steps:
    - uses: actions/checkout@v3
    
    - name: Install uv
      run: curl -LsSf https://astral.sh/uv/install.sh | sh
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        uv sync
    
    - name: Run import tests
      run: |
        uv run tests/test_imports.py
    
    - name: Run ruff
      run: |
        uv run ruff check .
```

### Publish to PyPI Workflow

Create `.github/workflows/publish.yml`:

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
    
    - name: Build package
      run: uv build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        pip install twine
        twine upload dist/*
```

Add `PYPI_API_TOKEN` to repository secrets:
1. Settings → Secrets and variables → Actions
2. New repository secret
3. Name: `PYPI_API_TOKEN`
4. Value: Your PyPI token

## README Badges

Add to top of `README.md`:

```markdown
# sen2p

[![PyPI version](https://badge.fury.io/py/sen2p.svg)](https://pypi.org/project/sen2p/)
[![Python versions](https://img.shields.io/pypi/pyversions/sen2p.svg)](https://pypi.org/project/sen2p/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://github.com/YOUR_USERNAME/sen2p/workflows/Tests/badge.svg)](https://github.com/YOUR_USERNAME/sen2p/actions)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

Lightweight Python library for downloading Sentinel-2 satellite imagery.
```

## Social Preview

1. Go to Settings → General
2. Scroll to Social Preview
3. Upload image (1280x640px recommended)
4. Suggestion: Create image with project name and description

## Topics/Tags

Add these topics to your repository:

- `sentinel-2`
- `satellite-imagery`
- `remote-sensing`
- `copernicus`
- `python`
- `earth-observation`
- `geospatial`
- `imagery-download`
- `sentinel-hub`

## License Display

GitHub automatically detects `LICENSE` file and displays it.

## Collaboration

### Adding Collaborators

1. Settings → Collaborators
2. Add people
3. Choose permission level

### Code Owners (Optional)

Create `.github/CODEOWNERS`:

```
# Default owner for everything
* @YOUR_USERNAME

# Documentation
/docs/ @YOUR_USERNAME

# Core code
/sen2p/ @YOUR_USERNAME
```

## Discussions (Optional)

Enable Discussions for Q&A and community:

1. Settings → General → Features
2. Enable Discussions

Categories:
- Q&A
- Ideas
- Show and tell
- General

## Security

### Security Policy

Create `SECURITY.md`:

```markdown
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

Please report security vulnerabilities to: security@example.com

Do not open public issues for security vulnerabilities.

We will respond within 48 hours.
```

### Dependabot (Optional)

Create `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

## Useful Commands

```bash
# Clone your repo
git clone https://github.com/YOUR_USERNAME/sen2p.git

# Create branch
git checkout -b feature/my-feature

# Push branch
git push -u origin feature/my-feature

# Create PR
# Go to GitHub and click "Create Pull Request"

# Update from remote
git pull origin main

# Push tags
git push --tags
```

## Resources

- [GitHub Docs](https://docs.github.com/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [GitHub Pages](https://pages.github.com/)
- [About Releases](https://docs.github.com/en/repositories/releasing-projects-on-github)

## Next Steps

After GitHub setup:
1. Publish to PyPI (see `docs/PUBLISHING.md`)
2. Set up CI/CD with GitHub Actions
3. Enable Discussions for community
4. Add badges to README
5. Create first release
