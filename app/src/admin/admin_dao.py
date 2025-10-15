from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .admin_schema import AdminWrite, AdminRead
from sqlalchemy import select, update, delete
from app.src.admin.admin_model import Admin
from app.utils.custom_exceptions import ItemNotFound


class AdminDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_one(self, id: int) -> AdminRead | None:
        result = await self.db.execute(select(Admin).where(Admin.id == id))
        return result.scalar_one_or_none()

    async def get_secret_one(self, secret: str) -> AdminRead | None:
        result = await self.db.execute(select(Admin).where(Admin.secret_name == secret))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[AdminRead] | None:
        result = await self.db.execute(select(Admin))
        return result.scalars().all()

    async def create(self, data: AdminWrite) -> Admin:
        new = Admin(**data.model_dump())
        self.db.add(new)
        await self.db.commit()
        await self.db.refresh(new)
        return new

    async def delete(self, id: int) -> bool:
        result = await self.db.execute(select(Admin).where(Admin.id == id))
        admin = result.scalar_one_or_none()
        if not admin:
            raise ItemNotFound(item_id=id, item="admin")

        await self.db.delete(admin)
        await self.db.commit()
        return True


async def get_admin_dao(db: AsyncSession = Depends(get_db)) -> AdminDao:
    return AdminDao(db)
