from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import OrderRead, OrderCreate, OrderUpdate
from sqlalchemy import select, update, delete
from app.src.order.model import Order
from sqlalchemy.orm import selectinload
from app.utils.custom_exceptions import ItemNotFound
from app.src.warehouse_product.model import WarehouseProduct
from app.src.order_product.model import OrderProduct
from app.src.client.model import Client


class OrderDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_one(self, id: int) -> OrderRead | None:
        result = await self.db.execute(
            select(Order)
            .options(
                selectinload(Order.client),
                selectinload(Order.order_products)
                .selectinload(OrderProduct.warehouse_product)
                .selectinload(WarehouseProduct.product),
            )
            .where(Order.id == id)
        )
        if not result:
            raise ItemNotFound(item_id=id, item="order")

        return result.scalar_one_or_none()

    async def get_all(self) -> list[OrderRead] | None:
        result = await self.db.execute(
            select(Order).options(
                selectinload(Order.client).selectinload(Client.user),
                selectinload(Order.client).selectinload(Client.products),
                selectinload(Order.order_products)
                .selectinload(OrderProduct.warehouse_product)
                .selectinload(WarehouseProduct.product),
            )
        )

        return result.scalars().all()

    async def create(self, data: OrderCreate) -> Order:
        new = data.to_order()
        self.db.add(new)
        await self.db.commit()
        await self.db.refresh(new)
        return new

    async def delete(self, id: int) -> bool:
        result = await self.db.execute(select(Order).where(Order.id == id))
        order = result.scalar_one_or_none()

        if not order:
            raise ItemNotFound(item_id=id, item="order")

        await self.db.delete(order)
        await self.db.commit()
        return True

    async def update(self, id: int, data: OrderUpdate):
        result = await self.db.get_one(Order, id)
        if not result:
            raise ItemNotFound(item_id=id, item="order")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(result, field, value)

        await self.db.commit()
        await self.db.refresh(result)
        return result


async def get_or_dao(db: AsyncSession = Depends(get_db)) -> OrderDao:
    return OrderDao(db)
