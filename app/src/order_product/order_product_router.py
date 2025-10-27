from fastapi import APIRouter, status, Depends, Response
from .order_product_dao import OrderProductDao, get_orp_dao
from typing import Optional
from app.utils.custom_exceptions import ItemNotFound
from app.src.order_product.order_product_schema import (
    OrderProdRead,
    OrderProdBase,
    OrderProdWrite,
)

router = APIRouter(prefix="/order_products", tags=["order_product"])


@router.get("/get_by_id/{id}", response_model=Optional[OrderProdRead])
async def get_by_id(id: int, dao: OrderProductDao = Depends(get_orp_dao)):
    order_prod = await dao.get_one(id)
    if not order_prod:
        raise ItemNotFound(item_id=id, item="order_prod")
    return order_prod


@router.get("/get_all", response_model=Optional[list[OrderProdRead]])
async def get_all(dao: OrderProductDao = Depends(get_orp_dao)):
    warehouse_prods = await dao.get_all()
    return warehouse_prods


@router.post("/create", response_model=OrderProdBase)
async def create(data: OrderProdWrite, dao: OrderProductDao = Depends(get_orp_dao)):
    warehouse_prod = await dao.create(data)
    if not warehouse_prod:
        raise Exception()
    return warehouse_prod


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, dao: OrderProductDao = Depends(get_orp_dao)):
    result = await dao.delete(id)
    if not result:
        raise Exception()
    return {"message": "Successfully deleted"}
