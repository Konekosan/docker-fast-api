from fastapi import FastAPI, WebSocket, APIRouter
from fastapi.responses import HTMLResponse

chat_router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <center>
            <h1>WebSocket Chat</h1>
            <form action="" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" autocomplete="off"/>
                <button>Send</button>
            </form>
            <ul id='messages'>
            </ul>
            <script>
                
                var ws = new WebSocket("ws://localhost:8000/chatbox/ws");

                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                function sendMessage(event) {                    
                    var input = document.getElementById("messageText")
                    ws.send('caca')
                    ws.send(input.value)
                    input.value = ''
                    event.preventDefault()
                }
            </script>
        </center>
    </body>
</html>
"""


@chat_router.get("/")
async def get():
    return HTMLResponse(html)


@chat_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print(websocket)
    await websocket.accept()
    print('aaaaaa')
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")