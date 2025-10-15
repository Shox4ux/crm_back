from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .user_schema import UserRead, UserWrite
from sqlalchemy import select, update, delete
from app.src.user.user_model import User
from app.utils.custom_exceptions import ItemNotFound


class UserDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_by_username(self, username: str) -> UserRead | None:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_id(self, id: int) -> UserRead | None:
        result = await self.db.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[UserRead] | None:
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def create(self, data: UserWrite) -> User:
        new_user = User(**data.model_dump())
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def delete(self, id: int) -> bool:
        result = await self.db.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()

        if not user:
            raise ItemNotFound(item_id=id, item="user")

        await self.db.delete(user)
        await self.db.commit()
        return True


async def get_user_dao(db: AsyncSession = Depends(get_db)) -> UserDao:
    return UserDao(db)
