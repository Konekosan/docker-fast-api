from fastapi import FastAPI
from app.database import engine, SessionLocal
from . import models
from . import router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get('/')
async def root():
    return {'message': 'Hello World'}

app.include_router(router.router, prefix='/user', tags=['user'])