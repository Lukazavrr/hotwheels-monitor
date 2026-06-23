# 🔥 Hot Wheels Monitor

Автоматический мониторинг сайта Mattel для отслеживания новых моделей Hot Wheels с уведомлениями в Telegram.

## ✨ Функционал

✅ **Мониторинг каждую минуту** - Проверка обновлений каждые 60 секунд  
✅ **Отслеживание новых товаров** - Уведомление о появлении новых моделей  
✅ **Отслеживание цены** - Уведомление об изменениях цены  
✅ **Отслеживание наличия** - Уведомление когда товар вернулся в наличие  
✅ **Telegram уведомления** - На 2 разных аккаунта  
✅ **База данных** - SQLite для сохранения истории  
✅ **Docker** - Развертывание на сервере 24/7  
✅ **Логирование** - Подробные логи всех операций  

## 🚀 Быстрый старт

### Локально (Windows/Mac/Linux)

1. **Клонируем репозиторий:**
```bash
git clone https://github.com/Lukazavrr/hotwheels-monitor.git
cd hotwheels-monitor
```

2. **Устанавливаем зависимости:**
```bash
pip install -r requirements.txt
```

3. **Скопируем файл конфига:**
```bash
cp .env.example .env
```

4. **Отредактируем `.env` (все данные уже заполнены):**
```bash
# Windows
type .env
# Mac/Linux
cat .env
```

5. **Запускаем:**
```bash
python main.py
```

## 🐳 Развертывание на сервере (Docker)

### На VPS/Сервере

1. **Устанавливаем Docker:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

2. **Клонируем репозиторий:**
```bash
git clone https://github.com/Lukazavrr/hotwheels-monitor.git
cd hotwheels-monitor
```

3. **Создаем `.env`:**
```bash
cp .env.example .env
```

4. **Запускаем Docker контейнер:**
```bash
docker-compose up -d
```

5. **Проверяем статус:**
```bash
docker-compose logs -f
```

6. **Остановка контейнера:**
```bash
docker-compose down
```

## 📝 Конфигурация (.env)

| Параметр | Описание | Значение |
|----------|---------|----------|
| `TELEGRAM_BOT_TOKEN` | Токен вашего Telegram бота | `8777184371:AAF8qi96Lzky3pCs6Unzapgt51bKZUFV6JU` |
| `TELEGRAM_CHAT_ID_1` | Telegram ID первого аккаунта | `535013845` |
| `TELEGRAM_CHAT_ID_2` | Telegram ID второго аккаунта | `386813053` |
| `HOTWHEELS_URL` | URL сайта для мониторинга | `https://creations.mattel.com/...` |
| `CHECK_INTERVAL` | Интервал проверки в секундах | `60` |
| `DB_PATH` | Путь к базе данных | `./data/hotwheels.db` |
| `LOG_LEVEL` | Уровень логирования | `INFO` |

## 📱 Telegram уведомления

Вы будете получать уведомления типа:

```
🆕 НОВЫЙ ТОВАР!

Название: Hot Wheels Special Edition 2024
Цена: $29.99
Статус: In Stock
Ссылка: https://...
```

```
💰 ИЗМЕНЕНИЕ ЦЕНЫ!

Товар: Hot Wheels Premium
Старая цена: $34.99
Новая цена: $24.99
Ссылка: https://...
```

```
📈 ТОВАР ВЕРНУЛСЯ В НАЛИЧИЕ!

Товар: Limited Edition Hot Wheels
Цена: $49.99
Ссылка: https://...
```

## 📊 Структура проекта

```
hotwheels-monitor/
├── main.py              # Главный файл
├── scraper.py           # Веб-скрейпер
├── telegram_notifier.py # Telegram уведомления
├── database.py          # Работа с БД
├── requirements.txt     # Python зависимости
├── .env.example         # Пример конфигурации
├── Dockerfile           # Docker конфигурация
├── docker-compose.yml   # Docker Compose
├── README.md            # Документация
├── logs/                # Логи (создается автоматически)
└── data/                # БД (создается автоматически)
```

## 🔧 Решение проблем

### Бот не отправляет сообщения
1. Проверьте токен бота
2. Проверьте Telegram ID (напишите `@userinfobot` чтобы узнать)
3. Убедитесь что чат с ботом открыт

### "Chrome не найден"
- Переустановите Google Chrome
- Переустановите ChromeDriver

### Ошибка подключения к сайту
- Проверьте интернет соединение
- Сайт может быть недоступен
- Измените USER-AGENT в scraper.py

## 📊 Логи

Все логи сохраняются в `logs/monitor.log`:

```bash
# Просмотр логов (локально)
tail -f logs/monitor.log

# Просмотр логов (Docker)
docker-compose logs -f
```

## ⚙️ Расширенная конфигурация

### Изменение интервала проверки

В `.env` измените `CHECK_INTERVAL` (в секундах):
```env
CHECK_INTERVAL=30  # проверка каждые 30 сек
CHECK_INTERVAL=300  # проверка каждые 5 мин
```

### Добавление еще одного аккаунта

Отредактируйте `telegram_notifier.py`:
```python
self.chat_ids = [
    int(os.getenv('TELEGRAM_CHAT_ID_1')),
    int(os.getenv('TELEGRAM_CHAT_ID_2')),
    int(os.getenv('TELEGRAM_CHAT_ID_3'))  # Добавьте эту строку
]
```

Добавьте в `.env`:
```env
TELEGRAM_CHAT_ID_3=123456789
```

## 🌍 Рекомендуемые VPS для 24/7 запуска

- **DigitalOcean** - от $4/месяц
- **Linode** - от $5/месяц
- **Vultr** - от $2.50/месяц
- **Hetzner** - от €3/месяц
- **Yandex Cloud** - бесплатный trial

## 📞 Поддержка

Если у вас есть вопросы или проблемы:
1. Проверьте логи
2. Убедитесь что конфиг правильный
3. Откройте Issue на GitHub

## 📄 Лицензия

MIT License - используйте свободно!

---

**Создано для отслеживания Hot Wheels моделей на Mattel.com** 🔥🚗