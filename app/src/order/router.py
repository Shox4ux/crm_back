from datetime import datetime
from fastapi import APIRouter, Depends
from app.src.order.dto import ClientOrdersDTO
from app.src.order_product.schema import OrderProCreate
from app.src.product.schema import ProductBase
from app.src.warehouse_product.schema import WareProdUpdate
from app.utils.custom_exceptions import ItemNotFound, ServerError
from app.utils.enums import OrderStatus
from .dao import OrderDao, get_or_dao
from typing import Optional
from app.src.order.schema import (
    OrderResponse,
    OrderBase,
    OrderCreate,
    OrderUpdate,
)
from app.src.order_product.dao import OrderProductDao, get_orp_dao
from app.src.warehouse_product.dao import WarehouseProductDao, get_wp_dao
from app.src.product.dao import ProductDao, get_prod_dao

router = APIRouter(prefix="/orders", tags=["order"])


@router.get("/clients/{client_id}/orders")
async def get_client_orders(
    client_id: int, start: datetime, end: datetime, dao: OrderDao = Depends(get_or_dao)
):
    return await dao.get_client_sales_report_between_dates(client_id, start, end)


@router.get("/get_by_id/{id}", response_model=Optional[OrderResponse])
async def get_by_id(id: int, dao: OrderDao = Depends(get_or_dao)):
    order_prod = await dao.get_one(id)
    return order_prod


@router.get("/get_all", response_model=Optional[list[OrderResponse]])
async def get_all(dao: OrderDao = Depends(get_or_dao)):
    orders = await dao.get_all()
    return orders


@router.post("/create")
async def create(
    data: OrderCreate,
    dao: OrderDao = Depends(get_or_dao),
    wp_dao: WarehouseProductDao = Depends(get_wp_dao),
    p_dao: ProductDao = Depends(get_prod_dao),
    orp_dao: OrderProductDao = Depends(get_orp_dao),
):
    if not data.order_products:
        raise ServerError(msg="Order products are required")

    order = await dao.create(data)
    if not order:
        raise Exception()

    await _reduce_wp_qty(data.order_products, wp_dao, p_dao)

    if data.delivery_on.date() > datetime.datetime.now().date():
        data.status = OrderStatus.PREPAID.value
    elif data.paid_amount == data.total_amount:
        data.status = OrderStatus.PAID.value
    else:
        data.status = OrderStatus.UNPAID.value

    await orp_dao.create(order.id, data.order_products)

    return "Successfully created"


async def _reduce_wp_qty(
    items: list[OrderProCreate], wp_dao: WarehouseProductDao, p_dao: ProductDao
):

    for item in items:
        wp = await wp_dao.get_one(item.warehouse_product_id)
        if not wp:
            raise ItemNotFound(
                item_id=item.warehouse_product_id, item="warehouse product"
            )
        if wp.quantity < item.custom_quantity:
            raise ServerError(
                msg=f"Not enough quantity for warehouse product id {item.warehouse_product_id}"
            )

        await wp_dao.update(
            id=item.warehouse_product_id,
            data=WareProdUpdate(quantity=wp.quantity - item.custom_quantity),
        )

        prod = await p_dao.get_one(wp.product.id)
        if not prod:
            raise ItemNotFound(item_id=wp.product.id, item="product")

        await p_dao.update(
            id=wp.product.id,
            data=ProductBase(total_quantity=prod.total_quantity - item.custom_quantity),
        )


@router.patch("/update/{id}", response_model=Optional[OrderBase])
async def update_status(
    id: int,
    data: OrderUpdate,
    dao: OrderDao = Depends(get_or_dao),
    orp_dao: OrderProductDao = Depends(get_orp_dao),
):

    order = await dao.get_one(id)
    if not order:
        raise ItemNotFound(item_id=id, item="order")
    order = await dao.update(id, data)
    if data.new_order_products:
        await orp_dao.create(order.id, data.new_order_products)
    if data.updated_order_products:
        for item in data.updated_order_products:
            await orp_dao.update(item)
    if data.deleted_order_products:
        for item_id in data.deleted_order_products:
            await orp_dao.delete(item_id)

    return order
