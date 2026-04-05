from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from db.session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    vk_id = Column(String(50), unique=True, index=True, nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    orders = relationship("Order", back_populates="client")
    messages = relationship("ChatMessage", back_populates="client")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), default="new") # new, in_progress, ready, delivered, cancelled
    price = Column(Float, default=0.0)
    cost_price = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    deadline = Column(DateTime, nullable=True)
    
    client = relationship("Client", back_populates="orders")

class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    quantity = Column(Float, default=0.0)
    unit = Column(String(20), default="шт") # шт, мм, см, м, кг
    min_quantity = Column(Float, default=0.0)
    cost_per_unit = Column(Float, default=0.0)

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    direction = Column(String(10)) # "in" (от клиента), "out" (от нас)
    text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_read = Column(Boolean, default=False)
    
    client = relationship("Client", back_populates="messages")

class SystemSettings(Base):
    __tablename__ = "system_settings"
    
    key = Column(String(50), primary_key=True, index=True)
    value = Column(Text, nullable=False)
