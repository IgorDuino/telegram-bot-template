from aiogram import Router
from .sample_dialog import ui


dialog_router = Router()
dialog_router.include_router(ui)
