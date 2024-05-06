from fastapi import APIRouter, HTTPException, Path, Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.schema.user_schema import UserSchema, RequestUser, Response
import app.controller.user_repository as user_repository

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(e)
    finally:
        db.close()

@router.post("/create")
async def create(request: RequestUser, db:Session=Depends(get_db)):
    _user = user_repository.add_user(db, request.parameter)
    return _user, 200

@router.get("/")
async def get(db:Session=Depends(get_db)):
    _user = user_repository.get_users(db, 0, 100)
    return _user, 200

@router.get("/{id}")
async def get_by_id(id: int, db:Session=Depends(get_db)):
    _user = user_repository.fetch_user_by_id(db, id)
    return _user, 200

@router.post("/update")
async def update_user(request: RequestUser, db:Session=Depends(get_db)):
    _user = user_repository.update_user(db, 
                                 request.parameter.id, 
                                 request.parameter.nom, 
                                 request.parameter.prenom,
                                 request.parameter.age)
    return _user, 200

@router.delete("/{id}")
async def delete(id: int, db:Session=Depends(get_db)):
    _user = user_repository.remove_user(db, id)
    return _user, 200

@router.get("/login")
def get(db:Session=Depends(get_db)):
    _user = user_repository.get_users(db, 0, 100)
    return _user, 200

@router.get("/logout")
def get(db:Session=Depends(get_db)):
    _user = user_repository.get_users(db, 0, 100)
    return _user, 200