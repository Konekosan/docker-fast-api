from fastapi import APIRouter, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter

connection_router = APIRouter()
templates = Jinja2Templates(directory="templates")

var_user = 'inject_var'


@connection_router.get("/")
async def get(request: Request):
           
    return templates.TemplateResponse("index.html", {"request": request, "user": var_user})

@connection_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")