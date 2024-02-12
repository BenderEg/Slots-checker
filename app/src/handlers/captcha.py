from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from containers.container import Container
from core.state import FSMmodel
from dependency_injector.wiring import Provide, inject
from models.filters import SixDigitCaptchaFilter

router: Router = Router()

@router.message(
        StateFilter(FSMmodel.captcha),
        SixDigitCaptchaFilter()
        )
@inject
async def solve_captcha(message: Message,
                        state: FSMContext,
                        value: str,
                        request_service: Provide[Container.request_service]
                        ):
    data = await state.get_data()
    headers = data.get("headers")
    cookies = data.get("cookies")
    payload = data.get("payload")
    print(f"{headers=}")
    print(f"{cookies=}")
    print(f"{payload=}")
    await message.answer(text=f"I got captcha {value}")