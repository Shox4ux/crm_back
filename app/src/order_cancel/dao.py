from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.src.admin.model import Admin
from app.src.order_cancel.model import OrderCancelInfo


class OrderCancelInfoDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_one(self, id: int) -> OrderCancelInfo:
        result = await self.db.execute(
            select(OrderCancelInfo)
            .options(selectinload(OrderCancelInfo.canceler).selectinload(Admin.user))
            .where(OrderCancelInfo.id == id)
        )
        return result.scalar_one_or_none()

    async def get_one_by_order_id(self, order_id: int) -> OrderCancelInfo:
        result = await self.db.execute(
            select(OrderCancelInfo)
            .options(selectinload(OrderCancelInfo.canceler))
            .where(OrderCancelInfo.order_id == order_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[OrderCancelInfo] | None:
        result = await self.db.execute(
            select(OrderCancelInfo).options(
                selectinload(OrderCancelInfo.canceler).selectinload(Admin.user)
            )
        )
        return result.scalars().all()

    async def create(self, data: OrderCancelInfo) -> OrderCancelInfo:
        self.db.add(data)
        await self.db.commit()
        await self.db.refresh(data)
        return data

    async def delete(self, data: OrderCancelInfo) -> bool:
        await self.db.delete(data)
        await self.db.commit()
        return True


async def get_cancel_dao(db: AsyncSession = Depends(get_db)) -> OrderCancelInfo:
    return OrderCancelInfoDao(db)
