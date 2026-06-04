# sen2p Project Structure

Clean, organized structure for easy navigation.

## Directory Layout

```
sen2p/
├── sen2p/              # Core package
│   ├── __init__.py
│   └── downloader.py
│
├── docs/               # All documentation (12 files)
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── INTEGRATION.md
│   ├── SENTINEL2_REFERENCE.md
│   ├── FAQ.md
│   ├── CONTRIBUTING.md
│   ├── DEVELOPER_GUIDE.md
│   ├── PROJECT_STRUCTURE.md
│   ├── PUBLISHING.md
│   ├── SUMMARY.md
│   ├── INDEX.md
│   └── PROJECT_SUMMARY.txt
│
├── examples/           # Usage examples
│   ├── README.md
│   ├── demo.py         # Quick demo
│   └── basic.py        # Basic examples
│
├── tests/              # Test suite
│   ├── README.md
│   └── test_imports.py
│
├── README.md           # Main documentation
├── CHANGELOG.md        # Version history
├── LICENSE             # MIT License
├── pyproject.toml      # Package configuration
├── .env.example        # Credentials template
├── .gitignore          # Git ignore rules
└── uv.lock             # Dependency lock
```

## Quick Start

1. **Installation:** See root `README.md`
2. **Quick Guide:** See `docs/QUICKSTART.md`
3. **Examples:** See `examples/`
4. **Full Docs:** See `docs/`

## Key Files

### Root Level (Clean!)
- `README.md` - Main documentation and API reference
- `CHANGELOG.md` - What changed in each version
- `LICENSE` - MIT License
- `pyproject.toml` - Package configuration (with Ruff + mypy)

### Core Package (`sen2p/`)
- `__init__.py` - Exports `download()` function
- `downloader.py` - All download logic

### Documentation (`docs/`)
Organized by purpose:
- **Getting Started:** QUICKSTART.md, SUMMARY.md
- **User Guides:** INTEGRATION.md, SENTINEL2_REFERENCE.md, FAQ.md
- **Developer:** CONTRIBUTING.md, DEVELOPER_GUIDE.md, PROJECT_STRUCTURE.md, PUBLISHING.md
- **Reference:** INDEX.md, PROJECT_SUMMARY.txt

### Examples (`examples/`)
- `demo.py` - Quick demonstration
- `basic.py` - Multiple usage patterns
- `README.md` - How to run examples

### Tests (`tests/`)
- `test_imports.py` - Verify imports work
- `README.md` - Testing guide

## Navigation

### For Users
```
README.md → docs/QUICKSTART.md → examples/ → docs/INTEGRATION.md
```

### For Contributors
```
README.md → docs/CONTRIBUTING.md → docs/DEVELOPER_GUIDE.md → sen2p/
```

### For Documentation
```
docs/README.md → docs/INDEX.md → (any specific doc)
```

## Design Principles

1. **Clean Root** - Only essential files in root
2. **Organized Docs** - All documentation in `docs/`
3. **Clear Examples** - Runnable scripts in `examples/`
4. **Testable** - Tests isolated in `tests/`
5. **Discoverable** - README in each directory

## File Counts

- **Core Code:** 2 Python files
- **Documentation:** 12 files
- **Examples:** 2 scripts + README
- **Tests:** 1 test + README
- **Config:** 5 files (pyproject.toml, .gitignore, etc.)

Total: ~22 files (excluding .venv, .git)

## Benefits

✓ **Easy to Navigate** - Clear directory structure  
✓ **Clean Root** - Not cluttered with docs  
✓ **Self-Documenting** - README in each directory  
✓ **Scalable** - Easy to add more docs/examples/tests  
✓ **Standard** - Follows Python package conventions

## Related Files

- Root `README.md` - Entry point
- `docs/INDEX.md` - Complete documentation map
- `docs/PROJECT_STRUCTURE.md` - Detailed architecture
- `pyproject.toml` - Configuration with Ruff + mypy

---

**Last Updated:** 2026-06-04  
**Structure Version:** 1.0 (Organized)
