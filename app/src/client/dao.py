from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import ClientResponse, ClientProdWrite, ClientProdUpdt
from sqlalchemy import select
from .model import Client, ClientProduct
from sqlalchemy.orm import selectinload
from app.utils.custom_exceptions import ItemNotFound
from app.src.order.model import Order
from app.src.order_product.model import OrderProduct
from app.src.warehouse_product.model import WarehouseProduct
from app.src.product.model import Product


class ClientDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_by_id(self, id: int) -> ClientResponse | None:
        result = await self.db.execute(
            select(Client)
            .options(
                selectinload(Client.user),
                selectinload(Client.products)
                .selectinload(ClientProduct.product)
                .selectinload(Product.base_expenses),
                selectinload(Client.orders)
                .selectinload(Order.order_products)
                .selectinload(OrderProduct.warehouse_product)
                .selectinload(WarehouseProduct.product)
                .selectinload(Product.base_expenses),
            )
            .where(Client.id == id)
            .limit(1)
        )
        client = result.scalar_one_or_none()
        if not client:
            raise ItemNotFound(item_id=id, item="client")

        return client

    async def get_all(self) -> list[ClientResponse] | None:
        result = await self.db.execute(
            select(Client).options(
                selectinload(Client.user),
                selectinload(Client.products)
                .selectinload(ClientProduct.product)
                .selectinload(Product.base_expenses),
                selectinload(Client.orders)
                .selectinload(Order.order_products)
                .selectinload(OrderProduct.warehouse_product)
                .selectinload(WarehouseProduct.product)
                .selectinload(Product.base_expenses),
            )
        )
        return result.scalars().all()

    async def create(self, client: Client) -> Client:
        self.db.add(client)
        await self.db.commit()
        await self.db.refresh(client)
        return client

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
