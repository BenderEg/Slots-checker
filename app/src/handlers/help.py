from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router: Router = Router()

@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(text="Бот помогает автоматизировать \
проверку свободных слотов для записи. Пользователь ежедневно получает запрос от бота \
на решение капчи. Остальное бот делает сам.")