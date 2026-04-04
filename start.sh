#!/bin/bash

# ▶️ Laser CRM - Запуск сервисов

echo "▶️ Запуск Laser CRM..."

# Перезапуск backend сервиса
echo "🔄 Перезапуск backend (uvicorn)..."
sudo systemctl restart lasercrm
if [ $? -eq 0 ]; then
    echo "✅ Backend запущен."
else
    echo "❌ Ошибка запуска backend!"
    exit 1
fi

# Перезапуск web сервера
echo "🔄 Перезапуск web server (nginx)..."
sudo systemctl restart nginx
if [ $? -eq 0 ]; then
    echo "✅ Nginx запущен."
else
    echo "❌ Ошибка запуска nginx!"
    exit 1
fi

echo "--------------------------"
echo "🎉 Система полностью запущена!"
echo "🌐 Доступно по адресу: http://$(hostname -I | awk '{print $1}')"
