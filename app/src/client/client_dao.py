from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .client_schema import ClientRead, ClientWrite
from sqlalchemy import select, update, delete
from .client_model import Client
from sqlalchemy.orm import selectinload, joinedload
from app.utils.custom_exceptions import ItemNotFound


class ClientDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_by_uid(self, user_id: int) -> ClientRead | None:
        result = await self.db.execute(
            select(Client)
            .options(selectinload(Client.user), selectinload(Client.products))
            .where(Client.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[ClientRead] | None:
        result = await self.db.execute(
            select(Client).options(
                selectinload(Client.user), selectinload(Client.products)
            )
        )
        return result.scalars().all()

    async def create(self, data: ClientWrite) -> Client:
        new = Client(**data.model_dump())
        self.db.add(new)
        await self.db.commit()
        await self.db.refresh(new)
        return new

    async def delete(self, user_id: int) -> bool:
        result = await self.db.execute(select(Client).where(Client.user_id == user_id))
        client = result.scalar_one_or_none()
        if not client:
            raise ItemNotFound(item_id=user_id, item="client")

        await self.db.delete(client)
        await self.db.commit()
        return True


async def get_c_dao(db: AsyncSession = Depends(get_db)) -> ClientDao:
    return ClientDao(db)
