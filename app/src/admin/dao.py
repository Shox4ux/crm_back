from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.src.admin.model import Admin


class AdminDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_by_uid(self, user_id: int) -> Admin:
        result = await self.db.execute(
            select(Admin)
            .options(selectinload(Admin.user))
            .where(Admin.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, id: int) -> Admin:
        result = await self.db.execute(
            select(Admin).options(selectinload(Admin.user)).where(Admin.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Admin] | None:
        result = await self.db.execute(select(Admin).options(selectinload(Admin.user)))
        return result.scalars().all()

    async def create(self, admin: Admin) -> Admin:
        self.db.add(admin)
        await self.db.commit()
        await self.db.refresh(admin)
        return admin

    async def delete(self, admin: Admin) -> bool:
        await self.db.delete(admin)
        await self.db.commit()
        return True


async def get_admin_dao(db: AsyncSession = Depends(get_db)) -> AdminDao:
    return AdminDao(db)
