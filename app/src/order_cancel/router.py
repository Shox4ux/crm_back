from fastapi import APIRouter, status, Depends

from app.src.order.schema import OrderUpdate
from app.src.order_cancel.model import OrderCancelInfo
from app.src.order_product.schema import OrderProdResponse
from app.src.product.schema import ProductBase
from app.src.warehouse_product.schema import WareProdUpdate
from .dao import OrderCancelInfoDao, get_cancel_dao
from typing import Optional
from app.utils.custom_exceptions import ItemNotFound, ServerError
from .schema import OrderCancelCreate, OrderCancelResponse
from app.src.order.dao import OrderDao, get_or_dao
from app.src.order.model import Order
from app.utils.enums import CancelType, OrderStatus
from app.src.order_product.dao import OrderProductDao, get_orp_dao
from app.src.warehouse_product.dao import WarehouseProductDao, get_wp_dao
from app.src.product.dao import ProductDao, get_prod_dao

router = APIRouter(prefix="/order_cancels", tags=["order_cancel"])


@router.get("/get_one/{id}", response_model=Optional[OrderCancelResponse])
async def get_by_id(id: int, dao: OrderCancelInfoDao = Depends(get_cancel_dao)):
    cancel_info = await dao.get_one(id)
    if not cancel_info:
        raise ItemNotFound(item_id=id, item="cancel_info")
    return cancel_info


@router.get("/get_all", response_model=Optional[list[OrderCancelResponse]])
async def get_all(dao: OrderCancelInfoDao = Depends(get_cancel_dao)):
    cancel_infos = await dao.get_all()
    return cancel_infos


@router.post("/create")
async def create(
    data: OrderCancelCreate,
    can_dao: OrderCancelInfoDao = Depends(get_cancel_dao),
    ord_dao: OrderDao = Depends(get_or_dao),
    p_dao: ProductDao = Depends(get_prod_dao),
    wp_dao: WarehouseProductDao = Depends(get_wp_dao),
):

    canceled_ord = await can_dao.get_one_by_order_id(data.order_id)
    if canceled_ord:
        raise ServerError(msg=f"Order with id {data.order_id} is already canceled")

    order = await ord_dao.get_one(data.order_id)
    if not order:
        raise ItemNotFound(item_id=data.order_id, item="order")

    cancel_info = await can_dao.create(OrderCancelInfo(**data.model_dump()))
    if not cancel_info:
        raise Exception()

    if data.cancel_type == CancelType.RETURN.value:
        await _return_wp_qty(order.order_products, wp_dao, p_dao)

    await _change_order_status(data=data, ord_dao=ord_dao)

    return {"message": "Successfully canceled"}


async def _return_wp_qty(
    items: list[OrderProdResponse], wp_dao: WarehouseProductDao, p_dao: ProductDao
):
    for item in items:
        wp = await wp_dao.get_one(item.warehouse_product_id)
        if not wp:
            raise ItemNotFound(
                item_id=item.warehouse_product_id, item="warehouse product"
            )

        await wp_dao.update(
            id=item.warehouse_product_id,
            data=WareProdUpdate(quantity=wp.quantity + item.custom_quantity),
        )

        prod = await p_dao.get_one(wp.product.id)
        if not prod:
            raise ItemNotFound(item_id=wp.product.id, item="product")
        await p_dao.update(
            id=wp.product.id,
            data=ProductBase(total_quantity=prod.total_quantity + item.custom_quantity),
        )


async def _change_order_status(data: OrderCancelCreate, ord_dao: OrderDao):
    order = await ord_dao.get_one(data.order_id)
    if not order:
        raise ItemNotFound(item_id=data.order_id, item="order")
    if data.cancel_type == CancelType.REFUND.value:
        new_status = OrderStatus.REFUND.value
    else:
        new_status = OrderStatus.RETURN.value
    await ord_dao.update(data=OrderUpdate(status=new_status), id=data.order_id)


async def _restore_order(
    cancel_info: OrderCancelInfo,
    ord_dao: OrderDao,
    p_dao: ProductDao,
    wp_dao: WarehouseProductDao,
):
    restore_status: int
    order = await ord_dao.get_one(cancel_info.order_id)
    if not order:
        raise ItemNotFound(item_id=cancel_info.order_id, item="order")

    for ord_prod in order.order_products:
        wp = await wp_dao.get_one(ord_prod.warehouse_product_id)

        if not wp:
            raise ItemNotFound(
                item_id=ord_prod.warehouse_product_id, item="warehouse product"
            )

        await wp_dao.update(
            id=ord_prod.warehouse_product_id,
            data=WareProdUpdate(quantity=wp.quantity - ord_prod.custom_quantity),
        )

        prod = await p_dao.get_one(wp.product.id)
        if not prod:
            raise ItemNotFound(item_id=wp.product.id, item="product")
        await p_dao.update(
            id=wp.product.id,
            data=ProductBase(
                total_quantity=prod.total_quantity - ord_prod.custom_quantity
            ),
        )

    if order.delivery_on.date() > order.created_at.date():
        restore_status = OrderStatus.PREPAID.value
    elif order.total_amount == order.paid_amount:
        restore_status = OrderStatus.PAID.value
    else:
        restore_status = OrderStatus.UNPAID.value

    await ord_dao.update(data=OrderUpdate(status=restore_status), id=order.id)


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(
    id: int,
    can_dao: OrderCancelInfoDao = Depends(get_cancel_dao),
    ord_dao: OrderDao = Depends(get_or_dao),
    p_dao: ProductDao = Depends(get_prod_dao),
    wp_dao: WarehouseProductDao = Depends(get_wp_dao),
):

    cancel_info = await can_dao.get_one(id)

    if not cancel_info:
        raise ItemNotFound(item_id=id, item="cancel_info")

    await _restore_order(cancel_info, ord_dao, p_dao, wp_dao)

    result = await can_dao.delete(cancel_info)
    if not result:
        raise Exception()

    return {"message": "Successfully deleted"}
