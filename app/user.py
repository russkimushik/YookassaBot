import asyncio
import aiosqlite
import sqlite3
import aiosqlite
import config as cfg
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, LabeledPrice, ChatJoinRequest
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from app.database.requests import set_user
import config
import app.keyboards as kb

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
user = Router()

user.chat_join_request.filter(F.chat.id == -1002574487484)

@user.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id, message.from_user.username)
    await message.answer('Добро пожаловать!!!\nЭто бот для оплаты подписки в закрытый ТГ канал. Нажми на кнопку, чтобы оплатить и попасть в канал.', reply_markup=kb.start)
@user.callback_query(F.data == 'pay')
async def fin_pay(callback: CallbackQuery):
    price = [LabeledPrice(label='RUB', amount= 80*100)]
    await callback.message.answer_invoice('Покупка тарифа',
                                          'Покупка платного сообщения',
                                          'order_payload',
                                          provider_token=config.PAYMENT_TOKEN,
                                          currency = 'RUB',
                                          prices = price,
                                          start_parameter='pay_order')
@user.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
@user.message(F.successful_payment)
async def succ_pay(message: Message):
    await message.answer('Платеж прошел успешно. Нажмите на кнопку, для того чтобы перейти в канал', reply_markup=kb.channel)
    try:
        async with aiosqlite.connect('db.sqlite3') as db:
            await db.execute(
                'INSERT INTO pay_users (tg_id, username) VALUES (?, ?)',
                (message.from_user.id, message.from_user.username))
            await db.commit()
    except Exception as e:
        print(e)

@user.chat_join_request()
async def succ_pay(update: ChatJoinRequest):
    chat_id = update.from_user.id
    exists = cursor.execute("SELECT 1 FROM pay_users WHERE tg_id = ?", [chat_id]).fetchone()
    print(exists)
    if exists:
        await update.approve()
        await update.bot.send_message(update.from_user.id, 'Вы теперь в канале!')
    else:
        await update.decline()
        await update.bot.send_message(update.from_user.id, 'Вы не оплатили доступ')