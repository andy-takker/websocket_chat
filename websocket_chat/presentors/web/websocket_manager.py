from collections import defaultdict
from typing import Any
from uuid import UUID

from fastapi import WebSocket

WSKey = tuple[UUID, UUID, UUID]  # (chat_id, user_id, device_id)


class WebsocketManager:
    def __init__(self) -> None:
        self._ws: dict[UUID, dict[WSKey, set[WebSocket]]] = defaultdict(dict)

    async def connect(
        self,
        chat_id: UUID,
        user_id: UUID,
        device_id: UUID,
        ws: WebSocket,
    ) -> None:
        await ws.accept()
        key = (chat_id, user_id, device_id)
        self._ws[chat_id].setdefault(key, set()).add(ws)

    def disconnect(
        self,
        chat_id: UUID,
        user_id: UUID,
        device_id: UUID,
        ws: WebSocket,
    ) -> None:
        key = (chat_id, user_id, device_id)
        conns = self._ws[chat_id].get(key)
        if conns is None:
            return
        conns.discard(ws)
        if not conns:
            self._ws[chat_id].pop(key, None)
        if not self._ws[chat_id]:
            self._ws.pop(chat_id, None)

    async def broadcast_chat(self, chat_id: UUID, data: dict[str, Any]) -> None:
        for conns in self._ws.get(chat_id, {}).values():
            for ws in conns:
                await ws.send_json(data)

    async def broadcast_user(
        self, chat_id: UUID, user_id: UUID, data: dict[str, Any]
    ) -> None:
        for (cid, uid, _), conns in self._ws.get(chat_id, {}).items():
            if uid == user_id:
                for ws in conns:
                    await ws.send_json(data)
