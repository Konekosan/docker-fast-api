from fastapi import APIRouter, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends

from typing import Annotated
from app.model.usager import Usager
from app.auth.auth import get_current_usager

connection_router = APIRouter()
templates = Jinja2Templates(directory="test_templates")

var_user = 'inject_var'

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <center>
            <h1>Qui est connecté?</h1>
            {{ test }}
        </center>
    </body>
</html>
"""

@connection_router.get("/")
async def get(request: Request):
    current_user =  Annotated[Usager, Depends(get_current_usager)]
                        
    return templates.TemplateResponse("index.html", {"request": request, "user": var_user})

@connection_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")