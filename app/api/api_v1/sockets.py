from app.utils.sockets import manager

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState

socket_router = APIRouter()


@socket_router.websocket("/{user_id}/{peer_id}/")
async def websocket_endpoint(
    websocket: WebSocket,
    peer_id: int,
    user_id: int,
):
    await manager.connect(websocket, user_id, peer_id)
    try:
        while websocket.application_state == WebSocketState.CONNECTED:
            data = await websocket.receive_text()
            await manager.send_to_peer(data, user_id, peer_id)
    except WebSocketDisconnect:
        manager.disconnect(user_id, peer_id)
