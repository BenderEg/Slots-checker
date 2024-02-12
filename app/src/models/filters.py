from aiogram.filters import BaseFilter
from aiogram.types import Message


class SixDigitCaptchaFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text and len(message.text)==6 and message.text.isdigit():
            return {'value': message.text}
        return False