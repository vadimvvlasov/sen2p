"""
Скачать 3 лучших снимка Sentinel-2
"""

import os
from pathlib import Path

from sen2p import download


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


# Загружаем .env
load_env()

# Координаты из примера: Крайстчерч, Новая Зеландия
LOCATION = [172.1, -43.5]

# Параметры поиска
START_DATE = "2024-01-01"
END_DATE = "2024-01-31"
CLOUD_MAX = 20  # Максимум 20% облачности
OUTPUT_DIR = "sentinel_data"

print("=" * 70)
print("Скачивание 3 лучших снимков Sentinel-2")
print("=" * 70)
print()
print(f"Локация: Крайстчерч, Новая Зеландия {LOCATION}")
print(f"Период: {START_DATE} - {END_DATE}")
print(f"Макс. облачность: {CLOUD_MAX}%")
print("Количество: 3 лучших")
print()

try:
    results = download(
        start_date=START_DATE,
        end_date=END_DATE,
        location=LOCATION,
        output_dir=OUTPUT_DIR,
        cloud_max=CLOUD_MAX,
        max_products=3,  # ← Скачать только 3 лучших
        producttype="S2MSI2A",  # Level-2A (атмосферно скорректированный)
    )

    if results:
        print()
        print("=" * 70)
        print(f"✓ Успешно скачано: {len(results)} снимк(ов)")
        print("=" * 70)
        print()

        for i, r in enumerate(results, 1):
            print(f"Снимок #{i}:")
            print(f"  Название: {r['title']}")
            print(f"  Дата: {r['date']}")
            print(f"  Облачность: {r['cloud_cover']}%")
            print(f"  Размер: {r['size']}")
            print(f"  Путь: {r['path']}")
            print()

        print("Следующие шаги:")
        print("  1. Обработайте снимки с помощью rasteric")
        print("  2. Извлеките нужные каналы")
        print("  3. Вычислите NDVI или другие индексы")
        print()
        print("Пример обработки:")
        print("  from rasteric import raster")
        print(
            f"  raster.ndvi('{results[0]['path']}', 'ndvi.tif', red_band=4, nir_band=8)"
        )
        print()
    else:
        print("=" * 70)
        print("✗ Снимки не найдены")
        print("=" * 70)
        print()
        print("Попробуйте:")
        print("  • Увеличить период поиска")
        print("  • Увеличить cloud_max (например, до 50)")
        print("  • Проверить координаты")

except ValueError as e:
    print("=" * 70)
    print("✗ Ошибка конфигурации")
    print("=" * 70)
    print()
    print(str(e))
    print()
    print("⚠️  Важно: Старый портал закрыт с октября 2023!")
    print()
    print("Зарегистрируйтесь на НОВОМ портале:")
    print("  https://dataspace.copernicus.eu")
    print()
    print("Затем установите credentials:")
    print("  export CDSE_USER='ваш_email@example.com'")
    print("  export CDSE_PASSWORD='ваш_пароль'")

except RuntimeError as e:
    print("=" * 70)
    print("✗ Ошибка загрузки")
    print("=" * 70)
    print()
    print(f"Детали: {e}")
    print()
    print("Возможные причины:")
    print("  • Проблемы с интернет-соединением")
    print("  • Сервер Copernicus временно недоступен")
    print("  • Превышен лимит запросов")
    print()
    print("Попробуйте позже или проверьте статус:")
    print("  https://dataspace.copernicus.eu")

except Exception as e:
    print("=" * 70)
    print("✗ Неожиданная ошибка")
    print("=" * 70)
    print()
    print(f"Ошибка: {e}")
    print()
    print("Если проблема повторяется, проверьте:")
    print("  • Документацию: docs/QUICKSTART.md")
    print("  • FAQ: docs/FAQ.md")
    print("  • Миграцию: docs/MIGRATION_CDSE.md")

print()
print("=" * 70)
