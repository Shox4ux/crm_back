from fastapi import APIRouter, status, Depends
from .user_dao import UserDao, get_user_dao
from typing import Optional
from app.src.user.user_schema import UserRead, UserWrite, UserUpdt
from app.src.auth.auth_method import get_pass_hashed

router = APIRouter(prefix="/users", tags=["user"])


@router.get("/get_by_username/{uname}", response_model=Optional[UserRead])
async def get_by_username(uname: str, dao: UserDao = Depends(get_user_dao)):
    user = await dao.get_by_username(uname)
    return user


@router.get("/get_all", response_model=Optional[list[UserRead]])
async def get_all(dao: UserDao = Depends(get_user_dao)):
    users = await dao.get_all()
    return users


@router.post("/create", response_model=UserRead)
async def create(data: UserWrite, dao: UserDao = Depends(get_user_dao)):
    data.password = get_pass_hashed(data.password)
    user = await dao.create(data)
    if not user:
        raise Exception()
    return user


@router.patch("/update/{id}", response_model=Optional[UserRead])
async def get_by_username(id: int, d: UserUpdt, dao: UserDao = Depends(get_user_dao)):
    user = await dao.update(id, d)
    return user


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, dao: UserDao = Depends(get_user_dao)):
    result = await dao.delete(id)
    if not result:
        raise Exception()
    return {"message": "Successfully deleted"}
