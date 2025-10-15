from datetime import timedelta, timezone, datetime

from jwt.exceptions import InvalidTokenError

import jwt
from pwdlib import PasswordHash
from dotenv import load_dotenv
from app.src.auth.auth_schema import TokenPayload, TokenRead
import os


load_dotenv(os.getenv("ENV_FILE"))


EXPIRES = int(os.getenv("EXPIRES"))
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_KEY = os.getenv("TOKEN_KEY").strip()


pwd_context = PasswordHash.recommended()


def get_pass_hashed(password: str) -> str:
    return pwd_context.hash(password)


def verify_key(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(role: int, id: int) -> TokenRead:
    expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=EXPIRES)
    to_encode = {"role": role, "user_id": id, "exp": int(expire.timestamp())}
    try:
        token = jwt.encode(to_encode, TOKEN_KEY, algorithm=ALGORITHM)

    except Exception:
        raise Exception()

    return TokenRead(
        access_token=token,
        token_type="bearer",
        expires_at=expire.isoformat(),
    )


def decode_access_token(token: str) -> TokenPayload:
    try:
        decoded = jwt.decode(token, TOKEN_KEY, algorithms=[ALGORITHM])
        return TokenPayload(**decoded)
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
    except jwt.InvalidSignatureError:
        print("Invalid signature. Wrong secret key or algorithm.")
    except Exception as e:
        print("Other error:", e)
