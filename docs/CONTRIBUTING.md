# Contributing to sen2p

Thanks for your interest in contributing!

## Development Setup

1. Clone the repository
2. Install dependencies with `uv`:

```bash
uv sync
```

3. Set up your Copernicus credentials:

```bash
cp .env.example .env
# Edit .env with your credentials
```

## Project Structure

```
sen2p/
├── sen2p/              # Main package
│   ├── __init__.py     # Public API
│   └── downloader.py   # Core download logic
├── example.py          # Usage examples
├── main.py             # Demo script
├── INTEGRATION.md      # Integration guide with rasteric
└── tests/              # Tests (coming soon)
```

## Design Principles

1. **Single Responsibility**: sen2p only downloads, processing is for rasteric
2. **Simple API**: Minimize configuration, maximize usability
3. **Clean Output**: Return structured data that's easy to pass to rasteric

## Making Changes

1. Keep the public API minimal - just `download()` function
2. Ensure output format is compatible with rasteric
3. Add docstrings for any new functions
4. Update README.md if adding features

## Testing

```bash
# Run the demo
uv run main.py

# Run examples
uv run example.py
```

## Code Style

- Follow PEP 8
- Use type hints
- Add docstrings for public functions
- Keep functions focused and small

## Questions?

Open an issue for discussion before starting major changes.
