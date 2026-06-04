# Migration to Copernicus Data Space Ecosystem (CDSE)

## ⚠️ Important Update - October 2023

**The old Copernicus Open Access Hub (`scihub.copernicus.eu`) was shut down in October 2023.**

All users must migrate to the new **Copernicus Data Space Ecosystem (CDSE)**.

---

## What Changed?

### Old System (Discontinued)
- **Portal:** https://scihub.copernicus.eu
- **API:** https://scihub.copernicus.eu/dhus
- **Status:** ❌ Shut down October 2023
- **Variables:** `COPERNICUS_USER`, `COPERNICUS_PASSWORD`

### New System (Current)
- **Portal:** https://dataspace.copernicus.eu
- **API:** https://catalogue.dataspace.copernicus.eu/odata/v1
- **Status:** ✅ Active
- **Variables:** `CDSE_USER`, `CDSE_PASSWORD` (or keep old names)

---

## Migration Steps

### 1. Create New Account

⚠️ **You MUST register a new account** - old credentials will NOT work!

1. Go to **https://dataspace.copernicus.eu**
2. Click **REGISTER** (top right)
3. Fill in the form:
   - First name
   - Last name
   - **Email** (this will be your username)
   - Password
   - Accept terms
4. Click **REGISTER**
5. **Check your email** and click "Verify email address"
6. Wait for confirmation (usually instant)

### 2. Update Environment Variables

**Option A: Use new variable names (recommended)**
```bash
# Linux / macOS
export CDSE_USER="your_email@example.com"
export CDSE_PASSWORD="your_password"

# Windows PowerShell
$env:CDSE_USER="your_email@example.com"
$env:CDSE_PASSWORD="your_password"
```

**Option B: Keep old variable names (also supported)**
```bash
# Linux / macOS  
export COPERNICUS_USER="your_email@example.com"
export COPERNICUS_PASSWORD="your_password"

# Windows PowerShell
$env:COPERNICUS_USER="your_email@example.com"
$env:COPERNICUS_PASSWORD="your_password"
```

**Option C: Update .env file**
```bash
# Copy example
cp .env.example .env

# Edit .env
CDSE_USER=your_email@example.com
CDSE_PASSWORD=your_password
```

### 3. Update Your Code

**No code changes needed!** 

sen2p automatically detects both old and new variable names:
- Checks `CDSE_USER` first
- Falls back to `COPERNICUS_USER`
- Same for password

Your existing code will work:
```python
from sen2p import download

results = download(
    start_date="2024-01-01",
    end_date="2024-01-31",
    location=[172.1, -43.5],
    output_dir="data",
)
```

---

## Key Differences

### Registration
| Old | New |
|-----|-----|
| Username-based | **Email-based** |
| scihub.copernicus.eu | **dataspace.copernicus.eu** |

### Authentication
| Old | New |
|-----|-----|
| Username + Password | **Email + Password** |
| Basic auth only | OAuth2 + Basic auth |

### API Endpoint
| Old | New |
|-----|-----|
| scihub.copernicus.eu/dhus | **catalogue.dataspace.copernicus.eu/odata/v1** |

### Data Access
| Feature | Old | New |
|---------|-----|-----|
| Sentinel-2 | ✅ | ✅ |
| Level-1C | ✅ | ✅ |
| Level-2A | ✅ | ✅ |
| Cloud filtering | ✅ | ✅ |
| Historical data | ✅ | ✅ |

---

## Troubleshooting

### "Authentication failed"
- ✅ Make sure you verified your email
- ✅ Use your **email address** as username (not a username)
- ✅ Check password is correct
- ✅ Re-register if needed (free)

### "Old credentials don't work"
- ❌ Old credentials **cannot be migrated**
- ✅ You **must create a new account** at dataspace.copernicus.eu
- ✅ Use your email as the username

### "Connection error"
- ❌ Don't use scihub.copernicus.eu (shut down)
- ✅ sen2p now uses dataspace.copernicus.eu automatically
- ✅ Update to latest sen2p version

### Environment variables not found
```python
# Check what's set
import os
print("CDSE_USER:", os.getenv("CDSE_USER"))
print("COPERNICUS_USER:", os.getenv("COPERNICUS_USER"))

# If both are None, set them:
export CDSE_USER="your_email@example.com"
export CDSE_PASSWORD="your_password"
```

---

## FAQ

### Do I need to re-download my data?
No. Downloaded .SAFE files remain valid.

### Can I use my old username?
No. The new system requires an email address.

### What about my API scripts?
sen2p handles the API change automatically. Just update your credentials.

### Is the data the same?
Yes. Same Sentinel-2 products, same quality.

### Is registration still free?
Yes! Copernicus Data Space Ecosystem is free.

### What about other Sentinel missions?
CDSE supports all Sentinel missions (1, 2, 3, 5P).

---

## Resources

- **New Portal:** https://dataspace.copernicus.eu
- **Documentation:** https://documentation.dataspace.copernicus.eu
- **API Guide:** https://documentation.dataspace.copernicus.eu/APIs.html
- **Help:** https://helpcenter.dataspace.copernicus.eu

---

## Timeline

- **Before October 2023:** Old system operational
- **October 2023:** Old system shut down
- **Now:** New CDSE system only

---

## Summary

**What you need to do:**

1. ✅ Register new account at dataspace.copernicus.eu
2. ✅ Verify your email
3. ✅ Update environment variables with your email
4. ✅ Keep using sen2p as before

**That's it!** sen2p handles the rest automatically.

---

*Last updated: 2026-06-04*
