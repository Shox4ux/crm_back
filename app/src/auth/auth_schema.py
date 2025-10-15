from pydantic import BaseModel

from datetime import datetime


class AuthData(BaseModel):
    role: int
    username: str
    password: str


class TokenRead(BaseModel):
    access_token: str
    token_type: str
    expires_at: str


class TokenPayload(BaseModel):
    role: int
    user_id: int
    exp: datetime
