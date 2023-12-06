from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Update
from cachetools import TTLCache

import config


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self):
        self.cache = TTLCache(maxsize=10_000, ttl=config.throttling_rate)

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        if event.chat.id in self.cache:
            return
        self.cache[event.chat.id] = None
        return await handler(event, data)


def register_middleware(dp: Dispatcher):
    throttling_middleware = ThrottlingMiddleware()
    dp.message.middleware(throttling_middleware)
