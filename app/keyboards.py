from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Перейти к оплате', callback_data='pay')]
])

channel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Канал', url ='https://t.me/+ptADpilMe49jZWRi')]
])