#!/bin/bash

# 🔧 Laser CRM - Автоматический установщик (Bulletproof Edition v3.0)
# Оптимизировано для Raspberry Pi (Python 3.13+)

set -e

echo "🚀 Начало установки Laser CRM..."

# 1. Определение переменных окружения
PROJECT_DIR=$(pwd)
USER_NAME=$(whoami)
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"
VENV_DIR="$BACKEND_DIR/venv"
DATA_DIR="$PROJECT_DIR/data"

echo "📂 Проект расположен в: $PROJECT_DIR"
echo "👤 Пользователь: $USER_NAME"

if [ "$EUID" -eq 0 ]; then
  echo "❌ Пожалуйста, не запускайте этот скрипт от root. Запустите как обычный пользователь."
  exit 1
fi

# Создаем папку для базы данных на всякий случай
mkdir -p "$DATA_DIR"

# 2. Установка системных зависимостей (включая тяжелые ИИ библиотеки)
echo "📦 Установка системных пакетов..."
sudo apt update
sudo apt install -y python3-venv python3-dev nginx ufw git python3-numpy python3-sklearn dos2unix

# 3. Подготовка правильных requirements
echo "📝 Оптимизация зависимостей (решение конфликтов версий)..."
cat > "$BACKEND_DIR/requirements.txt" << 'EOF'
fastapi
uvicorn[standard]
sqlalchemy
aiosqlite
pydantic
pydantic-settings
vkbottle
aiohttp
python-multipart
PyJWT
passlib[bcrypt]
EOF

# 4. Настройка Python окружения
echo "🐍 Создание виртуального окружения..."
if [ ! -d "$VENV_DIR" ]; then
    # Используем системные пакеты для numpy/sklearn
    python3 -m venv --system-site-packages "$VENV_DIR"
else
    echo "⚠️ Виртуальное окружение уже существует. Пересоздаем для надежности..."
    rm -rf "$VENV_DIR"
    python3 -m venv --system-site-packages "$VENV_DIR"
fi

echo "⬇️ Установка Python зависимостей..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$BACKEND_DIR/requirements.txt"
deactivate

# 5. Исправление относительных импортов (Фикс ошибки нейросети)
echo "🧹 Исправление синтаксиса Python импортов..."
# Ищем во всех папках, КРОМЕ venv, и исправляем двойные точки
find "$BACKEND_DIR" -type f -name "*.py" -not -path "*/venv/*" -exec sed -i 's/from \.\./from /g' {} +
# Убираем одинарные точки только в главном файле
sed -i -E 's/from \.([a-zA-Z])/from \1/g' "$BACKEND_DIR/main.py" 2>/dev/null || true

# 6. Генерация файла .env если его нет
if [ ! -f "$BACKEND_DIR/.env" ]; then
    echo "⚙️ Создание файла .env..."
    cat > "$BACKEND_DIR/.env" <<EOF
VK_TOKEN=ваш_токен_группы
SECRET_KEY=super_secret_key_change_me_$(openssl rand -hex 16)
DATABASE_URL=sqlite+aiosqlite:///$DATA_DIR/laser_crm.sqlite3
EOF
fi

# 7. Настройка Systemd
echo "🔧 Настройка сервиса Systemd..."
sudo tee /etc/systemd/system/lasercrm.service > /dev/null <<EOF
[Unit]
Description=Laser CRM Application
After=network.target

[Service]
User=$USER_NAME
Group=$USER_NAME
WorkingDirectory=$BACKEND_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 8. Настройка Nginx (с защитой переменных)
echo "🌐 Настройка Nginx..."
sudo rm -f /etc/nginx/sites-available/default
sudo rm -f /etc/nginx/sites-enabled/default
sudo tee /etc/nginx/sites-available/lasercrm > /dev/null << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        root FRONTPATH;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
EOF
# Подменяем путь фронтенда
sudo sed -i "s|FRONTPATH|$FRONTEND_DIR|g" /etc/nginx/sites-available/lasercrm

# Активация конфига Nginx
sudo ln -sf /etc/nginx/sites-available/lasercrm /etc/nginx/sites-enabled/lasercrm
sudo nginx -t

# 9. Настройка Firewall (UFW)
echo "🔒 Настройка брандмауэра UFW..."
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx HTTP'
echo "y" | sudo ufw enable || true

# 10. Запуск служб
echo "▶️ Запуск служб..."
sudo systemctl daemon-reload
sudo systemctl enable lasercrm
sudo systemctl restart lasercrm
sudo systemctl enable nginx
sudo systemctl restart nginx

echo ""
echo "✅ Установка завершена успешно!"
echo "--------------------------------"
echo "🌐 Приложение доступно по адресу: http://$(hostname -I | awk '{print $1}')"
echo "🔑 Дефолтные доступы: admin / admin"
