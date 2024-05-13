from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import RedirectResponse, HTMLResponse

from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.schema.usager_schema import RequestUser, UsagerSchema
import app.controller.user_repository as user_repository
from pymongo.mongo_client import MongoClient
from typing import Annotated
from app.model.usager import Usager
from app.schema.auth_schemas import (
    LoginResponseSchema,
    LoginRequestSchema
)
from app.auth.auth import create_access_token, create_refresh_token, get_current_usager, verify_token
from app.auth.utils import verify_password
from app.app_config.database_config import get_db

router = APIRouter()

db_dependancy = Annotated[Session, Depends(get_db)]

# Loggin
@router.post("/login", response_model=LoginResponseSchema)
async def login(payload: LoginRequestSchema, db: Session = Depends(get_db)):
    user = user_repository.fetch_user_by_username(db, payload.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials."
        )

    if not verify_password(payload.password, user.hashed_pwd):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials."
        )

    access_token = create_access_token(data={"usager_id": user.id})
    refresh_token = create_refresh_token(data={"usager_id": user.id})

    return LoginResponseSchema(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )

@router.get("/mes")
async def read_users_me():
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2FnZXJfaWQiOjExLCJleHAiOjE3MTU1OTMyNzAsInRva2VuX2RhdGEiOiJhY2Nlc3NfdG9rZW4ifQ.WKG6wLOFU-8-AB8Of2q9xpm5ugnCrbSN12XOILozne0"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = Depends(get_current_usager)
    verify_token(access_token, credentials_exception)

    return user


# Return current usager if logged
@router.get("/me")
async def get_me(user: Usager = Depends(get_current_usager), db: Session = Depends(get_db)) -> UsagerSchema:
    if not user or (user.id is None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials."
        )
    return user

# Creation d'un usager
@router.post("/create")
async def create(request: RequestUser, db:Session=Depends(get_db)):
    _user = user_repository.add_user(db, request.parameter)
    return _user, 200

# Get all usagers
@router.get("/")
async def get(db:Session=Depends(get_db)):
    _user = user_repository.get_users(db, 0, 100)
    return _user, 200

# Get usager by username
@router.get("/username/{username}")
async def get_by_username(username: str, db:Session=Depends(get_db)):
    _user = user_repository.fetch_user_by_username(db, username)
    return _user, 200

# Get usager by id
@router.get("/{id}")
async def get_by_id(id: int, db:Session=Depends(get_db)):
    _user = user_repository.fetch_user_by_id(db, id)
    return _user, 200

# Update usager by fields
@router.post("/update")
async def update_user(request: RequestUser, db:Session=Depends(get_db)):
    _user = user_repository.update_user(db, 
                                 request.parameter.id, 
                                 request.parameter.nom, 
                                 request.parameter.prenom,
                                 request.parameter.age)
    return _user, 200

# Delete usager by id
@router.delete("/{id}")
def delete(id: int, db:Session=Depends(get_db)):
    _user = user_repository.remove_user(db, id)
    return _user, 200


@router.get("/logout")
def logout(response : HTMLResponse):
  #response = RedirectResponse('*your login page*', status_code= 302)
  #response.delete_cookie(key ='*your access token name*')
  return response