from fastapi import APIRouter, status, Depends, Response
from .client_dao import ClientDao, get_c_dao
from typing import Optional
from app.utils.custom_exceptions import ItemNotFound
from app.src.client.client_schema import ClientBase, ClientRead, ClientWrite

router = APIRouter(prefix="/clients", tags=["client"])


@router.get("/get_by_user_id/{user_id}", response_model=Optional[ClientRead])
async def get_by_id(user_id: int, dao: ClientDao = Depends(get_c_dao)):
    client = await dao.get_by_uid(user_id)
    if not client:
        raise ItemNotFound(item_id=user_id, item="client")
    return client


@router.get("/get_all", response_model=Optional[list[ClientRead]])
async def get_all(dao: ClientDao = Depends(get_c_dao)):
    clients = await dao.get_all()
    return clients


@router.post("/create", response_model=ClientBase)
async def create(data: ClientWrite, dao: ClientDao = Depends(get_c_dao)):
    warehouse = await dao.create(data)
    if not warehouse:
        raise Exception()
    return warehouse


@router.delete("/delete/{user_id}")
async def delete(user_id: int, dao: ClientDao = Depends(get_c_dao)):
    result = await dao.delete(user_id)
    if not result:
        raise Exception()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
