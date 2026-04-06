from datetime import datetime, timezone
from typing import List, Optional
import enum
from sqlalchemy import String, Float, Integer, Boolean, ForeignKey, DateTime, Enum as SAEnum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.session import Base

# --- Энумераторы (Enums) ---

class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    master = "master"

class OrderStatus(str, enum.Enum):
    NEW = "NEW"
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    DELIVERED = "DELIVERED"

class OrderPriority(str, enum.Enum):
    NORMAL = "NORMAL"
    URGENT = "URGENT"

class ChatDirection(str, enum.Enum):
    IN = "in"   # От клиента к нам
    OUT = "out" # От нас клиенту

# --- Модели БД (SQLAlchemy 2.0 Mapped) ---

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), default=UserRole.manager, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    vk_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True, index=True, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    ltv: Mapped[float] = mapped_column(Float, default=0.0, nullable=False) # Lifetime Value (общая выручка)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cashback_balance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Связи
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="client", cascade="all, delete")
    messages: Mapped[List["ChatMessage"]] = relationship("ChatMessage", back_populates="client", cascade="all, delete")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(SAEnum(OrderStatus), default=OrderStatus.NEW, nullable=False)
    price: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    cost_price: Mapped[float] = mapped_column(Float, default=0.0, nullable=False) # Себестоимость
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    priority: Mapped[OrderPriority] = mapped_column(SAEnum(OrderPriority), default=OrderPriority.NORMAL, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Связи
    client: Mapped["Client"] = relationship("Client", back_populates="orders")


class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    quantity: Mapped[float] = mapped_column(Float, default=0.0, nullable=False) # Может быть в см2, метрах или штуках
    min_quantity_alert: Mapped[float] = mapped_column(Float, default=10.0, nullable=False)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    direction: Mapped[ChatDirection] = mapped_column(SAEnum(ChatDirection), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Связи
    client: Mapped["Client"] = relationship("Client", back_populates="messages")


class SystemSettings(Base):
    __tablename__ = "system_settings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    key: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
