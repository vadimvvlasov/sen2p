"""
Тест фильтрации по датам в CDSE OData API
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

print("Тест фильтрации по датам")
print("=" * 70)
print()

# Test different date filter formats
test_filters = [
    # Format 1: ContentDate/Start gt 2023-06-01T00:00:00.000Z
    "Collection/Name eq 'SENTINEL-2' and contains(Name,'MSIL2A') and ContentDate/Start gt 2023-06-01T00:00:00.000Z and ContentDate/Start lt 2023-07-01T00:00:00.000Z",
    # Format 2: With quotes
    "Collection/Name eq 'SENTINEL-2' and contains(Name,'MSIL2A') and ContentDate/Start gt '2023-06-01T00:00:00.000Z' and ContentDate/Start lt '2023-07-01T00:00:00.000Z'",
    # Format 3: Simple date
    "Collection/Name eq 'SENTINEL-2' and contains(Name,'MSIL2A') and ContentDate/Start ge 2023-06-01T00:00:00Z",
]

for i, filter_str in enumerate(test_filters, 1):
    print(f"Тест {i}:")
    print(f"  Фильтр: {filter_str[:100]}...")
    print()

    catalog_url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter={filter_str}&$top=5"

    try:
        response = requests.get(catalog_url, headers=headers, timeout=60)
        print(f"  Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            count = len(data.get("value", []))
            print(f"  ✓ Результатов: {count}")

            if count > 0:
                first = data["value"][0]
                print(f"    Первый: {first.get('Name')[:60]}")
                content_date = first.get("ContentDate", {})
                print(f"    Дата: {content_date.get('Start', 'N/A')}")
        else:
            error_text = response.text[:150]
            print(f"  ✗ Ошибка: {error_text}")
    except Exception as e:
        print(f"  ✗ Exception: {e}")

    print()

print("=" * 70)
