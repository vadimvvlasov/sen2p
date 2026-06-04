"""
Проверка footprint'ов продуктов для Бразилии
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

print("Проверка footprint'ов для Бразилии")
print("=" * 70)
print()

# Target location
TARGET_LON, TARGET_LAT = -51.2, -30.0
print(f"Целевая точка: lon={TARGET_LON}, lat={TARGET_LAT}")
print()

# Get some products from June 2023
filter_query = "Collection/Name eq 'SENTINEL-2' and contains(Name,'MSIL2A') and ContentDate/Start gt 2023-06-01T00:00:00Z and ContentDate/Start lt 2023-06-10T00:00:00Z"

catalog_url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter={filter_query}&$top=10"

response = requests.get(catalog_url, headers=headers, timeout=60)
data = response.json()

products = data.get("value", [])
print(f"Получено {len(products)} продуктов")
print()

# Check first few products
for i, item in enumerate(products[:5], 1):
    product_id = item.get("Id")
    product_name = item.get("Name", "")

    print(f"{i}. {product_name[:70]}")
    print(f"   ID: {product_id}")

    # Get attributes
    attrs_url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({product_id})/Attributes"

    try:
        attrs_response = requests.get(attrs_url, headers=headers, timeout=30)
        print(f"   Attributes response status: {attrs_response.status_code}")

        if attrs_response.status_code == 200:
            attrs_data = attrs_response.json()
            attrs = {}
            for attr in attrs_data.get("value", []):
                attrs[attr.get("Name")] = attr.get("Value")

            cloud_cover = attrs.get("cloudCover", "N/A")
            footprint = attrs.get("footprint", "")

            print(f"   Cloud cover: {cloud_cover}%")

            if footprint:
                # Extract bbox from footprint
                try:
                    coords_str = footprint.split("((")[1].split("))")[0]
                    coords = []
                    for pair in coords_str.split(","):
                        parts = pair.strip().split()
                        if len(parts) == 2:
                            coords.append((float(parts[0]), float(parts[1])))

                    if coords:
                        lons = [c[0] for c in coords]
                        lats = [c[1] for c in coords]

                        min_lon, max_lon = min(lons), max(lons)
                        min_lat, max_lat = min(lats), max(lats)

                        print(
                            f"   BBox: lon=[{min_lon:.2f}, {max_lon:.2f}], lat=[{min_lat:.2f}, {max_lat:.2f}]"
                        )

                        # Check if our point is in bbox
                        in_bbox = (
                            min_lon <= TARGET_LON <= max_lon
                            and min_lat <= TARGET_LAT <= max_lat
                        )
                        print(f"   Точка в BBox: {'✓ ДА' if in_bbox else '✗ НЕТ'}")
                except Exception as e:
                    print(f"   Ошибка парсинга footprint: {e}")
            else:
                print("   Footprint: отсутствует")

    except Exception as e:
        print(f"   Ошибка получения атрибутов: {e}")

    print()

print("=" * 70)
