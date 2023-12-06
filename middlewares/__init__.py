from aiogram import Dispatcher

import config


def register_middlewares(dp: Dispatcher):
    from . import throttling

    throttling.register_middleware(dp=dp)
