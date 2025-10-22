from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .warehouse_product_schema import WarehouseProdRead, WarehouseProdWrite
from sqlalchemy import select, update, delete
from app.src.warehouse_product.warehouse_product_model import WarehouseProduct
from sqlalchemy.orm import selectinload, joinedload
from app.utils.custom_exceptions import ItemNotFound


class WarehouseProductDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_one(self, id: int) -> WarehouseProdRead | None:
        result = await self.db.execute(
            select(WarehouseProduct)
            .options(selectinload(WarehouseProduct.product))
            .where(WarehouseProduct.id == id)
        )
        return result.unique().scalar_one_or_none()

    async def get_all(self) -> list[WarehouseProdRead] | None:
        result = await self.db.execute(
            select(WarehouseProduct).options(joinedload(WarehouseProduct.product))
        )
        return result.unique().scalars().all()

    async def create(self, data: WarehouseProdWrite) -> WarehouseProduct:
        new = WarehouseProduct(**data.model_dump())
        self.db.add(new)

        await self.db.commit()
        await self.db.refresh(new)

        result = await self.db.execute(
            select(WarehouseProduct)
            .options(selectinload(WarehouseProduct.product))
            .where(WarehouseProduct.id == new.id)
        )
        return result.scalars().first()

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
