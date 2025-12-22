from fastapi import APIRouter, status, Depends
from .dao import AdminDao, get_admin_dao
from typing import Optional
from app.utils.custom_exceptions import ItemNotFound
from app.src.user.dao import UserDao, get_user_dao
from app.utils.img_uploader import img_uploader
from .schema import AdminCreate, AdminResponse

router = APIRouter(prefix="/admins", tags=["admin"])


@router.get("/get_by_user_id/{user_id}", response_model=Optional[AdminResponse])
async def get_by_id(user_id: int, dao: AdminDao = Depends(get_admin_dao)):
    admin = await dao.get_by_uid(user_id)
    if not admin:
        raise ItemNotFound(item_id=user_id, item="admin")
    return admin


@router.get("/get_all", response_model=Optional[list[AdminResponse]])
async def get_all(dao: AdminDao = Depends(get_admin_dao)):
    admins = await dao.get_all()
    return admins


@router.post("/create", response_model=AdminResponse)
async def create(
    data: AdminCreate = Depends(),
    a_dao: AdminDao = Depends(get_admin_dao),
    u_dao: UserDao = Depends(get_user_dao),
):
    img_path = img_uploader(data.img) if data.img else None
    user = await u_dao.create(data.to_user(img_path))
    if not user:
        raise Exception()
    admin = await a_dao.create(data.to_admin(user.id))
    if not admin:
        raise Exception()
    return admin


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, dao: AdminDao = Depends(get_admin_dao)):
    admin = await dao.get_by_id(id)
    if not admin:
        raise ItemNotFound(item_id=id, item="admin")
    result = await dao.delete(admin)

    if not result:
        raise Exception()
    return {"message": "Successfully deleted"}
