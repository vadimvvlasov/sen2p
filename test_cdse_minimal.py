"""
Минимальный тест CDSE API - без фильтров
"""

import os
from pathlib import Path

import requests


# Загрузка credentials из .env файла
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

print("Тест CDSE API")
print("=" * 70)
print()

# Step 1: Get access token
print("1. Получение access token...")
token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"

data = {
    "client_id": "cdse-public",
    "username": username,
    "password": password,
    "grant_type": "password",
}

response = requests.post(token_url, data=data, timeout=30)
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    access_token = response.json()["access_token"]
    print(f"   ✓ Token получен (length: {len(access_token)})")
else:
    print(f"   ✗ Ошибка: {response.text}")
    exit(1)

print()

# Step 2: Test WITHOUT filters
print("2. Запрос БЕЗ фильтров (первые 5 записей)...")
catalog_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$top=5"

headers = {"Authorization": f"Bearer {access_token}"}

response = requests.get(catalog_url, headers=headers, timeout=60)
print(f"   Status: {response.status_code}")
print(f"   Response length: {len(response.text)}")

if response.status_code == 200:
    data = response.json()
    count = len(data.get("value", []))
    print(f"   ✓ Получено записей: {count}")

    if count > 0:
        print()
        print("   Первая запись:")
        first = data["value"][0]
        print(f"     ID: {first.get('Id')}")
        print(f"     Name: {first.get('Name')}")
        print(f"     Collection: {first.get('Collection')}")
else:
    print(f"   ✗ Ошибка: {response.text[:200]}")
    exit(1)

print()

# Step 3: Test with SENTINEL-2 filter only
print("3. Запрос с фильтром Collection/Name eq 'SENTINEL-2' (первые 5)...")
catalog_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq 'SENTINEL-2'&$top=5"

response = requests.get(catalog_url, headers=headers, timeout=60)
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    count = len(data.get("value", []))
    print(f"   ✓ Получено записей: {count}")

    if count > 0:
        print()
        print("   Первая запись:")
        first = data["value"][0]
        print(f"     ID: {first.get('Id')}")
        print(f"     Name: {first.get('Name')}")

        # Check collection details
        if "Collection" in first:
            coll = first["Collection"]
            if isinstance(coll, dict):
                print(f"     Collection Name: {coll.get('Name')}")
else:
    print(f"   ✗ Ошибка: {response.text[:200]}")

print()

# Step 4: Check Collections endpoint
print("4. Проверка доступных коллекций...")
collections_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Collections"

response = requests.get(collections_url, headers=headers, timeout=60)
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    collections = data.get("value", [])
    print(f"   ✓ Найдено коллекций: {len(collections)}")
    print()
    print("   Список коллекций:")
    for coll in collections[:10]:
        print(f"     - {coll.get('Name')}")
else:
    print(f"   ✗ Ошибка: {response.text[:200]}")

print()
print("=" * 70)
