from fastapi import APIRouter, status, Depends
from .client_dao import ClientDao, get_c_dao
from typing import Optional
from app.src.client.client_schema import (
    ClientBase,
    ClientRead,
    ClientWrite,
    ClientProdWrite,
)
from app.src.product.product_dao import ProductDao, get_prod_dao

router = APIRouter(prefix="/clients", tags=["client"])


@router.get("/get_by_user_id/{user_id}", response_model=Optional[ClientRead])
async def get_by_id(user_id: int, dao: ClientDao = Depends(get_c_dao)):
    client = await dao.get_by_uid(user_id)
    return client


@router.get("/get_all", response_model=Optional[list[ClientRead]])
async def get_all(dao: ClientDao = Depends(get_c_dao)):
    clients = await dao.get_all()
    return clients


@router.post("/create", response_model=ClientRead)
async def create(data: ClientWrite, dao: ClientDao = Depends(get_c_dao)):
    client = await dao.create(data)
    if not client:
        raise Exception()
    await _create_client_prods(client.id)

    return client


async def _create_client_prods(
    c_id: int,
    p_dao: ProductDao = Depends(get_prod_dao),
    c_dao: ClientDao = Depends(get_c_dao),
):

    products = await p_dao.get_all()

    for p in products:
        await c_dao.create_cp(ClientProdWrite(c_id, p.id, p.sell_price))


@router.delete("/delete/{user_id}", status_code=status.HTTP_200_OK)
async def delete(user_id: int, dao: ClientDao = Depends(get_c_dao)):
    result = await dao.delete(user_id)
    if not result:
        raise Exception()
    return {"message": "Successfully deleted"}
