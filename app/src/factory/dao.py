from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.src.factory.schema import FactoryRead, FactoryWrite
from sqlalchemy.orm import selectinload
from app.utils.custom_exceptions import ItemNotFound
from app.src.factory.model import Factory


class FactoryDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_one(self, id: int) -> FactoryRead | None:
        result = await self.db.execute(
            select(Factory)
            .options(selectinload(Factory.products))
            .where(Factory.id == id)
        )
        return result.unique().scalar_one_or_none()

    async def get_all(self) -> list[FactoryRead] | None:
        result = await self.db.execute(
            select(Factory).options(selectinload(Factory.products))
        )
        return result.unique().scalars().all()

    async def create(self, data: FactoryWrite) -> Factory:
        new_obj = Factory(**data.model_dump())
        self.db.add(new_obj)

        await self.db.commit()
        await self.db.refresh(new_obj)

        result = await self.db.execute(
            select(Factory)
            .options(selectinload(Factory.products))
            .where(Factory.id == new_obj.id)
        )
        return result.scalars().first()

    async def update(self, id: int, data: FactoryWrite) -> Factory:
        result = await self.db.execute(
            select(Factory)
            .options(selectinload(Factory.products))
            .where(Factory.id == id)
        )
        factory = result.scalar_one_or_none()
        if not factory:
            raise ItemNotFound(item_id=id, item="factory")
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(factory, field, value)
        await self.db.commit()
        await self.db.refresh(factory)
        return factory

    async def delete(self, id: int) -> bool:
        result = await self.db.execute(select(Factory).where(Factory.id == id))
        factory = result.scalar_one_or_none()
        if not factory:
            raise ItemNotFound(item_id=id, item="factory")

        await self.db.delete(factory)
        await self.db.commit()
        return True


async def get_f_dao(db: AsyncSession = Depends(get_db)) -> FactoryDao:
    return FactoryDao(db)
