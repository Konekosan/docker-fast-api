from fastapi import APIRouter, Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.app_config.database_config import get_db
from app.controller import review_repository
from app.schema.revue_schemas import RequestRevue

review_router = APIRouter()

@review_router.get("/")
async def get(db:Session=Depends(get_db)):
    _review = review_repository.get_review(db, 0, 100)
    return _review, 200

# Creation d'un usager
@review_router.post("/create")
async def create(request: RequestRevue, db:Session=Depends(get_db)):
    _review = review_repository.create_review(db, request.parameter)
    return _review, 200