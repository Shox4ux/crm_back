from fastapi import APIRouter, status, Depends
from .dao import WarehouseProductDao, get_wp_dao
from ..product.dao import ProductDao, get_prod_dao
from ..product.schema import ProductBase, ProductRead
from typing import Optional
from app.utils.custom_exceptions import ItemNotFound
from app.src.warehouse_product.schema import WareProdRead, WareProdWrite
from app.src.warehouse.dao import WarehouseDao, get_w_dao

router = APIRouter(prefix="/warehouse_products", tags=["warehouse_product"])


@router.get("/get_by_id/{id}", response_model=Optional[WareProdRead])
async def get_by_id(id: int, dao: WarehouseProductDao = Depends(get_wp_dao)):
    warehouse_prod = await dao.get_one(id)
    if not warehouse_prod:
        raise ItemNotFound(item_id=id, item="warehouse_prod")
    return warehouse_prod


@router.get("/get_all/{ware_id}", response_model=Optional[list[WareProdRead]])
async def get_all(
    ware_id: int,
    dao: WarehouseProductDao = Depends(get_wp_dao),
    w_dao: WarehouseDao = Depends(get_w_dao),
):
    warehouse = await w_dao.get_one(id=ware_id)
    if not warehouse:
        raise ItemNotFound(item_id=ware_id, item="warehouse")

    warehouse_prods = await dao.get_all_by_w_id(ware_id)
    return warehouse_prods


@router.get("/get_all/", response_model=Optional[list[WareProdRead]])
async def get_all(dao: WarehouseProductDao = Depends(get_wp_dao)):
    warehouse_prods = await dao.get_all()
    return warehouse_prods


@router.post("/create")
async def create(
    data: WareProdWrite,
    dao: WarehouseProductDao = Depends(get_wp_dao),
    p_dao: ProductDao = Depends(get_prod_dao),
):
    warehouse_prod = await dao.create(data)

    if not warehouse_prod:
        raise Exception()

    product: ProductRead = await p_dao.get_one(data.product_id)
    if not product:
        raise Exception()

    # update product active quantity
    product.active_quantity = product.active_quantity - data.quantity
    i: dict = {k: v for k, v in product.__dict__.items() if not k.startswith("_")}
    updated_product = await p_dao.update(product.id, ProductBase(**i))
    if not updated_product:
        raise Exception()

    return "Successfully created"


@router.patch("/update/{id}")
async def update(
    id: int,
    data: WareProdWrite,
    dao: WarehouseProductDao = Depends(get_wp_dao),
):
    wp_updated = await dao.update(data=data, id=id)
    if not wp_updated:
        raise Exception()
    return "Successfully updated"


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(
    id: int,
    dao: WarehouseProductDao = Depends(get_wp_dao),
    p_dao: ProductDao = Depends(get_prod_dao),
):
    warehouse_prod = await dao.get_one(id)
    if not warehouse_prod:
        raise ItemNotFound(item_id=id, item="warehouse_prod")
    product: ProductRead = await p_dao.get_one(warehouse_prod.product.id)
    if not product:
        raise Exception()
    product.active_quantity = product.active_quantity + warehouse_prod.quantity
    i: dict = {k: v for k, v in product.__dict__.items() if not k.startswith("_")}
    updated_product = await p_dao.update(product.id, ProductBase(**i))
    if not updated_product:
        raise Exception()

    result = await dao.delete(id)
    if not result:
        raise Exception()
    return {"message": "Successfully deleted"}
