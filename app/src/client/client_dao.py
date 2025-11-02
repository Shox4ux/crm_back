from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .client_schema import (
    ClientRead,
    ClientWrite,
    ClientProdWrite,
    ClientUpdt,
    ClientProdUpdt,
)
from sqlalchemy import select, update, delete
from .client_model import Client, ClientProduct
from sqlalchemy.orm import selectinload, joinedload
from app.utils.custom_exceptions import ItemNotFound
from app.src.order.order_model import Order
from app.src.order_product.order_product_model import OrderProduct
from app.src.warehouse_product.warehouse_product_model import WarehouseProduct


class ClientDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_by_uid(self, user_id: int) -> ClientRead | None:
        result = await self.db.execute(
            select(Client)
            .options(
                selectinload(Client.user),
                selectinload(Client.products).selectinload(ClientProduct.product),
                selectinload(Client.orders)
                .selectinload(Order.order_products)
                .selectinload(OrderProduct.warehouse_product)
                .selectinload(WarehouseProduct.product),
            )
            .where(Client.user_id == user_id)
        )

        if not result:
            raise ItemNotFound(item_id=user_id, item="client")

        return result.scalar_one_or_none()

    async def get_by_id(self, id: int) -> ClientRead | None:
        result = await self.db.execute(
            select(Client)
            .options(selectinload(Client.user), selectinload(Client.products))
            .where(Client.id == id)
        )

        if not result:
            raise ItemNotFound(item_id=id, item="client")

        return result.scalar_one_or_none()

    async def get_all(self) -> list[ClientRead] | None:
        result = await self.db.execute(
            select(Client).options(
                selectinload(Client.user),
                selectinload(Client.products).selectinload(ClientProduct.product),
                selectinload(Client.orders)
                .selectinload(Order.order_products)
                .selectinload(OrderProduct.warehouse_product)
                .selectinload(WarehouseProduct.product),
            )
        )
        return result.scalars().all()

    async def create(self, data: ClientWrite) -> Client:
        new = Client(**data.model_dump())
        self.db.add(new)
        await self.db.commit()
        await self.db.refresh(new)
        return new

    async def create_cp(self, data: ClientProdWrite):
        new = ClientProduct(**data.model_dump())
        self.db.add(new)
        await self.db.commit()
        await self.db.refresh(new)

    async def delete(self, id: int) -> bool:
        result = await self.db.execute(select(Client).where(Client.id == id))
        client = result.scalar_one_or_none()
        if not client:
            raise ItemNotFound(item_id=id, item="client")

        await self.db.delete(client)
        await self.db.commit()
        return True

    async def update(self, id: int, data: ClientUpdt):
        result = await self.db.get_one(Client, id)

        if not result:
            raise ItemNotFound(item_id=id, item="client")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(result, field, value)

        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def update_cp(self, id: int, data: ClientProdUpdt):
        result = await self.db.get_one(ClientProduct, id)

        if not result:
            raise ItemNotFound(item_id=id, item="client product")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(result, field, value)

        await self.db.commit()
        await self.db.refresh(result)
        return result


async def get_c_dao(db: AsyncSession = Depends(get_db)) -> ClientDao:
    return ClientDao(db)
