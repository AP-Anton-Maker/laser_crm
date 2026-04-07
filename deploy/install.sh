#!/bin/bash

# Останавливаем скрипт при любой ошибке
set -e

# Цвета для вывода логов
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}   Установка Laser CRM (Production)    ${NC}"
echo -e "${BLUE}=======================================${NC}"

# Проверка на запуск от имени root (через sudo)
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Ошибка: Пожалуйста, запустите скрипт через sudo.${NC}"
  echo "Пример: sudo ./deploy/install.sh"
  exit 1
fi

# Получаем имя пользователя, который вызвал sudo, и абсолютный путь к проекту
ACTUAL_USER=${SUDO_USER:-root}
PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

echo -e "${GREEN}[1/7] Настройка прав доступа...${NC}"
# Даем права Nginx читать файлы из домашней директории
chmod 755 /home/$ACTUAL_USER
chmod -R 755 $PROJECT_ROOT/frontend

echo -e "${GREEN}[2/7] Обновление системы и установка пакетов...${NC}"
apt-get update
apt-get install -y python3-venv python3-dev nginx ufw curl

echo -e "${GREEN}[3/7] Создание виртуального окружения и установка зависимостей...${NC}"
sudo -u $ACTUAL_USER python3 -m venv $PROJECT_ROOT/venv
sudo -u $ACTUAL_USER $PROJECT_ROOT/venv/bin/pip install --upgrade pip
sudo -u $ACTUAL_USER $PROJECT_ROOT/venv/bin/pip install -r $PROJECT_ROOT/backend/requirements.txt

echo -e "${GREEN}[4/7] Создание файла конфигурации .env (если его нет)...${NC}"
ENV_FILE="$PROJECT_ROOT/.env"
if [ ! -f "$ENV_FILE" ]; then
    sudo -u $ACTUAL_USER cat <<EOF > $ENV_FILE
PROJECT_NAME="Laser CRM Enterprise"
ENVIRONMENT="production"
SECRET_KEY="$(openssl rand -hex 32)"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=10080
DATABASE_URL="sqlite+aiosqlite:///./laser_crm.db"
FIRST_SUPERUSER="admin"
FIRST_SUPERUSER_PASSWORD="admin"
VK_TOKEN=""
VK_GROUP_ID=""
EOF
    echo -e "${BLUE}Создан базовый файл настроек .env. Не забудьте потом вписать туда VK_TOKEN!${NC}"
fi

echo -e "${GREEN}[5/7] Настройка Systemd (Демон приложения)...${NC}"
SERVICE_FILE="/etc/systemd/system/lasercrm.service"
cat <<EOF > $SERVICE_FILE
[Unit]
Description=Laser CRM FastAPI Backend
After=network.target

[Service]
User=$ACTUAL_USER
Group=www-data
WorkingDirectory=$PROJECT_ROOT
Environment="PATH=$PROJECT_ROOT/venv/bin"
# Надежный промышленный запуск через uvicorn
ExecStart=$PROJECT_ROOT/venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable lasercrm

echo -e "${GREEN}[6/7] Настройка Nginx (Reverse Proxy)...${NC}"
NGINX_CONF="/etc/nginx/sites-available/lasercrm"
cat <<EOF > $NGINX_CONF
server {
    listen 80;
    server_name _;
    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        # Поддержка WebSocket для чатов
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

ln -sf /etc/nginx/sites-available/lasercrm /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t

echo -e "${GREEN}[7/7] Настройка брандмауэра и запуск...${NC}"
ufw allow 22/tcp
ufw allow 80/tcp
ufw --force enable

systemctl restart lasercrm
systemctl restart nginx

echo -e "${BLUE}=======================================${NC}"
echo -e "${GREEN}Установка успешно завершена!${NC}"
echo -e "Откройте IP-адрес этого сервера в браузере."
echo -e "${BLUE}=======================================${NC}"#!/bin/bash

# Останавливаем скрипт при любой ошибке
set -e

# Цвета для вывода логов
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}   Установка Laser CRM (Production)    ${NC}"
echo -e "${BLUE}=======================================${NC}"

# Проверка на запуск от имени root (через sudo)
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Ошибка: Пожалуйста, запустите скрипт через sudo.${NC}"
  echo "Пример: sudo ./deploy/install.sh"
  exit 1
fi

# Получаем имя пользователя, который вызвал sudo, и абсолютный путь к проекту
ACTUAL_USER=${SUDO_USER:-root}
PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

echo -e "${GREEN}[1/6] Обновление системы и установка пакетов...${NC}"
apt-get update
apt-get install -y python3-venv python3-dev nginx ufw curl

echo -e "${GREEN}[2/6] Создание виртуального окружения и установка Python зависимостей...${NC}"
# Создаем venv от имени реального пользователя, чтобы избежать проблем с правами
sudo -u $ACTUAL_USER python3 -m venv $PROJECT_ROOT/venv
sudo -u $ACTUAL_USER $PROJECT_ROOT/venv/bin/pip install --upgrade pip

# Если файла requirements.txt нет, создаем базовый на лету
if [ ! -f "$PROJECT_ROOT/backend/requirements.txt" ]; then
    echo -e "${BLUE}Файл requirements.txt не найден. Создаю базовый...${NC}"
    sudo -u $ACTUAL_USER cat <<EOF > $PROJECT_ROOT/backend/requirements.txt
fastapi
uvicorn[standard]
sqlalchemy
aiosqlite
pydantic
pydantic-settings
passlib[bcrypt]
pyjwt
vkbottle
scikit-learn
numpy
EOF
fi

sudo -u $ACTUAL_USER $PROJECT_ROOT/venv/bin/pip install -r $PROJECT_ROOT/backend/requirements.txt

echo -e "${GREEN}[3/6] Настройка Systemd (Демон приложения)...${NC}"
SERVICE_FILE="/etc/systemd/system/lasercrm.service"
cat <<EOF > $SERVICE_FILE
[Unit]
Description=Laser CRM FastAPI Backend
After=network.target

[Service]
User=$ACTUAL_USER
Group=www-data
WorkingDirectory=$PROJECT_ROOT
Environment="PATH=$PROJECT_ROOT/venv/bin"
# Если в main.py есть uvicorn.run(), запускаем через python. 
# Альтернативно: ExecStart=$PROJECT_ROOT/venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port 8000
ExecStart=$PROJECT_ROOT/venv/bin/python backend/main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable lasercrm

echo -e "${GREEN}[4/6] Настройка Nginx (Reverse Proxy)...${NC}"
NGINX_CONF="/etc/nginx/sites-available/lasercrm"
cat <<EOF > $NGINX_CONF
server {
    listen 80;
    server_name _; # Принимает запросы по любому IP

    # Разрешаем загрузку больших макетов (до 50 МБ)
    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Включаем конфиг и отключаем дефолтный
ln -sf /etc/nginx/sites-available/lasercrm /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t # Проверка синтаксиса конфигурации

echo -e "${GREEN}[5/6] Настройка брандмауэра (UFW)...${NC}"
ufw allow 22/tcp
ufw allow 80/tcp
# Принудительное включение без интерактивного вопроса
ufw --force enable

echo -e "${GREEN}[6/6] Запуск сервисов...${NC}"
systemctl restart lasercrm
systemctl restart nginx

echo -e "${BLUE}=======================================${NC}"
echo -e "${GREEN}Установка успешно завершена!${NC}"
echo -e "Система работает. Откройте IP-адрес этого сервера в браузере."
echo -e "Для проверки статуса используйте: ./deploy/status.sh"
echo -e "${BLUE}=======================================${NC}"
