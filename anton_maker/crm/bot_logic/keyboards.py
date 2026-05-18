import json

def get_main_keyboard():
    keyboard = {
        "one_time": False,
        "inline": False,
        "buttons": [
            [{"action": {"type": "text", "label": "📝 Новый заказ"}, "color": "primary"}],
            [{"action": {"type": "text", "label": "📦 Мои заказы"}, "color": "secondary"}],
            [{"action": {"type": "text", "label": "ℹ️ Помощь"}, "color": "default"}]
        ]
    }
    return json.dumps(keyboard, ensure_ascii=False)

def get_cancel_keyboard():
    keyboard = {
        "one_time": True,
        "inline": False,
        "buttons": [
            [{"action": {"type": "text", "label": "❌ Отмена"}, "color": "negative"}]
        ]
    }
    return json.dumps(keyboard, ensure_ascii=False)

def get_yes_no_keyboard():
    keyboard = {
        "one_time": True,
        "inline": False,
        "buttons": [
            [{"action": {"type": "text", "label": "✅ Да"}, "color": "positive"}, {"action": {"type": "text", "label": "❌ Нет"}, "color": "negative"}]
        ]
    }
    return json.dumps(keyboard, ensure_ascii=False)
