import pathlib

from datetime import datetime
from json import dumps
from uuid import UUID

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bs4 import BeautifulSoup
from dependency_injector.wiring import Provide, inject
from redis.asyncio import Redis

from containers.container import Container
from core.config import settings
from core.state import FSMmodel
from services.abstract import AbstractContentGetter, AbstractImageService

scheduler = AsyncIOScheduler()

@inject
async def check_status(
        redis: Redis = Provide[Container.redis],
        bot: Bot = Provide[Container.bot],
        request_service: AbstractContentGetter = Provide[Container.request_service],
        image_service: AbstractImageService = Provide[Container.image_service]
        ):
    state = FSMContext(storage=RedisStorage(redis=redis),
                       key=StorageKey(bot_id=bot.id,
                                      chat_id=settings.owner_id,
                                      user_id=settings.owner_id)
                                      )
    html_text, _, _ = await request_service.get_text(settings.link)
    soup = BeautifulSoup(html_text, 'lxml')
    img_tag = soup.find("img")
    img_link = f"{settings.link.scheme}://{settings.link.host}/queue/{img_tag.get('src')}"
    image, headers, cookies = await request_service.get_content(img_link)
    image_service.save_image(image)
    captcha = FSInputFile(path=image_service.path)
    c_form = soup.find("form")
    data = {e.attrs.get("name"): e.attrs.get("value") for e in c_form.find_all("input")}
    data["__EVENTTARGET"] = ''
    data["__EVENTARGUMENT"] = ''

    ASP_session_id = cookies.get("ASP.NET_SessionId")
    headers = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
   'Content-Type': 'application/x-www-form-urlencoded',
   'Accept-Encoding': 'gzip, deflate, br',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
   'Connection': 'keep-alive',
   'Host': 'trabzon.kdmid.ru',
   'Cookie': "; ".join([f"{key}={value}" for (key, value) in cookies.items()]+[f'ASP.NET_SessionId={ASP_session_id}'])
}
    await state.set_state(FSMmodel.captcha)
    await state.update_data(payload=data, headers=headers, cookies=cookies)
    await bot.send_photo(chat_id=settings.owner_id,
                         photo=captcha,
                         #caption="В ответ пришлите расшифровку кэпчи."
                         )
    image_service.delete_image()


scheduler.add_job(check_status, "cron", hour=11, minute=8)