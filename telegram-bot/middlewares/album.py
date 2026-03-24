import asyncio
from typing import Any, Dict, List, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import Message

class AlbumMiddleware(BaseMiddleware):
    def __init__(self, latency: float = 0.5):
        self.latency = latency
        self.album_data: Dict[str, List[Message]] = {}

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        
        if not event.media_group_id:
            return await handler(event, data)
        
        try:
            self.album_data[event.media_group_id].append(event)
            return 
        
        except KeyError:
            self.album_data[event.media_group_id] = [event]

            await asyncio.sleep(self.latency)

            data["album"] = self.album_data.pop(event.media_group_id)

            return await handler(event, data)