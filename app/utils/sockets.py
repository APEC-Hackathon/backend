from typing import List

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.websocket_to_userid: dict[WebSocket, (int, int)] = {}
        self.userid_to_websocket: dict[(int, int), WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int, peer_id: int):
        await websocket.accept()
        self.websocket_to_userid[websocket] = (user_id, peer_id)
        self.userid_to_websocket[(user_id, peer_id)] = websocket
    
    def get_websocket(self, user_id: int, peer_id: int) -> WebSocket:
        if (user_id, peer_id) not in self.userid_to_websocket:
            return None
        return self.userid_to_websocket[(user_id, peer_id)]

    def disconnect(self, user_id: int, peer_id: int):
        self.websocket_to_userid.pop(self.userid_to_websocket[(user_id, peer_id)])
        self.userid_to_websocket.pop((user_id, peer_id))
    
    def get_connected_peer_socket(self, user_id: int, peer_id: int) -> WebSocket:
        if (peer_id, user_id) in self.userid_to_websocket:
            return self.get_websocket(peer_id, user_id)
        return None 

    async def send_to_peer(self, message: str, user_id, peer_id: int):
        peer_socket = self.get_connected_peer_socket(user_id, peer_id)
        if peer_socket:
            await peer_socket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()
