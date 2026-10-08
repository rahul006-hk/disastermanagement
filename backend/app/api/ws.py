import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

@router.websocket("/ws/replanning")
async def websocket_replanning(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep-alive heartbeat & client event reception
            data = await websocket.receive_text()
            payload = json.loads(data)
            # Echo broadcast replanning notification
            await manager.broadcast({
                "type": "REPLANNING_EVENT_RECEIVED",
                "payload": payload
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
