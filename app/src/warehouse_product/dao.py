from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import WareProdRead, WareProdWrite, InnerWareProdRead
from sqlalchemy import select
from app.src.warehouse_product.model import WarehouseProduct
from sqlalchemy.orm import selectinload
from app.utils.custom_exceptions import ItemNotFound


class WarehouseProductDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_one(self, id: int) -> InnerWareProdRead | None:
        result = await self.db.execute(
            select(WarehouseProduct)
            .options(selectinload(WarehouseProduct.product))
            .where(WarehouseProduct.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all_by_w_id(self, ware_id: int) -> list[WareProdRead] | None:
        result = await self.db.execute(
            select(WarehouseProduct)
            .options(selectinload(WarehouseProduct.product))
            .where(WarehouseProduct.warehouse_id == ware_id)
        )
        return result.scalars().all()

    async def get_all(self) -> list[WareProdRead] | None:
        result = await self.db.execute(
            select(WarehouseProduct).options(
                selectinload(WarehouseProduct.product),
                selectinload(WarehouseProduct.warehouse),
            )
        )
        return result.scalars().all()

    async def create(self, data: WareProdWrite) -> WarehouseProduct:
        new = WarehouseProduct(**data.model_dump())
        self.db.add(new)

        await self.db.commit()
        await self.db.refresh(new)
        return new

    async def delete(self, id: int) -> bool:
        result = await self.db.execute(
            select(WarehouseProduct).where(WarehouseProduct.id == id)
        )
        warehouseProd = result.scalar_one_or_none()
        if not warehouseProd:
            raise ItemNotFound(item_id=id, item="warehouse product")

        await self.db.delete(warehouseProd)
        await self.db.commit()
        return True


async def get_wp_dao(db: AsyncSession = Depends(get_db)) -> WarehouseProductDao:
    return WarehouseProductDao(db)
