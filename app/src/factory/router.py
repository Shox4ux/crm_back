from fastapi import APIRouter, status, Depends
from .dao import FactoryDao, get_f_dao
from typing import Optional
from app.utils.custom_exceptions import ItemNotFound
from app.src.factory.schema import FactoryWrite, FactoryRead

router = APIRouter(prefix="/factories", tags=["factory"])


@router.get("/get_by_id/{id}", response_model=Optional[FactoryRead])
async def get_by_id(id: int, dao: FactoryDao = Depends(get_f_dao)):
    factory = await dao.get_one(id)
    if not factory:
        raise ItemNotFound(item_id=id, item="factory")
    return factory


@router.get("/get_all", response_model=Optional[list[FactoryRead]])
async def get_all(dao: FactoryDao = Depends(get_f_dao)):
    factories = await dao.get_all()
    return factories


@router.post("/create", response_model=FactoryRead)
async def create(data: FactoryWrite, dao: FactoryDao = Depends(get_f_dao)):
    factory = await dao.create(data)
    if not factory:
        raise Exception()
    return factory


@router.patch("/update/{id}", response_model=FactoryRead)
async def update(id: int, data: FactoryWrite, dao: FactoryDao = Depends(get_f_dao)):
    factory = await dao.update(id, data)
    if not factory:
        raise Exception()
    return factory


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, dao: FactoryDao = Depends(get_f_dao)):
    result = await dao.delete(id)
    if not result:
        raise Exception()

    return {"message": "Successfully deleted"}
