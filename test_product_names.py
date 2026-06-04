"""
Проверка имен продуктов Sentinel-2 в CDSE
"""

import os
from pathlib import Path

import requests


def load_env():
    """Загружает переменные из .env файла"""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()


load_env()

username = os.getenv("CDSE_USER")
password = os.getenv("CDSE_PASSWORD")

print("Анализ имен продуктов Sentinel-2")
print("=" * 70)
print()

# Get access token
token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
data = {
    "client_id": "cdse-public",
    "username": username,
    "password": password,
    "grant_type": "password",
}

response = requests.post(token_url, data=data, timeout=30)
access_token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {access_token}"}

print("Получение первых 50 продуктов SENTINEL-2...")
print()

# Get products
catalog_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq 'SENTINEL-2'&$top=50"

response = requests.get(catalog_url, headers=headers, timeout=60)
data = response.json()

# Analyze product names
product_types = {}
for item in data.get("value", []):
    name = item.get("Name", "")

    # Extract product type from name
    # Sentinel-2 names typically start with S2A_ or S2B_
    parts = name.split("_")
    if len(parts) >= 2:
        # Get satellite and product level
        satellite = parts[0]  # S2A, S2B, etc.
        if len(parts) >= 4:
            product_level = parts[1]  # MSIL2A, MSIL1C, OPER, etc.
        else:
            product_level = parts[1] if len(parts) > 1 else "UNKNOWN"

        type_key = f"{satellite}_{product_level}"

        if type_key not in product_types:
            product_types[type_key] = []

        product_types[type_key].append(name[:80])  # First 80 chars

print(f"Найдено уникальных типов продуктов: {len(product_types)}")
print()

for ptype, examples in sorted(product_types.items()):
    print(f"{ptype}: {len(examples)} продуктов")
    print(f"  Пример: {examples[0]}")
    print()

# Now let's specifically search for MSIL2A products
print("=" * 70)
print()
print("Поиск продуктов содержащих 'MSIL2A'...")
print()

catalog_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq 'SENTINEL-2' and contains(Name,'MSIL2A')&$top=5"

response = requests.get(catalog_url, headers=headers, timeout=60)
data = response.json()

count = len(data.get("value", []))
print(f"✓ Найдено: {count} продуктов")
print()

if count > 0:
    for i, item in enumerate(data["value"][:3], 1):
        print(f"{i}. {item.get('Name')}")
        print(f"   ID: {item.get('Id')}")
        print(f"   Size: {item.get('ContentLength', 0) / 1024 / 1024:.1f} MB")
        print()

print("=" * 70)
