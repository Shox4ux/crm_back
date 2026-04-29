import datetime
from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.src.user.model import User
from .schema import ClientResponse, ClientProdWrite, ClientProdUpdt
from sqlalchemy import func, select
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

    async def get_client_stats(self, start: datetime, end: datetime) -> list[dict]:
        sold_date_expr = func.date(Order.created_at)
        stmt = (
            select(
                Client.id.label("client_id"),
                User.id.label("user_id"),
                User.username.label("username"),
                User.phone.label("phone"),
                User.address.label("address"),
                Product.id.label("prod_id"),
                Product.name.label("prod_name"),
                Product.sell_price.label("prod_price"),
                sold_date_expr.label("sold_date"),
                OrderProduct.custom_price.label("sold_price"),
                func.sum(OrderProduct.custom_quantity).label("sold_quantity"),
            )
            .join(User, User.id == Client.user_id)
            .join(Order, Order.client_id == Client.id)
            .join(OrderProduct, OrderProduct.order_id == Order.id)
            .join(
                WarehouseProduct,
                WarehouseProduct.id == OrderProduct.warehouse_product_id,
            )
            .join(Product, Product.id == WarehouseProduct.product_id)
            .where(sold_date_expr >= start, sold_date_expr <= end)
            .group_by(
                Client.id,
                User.id,
                User.username,
                User.phone,
                User.address,
                Product.id,
                Product.name,
                Product.sell_price,
                sold_date_expr,
                OrderProduct.custom_price,
            )
            .order_by(Client.id, Product.id, sold_date_expr)
        )

        result = await self.db.execute(stmt)
        rows = result.mappings().all()

        if not rows:
            return None

        clients_map: dict[int, dict] = {}

        for row in rows:
            client_id = row["client_id"]
            prod_id = row["prod_id"]

            # Create client if not exists
            if client_id not in clients_map:
                clients_map[client_id] = {
                    "client_id": client_id,
                    "user_id": row["user_id"],
                    "username": row["username"],
                    "phone": row["phone"],
                    "address": row["address"],
                    "purchased_prods": [],
                }

            # Find or create product inside this client
            client_obj = clients_map[client_id]

            # We need a product map per client
            if "_prods_map" not in client_obj:
                client_obj["_prods_map"] = {}

            prods_map = client_obj["_prods_map"]

            if prod_id not in prods_map:
                prods_map[prod_id] = {
                    "prod_id": prod_id,
                    "name": row["prod_name"],
                    "price": row["prod_price"],
                    "sales_data": [],
                }

            prods_map[prod_id]["sales_data"].append(
                {
                    "sold_date": str(row["sold_date"]),
                    "sold_price": row["sold_price"],
                    "sold_quantity": int(row["sold_quantity"]),
                }
            )

        # Convert maps into final lists
        response: list[dict] = []

        for client in clients_map.values():
            client["purchased_prods"] = list(client["_prods_map"].values())
            del client["_prods_map"]  # remove internal helper
            response.append(client)

        return response

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
                .options(
                    selectinload(WarehouseProduct.product).selectinload(
                        Product.base_expenses
                    ),
                    selectinload(WarehouseProduct.warehouse),
                ),
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
                .options(
                    selectinload(WarehouseProduct.product).selectinload(
                        Product.base_expenses
                    ),
                    selectinload(WarehouseProduct.warehouse),
                ),
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
