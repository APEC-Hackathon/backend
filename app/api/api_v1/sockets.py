import json 

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from fastapi.websockets import WebSocketState
from sqlalchemy.orm import Session

from app.utils.sockets import manager
from app import crud
from app.utils.translation import translate
from app.api import deps

socket_router = APIRouter()


@socket_router.websocket("/{user_id}/{peer_id}/")
async def websocket_endpoint(
    websocket: WebSocket,
    peer_id: int,
    user_id: int,
    db: Session = Depends(deps.get_db),
):
    await manager.connect(websocket, user_id, peer_id)
    try:
        target_lang = crud.user.get(db=db, id=peer_id).prefered_language
        while websocket.application_state == WebSocketState.CONNECTED:
            data = await websocket.receive_text()
            data = json.loads(data)
            data['translated_content'] = translate(data['content'], target_lang)
            data = json.dumps(data)
            await manager.send_to_peer(data, user_id, peer_id)
    except WebSocketDisconnect:
        manager.disconnect(user_id, peer_id)
