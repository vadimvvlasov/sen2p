# CDSE Setup Guide - Пошаговая инструкция

## ✅ Рабочее решение для скачивания Sentinel-2

### Шаг 1: Регистрация

1. Откройте https://dataspace.copernicus.eu
2. Нажмите **REGISTER** (правый верхний угол)
3. Заполните форму:
   - First name
   - Last name  
   - **Email** (будет вашим username)
   - Password
   - Подтвердите password
4. Примите условия
5. Нажмите **REGISTER**

### Шаг 2: Подтверждение email

⚠️ **ВАЖНО:** Без этого шага API не работает!

1. Проверьте почту (включая спам)
2. Найдите письмо от Copernicus Data Space Ecosystem
3. Кликните на ссылку **"Verify email address"**
4. Дождитесь подтверждения

### Шаг 3: Первый вход через веб

⚠️ **КРИТИЧНО:** Войдите хотя бы раз через браузер!

1. Откройте https://dataspace.copernicus.eu
2. Нажмите **LOGIN**
3. Введите:
   - Email (не username!)
   - Password
4. Войдите в систему
5. Посмотрите Dashboard
6. **Это активирует ваш аккаунт для API!**

### Шаг 4: Настройка credentials

Создайте или обновите `.env` файл:

```bash
# В корне проекта sen2p
cat > .env << 'EOF'
CDSE_USER=ваш_email@example.com
CDSE_PASSWORD=ваш_пароль
EOF
```

Или установите переменные окружения:

```bash
export CDSE_USER="ваш_email@example.com"
export CDSE_PASSWORD="ваш_пароль"
```

### Шаг 5: Тест

Запустите тестовый скрипт:

```bash
uv run download_cdse.py
```

## 🎯 Что должно работать

### Успешный вывод:

```
======================================================================
Скачивание Sentinel-2 через CDSE API
======================================================================

Локация: [172.1, -43.5]
Период: 2024-01-01 - 2024-01-31
Макс. облачность: 20%
Количество: 3 лучших

✓ Credentials загружены
Получение access token...
✓ Access token получен

Поиск снимков...
✓ Найдено: X снимков

Топ 3 снимков:
  1. S2A_MSIL2A_...
     Облачность: 5.2%
     Дата: 2024-01-15T...
  ...

Начинаем скачивание в sentinel_data_cdse/...
```

## ❌ Частые ошибки

### "Account is not fully set up"

**Причина:** Email не подтверждён или не было первого входа

**Решение:**
1. Проверьте email и подтвердите
2. Войдите через браузер хотя бы раз
3. Подождите 5-10 минут
4. Попробуйте снова

### "Invalid credentials"

**Причина:** Неверный email или пароль

**Решение:**
1. Проверьте, что используете **email**, а не username
2. Проверьте пароль (попробуйте войти через браузер)
3. Убедитесь, что нет лишних пробелов в .env файле

### "Connection error"

**Причина:** Проблемы с сетью или сервер недоступен

**Решение:**
1. Проверьте интернет
2. Проверьте статус: https://dataspace.copernicus.eu
3. Попробуйте позже

## 📋 Чеклист готовности

- [ ] Зарегистрирован на dataspace.copernicus.eu
- [ ] Email подтверждён (проверьте спам!)
- [ ] Вошли через браузер хотя бы раз
- [ ] Credentials в .env файле
- [ ] Email (не username!) используется
- [ ] Пароль правильный
- [ ] Нет лишних пробелов в .env
- [ ] Интернет работает

## 🔍 Debug

Если проблемы продолжаются:

```python
# Проверьте credentials
import os

print("User:", os.getenv("CDSE_USER"))
print("Password set:", "Yes" if os.getenv("CDSE_PASSWORD") else "No")
```

```bash
# Проверьте доступность API
curl https://identity.dataspace.copernicus.eu/auth/realms/CDSE/.well-known/openid-configuration
```

```bash
# Попробуйте получить токен вручную
curl -X POST "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=cdse-public" \
  -d "username=ваш_email@example.com" \
  -d "password=ваш_пароль" \
  -d "grant_type=password"
```

Если получили access_token - всё ок, проблема в коде.
Если ошибка - проблема с аккаунтом.

## 📚 Дополнительные ресурсы

- Документация CDSE: https://documentation.dataspace.copernicus.eu
- Форум поддержки: https://forum.dataspace.copernicus.eu
- Help Center: https://helpcenter.dataspace.copernicus.eu

## ✅ После успешной настройки

Используйте:

```python
from sen2p.cdse_downloader import CDSEDownloader

downloader = CDSEDownloader()
products = downloader.search(
    location=(172.1, -43.5),
    start_date="2024-01-01",
    end_date="2024-01-31",
    cloud_max=20,
)

results = downloader.download_products(products, max_products=3)
```

Или просто:

```bash
uv run download_cdse.py
```

## 🎊 Готово!

Теперь вы можете скачивать Sentinel-2 снимки через CDSE API!

---

*Последнее обновление: 2026-06-04*
