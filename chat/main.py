from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import redis
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

r = redis.Redis(host='localhost', port=6379, db=0)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def get():
    return HTMLResponse(open(os.path.join("app", "templates", "index.html")).read())

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = f"Client #{client_id}: {data}"
            r.rpush("chat_history", message)
            await manager.send_message(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.send_message(f"Client #{client_id} Saiu do chat")
