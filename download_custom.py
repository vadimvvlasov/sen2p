"""
Скачивание Sentinel-2 с настраиваемыми параметрами
"""

import os
import sys
from datetime import datetime, timedelta
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


def download_sentinel2(
    location,
    days_back=30,
    max_products=3,
    cloud_max=20,
    output_dir="sentinel_data",
):
    """
    Скачать Sentinel-2 снимки

    Args:
        location: [longitude, latitude]
        days_back: Сколько дней назад искать (по умолчанию 30)
        max_products: Сколько лучших снимков скачать
        cloud_max: Максимальная облачность (%)
        output_dir: Директория для сохранения
    """
    # Вычисляем даты
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)

    print("=" * 70)
    print("Скачивание Sentinel-2")
    print("=" * 70)
    print()
    print(f"Локация: {location}")
    print(f"Период: {start_date.date()} - {end_date.date()} ({days_back} дней)")
    print(f"Макс. облачность: {cloud_max}%")
    print(f"Количество: {max_products} лучших")
    print(f"Сохранить в: {output_dir}/")
    print()

    try:
        results = download(
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            location=location,
            output_dir=output_dir,
            cloud_max=cloud_max,
            max_products=max_products,
            producttype="S2MSI2A",
        )

        if results:
            print()
            print("=" * 70)
            print(f"✓ Успешно скачано: {len(results)} снимк(ов)")
            print("=" * 70)
            print()

            for i, r in enumerate(results, 1):
                print(f"#{i}: {r['title']}")
                print(f"     Дата: {r['date']}")
                print(f"     Облачность: {r['cloud_cover']}%")
                print(f"     Путь: {r['path']}")
                print()

            return results
        else:
            print("✗ Снимки не найдены")
            print()
            print("Попробуйте:")
            print(f"  • Увеличить период (сейчас: {days_back} дней)")
            print(f"  • Увеличить облачность (сейчас: {cloud_max}%)")
            return []

    except ValueError:
        print("=" * 70)
        print("✗ Ошибка: Не настроены учётные данные")
        print("=" * 70)
        print()
        print("Зарегистрируйтесь: https://dataspace.copernicus.eu")
        print()
        print("Затем установите:")
        print("  export CDSE_USER='ваш_email@example.com'")
        print("  export CDSE_PASSWORD='ваш_пароль'")
        print()
        sys.exit(1)

    except Exception as e:
        print(f"✗ Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Примеры использования:

    # 1. Крайстчерч, Новая Зеландия (из примера)
    print("Пример 1: Крайстчерч, Новая Зеландия")
    location_nz = [172.1, -43.5]
    results = download_sentinel2(
        location=location_nz,
        days_back=30,
        max_products=3,
        cloud_max=20,
        output_dir="data/christchurch",
    )

    # 2. Ваша локация (раскомментируйте и измените координаты)
    # print("\nПример 2: Пользовательская локация")
    # location_custom = [37.6, 55.75]  # Москва
    # results = download_sentinel2(
    #     location=location_custom,
    #     days_back=60,
    #     max_products=5,
    #     cloud_max=30,
    #     output_dir="data/custom"
    # )

    # 3. Быстрый поиск с высокой облачностью
    # print("\nПример 3: Быстрый поиск")
    # results = download_sentinel2(
    #     location=[0.0, 51.5],  # Лондон
    #     days_back=90,
    #     max_products=1,
    #     cloud_max=50,
    #     output_dir="data/quick"
    # )
