from fastapi import APIRouter, status, Depends, Response
from .warehouse_dao import WarehouseDao, get_w_dao
from typing import Optional
from app.utils.custom_exceptions import ItemNotFound
from app.src.warehouse.warehouse_schema import (
    WarehouseRead,
    WarehouseWrite,
    WarehouseBase,
)

router = APIRouter(prefix="/warehouses", tags=["warehouse"])


@router.get("/get_by_id/{id}", response_model=Optional[WarehouseRead])
async def get_by_id(id: int, dao: WarehouseDao = Depends(get_w_dao)):
    warehouse = await dao.get_one(id)
    if not warehouse:
        raise ItemNotFound(item_id=id, item="warehouse")
    return warehouse


@router.get("/get_all", response_model=Optional[list[WarehouseRead]])
async def get_all(dao: WarehouseDao = Depends(get_w_dao)):
    warehouses = await dao.get_all()
    return warehouses


@router.post("/create", response_model=WarehouseRead)
async def create(data: WarehouseWrite, dao: WarehouseDao = Depends(get_w_dao)):
    warehouse = await dao.create(data)
    if not warehouse:
        raise Exception()
    return warehouse


@router.delete("/delete/{id}")
async def delete(id: int, dao: WarehouseDao = Depends(get_w_dao)):
    result = await dao.delete(id)
    if not result:
        raise Exception()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
