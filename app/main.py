from fastapi import FastAPI
from app.database import engine, SessionLocal
from app.model import usager
from . import router
from app.auth import handler
from app.templates import chatbox, connection
from jose import jwt
#from pymongo.mongo_client import MongoClient

#uri =  'mongodb://localhost:27017/test'

#conn = MongoClient()
#db = conn.test_db

#collection_name = db['message_collection']

app = FastAPI()

usager.Base.metadata.create_all(bind=engine)

@app.get('/')
async def root():
    return {'message': 'Hello World'}

app.include_router(router.router, prefix='/user', tags=['user'])
app.include_router(chatbox.chat_router, prefix='/chatbox', tags=['chatbox'])
app.include_router(handler.auth_router, prefix='/auth', tags=['auth'])
app.include_router(connection.connection_router, prefix='/connection', tags=['auth'])