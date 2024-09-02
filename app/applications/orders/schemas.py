from datetime import datetime
from enum import Enum
from pydantic import BaseModel

from applications.users.schemas import UserRead


class OrderStatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    canceled = "canceled"


class OrderBase(BaseModel):
    details: str

    class Config:
        orm_mode = True


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: int
    user: UserRead
    status: OrderStatusEnum
    created_at: datetime
    updated_at: datetime
