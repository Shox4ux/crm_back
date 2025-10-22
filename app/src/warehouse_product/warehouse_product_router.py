from fastapi import APIRouter, status, Depends, Response
from .warehouse_product_dao import WarehouseProductDao, get_wp_dao
from typing import Optional
from app.utils.custom_exceptions import ItemNotFound
from app.src.warehouse_product.warehouse_product_schema import (
    WarehouseProdRead,
    WarehouseProdWrite,
)

router = APIRouter(prefix="/warehouse_products", tags=["warehouse_product"])


@router.get("/get_by_id/{id}", response_model=Optional[WarehouseProdRead])
async def get_by_id(id: int, dao: WarehouseProductDao = Depends(get_wp_dao)):
    warehouse_prod = await dao.get_one(id)
    if not warehouse_prod:
        raise ItemNotFound(item_id=id, item="warehouse_prod")
    return warehouse_prod


@router.get("/get_all", response_model=Optional[list[WarehouseProdRead]])
async def get_all(dao: WarehouseProductDao = Depends(get_wp_dao)):
    warehouse_prods = await dao.get_all()
    return warehouse_prods


@router.post("/create", response_model=WarehouseProdRead)
async def create(
    data: WarehouseProdWrite, dao: WarehouseProductDao = Depends(get_wp_dao)
):
    warehouse_prod = await dao.create(data)
    if not warehouse_prod:
        raise Exception()
    return warehouse_prod


@router.delete("/delete/{id}")
async def delete(id: int, dao: WarehouseProductDao = Depends(get_wp_dao)):
    result = await dao.delete(id)
    if not result:
        raise Exception()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
