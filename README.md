# 🛠️ CRM «Лазерная Мастерская»

Полнофункциональная, асинхронная Enterprise CRM-система, разработанная специально для соло-предпринимателей и мастерских лазерной резки. 

Система работает автономно, требует минимум ресурсов и идеально подходит для запуска на мини-компьютерах (например, Raspberry Pi 3B+).

---

## ✨ Ключевые возможности

- 🧮 **Умный калькулятор:** 11 алгоритмов расчета (по площади, периметру, времени, 3D-клише) с автоматическим учетом оптовых скидок.
- 🤖 **Интеграция ВКонтакте (VKBottle):** Фоновый бот автоматически ловит сообщения, сохраняет их в CRM и позволяет отвечать прямо из интерфейса.
- 🏖️ **Режим «Отпуск»:** Специальный тумблер. При включении бот отвечает клиентам заранее заданным сообщением с датой вашего возвращения.
- 🧠 **AI-Аналитика (Scikit-learn):** Машинное обучение анализирует тренды за 30 дней и предсказывает завтрашнюю выручку.
- 💰 **Система лояльности (LTV):** Начисление 5% кэшбека при статусе заказа "Выполнен", авто-присвоение статусов (Новый ➔ Постоянный ➔ VIP).
- 📦 **Складской учет:** Отслеживание материалов с красными алертами на главном экране при падении остатков ниже минимума.
- 🔒 **Безопасность:** JWT-авторизация (OAuth2), хэширование паролей, защищенные API-маршруты.
- 💾 **Система бэкапов:** Скачивание дампа базы данных (SQLite) и экспорт таблиц в CSV (utf-8-sig для Excel) в один клик.

---

## 🛠 Стек технологий

**Backend:** Python 3.10+, FastAPI, SQLAlchemy (aiosqlite), VKBottle, Scikit-learn, PyJWT.
**Frontend:** HTML5, CSS3 (Модульная архитектура), Vanilla JS, Chart.js.

---

## 📂 Структура проекта

    laser_crm/
    ├── backend/
    │   ├── api/          # Маршруты FastAPI
    │   ├── core/         # Конфиги и безопасность
    │   ├── db/           # База данных и модели
    │   ├── schemas/      # Pydantic модели
    │   ├── services/     # Логика (AI, VK бот, Калькулятор)
    │   ├── main.py       # Точка входа
    │   └── requirements.txt
    ├── frontend/
    │   ├── js/           # JS логика
    │   ├── styles/       # CSS стили
    │   └── index.html    # SPA интерфейс
    └── README.md

---

## 💻 1. Локальный запуск (Для ПК)

Идеально для разработки и тестирования на Windows/Mac/Linux.

**Шаг 1. Клонирование и настройка окружения**
Откройте терминал в папке `backend`:
    
    python -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate
    pip install -r requirements.txt
    
**Шаг 2. Переменные окружения**
Создайте файл `.env` в папке `backend`:

    VK_TOKEN=vk1.a.ваш_токен_здесь
    SECRET_KEY=super_secret_key_123
    
**Шаг 3. Запуск сервера**
    
    python main.py
    
**Шаг 4. Вход в систему**
Откройте в браузере файл `frontend/index.html`. 
При первом запуске автоматически создается учетная запись:
- **Логин:** `admin`
- **Пароль:** `admin`

*Документация API (Swagger UI) доступна по адресу: http://localhost:8000/docs*

---

## 🍓 2. Установка на Raspberry Pi 3B+ (Production)

Так как Raspberry Pi 3B+ имеет всего 1 ГБ ОЗУ, мы не используем ресурсоемкий Docker. Система разворачивается нативно (Nginx + Systemd).

**Шаг 1. Подготовка системы**
Подключитесь к Raspberry Pi по SSH и обновите пакеты:
    
    sudo apt update && sudo apt upgrade -y
    sudo apt install python3-venv python3-dev nginx git ufw -y
    
**Шаг 2. Загрузка проекта и зависимости**
Поместите папку `laser_crm` в домашнюю директорию `/home/pi/laser_crm`.
    
    cd /home/pi/laser_crm/backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
Не забудьте создать файл `.env` с токеном ВК, как в локальной инструкции.

**Шаг 3. Настройка Systemd (Автозапуск бэкенда)**
Создайте службу для автоматического запуска сервера:
    
    sudo nano /etc/systemd/system/lasercrm.service
    
Вставьте этот конфиг:

    [Unit]
    Description=Laser CRM FastAPI Backend
    After=network.target

    [Service]
    User=pi
    Group=www-data
    WorkingDirectory=/home/pi/laser_crm/backend
    Environment="PATH=/home/pi/laser_crm/backend/venv/bin"
    ExecStart=/home/pi/laser_crm/backend/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --workers 1
    Restart=always

    [Install]
    WantedBy=multi-user.target
    
Запустите службу:
    
    sudo systemctl daemon-reload
    sudo systemctl enable lasercrm
    sudo systemctl start lasercrm
    
**Шаг 4. Настройка Nginx (Фронтенд)**
Удалите стандартный конфиг и создайте новый:
    
    sudo rm /etc/nginx/sites-enabled/default
    sudo nano /etc/nginx/sites-available/lasercrm
    
Вставьте этот конфиг:

    server {
        listen 80;
        server_name _;

        root /home/pi/laser_crm/frontend;
        index index.html;

        # Отдача статики
        location / {
            try_files $uri $uri/ /index.html;
        }

        # Проксирование API
        location /api/ {
            proxy_pass http://127.0.0.1:8000/api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    
Активируйте конфиг и перезапустите Nginx:
    
    sudo ln -s /etc/nginx/sites-available/lasercrm /etc/nginx/sites-enabled/
    sudo systemctl restart nginx
    
**Шаг 5. Настройка Firewall (Безопасность)**
Откройте только нужные порты:
    
    sudo ufw allow 'Nginx HTTP'
    sudo ufw allow OpenSSH
    sudo ufw enable
    
**Готово! 🎉** 
Теперь вы можете открыть интерфейс CRM с любого устройства в вашей Wi-Fi сети, просто введя локальный IP-адрес Raspberry Pi в браузере (например: `http://192.168.1.15`).
