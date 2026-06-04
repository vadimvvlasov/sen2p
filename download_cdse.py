"""
Скачивание Sentinel-2 через нативный CDSE API
"""

import os
from pathlib import Path

from sen2p.cdse_downloader import CDSEDownloader


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

# Параметры
LOCATION = [-51.2, -30.0]  # Порту-Алегри, Рио-Гранде-ду-Сул, Бразилия
START_DATE = "2023-06-01"  # Расширяем период
END_DATE = "2023-12-31"
CLOUD_MAX = 50  # Увеличиваем допустимую облачность
MAX_PRODUCTS = 3
OUTPUT_DIR = "sentinel_data_cdse"

print("=" * 70)
print("Скачивание Sentinel-2 через CDSE API")
print("=" * 70)
print()
print(f"Локация: {LOCATION}")
print(f"Период: {START_DATE} - {END_DATE}")
print(f"Макс. облачность: {CLOUD_MAX}%")
print(f"Количество: {MAX_PRODUCTS} лучших")
print()

try:
    # Создаём downloader
    downloader = CDSEDownloader()
    print("✓ Credentials загружены")

    # Получаем access token
    print("Получение access token...")
    downloader.get_access_token()
    print("✓ Access token получен")
    print()

    # Поиск продуктов
    print("Поиск снимков...")
    products = downloader.search(
        location=tuple(LOCATION),
        start_date=START_DATE,
        end_date=END_DATE,
        cloud_max=CLOUD_MAX,
        collection="SENTINEL-2",
        producttype="MSIL2A",
    )

    print(f"✓ Найдено: {len(products)} снимков")
    print()

    if products:
        # Показываем первые несколько
        print(f"Топ {min(MAX_PRODUCTS, len(products))} снимков:")
        for i, p in enumerate(products[:MAX_PRODUCTS], 1):
            print(f"  {i}. {p['name']}")
            print(f"     Облачность: {p['cloud_cover']:.1f}%")
            print(f"     Дата: {p['date']}")
        print()

        # Скачиваем
        print(f"Начинаем скачивание в {OUTPUT_DIR}/...")
        print()

        results = downloader.download_products(
            products, output_dir=OUTPUT_DIR, max_products=MAX_PRODUCTS
        )

        print()
        print("=" * 70)
        print(f"✓ Успешно скачано: {len(results)} снимк(ов)")
        print("=" * 70)
        print()

        for i, r in enumerate(results, 1):
            print(f"Снимок #{i}:")
            print(f"  Название: {r['title']}")
            print(f"  Облачность: {r['cloud_cover']:.1f}%")
            print(f"  Дата: {r['date']}")
            print(f"  Путь: {r['path']}")
            print()

        print("Следующие шаги:")
        print("  • Распакуйте .zip файлы")
        print("  • Обработайте с помощью rasteric")
        print("  • Вычислите NDVI или другие индексы")

    else:
        print("=" * 70)
        print("✗ Снимки не найдены")
        print("=" * 70)
        print()
        print("Попробуйте:")
        print("  • Увеличить период")
        print("  • Увеличить cloud_max")
        print("  • Проверить координаты")

except ValueError as e:
    print("=" * 70)
    print("✗ Ошибка конфигурации")
    print("=" * 70)
    print()
    print(str(e))
    print()
    print("Зарегистрируйтесь на: https://dataspace.copernicus.eu")
    print()
    print("Затем установите:")
    print("  export CDSE_USER='ваш_email@example.com'")
    print("  export CDSE_PASSWORD='ваш_пароль'")

except RuntimeError as e:
    print("=" * 70)
    print("✗ Ошибка выполнения")
    print("=" * 70)
    print()
    print(f"Детали: {e}")
    print()
    print("Возможные причины:")
    print("  • Неверные credentials")
    print("  • Проблемы с сетью")
    print("  • Сервер временно недоступен")

except Exception as e:
    print("=" * 70)
    print("✗ Неожиданная ошибка")
    print("=" * 70)
    print()
    print(f"Ошибка: {e}")
    print()
    print("Если проблема повторяется:")
    print("  • Проверьте интернет-соединение")
    print("  • Проверьте credentials")
    print("  • Посмотрите документацию")

print()
print("=" * 70)
