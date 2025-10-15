from fastapi import APIRouter, status, Depends, Response
from .admin_dao import AdminDao, get_admin_dao
from typing import Optional
from app.utils.custom_exceptions import ItemNotFound
from app.src.admin.admin_schema import AdminRead, AdminWrite

router = APIRouter(prefix="/admins", tags=["admin"])


@router.get("/get_by_id/{id}", response_model=Optional[AdminRead])
async def get_by_id(id: int, dao: AdminDao = Depends(get_admin_dao)):
    admin = await dao.get_one(id)
    if not admin:
        raise ItemNotFound(item_id=id, item="admin")
    return admin


@router.get("/get_all", response_model=Optional[list[AdminRead]])
async def get_all(dao: AdminDao = Depends(get_admin_dao)):
    admins = await dao.get_all()
    return admins


@router.post("/create", response_model=AdminRead)
async def create(data: AdminWrite, dao: AdminDao = Depends(get_admin_dao)):
    admin = await dao.create(data)
    if not admin:
        raise Exception()
    return admin


@router.delete("/delete/{id}")
async def delete(id: int, dao: AdminDao = Depends(get_admin_dao)):
    result = await dao.delete(id)
    if not result:
        raise Exception()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
