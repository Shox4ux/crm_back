from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .order_product_schema import OrderProdRead, OrderProdWrite, OrderProdBase
from sqlalchemy import select
from app.src.order_product.order_product_model import OrderProduct
from app.src.warehouse_product.warehouse_product_model import WarehouseProduct
from sqlalchemy.orm import selectinload
from app.utils.custom_exceptions import ItemNotFound


class OrderProductDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_one(self, id: int) -> OrderProdRead | None:
        result = await self.db.execute(
            select(OrderProduct)
            .options(selectinload(OrderProduct.warehouse_product))
            .where(OrderProduct.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[OrderProdRead] | None:
        result = await self.db.execute(
            select(OrderProduct).options(
                selectinload(OrderProduct.warehouse_product).selectinload(
                    WarehouseProduct.product
                ),
            )
        )
        return result.scalars().all()

    async def create(self, data: OrderProdWrite) -> OrderProduct:
        new = OrderProduct(**data.model_dump())
        self.db.add(new)
        await self.db.commit()
        await self.db.refresh(new)

        return new

    async def delete(self, id: int) -> bool:
        result = await self.db.execute(
            select(OrderProduct).where(OrderProduct.id == id)
        )
        orderProd = result.scalar_one_or_none()
        if not orderProd:
            raise ItemNotFound(item_id=id, item="order product")

        await self.db.delete(orderProd)
        await self.db.commit()
        return True

    async def update(self, id: int, data: OrderProdBase):
        result = await self.db.get_one(OrderProduct, id)

        if not result:
            raise ItemNotFound(item_id=id, item="order")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(result, field, value)

        await self.db.commit()
        await self.db.refresh(result)
        return result


async def get_orp_dao(db: AsyncSession = Depends(get_db)) -> OrderProductDao:
    return OrderProductDao(db)
