from fastapi import FastAPI
from app.database import engine
from app.model import usager
from . import router
from app.auth import handler
from app.webchat import connection
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from app.view import etablissement_api
from app.view import admin_api
from app.view import review_api

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

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
app.include_router(etablissement_api.etablissement_router, prefix='/etablissement', tags=['etablissement'])
app.include_router(handler.auth_router, prefix='/auth', tags=['auth'])
app.include_router(connection.connection_router, prefix='/connection', tags=['connection'])
app.include_router(admin_api.admin_router, prefix='/admin', tags=['admin'])
app.include_router(review_api.review_router, prefix='/review', tags=['review'])