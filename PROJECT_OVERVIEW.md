# sen2p - Project Overview

**Версия:** 0.1.0  
**Статус:** Готов к использованию ✓  
**Лицензия:** MIT  
**Python:** 3.10+

---

## ✅ Что создано

### 🎯 Основной функционал
- ✓ Библиотека для загрузки спутниковых снимков Sentinel-2
- ✓ Простой API с одной основной функцией `download()`
- ✓ Фильтрация по облачности
- ✓ Поддержка Level-1C и Level-2A продуктов
- ✓ Интеграция с Copernicus Open Access Hub

### 📦 Структура проекта

```
sen2p/                          # Чистый корень!
├── sen2p/                      # Код (2 файла)
├── docs/                       # Документация (12 файлов)
├── examples/                   # Примеры (2 скрипта)
├── tests/                      # Тесты (1 тест)
├── README.md                   # Главная документация
├── CHANGELOG.md                # История версий
├── STRUCTURE.md                # Обзор структуры
└── pyproject.toml              # Конфигурация (с Ruff + mypy)
```

### 📚 Документация (12 файлов)

**Для пользователей:**
- `QUICKSTART.md` - Быстрый старт за 5 минут
- `INTEGRATION.md` - Интеграция с rasteric
- `SENTINEL2_REFERENCE.md` - Спецификация Sentinel-2
- `FAQ.md` - Часто задаваемые вопросы
- `SUMMARY.md` - Обзор проекта

**Для разработчиков:**
- `CONTRIBUTING.md` - Как внести вклад
- `DEVELOPER_GUIDE.md` - Руководство разработчика
- `PROJECT_STRUCTURE.md` - Архитектура проекта
- `PUBLISHING.md` - Как публиковать релизы

**Справочная:**
- `INDEX.md` - Навигация по документации
- `PROJECT_SUMMARY.txt` - Краткая справка
- `README.md` - Обзор документации

### 💻 Примеры

1. **demo.py** - Быстрая демонстрация с обработкой ошибок
2. **basic.py** - Различные сценарии использования
3. **README.md** - Инструкции по запуску

### 🧪 Тесты

- **test_imports.py** - Проверка импортов
- **README.md** - Руководство по тестированию

### ⚙️ Конфигурация

- **pyproject.toml** - Полная конфигурация:
  - Метаданные пакета
  - Зависимости
  - Настройки Ruff (форматирование + линтинг)
  - Настройки mypy (проверка типов)
  - Build system (hatchling)

---

## 🚀 Быстрый старт

```bash
# 1. Установка
uv add sen2p

# 2. Настройка credentials
export COPERNICUS_USER="your_username"
export COPERNICUS_PASSWORD="your_password"

# 3. Использование
python
>>> from sen2p import download
>>> results = download(
...     start_date="2024-01-01",
...     end_date="2024-01-31",
...     location=[172.1, -43.5],
...     output_dir="data",
...     cloud_max=20
... )
```

---

## 📖 Навигация

### Начать работу
1. `README.md` (корень) - Обзор и API
2. `docs/QUICKSTART.md` - 5-минутная настройка
3. `examples/demo.py` - Запустить пример
4. `docs/INTEGRATION.md` - Полный workflow

### Внести вклад
1. `docs/CONTRIBUTING.md` - Руководство для контрибьюторов
2. `docs/DEVELOPER_GUIDE.md` - Детали разработки
3. `docs/PROJECT_STRUCTURE.md` - Архитектура

### Найти информацию
1. `docs/FAQ.md` - Частые вопросы
2. `docs/SENTINEL2_REFERENCE.md` - Спецификации Sentinel-2
3. `docs/INDEX.md` - Полная карта документации

---

## 🛠 Инструменты разработки

### Форматирование и линтинг
```bash
# Установить ruff
uv add --dev ruff

# Проверить код
uv run ruff check .

# Форматировать код
uv run ruff format .
```

### Проверка типов
```bash
# Установить mypy
uv add --dev mypy

# Проверить типы
uv run mypy sen2p
```

### Тестирование
```bash
# Проверить импорты
uv run tests/test_imports.py

# Запустить примеры
uv run examples/demo.py
```

---

## 📊 Статистика проекта

- **Код:** 2 Python модуля (~400 строк)
- **Документация:** 12 MD файлов (~3000 строк)
- **Примеры:** 2 скрипта
- **Тесты:** 1 тест
- **Зависимости:** sentinelsat, requests
- **Python:** 3.10+

---

## 🎨 Философия дизайна

1. **Разделение ответственности**
   - sen2p загружает
   - rasteric обрабатывает

2. **Простота**
   - Одна основная функция
   - Разумные значения по умолчанию
   - Минимум настроек

3. **Чистота**
   - Организованная структура
   - Чистый корень проекта
   - README в каждой директории

4. **Документированность**
   - 12 файлов документации
   - Примеры для всех случаев
   - Пошаговые руководства

---

## 🔄 Workflow: sen2p + rasteric

```
1. sen2p.download()         → Скачивает .SAFE файлы
   ↓
2. rasteric.extract_bands() → Извлекает нужные каналы
   ↓
3. rasteric.ndvi()          → Вычисляет индексы
   ↓
4. rasteric.mosaic()        → Объединяет сцены
   ↓
5. Анализ
```

---

## ✨ Особенности

- ✅ Простой API
- ✅ Фильтрация по облачности
- ✅ Бесплатные данные через Copernicus
- ✅ Type hints
- ✅ Полная документация
- ✅ Интеграция с rasteric
- ✅ uv package manager
- ✅ Ruff форматирование
- ✅ mypy проверка типов

---

## 📦 Публикация

Проект готов к публикации на PyPI:

```bash
# 1. Build
uv build

# 2. Test на TestPyPI
uv publish --publish-url https://test.pypi.org/legacy/

# 3. Publish на PyPI
uv publish
```

См. `docs/PUBLISHING.md` для деталей.

---

## 🔗 Полезные ссылки

- **Регистрация:** https://scihub.copernicus.eu/dhus/#/self-registration
- **Sentinel-2:** https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-2
- **sentinelsat:** https://sentinelsat.readthedocs.io/
- **uv:** https://docs.astral.sh/uv/

---

## 📝 Следующие шаги

### Для пользователей:
1. Прочитать `docs/QUICKSTART.md`
2. Зарегистрироваться на Copernicus Hub
3. Запустить `examples/demo.py`
4. Изучить `docs/INTEGRATION.md`

### Для разработчиков:
1. Прочитать `docs/CONTRIBUTING.md`
2. Изучить `docs/DEVELOPER_GUIDE.md`
3. Ознакомиться с кодом в `sen2p/`
4. Добавить тесты в `tests/`

---

## ✅ Checklist готовности

- [x] Код реализован и работает
- [x] Документация написана (12 файлов)
- [x] Примеры созданы и протестированы
- [x] Тесты работают
- [x] Структура организована
- [x] pyproject.toml настроен (Ruff + mypy)
- [x] README файлы в каждой директории
- [x] .gitignore настроен
- [x] LICENSE добавлен (MIT)
- [x] CHANGELOG.md создан

**Статус: ✅ Готово к использованию!**

---

## 🎉 Итого

Создан полноценный Python пакет для загрузки спутниковых снимков Sentinel-2:

- **Функциональность:** Полная реализация
- **Документация:** Исчерпывающая (12 файлов)
- **Примеры:** Работающие скрипты
- **Структура:** Чистая и организованная
- **Качество:** Ruff + mypy настроены
- **Готовность:** 100% для использования и публикации

**Проект готов! 🚀**
