from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.state import FSMmodel
from models.filters import SixDigitCaptchaFilter

router: Router = Router()

@router.message(
        #StateFilter(FSMmodel.captcha),
        SixDigitCaptchaFilter()
        )
async def solve_captcha(message: Message,
                        state: FSMContext,
                        value: str,
                        #service: csv_service
                        ):
    await message.answer(text=f"I got captcha {value}")