from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.src.user.user_schema import CreateAsClient, CreateAsAdmin, UserUpdate
from sqlalchemy import select
from app.src.user.user_model import User
from app.utils.custom_exceptions import ItemNotFound
from app.src.auth.auth_method import get_pass_hashed


class UserDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def create_client(self, data: CreateAsClient, img_path: str | None):
        user = data.to_user(img_path)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def create_admin(self, data: CreateAsAdmin, img_path: str | None):
        user = User(
            username=data.username,
            password_hash=get_pass_hashed(data.password),
            role=1,
            img=img_path,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_all_clients(self):
        result = await self.db.execute(select(User).where(User.role == 0))
        return result.scalars().all()

    async def get_all_admins(self):
        result = await self.db.execute(select(User).where(User.role == 1))
        return result.scalars().all()

    async def get_user_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def delete_user(self, user: User) -> bool:
        await self.db.delete(user)
        await self.db.commit()
        return True

    async def update_user(self, user: User, data: UserUpdate, img_path: str | None):
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

        await self.db.commit()
        await self.db.refresh(user)
        return user


async def get_user_dao(db: AsyncSession = Depends(get_db)) -> UserDao:
    return UserDao(db)
