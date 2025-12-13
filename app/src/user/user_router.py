from fastapi import APIRouter, status, Depends
from .user_dao import UserDao, get_user_dao
from typing import Optional
from app.src.user.user_model import User
from app.utils.custom_exceptions import ItemNotFound, AlreadyExists
from app.utils.img_uploader import img_uploader
from app.src.user.user_schema import UserResponse

router = APIRouter(prefix="/users", tags=["user"])


@router.get("/clients", response_model=list[UserResponse])
async def list_clients(dao: UserDao = Depends(get_user_dao)):
    users = await dao.get_all_clients()
    return users


@router.get("/admins", response_model=list[UserResponse])
async def list_admins(dao: UserDao = Depends(get_user_dao)):
    users = await dao.get_all_admins()
    return users


@router.get("/get_by_username/{username}", response_model=UserResponse)
async def select_user_by_username(username: str, dao: UserDao = Depends(get_user_dao)):
    user = await dao.get_user_by_username(username)
    if not user:
        raise ItemNotFound(item_id=username, item="user")
    return user


@router.get("/get_by_id/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, dao: UserDao = Depends(get_user_dao)):
    user = await dao.get_user_by_id(user_id)
    if not user:
        raise ItemNotFound(item_id=user_id, item="user")
    return user


@router.delete("/delete/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, dao: UserDao = Depends(get_user_dao)):
    user = await dao.get_user_by_id(user_id)
    if not user:
        raise ItemNotFound(item_id=user_id, item="user")
    await dao.delete(user)
    return {"message": "Successfully deleted"}


# @router.patch("/client/{user_id}", response_model=UserResponse)
# async def update_client(
#     user_id: int,
#     data: UserUpdate = Depends(),
#     dao: UserDao = Depends(get_user_dao),
# ):
#     user: User = await dao.get_user_by_id(user_id)
#     if not user or user.role != 0:
#         raise ItemNotFound(item_id=user_id, item="user")
#     img_path = img_uploader(data.img) if data.img else None
#     user = await dao.update_user(user, data, img_path)
#     return user


# @router.patch("/admin/{user_id}", response_model=UserResponse)
# async def update_admin(
#     user_id: int,
#     data: UserUpdate = Depends(),
#     dao: UserDao = Depends(get_user_dao),
# ):
#     user: User = await dao.get_user_by_id(user_id)
#     if not user or user.role != 1:
#         raise ItemNotFound(item_id=user_id, item="user")
#     img_path = img_uploader(data.img) if data.img else None
#     user = await dao.update_user(user, data, img_path)
#     return user
