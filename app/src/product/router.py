from fastapi import APIRouter, File, status, Depends, UploadFile, Form
from .dao import ProductDao, get_prod_dao
from typing import Optional
from app.utils.custom_exceptions import ItemNotFound
from app.src.product.schema import (
    ProductRead,
    ProductCreate,
    ProductUpdate,
    ProductSimpleRead,
    ProductBase,
)
from app.utils.img_uploader import img_uploader, delete_image
from app.src.client.dao import ClientDao, get_c_dao
from app.src.client.schema import ClientProdWrite

from app.src.order_product.dao import OrderProductDao, get_orp_dao

router = APIRouter(prefix="/products", tags=["product"])


@router.get("/get_by_id/{id}", response_model=Optional[ProductRead])
async def get_by_id(id: int, dao: ProductDao = Depends(get_prod_dao)):
    product = await dao.get_one(id)
    if not product:
        raise ItemNotFound(item_id=id, item="product")
    return product


@router.get("/get_all", response_model=Optional[list[ProductRead]])
async def get_all(dao: ProductDao = Depends(get_prod_dao)):
    products = await dao.get_all()
    return products


@router.get("/get_all_archived", response_model=Optional[list[ProductRead]])
async def get_all_archived(dao: ProductDao = Depends(get_prod_dao)):
    products = await dao.get_all_archived()
    return products


@router.get("/get_all_active", response_model=Optional[list[ProductRead]])
async def get_all_active(dao: ProductDao = Depends(get_prod_dao)):
    products = await dao.get_all_active()
    return products


@router.post("/create", response_model=ProductSimpleRead)
async def create(
    data: ProductCreate = Depends(),
    dao: ProductDao = Depends(get_prod_dao),
    c_dao: ClientDao = Depends(get_c_dao),
):
    img_path = None
    if data.img:
        img_path = img_uploader(data.img)
        if not img_path:
            raise Exception()
    product = await dao.create(data.to_prod(img_path=img_path))
    if not product:
        raise Exception()
    await _create_cp_for_each_c(product, c_dao)

    return product


@router.patch("/update/{id}", status_code=status.HTTP_200_OK)
async def update(
    id: int,
    data: ProductUpdate = Depends(),
    dao: ProductDao = Depends(get_prod_dao),
):
    prod = await dao.get_one(id)
    img_path = prod.img_url
    if data.img:
        delete_image(image_path=prod.img_url)
        img_path = img_uploader(data.img)

    p_updated = await dao.update(id=id, data=data.to_update(img_path=img_path))

    if not p_updated:
        raise Exception()

    return {"message": "Successfully updated"}


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(
    id: int,
    dao: ProductDao = Depends(get_prod_dao),
    orp_dao: OrderProductDao = Depends(get_orp_dao),
):
    prod = await dao.get_one(id)

    if not prod:
        raise ItemNotFound(item_id=id, item="product")

    orp = await orp_dao.get_by_pro_id(product_id=id)
    if orp:
        return {
            "message": "Cannot delete product with existing order products,"
            "\n it will be archived instead."
        }

    delete_image(image_path=prod.img_url)
    result = await dao.delete(id)

    if not result:
        raise Exception()

    return {"message": "Successfully deleted"}


async def _create_cp_for_each_c(p: ProductRead, c_dao: ClientDao):

    clients = await c_dao.get_all()

    if clients:
        for c in clients:
            d = ClientProdWrite(
                client_id=c.id, product_id=p.id, custom_price=p.sell_price
            )

            await c_dao.create_cp(d)
