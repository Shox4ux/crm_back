from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .warehouse_schema import WarehouseRead, WarehouseWrite
from sqlalchemy import select, update, delete
from app.src.warehouse.warehouse_model import Warehouse
from sqlalchemy.orm import selectinload, joinedload
from app.utils.custom_exceptions import ItemNotFound


class WarehouseDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_one(self, id: int) -> WarehouseRead | None:
        result = await self.db.execute(
            select(Warehouse)
            .options(selectinload(Warehouse.products))
            .where(Warehouse.id == id)
        )
        return result.unique().scalar_one_or_none()

    async def get_all(self) -> list[WarehouseRead] | None:
        result = await self.db.execute(
            select(Warehouse).options(joinedload(Warehouse.products))
        )
        return result.unique().scalars().all()

    async def create(self, data: WarehouseWrite) -> Warehouse:
        new_warehouse = Warehouse(**data.model_dump())
        self.db.add(new_warehouse)

        await self.db.commit()
        await self.db.refresh(new_warehouse)

        result = await self.db.execute(
            select(Warehouse)
            .options(selectinload(Warehouse.products))
            .where(Warehouse.id == new_warehouse.id)
        )
        return result.scalars().first()

    async def delete(self, id: int) -> bool:
        result = await self.db.execute(select(Warehouse).where(Warehouse.id == id))
        warehouse = result.scalar_one_or_none()
        if not warehouse:
            raise ItemNotFound(item_id=id, item="warehouse")

        await self.db.delete(warehouse)
        await self.db.commit()
        return True


async def get_w_dao(db: AsyncSession = Depends(get_db)) -> WarehouseDao:
    return WarehouseDao(db)
