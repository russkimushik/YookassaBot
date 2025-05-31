import aiosqlite
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, Command
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.database.requests import get_users

admin = Router()

class Admin(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in [### Список админов ###]

@admin.message(Admin(), Command('send_mes'))
async def newsletter(message: Message, state: FSMContext):
    await state.set_state(Send_Mes.message)
    await message.answer('Введитие сообщение для рассылки')
