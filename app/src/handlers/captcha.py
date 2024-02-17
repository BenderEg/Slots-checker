from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from bs4 import BeautifulSoup

from containers.container import Container
from core.config import Settings
from core.state import FSMmodel
from dependency_injector.wiring import Provide, inject
from models.filters import SixDigitCaptchaFilter
from services.abstract import AbstractContentGetter, AbstractImageService

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
                        request_service: AbstractContentGetter = Provide[Container.request_service],
                        image_service: AbstractImageService = Provide[Container.image_service],
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
    check_captcha = soup.find("span", id="ctl00_MainContent_lblCodeErr")
    if check_captcha:
        img_tag = soup.find("img")
        img_link = f"{settings.link.scheme}://{settings.link.host}/queue/{img_tag.get('src')}"
        image, _, cookies = await request_service.get_content(img_link)
        image_service.save_image(image)
        captcha = FSInputFile(path=image_service.path)
        c_form = soup.find("form")
        data = {e.attrs.get("name"): e.attrs.get("value") for e in c_form.find_all("input")}
        data["__EVENTTARGET"] = ''
        data["__EVENTARGUMENT"] = ''
        ASP_session_id = cookies.get("ASP.NET_SessionId")
        headers["Cookie"] = "; ".join(
            [f"{key}={value}" for (key, value) in cookies.items()
             ]+[f'ASP.NET_SessionId={ASP_session_id}'])
        await state.update_data(payload=data, headers=headers, cookies=cookies)
        await message.answer(
            text="Символы с картинки введены неправильно. Пожалуйста, повторите попытку."
            )
        await message.answer_photo(photo=captcha)
        image_service.delete_image()
        return
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
    if result:
        msg = result + "\n" + str(settings.link)
    else:
        msg = "Появились доступные даты для записи:" + "\n" + str(settings.link)
    await message.answer(text=msg)
    await state.set_state(state=None)

@router.message(StateFilter(FSMmodel.captcha))
async def wrong_input(message: Message):
    await message.answer(text="Неверный ввод для капча. Попробуйте еще раз.")