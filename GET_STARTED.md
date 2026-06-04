# Get Started with sen2p

Quick guide to start using sen2p in 3 minutes.

## 1. Install

```bash
uv add sen2p
```

## 2. Get Credentials

Register (free): https://scihub.copernicus.eu/dhus/#/self-registration

Set environment variables:
```bash
export COPERNICUS_USER="your_username"
export COPERNICUS_PASSWORD="your_password"
```

## 3. Download

```python
from sen2p import download

results = download(
    start_date="2024-01-01",
    end_date="2024-01-31",
    location=[172.1, -43.5],  # [lon, lat]
    output_dir="data",
    cloud_max=20,
)

print(f"Downloaded {len(results)} images")
```

## 4. Done! 🎉

**Next Steps:**
- See [README.md](README.md) for API details
- Check [docs/](docs/) for full documentation
- Run [examples/](examples/) for more patterns
- Integrate with rasteric for processing

## Need Help?

- **Quick Start:** [docs/QUICKSTART.md](docs/QUICKSTART.md)
- **FAQ:** [docs/FAQ.md](docs/FAQ.md)
- **Examples:** [examples/demo.py](examples/demo.py)
- **Full Docs:** [docs/INDEX.md](docs/INDEX.md)
