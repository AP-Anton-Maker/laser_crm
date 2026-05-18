# Anton Maker CRM

CRM-система с VK ботом для лазерной мастерской.

## Стек
- Django 4.2 + Unfold Admin
- SQLite (WAL режим)
- Gunicorn + Nginx
- VK API Bot

## Быстрый старт

1. Клонировать и настроить:
```bash
cd /opt
git clone <repo_url> anton_maker
cd anton_maker
cp .env.example .env
nano .env  # Заполните переменные
```

2. Запустить установку:
```bash
bash deploy/install.sh
python3 manage.py createsuperuser
```

3. Настроить SSL:
```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d вашдомен.ru
```

4. Настроить VK Webhook:
- URL: https://вашдомен.ru/bot/webhook/
- Secret: из .env (VK_SECRET_KEY)

## Структура
- `config/` - настройки Django
- `crm/` - основное приложение
  - `models/` - модели данных
  - `admin/` - админка Unfold
  - `bot_logic/` - логика VK бота
  - `utils/` - утилиты
  - `management/commands/` - cron задачи
- `templates/` - HTML шаблоны
- `deploy/` - скрипты и конфиги

## Команды управления
```bash
python manage.py daily_briefing   # Ежедневная сводка
python manage.py check_stock      # Проверка запасов
```

## Бэкапы
Настраиваются через cron (см. deploy/cron.example)
