from fastapi import APIRouter, status, Depends
from .dao import UserDao, get_user_dao
from app.utils.custom_exceptions import ItemNotFound
from .schema import UserResponse

router = APIRouter(prefix="/users", tags=["user"])


@router.get("/get_by_username/{username}", response_model=UserResponse)
async def select_user_by_username(username: str, dao: UserDao = Depends(get_user_dao)):
    user = await dao.get_by_username(username)
    if not user:
        raise ItemNotFound(item_id=username, item="user")
    return user


@router.patch("/activate/{id}", response_model=UserResponse)
async def activate_user(id: int, dao: UserDao = Depends(get_user_dao)):
    user = await dao.get_by_id(id)
    if not user:
        raise ItemNotFound(item_id=id, item="user")
    user = await dao.activate(user)
    return user


@router.patch("/disactivate/{id}", response_model=UserResponse)
async def disactivate_user(id: int, dao: UserDao = Depends(get_user_dao)):
    user = await dao.get_by_id(id)
    if not user:
        raise ItemNotFound(item_id=id, item="user")
    user = await dao.disactivate(user)
    return user


@router.get("/get_by_id/{id}", response_model=UserResponse)
async def get_user(id: int, dao: UserDao = Depends(get_user_dao)):
    user = await dao.get_by_id(id)
    if not user:
        raise ItemNotFound(item_id=id, item="user")
    return user


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_user(id: int, dao: UserDao = Depends(get_user_dao)):
    user = await dao.get_by_id(id)
    if not user:
        raise ItemNotFound(item_id=id, item="user")
    await dao.delete(user)
    return {"message": "Successfully deleted"}
