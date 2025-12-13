from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .admin_schema import AdminWrite, AdminResponse
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.src.admin.admin_model import Admin, AdminPermission
from app.utils.custom_exceptions import ItemNotFound


class AdminDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_one_by_uid(self, user_id: int) -> AdminResponse | None:
        result = await self.db.execute(
            select(Admin)
            .options(selectinload(Admin.user))
            .where(Admin.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[AdminResponse] | None:
        result = await self.db.execute(select(Admin).options(selectinload(Admin.user)))
        return result.scalars().all()

    async def create(self, user_id: int) -> Admin:
        new = Admin(user_id=user_id, permission=AdminPermission.SUB.value)
        self.db.add(new)
        await self.db.commit()
        await self.db.refresh(new)
        return new

    async def delete(self, user_id: int) -> bool:
        result = await self.db.execute(select(Admin).where(Admin.user_id == user_id))
        admin = result.scalar_one_or_none()
        if not admin:
            raise ItemNotFound(item_id=user_id, item="admin")

        await self.db.delete(admin)
        await self.db.commit()
        return True


async def get_admin_dao(db: AsyncSession = Depends(get_db)) -> AdminDao:
    return AdminDao(db)
