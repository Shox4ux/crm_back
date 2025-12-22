from fastapi import APIRouter, status, Depends
from .dao import OrderProductDao, get_orp_dao
from typing import Optional
from app.utils.custom_exceptions import ItemNotFound
from app.src.product.schema import ProductBase, ProductRead
from app.src.warehouse_product.schema import WareProdRead
from app.src.product.dao import ProductDao, get_prod_dao
from app.src.order_product.schema import (
    OrderProdRead,
    OrderProdBase,
    OrderBulkWrite,
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
    order_prods = await dao.get_all()
    return order_prods


@router.post("/create", status_code=status.HTTP_200_OK)
async def create(
    data: OrderBulkWrite,
    dao: OrderProductDao = Depends(get_orp_dao),
    p_dao: ProductDao = Depends(get_prod_dao),
):
    order_prod = await dao.create(data)

    if not order_prod:
        raise Exception()

    op_prods = await get_all(dao=dao)

    for op in op_prods:
        product: ProductRead = await p_dao.get_one(op.warehouse_product.product.id)
        if not product:
            raise Exception()

        product.total_quantity = product.total_quantity - op.custom_quantity
        i: dict = {k: v for k, v in product.__dict__.items() if not k.startswith("_")}
        updated_product = await p_dao.update(product.id, ProductBase(**i))
        if not updated_product:
            raise Exception()

    return "Successfully created"


@router.patch("/update/{id}", response_model=OrderProdBase)
async def update(
    id: int, data: OrderProdBase, dao: OrderProductDao = Depends(get_orp_dao)
):
    order_prod = await dao.update(id, data)
    if not order_prod:
        raise Exception()
    return order_prod


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, dao: OrderProductDao = Depends(get_orp_dao)):
    result = await dao.delete(id)
    if not result:
        raise Exception()
    return {"message": "Successfully deleted"}
