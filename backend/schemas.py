from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- Токены ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Пользователи ---
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True

# --- Клиенты ---
class ClientBase(BaseModel):
    name: str
    vk_id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    notes: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Заказы ---
class OrderBase(BaseModel):
    description: str
    status: str = "new"
    price: float = 0.0
    cost_price: float = 0.0
    deadline: Optional[datetime] = None

class OrderCreate(OrderBase):
    client_id: int

class OrderUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[str] = None
    price: Optional[float] = None
    cost_price: Optional[float] = None
    deadline: Optional[datetime] = None

class OrderResponse(OrderBase):
    id: int
    client_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Склад (Инвентарь) ---
class InventoryBase(BaseModel):
    name: str
    quantity: float = 0.0
    unit: str = "шт"
    min_quantity: float = 0.0
    cost_per_unit: float = 0.0

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    min_quantity: Optional[float] = None
    cost_per_unit: Optional[float] = None

class InventoryResponse(InventoryBase):
    id: int

    class Config:
        from_attributes = True

# --- Чат ---
class ChatMessageResponse(BaseModel):
    id: int
    client_id: int
    direction: str
    text: str
    timestamp: datetime
    is_read: bool

    class Config:
        from_attributes = True
