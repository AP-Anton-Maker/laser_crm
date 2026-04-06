from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
import numpy as np
from sklearn.linear_model import LinearRegression

from db.models import Order, OrderStatus

class AIForecastService:
    @staticmethod
    async def predict_tomorrow_revenue(db: AsyncSession) -> dict:
        """
        Собирает выручку за последние 30 дней и с помощью LinearRegression
        строит прогноз (сумма на завтра и тренд).
        """
        today = datetime.now(timezone.utc)
        start_date = today - timedelta(days=30)
        
        # Запрашиваем выручку по дням для успешных заказов
        stmt = (
            select(
                func.date(Order.created_at).label("day"),
                func.sum(Order.price).label("daily_revenue")
            )
            .where(Order.status.in_([OrderStatus.DONE, OrderStatus.DELIVERED]))
            .where(Order.created_at >= start_date)
            .group_by("day")
            .order_by("day")
        )
        
        result = await db.execute(stmt)
        rows = result.fetchall()
        
        # Если данных слишком мало (менее 3 дней), AI не сможет построить адекватную модель
        if len(rows) < 3:
            return {
                "forecast": 0.0,
                "trend": "stable",
                "message": "Недостаточно данных для прогноза (нужно минимум 3 дня с выручкой)"
            }
            
        # Подготовка данных для машинного обучения
        # X: индексы дней (1, 2, 3...)
        # y: выручка в этот день
        X = []
        y = []
        
        for idx, row in enumerate(rows):
            X.append([idx]) # scikit-learn требует 2D массив для X
            # Если выручки нет, sum() возвращает None, защищаемся от этого
            revenue = float(row.daily_revenue) if row.daily_revenue else 0.0
            y.append(revenue)
            
        X = np.array(X)
        y = np.array(y)
        
        # Обучение модели линейной регрессии
        model = LinearRegression()
        model.fit(X, y)
        
        # Прогнозирование на завтра (индекс len(rows))
        next_day_idx = np.array([[len(rows)]])
        prediction = model.predict(next_day_idx)[0]
        
        # Определяем тренд (коэффициент наклона линии регрессии)
        slope = model.coef_[0]
        if slope > 50: # Если растет больше чем на 50 руб в день
            trend = "up"
        elif slope < -50:
            trend = "down"
        else:
            trend = "stable"
            
        # Защита от отрицательного прогноза
        predicted_revenue = max(0.0, float(prediction))
        
        return {
            "forecast": round(predicted_revenue, 2),
            "trend": trend,
            "message": "Прогноз успешно построен"
        }
