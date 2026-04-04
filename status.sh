#!/bin/bash

# 📊 Laser CRM - Мониторинг статуса

echo "📊 Статус системы Laser CRM"
echo "============================"

# 1. Статус сервиса приложения
CRM_STATUS=$(systemctl is-active lasercrm 2>/dev/null || echo "inactive")
if [ "$CRM_STATUS" == "active" ]; then
    echo "✅ CRM Service: $CRM_STATUS (Running)"
else
    echo "❌ CRM Service: $CRM_STATUS (Stopped)"
fi

# 2. Статус Nginx
NGINX_STATUS=$(systemctl is-active nginx 2>/dev/null || echo "inactive")
if [ "$NGINX_STATUS" == "active" ]; then
    echo "✅ Nginx Web Server: $NGINX_STATUS (Running)"
else
    echo "❌ Nginx Web Server: $NGINX_STATUS (Stopped)"
fi

echo "----------------------------"

# 3. IP адрес
IP_ADDR=$(hostname -I | awk '{print $1}')
echo "🌐 IP Адрес: $IP_ADDR"

# 4. Температура CPU (специфично для Raspberry Pi)
if [ -f /sys/class/thermal/thermal_zone0/temp ]; then
    TEMP=$(cat /sys/class/thermal/thermal_zone0/temp)
    TEMP_C=$((TEMP / 1000))
    if [ $TEMP_C -gt 80 ]; then
        echo "🌡️  Температура CPU: ${TEMP_C}°C (⚠️ HOT!)"
    else
        echo "🌡️  Температура CPU: ${TEMP_C}°C"
    fi
else
    echo "🌡️  Температура CPU: Н/Д (Не Raspberry Pi?)"
fi

# 5. Использование ОЗУ
echo "💾 Использование ОЗУ:"
free -h | grep --color=never Mem

echo "----------------------------"
echo "📝 Последние логи CRM (если есть ошибки):"
sudo journalctl -u lasercrm -n 5 --no-pager
