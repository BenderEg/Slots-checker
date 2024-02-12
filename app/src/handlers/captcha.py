from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bs4 import BeautifulSoup

from containers.container import Container
from core.config import Settings
from core.state import FSMmodel
from dependency_injector.wiring import Provide, inject
from models.filters import SixDigitCaptchaFilter
from services.abstract import AbstractContentGetter

router: Router = Router()

@router.message(
        StateFilter(FSMmodel.captcha),
        SixDigitCaptchaFilter()
        )
@inject
async def solve_captcha(message: Message,
                        state: FSMContext,
                        value: str,
                        settings: Settings = Provide[Container.settings],
                        request_service: AbstractContentGetter = Provide[Container.request_service]
                        ):
    data = await state.get_data()
    headers = data.get("headers")
    cookies = data.get("cookies")
    payload = data.get("payload")
    payload["ctl00$MainContent$txtCode"] = value
    html_text, _, _ = await request_service.post(settings.link,
                                                 data=payload,
                                                 headers=headers,
                                                 cookies=cookies
                                                 )
    soup = BeautifulSoup(html_text, 'lxml')
    c_form = soup.find("form")
    data = {e.attrs.get("name"): e.attrs.get("value") for e in c_form.find_all("input")}
    data["__EVENTTARGET"] = ''
    data["__EVENTARGUMENT"] = ''
    data["ctl00$MainContent$ButtonB.x"] = '120'
    data["ctl00$MainContent$ButtonB.y"] = '23'
    html_text, _, _ = await request_service.post(settings.link,
                                                 data=data,
                                                 headers=headers,
                                                 cookies=cookies
                                                 )
    soup = BeautifulSoup(html_text, 'lxml')
    result = soup.find("table").find("td", id="center-panel").find("p").text
    msg = result + "\n" + str(settings.link)
    await message.answer(text=msg)