import asyncio
import logging

import coloredlogs
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram_dialog import setup_dialogs
from aiohttp import web

import db
import config
from dialogs import dialog_router
from handlers import get_handlers_router
from middlewares import register_middlewares
from commands import remove_bot_commands, setup_bot_commands


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    register_middlewares(dp=dispatcher)

    dispatcher.include_router(get_handlers_router())
    dispatcher.include_router(dialog_router)
    setup_dialogs(dispatcher)

    await setup_bot_commands(bot)

    if config.use_webhook:
        webhook_url = (
            config.webhook_url + config.webhook_path
            if config.webhook_url
            else f"http://localhost:{config.webhook_port}{config.webhook_path}"
        )
        await bot.set_webhook(
            webhook_url,
            drop_pending_updates=config.drop_pending_updates,
            allowed_updates=dispatcher.resolve_used_update_types(),
        )
    else:
        await bot.delete_webhook(
            drop_pending_updates=config.drop_pending_updates,
        )

    await db.init_orm(config.tortoise_config)

    bot_info = await bot.get_me()

    logging.info(f"Name - {bot_info.full_name}")
    logging.info(f"Username - @{bot_info.username}")
    logging.info(f"ID - {bot_info.id}")

    states = {
        True: "Enabled",
        False: "Disabled",
    }

    logging.debug(f"Groups Mode - {states[bot_info.can_join_groups]}")
    logging.debug(f"Privacy Mode - {states[not bot_info.can_read_all_group_messages]}")
    logging.debug(f"Inline Mode - {states[bot_info.supports_inline_queries]}")

    logging.error("Bot started!")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    logging.warning("Stopping bot...")
    await remove_bot_commands(bot)
    await bot.delete_webhook(drop_pending_updates=config.drop_pending_updates)
    await dispatcher.fsm.storage.close()
    await bot.session.close()
    await db.close_orm()


async def main():
    coloredlogs.install(level=logging.INFO)
    logging.warning("Starting bot...")

    tortoise_config = config.tortoise_config

    await db.create_models(tortoise_config)

    token = config.bot_token
    bot_settings = {"parse_mode": "HTML"}

    bot = Bot(token, **bot_settings)

    if config.use_persistent_storage:
        storage = RedisStorage(
            redis=RedisStorage.from_url(config.redis_url),
            key_builder=DefaultKeyBuilder(with_destiny=True),
        )
    else:
        storage = MemoryStorage()

    dp = Dispatcher(storage=storage)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    context_kwargs = {"config": config}

    if config.use_webhook:
        logging.getLogger("aiohttp.access").setLevel(logging.CRITICAL)

        web_app = web.Application()
        SimpleRequestHandler(dispatcher=dp, bot=bot, **context_kwargs).register(
            web_app, path=config.webhook_path
        )

        setup_application(web_app, dp, bot=bot, **context_kwargs)

        runner = web.AppRunner(web_app)
        await runner.setup()
        site = web.TCPSite(runner, port=config.webhook_port)
        await site.start()

        await asyncio.Event().wait()
    else:
        await dp.start_polling(bot, **context_kwargs)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
