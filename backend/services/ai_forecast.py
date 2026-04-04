from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import numpy as np

from ..db.models import Order
from sklearn.linear_model import LinearRegression


async def predict_revenue(session: AsyncSession) -> Optional[Dict[str, Any]]:
    """
    Прогнозирует выручку на завтрашний день на основе данных за последние 30 дней.
    Использует линейную регрессию (Linear Regression).
    
    Возвращает:
    - prediction: прогнозируемая сумма
    - trend: 'up', 'down', 'stable'
    - confidence: условная уверенность (R^2 или вариация)
    """
    
    # 1. Получаем данные: сумма total_price по дням для завершенных заказов (DONE/COMPLETED)
    # Для SQLite используем date() функцию или работу со строками, если тип DateTime
    # Здесь упрощенный вариант: берем все заказы со статусом DONE за 30 дней и группируем вручную в Python,
    # так как агрегация по дате в разных СУБД отличается синтаксически.
    
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    stmt = (
        select(Order.total_price, Order.updated_at) # updated_at лучше отражает дату завершения
        .where(Order.status.in_(["DONE", "COMPLETED"]))
        .where(Order.updated_at >= thirty_days_ago)
        .order_by(Order.updated_at.asc())
    )
    
    result = await session.execute(stmt)
    rows = result.all()
    
    if not rows:
        return None

    # 2. Агрегируем данные по дням (день -> сумма)
    daily_revenue = {}
    for price, date_obj in rows:
        if date_obj is None:
            continue
        day_key = date_obj.date()
        daily_revenue[day_key] = daily_revenue.get(day_key, 0.0) + price

    # Преобразуем в списки для sklearn
    # X: номер дня относительно начала периода (0, 1, 2...)
    # y: выручка в этот день
    sorted_days = sorted(daily_revenue.keys())
    
    if len(sorted_days) < 3:
        # Недостаточно данных для обучения модели
        return {
            "prediction": sum(daily_revenue.values()) / len(daily_revenue),
            "trend": "stable",
            "confidence": 0.0,
            "message": "Недостаточно данных для точного прогноза (менее 3 дней)"
        }

    X = np.array([[i] for i in range(len(sorted_days))])
    y = np.array([daily_revenue[day] for day in sorted_days])

    # 3. Обучаем модель
    model = LinearRegression()
    model.fit(X, y)
    
    # 4. Делаем прогноз на следующий день (следующий индекс X)
    next_day_index = len(sorted_days)
    predicted_value = model.predict([[next_day_index]])[0]
    
    # 5. Определяем тренд по коэффициенту наклона (coef_)
    slope = model.coef_[0]
    if slope > 100: # Порог значимости роста (100 руб/день)
        trend = "up"
    elif slope < -100:
        trend = "down"
    else:
        trend = "stable"
        
    # 6. Расчет уверенности (R^2 score)
    confidence = model.score(X, y)
    
    # Ограничиваем прогноз нулем (не может быть минус выручки)
    final_prediction = max(0.0, round(predicted_value, 2))
    
    return {
        "prediction": final_prediction,
        "trend": trend,
        "confidence": round(confidence, 2),
        "message": f"Прогноз на основе {len(sorted_days)} дней активности"
    }
