import asyncio

from containers.container import Container
from core.menu import set_main_menu
from handlers import captcha


async def main() -> None:

    container = Container()
    container.init_resources()
    container.wire(modules=["background.regular", "handlers.captcha"])
    container.dp().include_router(captcha.router)

    #dp.message.middleware(DIMiddleware())
    #dp.callback_query.middleware(DIMiddleware())

    await set_main_menu(container.bot())

    from background.regular import scheduler

    scheduler.start()
    await container.bot().delete_webhook(drop_pending_updates=True)
    await container.dp().start_polling(container.bot())

if __name__ == '__main__':
    asyncio.run(main())