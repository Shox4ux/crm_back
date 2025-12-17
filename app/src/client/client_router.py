from fastapi import APIRouter, status, Depends
from .client_dao import ClientDao, get_c_dao
from typing import Optional
from app.src.client.client_schema import (
    ClientResponse,
    ClientProdWrite,
    ClientProdUpdt,
)
from app.src.user.user_schema import CreateAsClient, UserUpdate
from app.src.product.product_dao import ProductDao, get_prod_dao
from app.src.user.user_dao import UserDao, get_user_dao
from app.utils.img_uploader import img_uploader, delete_image

router = APIRouter(prefix="/clients", tags=["client"])


@router.get("/get_by_user_id/{user_id}", response_model=Optional[ClientResponse])
async def get_by_id(user_id: int, dao: ClientDao = Depends(get_c_dao)):
    client = await dao.get_by_uid(user_id)
    return client


@router.get("/get_all", response_model=Optional[list[ClientResponse]])
async def get_all(dao: ClientDao = Depends(get_c_dao)):
    clients = await dao.get_all()
    return clients


@router.post("/create")
async def create(
    data: CreateAsClient = Depends(),
    c_dao: ClientDao = Depends(get_c_dao),
    p_dao: ProductDao = Depends(get_prod_dao),
    u_dao: UserDao = Depends(get_user_dao),
):
    img_path = img_uploader(data.img) if data.img else None
    user = await u_dao.create_as_client(data, img_path)
    if not user:
        raise Exception()
    client = await c_dao.create(user.id)
    if not client:
        raise Exception()
    await _create_client_prods(client.id, p_dao, c_dao)
    return {"message": "Successfully created"}


async def _create_client_prods(c_id: int, p_dao: ProductDao, c_dao: ClientDao):
    products = await p_dao.get_all()
    if products:
        for p in products:
            d = ClientProdWrite(
                client_id=c_id, product_id=p.id, custom_price=p.sell_price
            )
            await c_dao.create_cp(d)


@router.patch("/update_client_product/{cp_id}", response_model=ClientProdWrite)
async def update_cp(cp_id: int, d: ClientProdUpdt, dao: ClientDao = Depends(get_c_dao)):
    result = await dao.update_cp(cp_id, d)
    return result


@router.patch("/update/{id}", response_model=ClientResponse)
async def update(
    id: int,
    data: UserUpdate = Depends(),
    u_dao: UserDao = Depends(get_user_dao),
    c_dao: ClientDao = Depends(get_c_dao),
):
    img_path: str | None = None
    client = await c_dao.get_by_id(id)
    if not client:
        raise Exception()

    if data.img:
        delete_image(client.user.img)
        img_path = img_uploader(data.img)

    await u_dao.update_user(client.user, data, img_path)
    return client


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(
    id: int,
    c_dao: ClientDao = Depends(get_c_dao),
    u_dao: UserDao = Depends(get_user_dao),
):
    client = await c_dao.get_by_id(id)
    if not client:
        raise Exception()
    res = await u_dao.delete(client.user.id)
    if not res:
        raise Exception()
    result = await c_dao.delete(id)
    if not result:
        raise Exception()
    return {"message": "Successfully deleted"}
