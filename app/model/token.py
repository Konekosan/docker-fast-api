from pydantic import BaseModel
from enum import Enum

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class TokenEnum(Enum):
    RefreshToken = "refresh_token"
    AccessToken = "access_token"