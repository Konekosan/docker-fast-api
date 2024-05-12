from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.app_config.config import (
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES,
)
from app.model.token import  TokenEnum
from app.app_config.database_config import get_db
from app.model.usager import Usager

auth_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Creation du access token
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=int(JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update(
        {"exp": int(expire.timestamp()), "token_kind": TokenEnum.AccessToken.value}
    )

    return jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)

# Creation du token de refresh
def create_refresh_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=int(JWT_REFRESH_TOKEN_EXPIRE_MINUTES))
    to_encode.update(
        {"exp": int(expire.timestamp()), "token_kind": TokenEnum.RefreshToken.value}
    )

    return jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)

# Vérification du token
def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        print(payload)
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception

        token_data = TokenEnum(id=id, **payload)
    except jwt.JWTError:
        raise credentials_exception

    return token_data

# Return current usager with token
def get_current_usager(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print('on passe la')
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_token(token, credentials_exception)
    print(token)
    user = db.query(Usager).filter(Usager.id == token.id).first()

    return user