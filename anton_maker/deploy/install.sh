#!/bin/bash
set -e

echo "🚀 Начало установки Anton Maker CRM..."

# 1. Системные зависимости
echo "📦 Установка системных пакетов..."
apt update
apt install -y python3-pip python3-venv nginx libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# 2. Создание виртуального окружения
PROJECT_DIR="/opt/anton_maker"
VENV_DIR="$PROJECT_DIR/venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "🐍 Создание виртуального окружения..."
    python3 -m venv "$VENV_DIR"
fi

# 3. Установка Python зависимостей
echo "⬇️ Установка Python пакетов..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$PROJECT_DIR/requirements.txt"

# 4. Настройка прав доступа
echo "🔐 Настройка прав доступа..."
usermod -a -G www-data $USER
chown -R www-data:www-data "$PROJECT_DIR/data"
chmod -R 755 "$PROJECT_DIR/data"

# Создание директории для сокета
mkdir -p /run/anton
chown www-data:www-data /run/anton

# 5. Настройка Systemd
echo "⚙️ Настройка systemd сервиса..."
cp "$PROJECT_DIR/deploy/anton-maker.service" /etc/systemd/system/anton-maker.service
systemctl daemon-reload
systemctl enable anton-maker

# 6. Настройка Nginx
echo "🌐 Настройка Nginx..."
rm -f /etc/nginx/sites-enabled/default
ln -sf "$PROJECT_DIR/deploy/nginx.conf" /etc/nginx/sites-available/anton-maker
ln -sf /etc/nginx/sites-available/anton-maker /etc/nginx/sites-enabled/anton-maker
nginx -t
systemctl restart nginx

# 7. Миграции и статика
echo "🗄️ Применение миграций и сбор статики..."
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

# 8. Запуск сервиса
echo "▶️ Запуск сервиса..."
systemctl start anton-maker

echo "✅ Установка завершена!"
echo "Не забудьте создать суперпользователя: python3 manage.py createsuperuser"
echo "И настроить переменные окружения в .env"
