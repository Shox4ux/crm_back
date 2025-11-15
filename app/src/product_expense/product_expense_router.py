from fastapi import APIRouter, status, Depends
from .product_expense_dao import ProdExpDao, get_prod_exp_dao
from typing import Optional
from app.utils.custom_exceptions import ItemNotFound
from app.src.product_expense.product_expense_schema import (
    ProdExpRead,
    ProdExpBulkWrite,
    ProdExpWrite,
)

router = APIRouter(prefix="/product_expense", tags=["product_expense"])


@router.get("/get_by_id/{id}", response_model=Optional[ProdExpRead])
async def get_by_id(id: int, dao: ProdExpDao = Depends(get_prod_exp_dao)):
    product = await dao.get_one(id)
    if not product:
        raise ItemNotFound(item_id=id, item="product")
    return product


@router.get("/get_all", response_model=Optional[list[ProdExpRead]])
async def get_all(dao: ProdExpDao = Depends(get_prod_exp_dao)):
    products = await dao.get_all()
    return products


@router.post("/create", status_code=status.HTTP_200_OK)
async def create(data: ProdExpBulkWrite, dao: ProdExpDao = Depends(get_prod_exp_dao)):
    prod_exp = await dao.create(data)
    if not prod_exp:
        raise Exception()
    return "Successfully created"


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, dao: ProdExpDao = Depends(get_prod_exp_dao)):

    result = await dao.delete(id)
    if not result:
        raise Exception()

    return {"message": "Successfully deleted"}


@router.patch("/update/{id}", response_model=ProdExpRead)
async def update(id: int, d: ProdExpWrite, dao: ProdExpDao = Depends(get_prod_exp_dao)):
    result = await dao.update(id, d)
    return result
