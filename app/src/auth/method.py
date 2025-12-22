from datetime import timedelta, timezone, datetime
from jwt.exceptions import InvalidTokenError
import jwt
from pwdlib import PasswordHash
from app.src.auth.schema import TokenPayload, TokenRead
from app.settings import Settings
from app.utils.custom_exceptions import InvalidToken, TokenExpired, ServerError

sttngs = Settings()


pwd_context = PasswordHash.recommended()


def get_pass_hashed(password: str) -> str:
    return pwd_context.hash(password)


def verify_key(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(role: int, id: int) -> TokenRead:
    expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=sttngs.EXPIRES)
    to_encode = {"role": role, "user_id": id, "exp": int(expire.timestamp())}
    try:
        token = jwt.encode(to_encode, sttngs.TOKEN_KEY, algorithm=sttngs.ALGORITHM)

    except Exception:
        raise InvalidTokenError()

    return TokenRead(
        access_token=token,
        token_type="bearer",
        expires_at=expire.isoformat(),
    )


def decode_access_token(token: str) -> TokenPayload:

    try:
        decoded = jwt.decode(token, sttngs.TOKEN_KEY, algorithms=[sttngs.ALGORITHM])

        return TokenPayload(**decoded)
    except jwt.ExpiredSignatureError:
        raise TokenExpired()
    except jwt.InvalidSignatureError:
        raise InvalidToken()
    except InvalidTokenError:
        raise ServerError
