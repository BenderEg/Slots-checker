import pathlib

from datetime import datetime
from json import dumps
from uuid import UUID

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bs4 import BeautifulSoup
from dependency_injector.wiring import Provide, inject

from containers.container import Container
from core import bot
from core.config import settings
from core.state import FSMmodel
from db.redis_storage import get_redis
from services.abstract import AbstractContentGetter
from services.request_service import get_data_getter


scheduler = AsyncIOScheduler()

async def process_image(image: bytes) -> FSInputFile:
    today = datetime.utcnow().date().isoformat()
    path = pathlib.Path.cwd().joinpath("tmp", f"{today}.jpeg")
    path.touch()
    path.write_bytes(image)
    return FSInputFile(path=path)


async def clear_tmp() -> None:
    today = datetime.utcnow().date().isoformat()
    path = pathlib.Path.cwd().joinpath("tmp", f"{today}.jpg")
    path.unlink(missing_ok=True)

@inject
async def check_status(service: AbstractContentGetter = Provide[Container.request_service]):
    redis = await get_redis()
    state = FSMContext(storage=RedisStorage(redis=redis),
                       key=StorageKey(bot_id=bot.bot.id,
                                      chat_id=settings.owner_id,
                                      user_id=settings.owner_id)
                                      )
    #service = await get_data_getter()
    html_text, _, _ = await service.get_text(settings.link)
    soup = BeautifulSoup(html_text, 'lxml')
    img_tag = soup.find("img")
    img_link = f"{settings.link.scheme}://{settings.link.host}/queue/{img_tag.get('src')}"
    image, headers, cookies = await service.get_content(img_link)
    captcha = await process_image(image)
    c_form = soup.find("form")
    data = {e.attrs.get("name"): e.attrs.get("value") for e in c_form.find_all("input")}
    data["__EVENTTARGET"] = ''
    data["__EVENTARGUMENT"] = ''
    #data["ctl00$MainContent$txtCode"] = ''

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
    await clear_tmp()
    await state.set_state(FSMmodel.captcha)
    await state.update_data(payload=data, headers=headers, cookies=cookies)
    await bot.bot.send_photo(chat_id=settings.owner_id,
                             photo=captcha,
                             #caption="В ответ пришлите расшифровку кэпчи."
                             )


scheduler.add_job(check_status, "interval", seconds=30)