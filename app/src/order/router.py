from fastapi import APIRouter, status, Depends

from app.utils.custom_exceptions import ItemNotFound
from .dao import OrderDao, get_or_dao
from typing import Optional
from app.src.order.schema import OrderResponse, OrderBase, OrderCreate, OrderUpdate
from app.src.order_product.dao import OrderProductDao, get_orp_dao

router = APIRouter(prefix="/orders", tags=["order"])


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
    orp_dao: OrderProductDao = Depends(get_orp_dao),
):

    print(data.model_dump_json())

    order = await dao.create(data)
    if not order:
        raise Exception()

    await orp_dao.create(order.id, data.order_products)

    return "Successfully created"


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


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, dao: OrderDao = Depends(get_or_dao)):
    result = await dao.delete(id)
    if not result:
        raise Exception()
    return {"message": "Successfully deleted"}
