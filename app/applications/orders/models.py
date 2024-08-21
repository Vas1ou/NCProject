from datetime import datetime
import enum
from sqlalchemy import Column, Integer, ForeignKey, Enum, String, DateTime
from sqlalchemy.orm import relationship

from db.base import Base


class OrderStatusEnum(enum.Enum):
    """
    Enum для статусов заказа.
    """

    # Заказ ожидает обработки
    PENDING = "pending"
    # Заказ в процессе выполнения
    IN_PROGRESS = "in_progress"
    # Заказ завершен
    COMPLETED = "completed"
    # Заказ отменен
    CANCELED = "canceled"


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    details = Column(String, nullable=False)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship('User', back_populates='orders')
    notifications = relationship("Notification", back_populates='order')


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    order = relationship(Order, back_populates='notifications')