from fastapi import WebSocket
from typing import Dict, List, Set
import json
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    """WebSocket connection manager"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_rooms: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, room: str = "default"):
        """Accept WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        
        if room not in self.connection_rooms:
            self.connection_rooms[room] = []
        self.connection_rooms[room].append(websocket)
        
        logger.info(f"WebSocket connected in room: {room}")
    
    def disconnect(self, websocket: WebSocket, room: str = "default"):
        """Remove WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        if room in self.connection_rooms and websocket in self.connection_rooms[room]:
            self.connection_rooms[room].remove(websocket)
        
        logger.info("WebSocket disconnected")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific connection"""
        await websocket.send_text(message)
    
    async def broadcast(self, message: str, room: str = "default"):
        """Broadcast message to all connections in room"""
        if room not in self.connection_rooms:
            return
        
        for connection in self.connection_rooms[room]:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Failed to send message: {e}")
                self.disconnect(connection, room)
    
    async def broadcast_json(self, data: Dict, room: str = "default"):
        """Broadcast JSON data to all connections in room"""
        await self.broadcast(json.dumps(data), room)
    
    async def send_lead_update(self, lead_id: str, data: Dict):
        """Send lead update notification"""
        await self.broadcast_json({
            "type": "lead_update",
            "lead_id": lead_id,
            "data": data
        })
    
    async def send_agent_status(self, status: Dict):
        """Send agent status update"""
        await self.broadcast_json({
            "type": "agent_status",
            "data": status
        })