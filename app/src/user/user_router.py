from fastapi import APIRouter, status, Depends
from .user_dao import UserDao, get_user_dao
from app.utils.custom_exceptions import ItemNotFound
from app.src.user.user_schema import UserResponse

router = APIRouter(prefix="/users", tags=["user"])


# @router.get("/clients", response_model=list[UserResponse])
# async def list_clients(dao: UserDao = Depends(get_user_dao)):
#     users = await dao.get_all_clients()
#     return users


# @router.get("/admins", response_model=list[UserResponse])
# async def list_admins(dao: UserDao = Depends(get_user_dao)):
#     users = await dao.get_all_admins()
#     return users


@router.get("/get_by_username/{username}", response_model=UserResponse)
async def select_user_by_username(username: str, dao: UserDao = Depends(get_user_dao)):
    user = await dao.get_user_by_username(username)
    if not user:
        raise ItemNotFound(item_id=username, item="user")
    return user


@router.get("/activate/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, dao: UserDao = Depends(get_user_dao)):
    user = await dao.get_user_by_id(user_id)
    if not user:
        raise ItemNotFound(item_id=user_id, item="user")
    user = await dao.activate_user(user)
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
