from fastapi import APIRouter, status, Depends
from .client_dao import ClientDao, get_c_dao
from typing import Optional
from app.src.client.client_schema import (
    ClientBase,
    ClientRead,
    ClientWrite,
    ClientProdWrite,
    ClientProdUpdt,
    ClientUpdt,
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


@router.post("/create", response_model=ClientBase)
async def create(
    data: ClientWrite,
    dao: ClientDao = Depends(get_c_dao),
    p_dao: ProductDao = Depends(get_prod_dao),
    c_dao: ClientDao = Depends(get_c_dao),
):
    client = await dao.create(data)
    if not client:
        raise Exception()
    await _create_client_prods(client.id, p_dao, c_dao)

    return client


async def _create_client_prods(c_id: int, p_dao: ProductDao, c_dao: ClientDao):

    products = await p_dao.get_all()

    if products:
        for p in products:
            d = ClientProdWrite(
                client_id=c_id, product_id=p.id, custom_price=p.sell_price
            )
            await c_dao.create_cp(d)


@router.patch("/update/{id}", response_model=ClientBase)
async def update(id: int, d: ClientUpdt, dao: ClientDao = Depends(get_c_dao)):
    result = await dao.update(id, d)
    return result


@router.patch("/update_client_product/{cp_id}", response_model=ClientProdWrite)
async def update_cp(cp_id: int, d: ClientProdUpdt, dao: ClientDao = Depends(get_c_dao)):
    result = await dao.update_cp(cp_id, d)
    return result


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, dao: ClientDao = Depends(get_c_dao)):
    result = await dao.delete(id)
    if not result:
        raise Exception()
    return {"message": "Successfully deleted"}
