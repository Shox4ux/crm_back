from fastapi import APIRouter, File, status, Depends, UploadFile, Form
from .product_dao import ProductDao, get_prod_dao
from typing import Optional
from app.utils.custom_exceptions import ItemNotFound
from app.src.product.product_schema import ProductRead, ProductWrite
from app.utils.img_uploader import img_uploader, delete_image
from app.src.client.client_dao import ClientDao, get_c_dao
from app.src.client.client_schema import ClientProdWrite

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


@router.post("/create", response_model=ProductRead)
async def create(
    img: UploadFile | None = File(None),
    name: str = Form(...),
    base_price: float = Form(...),
    sell_price: float = Form(...),
    total_quantity: int = Form(...),
    active_quantity: int = Form(...),
    dao: ProductDao = Depends(get_prod_dao),
    c_dao: ClientDao = Depends(get_c_dao),
):

    img_path = None
    if img:
        img_path = img_uploader(img)

        if not img_path:

            raise Exception()

    data = ProductWrite(
        img_url=img_path,
        name=name,
        base_price=base_price,
        total_quantity=total_quantity,
        active_quantity=active_quantity,
        sell_price=sell_price,
    )

    product = await dao.create(data)

    if not product:
        raise Exception()

    await _create_cp_for_each_c(product, c_dao)

    return product


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, dao: ProductDao = Depends(get_prod_dao)):
    prod = await dao.get_one(id)

    if not prod:
        raise ItemNotFound(item_id=id, item="product")

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
