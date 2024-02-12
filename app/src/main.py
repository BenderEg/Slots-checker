import asyncio

from redis.asyncio import Redis

from containers.container import Container
from core.bot import get_bot_instance
from core.menu import set_main_menu
from core.config import settings
from db import redis_storage
from handlers import captcha

#from aiogram3_di import DIMiddleware

async def main() -> None:

    redis_storage.redis = Redis(host=settings.redis.host,
                                port=settings.redis.port,
                                db=settings.redis.db,
                                encoding="utf-8",
                                decode_responses=True)
    bot, dp = await get_bot_instance()

    dp.include_router(captcha.router)

    #dp.message.middleware(DIMiddleware())
    #dp.callback_query.middleware(DIMiddleware())

    container = Container()
    container.init_resources()
    container.wire(modules=["background.regular"])

    await set_main_menu(bot)

    from background.regular import scheduler

    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())