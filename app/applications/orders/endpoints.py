from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.sessions import get_db
from .models import Order, OrderStatusEnum as OSEnum
from .schemas import OrderResponse, OrderCreate, OrderStatusEnum
from applications.users.models import User
from ..users.utils import get_current_user

router = APIRouter()


@router.post('', response_model=OrderResponse)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    db_order = Order(
        user_id = current_user.id,
        details = order.details,
    )

    db.add(db_order)
    await db.commit()
    await db.refresh(db_order, ["user"])
    """
    тут, возможно, буду отправлять уведомление о создании заказа через kafka, пока не разобрался
    """

    return db_order


@router.put('/{order_id}/status', response_model=OrderResponse)
async def update_order_status(order_id: int, status: OrderStatusEnum, db: AsyncSession = Depends(get_db),
                              current_user: User = Depends(get_current_user)):

    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()

    if not order:
        raise HTTPException(status_code=404, detail='Order not found')

    order.status = OSEnum(status)
    await db.commit()
    await db.refresh(order, ['user'])

    """
    Тут через кафку буду отправлять уведомления о смене статуса заказа
    """

    return order