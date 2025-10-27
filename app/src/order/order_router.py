from fastapi import APIRouter, status, Depends, Response
from .order_dao import OrderDao, get_or_dao
from typing import Optional
from app.utils.custom_exceptions import ItemNotFound
from app.src.order.order_schema import OrderRead, OrderBase, OrderWrite, OrderUpdt

router = APIRouter(prefix="/orders", tags=["order"])


@router.get("/get_by_id/{id}", response_model=Optional[OrderRead])
async def get_by_id(id: int, dao: OrderDao = Depends(get_or_dao)):
    order_prod = await dao.get_one(id)

    return order_prod


@router.get("/get_all", response_model=Optional[list[OrderRead]])
async def get_all(dao: OrderDao = Depends(get_or_dao)):
    warehouse_prods = await dao.get_all()
    return warehouse_prods


@router.post("/create", response_model=OrderBase)
async def create(data: OrderWrite, dao: OrderDao = Depends(get_or_dao)):
    warehouse_prod = await dao.create(data)
    return warehouse_prod


@router.patch("/update_status/{id}", response_model=Optional[OrderBase])
async def update_status(id: int, data: OrderUpdt, dao: OrderDao = Depends(get_or_dao)):
    warehouse_prod = await dao.update_status(id, data)
    return warehouse_prod


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, dao: OrderDao = Depends(get_or_dao)):
    result = await dao.delete(id)
    if not result:
        raise Exception()
    return {"message": "Successfully deleted"}
