from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List


class ClientBase(BaseModel):
    name: str = Field(..., description="Имя клиента")
    vk_id: Optional[str] = Field(None, description="ID ВКонтакте")
    phone: Optional[str] = Field(None, description="Телефон")


class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
    id: int
    segment: str
    total_orders: int
    total_spent: float
    cashback_balance: float
    created_at: datetime
    
    # Вычисляемое поле (можно добавить в сервисе, но здесь для примера структуры)
    # avg_check вычисляется на лету в API если нужно
    
    model_config = ConfigDict(from_attributes=True)


class CashbackHistoryResponse(BaseModel):
    id: int
    client_id: int
    operation_type: str  # earned, spent
    amount: float
    description: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
