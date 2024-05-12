from fastapi import APIRouter
from fastapi.responses import HTMLResponse

connection_router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <center>
            <h1>Qui est connecté?</h1>
        </center>
    </body>
</html>
"""

@connection_router.get("/")
async def get():
    return HTMLResponse(html)