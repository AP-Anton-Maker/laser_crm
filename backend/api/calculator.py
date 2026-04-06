from fastapi import APIRouter, Depends
from db.models import User
from api.deps import get_current_active_user
from services.calculator import CalculatorService, CalculatorParams

router = APIRouter(prefix="/calculator", tags=["Калькулятор"])

@router.post("/calculate", response_model=float)
async def calculate_price(
    params: CalculatorParams,
    current_user: User = Depends(get_current_active_user)
):
    """
    Эндпоинт для расчета стоимости заказа. 
    Вызывает CalculatorService со всеми 11 алгоритмами.
    """
    price = CalculatorService.calculate(params)
    return price
