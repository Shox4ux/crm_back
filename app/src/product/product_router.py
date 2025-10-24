from fastapi import APIRouter, status, Depends, Response, UploadFile, Form
from .product_dao import ProductDao, get_prod_dao
from typing import Optional
from app.utils.custom_exceptions import ItemNotFound
from app.src.product.product_schema import ProductRead, ProductWrite
from app.utils.img_uploader import img_uploader, delete_image

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
    img: UploadFile,
    name: str = Form(...),
    buy_price: float = Form(...),
    sell_price: float = Form(...),
    dao: ProductDao = Depends(get_prod_dao),
):

    img_path = img_uploader(img)
    if not img_path:
        raise Exception()

    data = ProductWrite(
        img_url=img_path,
        name=name,
        buy_price=buy_price,
        sell_price=sell_price,
    )

    product = await dao.create(data)

    if not product:
        raise Exception()
    return product


@router.delete("/delete/{id}")
async def delete(id: int, dao: ProductDao = Depends(get_prod_dao)):
    prod = await dao.get_one(id)

    if not prod:
        raise ItemNotFound(item_id=id, item="product")

    delete_image(image_path=prod.img_url)
    result = await dao.delete(id)

    if not result:
        raise Exception()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
