# Copernicus Data Space Ecosystem - Current Status

## ⚠️ Important Information

### CDSE Migration Status

**Date:** 2026-06-04  
**Status:** In Progress

### What We Know

1. **Old System Shut Down**
   - `scihub.copernicus.eu` closed in October 2023
   - Old API no longer accessible

2. **New System Active**
   - Portal: https://dataspace.copernicus.eu
   - Registration: Working ✅
   - API: https://catalogue.dataspace.copernicus.eu

3. **sentinelsat Library**
   - Current version (1.2.1) was built for old API
   - CDSE support is being added
   - May require newer version or alternative approach

### Current Situation

The `sentinelsat` library we use is still being updated for full CDSE compatibility.

**What works:**
- ✅ Registration at dataspace.copernicus.eu
- ✅ Account creation
- ✅ Credential loading

**What needs attention:**
- ⚠️ API authentication (403 Forbidden errors)
- ⚠️ May need OAuth2 tokens instead of basic auth
- ⚠️ Waiting for sentinelsat library updates

### Recommendations

#### Option 1: Wait for sentinelsat Update
Check for updates:
```bash
uv add --upgrade sentinelsat
```

#### Option 2: Use Alternative Tools

**A. Use Copernicus Browser**
- Manual download: https://browser.dataspace.copernicus.eu
- Web interface, no programming needed

**B. Use cdsetool (Python)**
```bash
pip install cdsetool
```

**C. Use sentinelhub-py**
```bash
pip install sentinelhub
```

#### Option 3: Direct API Access

Use CDSE API directly with requests:
```python
import requests

# Get access token
token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
data = {
    "grant_type": "password",
    "username": "your_email",
    "password": "your_password",
    "client_id": "cdse-public",
}

response = requests.post(token_url, data=data)
access_token = response.json()["access_token"]

# Use token for API calls
headers = {"Authorization": f"Bearer {access_token}"}
```

### For sen2p Users

We are actively monitoring the situation and will update sen2p when:
1. sentinelsat adds full CDSE support, OR
2. We implement direct CDSE API support

### Check for Updates

Monitor these resources:
- sentinelsat: https://github.com/sentinelsat/sentinelsat
- CDSE docs: https://documentation.dataspace.copernicus.eu
- sen2p: Check for updates

### Workaround

While waiting for full CDSE support:

1. **Manual Download**
   - Go to https://browser.dataspace.copernicus.eu
   - Search for your area
   - Download manually
   - Process with rasteric

2. **Alternative Libraries**
   - Try `sentinelhub-py` or `cdsetool`
   - They may have better CDSE support

### Status Updates

**We will update sen2p as soon as:**
- sentinelsat releases CDSE-compatible version
- OR we implement native CDSE support

### Questions?

Check:
- CDSE Documentation: https://documentation.dataspace.copernicus.eu
- sentinelsat Issues: https://github.com/sentinelsat/sentinelsat/issues
- CDSE Help Center: https://helpcenter.dataspace.copernicus.eu

---

**Last Updated:** 2026-06-04  
**Next Review:** When sentinelsat updates

This is a temporary situation during the CDSE migration period.
