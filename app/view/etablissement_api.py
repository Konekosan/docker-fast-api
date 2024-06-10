from fastapi import APIRouter, Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.app_config.database_config import get_db
from app.controller import etablissement_repository
from app.schema.etablissement_schema import RequestEtablissement

etablissement_router = APIRouter()


@etablissement_router.get("/")
async def get(db:Session=Depends(get_db)):
    _etablissement = etablissement_repository.get_etablissement(db, 0, 100)
    return _etablissement, 200

# Creation d'un usager
@etablissement_router.post("/create")
async def create(request: RequestEtablissement, db:Session=Depends(get_db)):
    print('aaaaa')
    print(request.parameter)
    print('aaaaa')
    _user = etablissement_repository.add_etablissement(db, request.parameter)
    return _user, 200