from datetime import timedelta, datetime
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from app.app_config.config import (
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES,
)
from app.model.token import TokenEnum
from app.schema.auth_schemas import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Creation du Token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=int(JWT_ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update(
        {"exp": int(expire.timestamp()), "token_kind": TokenEnum.AccessToken.value}
    )

    return jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)


# Refresh du Token
def create_refresh_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=int(JWT_REFRESH_TOKEN_EXPIRE_MINUTES))
    to_encode.update(
        {"exp": int(expire.timestamp()), "token_kind": TokenEnum.RefreshToken.value}
    )

    return jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)

        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception

        token_data = TokenData(id=id, **payload)
    except jwt.JWTError:
        raise credentials_exception

    return token_data