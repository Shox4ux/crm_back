from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .client_schema import ClientRead, ClientWrite
from sqlalchemy import select, update, delete
from .client_model import Client
from sqlalchemy.orm import selectinload, joinedload
from app.utils.custom_exceptions import ItemNotFound
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except InvalidTokenError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


class ClientDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_one(self, user_id: int) -> ClientRead | None:
        result = await self.db.execute(
            select(Client)
            .options(selectinload(Client.user), selectinload(Client.products))
            .where(Client.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_secret_one(self, id: int) -> ClientRead | None:
        result = await self.db.execute(select(Client).where(Client.id == id))
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

    async def delete(self, id: int) -> bool:
        result = await self.db.execute(select(Client).where(Client.id == id))
        admin = result.scalar_one_or_none()
        if not admin:
            raise ItemNotFound(item_id=id, item="admin")

        await self.db.delete(admin)
        await self.db.commit()
        return True


async def get_c_dao(db: AsyncSession = Depends(get_db)) -> ClientDao:
    return ClientDao(db)
