from fastapi import FastAPI
from app.database import engine, SessionLocal
from app.model import usager
from . import router
from app.auth import handler, doc
from app.templates import chatbox, connection
from fastapi.openapi.utils import get_openapi

#from pymongo.mongo_client import MongoClient

#uri =  'mongodb://localhost:27017/test'

#conn = MongoClient()
#db = conn.test_db

#collection_name = db['message_collection']

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

usager.Base.metadata.create_all(bind=engine)

@app.get('/')
async def root():
    return {'message': 'Hello World'}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(router.router, prefix='/user', tags=['user'])
app.include_router(chatbox.chat_router, prefix='/chatbox', tags=['chatbox'])
app.include_router(handler.auth_router, prefix='/auth', tags=['auth'])
app.include_router(connection.connection_router, prefix='/connection', tags=['connection'])
app.include_router(doc.app, prefix='/test_doc', tags=['test_doc'])