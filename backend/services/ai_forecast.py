from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple
import numpy as np

from ..db.models import Order

# Проверка наличия sklearn при импорте, чтобы избежать краша если пакет не установлен
try:
    from sklearn.linear_model import LinearRegression
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


async def predict_revenue(session: AsyncSession) -> Optional[Dict[str, Any]]:
    """
    Прогнозирует выручку на завтрашний день на основе данных за последние 30 дней.
    Использует линейную регрессию.
    
    :return: Словарь с прогнозом, трендом и уверенностью, либо None если мало данных.
    """
    if not SKLEARN_AVAILABLE:
        return {"error": "Scikit-learn not installed"}

    # 1. Получаем данные о завершенных заказах за последние 30 дней
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    stmt = (
        select(Order.total_price, Order.updated_at)
        .where(Order.status.in_(["DONE", "COMPLETED"]))
        .where(Order.updated_at >= thirty_days_ago)
        .order_by(Order.updated_at.asc())
    )
    
    result = await session.execute(stmt)
    rows = result.all()
    
    if not rows:
        return None

    # 2. Агрегация по дням (datetime.date -> sum_price)
    daily_revenue: Dict[datetime.date, float] = {}
    
    for price, date_obj in rows:
        if date_obj is None:
            continue
        day_key = date_obj.date()
        daily_revenue[day_key] = daily_revenue.get(day_key, 0.0) + float(price)

    # Если дней с активностью меньше 3, прогноз ненадежен
    if len(daily_revenue) < 3:
        avg_val = sum(daily_revenue.values()) / len(daily_revenue)
        return {
            "prediction": round(avg_val, 2),
            "trend": "stable",
            "confidence": 0.0,
            "message": "Недостаточно данных для ML-прогноза (менее 3 дней активности)"
        }

    # Подготовка данных для sklearn
    sorted_days = sorted(daily_revenue.keys())
    
    # X: порядковый номер дня (0, 1, 2...)
    # y: выручка в этот день
    X = np.array([[i] for i in range(len(sorted_days))])
    y = np.array([daily_revenue[day] for day in sorted_days])

    # 3. Обучение модели
    model = LinearRegression()
    model.fit(X, y)
    
    # 4. Предсказание на следующий день
    next_day_index = len(sorted_days)
    predicted_value = model.predict([[next_day_index]])[0]
    
    # 5. Определение тренда по коэффициенту наклона
    slope = model.coef_[0]
    
    # Пороги значимости тренда (можно настроить)
    if slope > 500: 
        trend = "up"
    elif slope < -500:
        trend = "down"
    else:
        trend = "stable"
        
    # 6. Расчет уверенности (R^2)
    confidence = model.score(X, y)
    
    # Финальная обработка результата
    final_prediction = max(0.0, predicted_value)
    
    return {
        "prediction": round(final_prediction, 2),
        "trend": trend,
        "confidence": round(confidence, 2),
        "message": f"Прогноз на основе {len(sorted_days)} дней активности"
    }
