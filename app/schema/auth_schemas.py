from pydantic import BaseModel, constr, EmailStr, ConfigDict
from typing import Optional
#from commons.enums import TokenKind
from app.model.token import TokenData

class RefreshTokenRequestSchema(BaseModel):
    refresh_token: str


class RefreshTokenResponseSchema(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]
    token_kind: Optional[TokenData]


class SignUpRequestSchema(BaseModel):
    name: str
    username: EmailStr
    password: str


class SignUpResponseSchema(BaseModel):
    detail: str


class LoginRequestSchema(BaseModel):
    username: str
    password: str


class LoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str