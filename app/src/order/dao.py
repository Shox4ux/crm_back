from datetime import datetime
from app.data.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.admin.model import Admin

from app.src.order_cancel.model import OrderCancelInfo
from app.src.order_cancel.schema import OrderCancelCreate
from app.src.product.model import Product
from app.src.user.model import User
from .schema import OrderResponse, OrderCreate, OrderUpdate
from sqlalchemy import func, select, update, delete
from app.src.order.model import Order
from sqlalchemy.orm import selectinload
from app.utils.custom_exceptions import ItemNotFound
from app.src.warehouse_product.model import WarehouseProduct
from app.src.order_product.model import OrderProduct
from app.src.client.model import Client


class OrderDao:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_client_sales_report_between_dates(
        self,
        client_id: int,
        start: datetime,
        end: datetime,
    ) -> dict | None:
        """
        Returns aggregated purchased products for ONE client between given dates.

        Output format:
        {
            client_id,
            user_id,
            username,
            phone,
            address,
            purchased_prods: [
                {
                    prod_id,
                    name,
                    price,
                    sales_data: [
                        { sold_date, sold_price, sold_quantity }
                    ]
                }
            ]
        }

        Rule:
        If same product is ordered multiple times on same date (same sold_price),
        sum quantities.

        Date filter:
        start <= Order.created_at <= end
        """

        sold_date_expr = func.date(Order.created_at)  # OR func.date(Order.delivery_on)

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
            .where(
                Client.id == client_id,
                sold_date_expr >= start,
                sold_date_expr <= end,
            )
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
            .order_by(Product.id, sold_date_expr)
        )

        result = await self.db.execute(stmt)
        rows = result.mappings().all()

        if not rows:
            return None

        response = {
            "client_id": rows[0]["client_id"],
            "user_id": rows[0]["user_id"],
            "username": rows[0]["username"],
            "phone": rows[0]["phone"],
            "address": rows[0]["address"],
            "purchased_prods": [],
        }

        prods_map: dict[int, dict] = {}

        for row in rows:
            prod_id = row["prod_id"]

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

        response["purchased_prods"] = list(prods_map.values())
        return response

    async def get_one(self, id: int) -> OrderResponse | None:
        result = await self.db.execute(
            select(Order)
            .options(
                selectinload(Order.client),
                selectinload(Order.order_products)
                .selectinload(OrderProduct.warehouse_product)
                .selectinload(WarehouseProduct.product),
                selectinload(Order.cancel_info)
                .selectinload(OrderCancelInfo.canceler)
                .selectinload(Admin.user),
            )
            .where(Order.id == id)
        )
        if not result:
            raise ItemNotFound(item_id=id, item="order")

        return result.scalar_one_or_none()

    async def get_all(self) -> list[OrderResponse] | None:
        result = await self.db.execute(
            select(Order).options(
                selectinload(Order.client).selectinload(Client.user),
                selectinload(Order.client).selectinload(Client.products),
                selectinload(Order.order_products)
                .selectinload(OrderProduct.warehouse_product)
                .options(
                    selectinload(WarehouseProduct.warehouse),
                    selectinload(WarehouseProduct.product),
                ),
                selectinload(Order.cancel_info)
                .selectinload(OrderCancelInfo.canceler)
                .selectinload(Admin.user),
            )
        )

        return result.scalars().all()

    async def create(self, data: OrderCreate) -> Order:
        new = data.to_order()
        self.db.add(new)
        await self.db.commit()
        await self.db.refresh(new)
        return new

    async def delete(self, id: int) -> bool:
        result = await self.db.execute(select(Order).where(Order.id == id))
        order = result.scalar_one_or_none()

        if not order:
            raise ItemNotFound(item_id=id, item="order")

        await self.db.delete(order)
        await self.db.commit()
        return True

    async def update(self, id: int, data: OrderUpdate):
        result = await self.db.get_one(Order, id)
        if not result:
            raise ItemNotFound(item_id=id, item="order")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(result, field, value)

        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def cancel(self, id: int, data: OrderCancelCreate):

        result = await self.db.get_one(Order, id)
        if not result:
            raise ItemNotFound(item_id=id, item="order")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(result, field, value)

        await self.db.commit()
        await self.db.refresh(result)
        return result


async def get_or_dao(db: AsyncSession = Depends(get_db)) -> OrderDao:
    return OrderDao(db)
