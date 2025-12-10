from fastapi import APIRouter, Depends
from app.src.user.user_dao import UserDao, get_user_dao
from .auth_schema import AuthData, TokenRead, TokenPayload
from app.src.user.user_model import User

# from app.src.user.user_schema import UserRead
from app.src.auth import auth_method as mtds
from enum import Enum
from app.utils.custom_exceptions import AuthError, InactiveUser


class AuthRole(Enum):
    client = 0
    admin = 1


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenRead)
async def login_for_access_token(data: AuthData, dao: UserDao = Depends(get_user_dao)):
    user: User = await dao.get_by_username(username=data.username)

    if not user:
        raise AuthError()
    if not mtds.verify_key(data.password, user.hashed_password):
        raise AuthError()

    return mtds.create_access_token(data.role, user.id)


@router.post("/verify_user")
async def token(token: str, dao: UserDao = Depends(get_user_dao)):

    payload: TokenPayload = mtds.decode_access_token(token)

    if not payload:
        raise Exception()

    user: User = await dao.get_by_id(id=payload.user_id)

    if not user.is_active:
        raise InactiveUser()

    return user
