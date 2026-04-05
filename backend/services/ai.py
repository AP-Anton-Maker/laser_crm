from sklearn.linear_model import LinearRegression
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta, timezone

from db.models import Order

class AIForecastService:
    @staticmethod
    async def predict_tomorrow_revenue(db: AsyncSession) -> dict:
        """
        Анализирует выручку за последние 30 дней с помощью линейной регрессии
        и предсказывает ожидаемую выручку на завтрашний день.
        """
        # Определяем окно в 30 дней
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        
        # Получаем данные о выручке по дням (для завершенных заказов)
        query = (
            select(
                func.date(Order.created_at).label("day"),
                func.sum(Order.price).label("daily_revenue")
            )
            .where(Order.created_at >= thirty_days_ago)
            .where(Order.status.in_(["ready", "delivered"]))
            .group_by(func.date(Order.created_at))
            .order_by("day")
        )
        
        result = await db.execute(query)
        rows = result.all()
        
        # Если данных слишком мало (меньше 3 дней), нейросети не на чем учиться
        if len(rows) < 3:
            return {
                "status": "not_enough_data",
                "message": "Недостаточно данных для AI-прогноза. Нужно минимум 3 дня продаж.",
                "predicted_revenue": 0.0,
                "trend": "neutral"
            }
            
        # Подготавливаем данные для scikit-learn (X - порядковый номер дня, y - выручка)
        X = np.array([[i] for i in range(len(rows))])
        y = np.array([float(row.daily_revenue) for row in rows])
        
        # Обучаем модель линейной регрессии
        model = LinearRegression()
        model.fit(X, y)
        
        # Предсказываем выручку на завтра (следующий день = len(rows))
        tomorrow_x = np.array([[len(rows)]])
        predicted = model.predict(tomorrow_x)[0]
        
        # Защита от отрицательной выручки (AI может уйти в минус при резком падении тренда)
        predicted_revenue = max(0.0, round(float(predicted), 2))
        
        # Определяем тренд (коэффициент наклона прямой)
        slope = model.coef_[0]
        if slope > 100:
            trend = "up"
        elif slope < -100:
            trend = "down"
        else:
            trend = "stable"
            
        return {
            "status": "success",
            "message": "Прогноз успешно построен",
            "predicted_revenue": predicted_revenue,
            "trend": trend,
            "data_points_used": len(rows)
        }
