from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.src.user.user_schema import UserUpdate
from sqlalchemy import select
from app.src.user.user_model import User
from app.src.auth.auth_method import get_pass_hashed


class UserDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def activate(self, user: User) -> User:
        if not user.is_active:
            user.is_active = True

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> User:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_by_username(self, username: str) -> User:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def delete(self, user: User) -> bool:
        await self.db.delete(user)
        await self.db.commit()
        return True

    async def update(self, user: User, data: UserUpdate, img_path: str | None):
        if data.username is not None:
            user.username = data.username

        if data.password is not None:  # always check None, not truthiness
            user.password_hash = get_pass_hashed(data.password)

        if img_path is not None:
            user.img = img_path

        if data.phone is not None:
            user.phone = data.phone

        if data.address is not None:
            user.address = data.address

        if data.is_active is not None:
            user.is_active = data.is_active

        await self.db.commit()
        await self.db.refresh(user)
        return user


async def get_user_dao(db: AsyncSession = Depends(get_db)) -> UserDao:
    return UserDao(db)
