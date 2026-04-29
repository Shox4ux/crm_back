from fastapi import APIRouter, status, Depends

from app.src.product.schema import ProductBase
from .dao import WarehouseDao, get_w_dao

from app.utils.custom_exceptions import ServerError

from app.src.order_product.dao import OrderProductDao, get_orp_dao
from app.src.product.dao import ProductDao, get_prod_dao
from typing import Optional
from app.utils.custom_exceptions import ItemNotFound
from app.src.warehouse.schema import WarehouseRead, WarehouseWrite

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
        raise ServerError(msg="Failed to create warehouse")
    return warehouse


@router.patch("/update/{id}", response_model=WarehouseRead)
async def update(id: int, data: WarehouseWrite, dao: WarehouseDao = Depends(get_w_dao)):
    warehouse = await dao.update(id, data)
    if not warehouse:
        raise ServerError(msg="Failed to update warehouse")
    return warehouse


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(
    id: int,
    dao: WarehouseDao = Depends(get_w_dao),
    p_dao: ProductDao = Depends(get_prod_dao),
    orp_dao: OrderProductDao = Depends(get_orp_dao),
):
    warehouse = await dao.get_one(id)
    if not warehouse:
        raise ItemNotFound(item_id=id, item="warehouse")

    for wp in warehouse.products:
        ord_pro = await orp_dao.get_ord_pro_by_ware_pro_id(wp.id)
        if ord_pro:
            raise ServerError(
                msg=f"Cannot delete warehouse {warehouse.name} because it has orders with product {ord_pro.warehouse_product.product.name}"
            )

        product = await p_dao.get_one(wp.product_id)
        if not product:
            raise ItemNotFound(item_id=wp.product_id, item="product")

        if product.active_quantity < wp.quantity:
            raise ServerError(
                msg=f"Not enough quantity for product {product.name} in warehouse {warehouse.name}"
            )
        product.active_quantity -= wp.quantity

        await p_dao.update(
            product.id, ProductBase(active_quantity=product.active_quantity)
        )

    result = await dao.delete(warehouse)
    if not result:
        raise ServerError(msg="Failed to delete warehouse")

    return {"message": "Successfully deleted"}
