from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from config import SUB_CH

btnProfile1 = KeyboardButton('Случайный фильм\U0001F3B2')
btnProfile2 = KeyboardButton('Ввести код от фильма\U0001F511')
profileKeyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(btnProfile1).add(btnProfile2)




def showChannels():

    kb = InlineKeyboardMarkup(row_width=1)
    for channel in SUB_CH:
            text = channel[0]
            btn = InlineKeyboardButton(text=text, url=channel[2])
            kb.insert(btn)



    btnDoneSub = InlineKeyboardButton(text=" Выполнено \u2705 ", callback_data="subchanneldone")
    kb.insert(btnDoneSub)
    return kb


def BackToTheFuture():

    ikb = InlineKeyboardMarkup(row_width=1)
    btn = InlineKeyboardButton(text="Назад \U0001F519", callback_data="back")
    ikb.add(btn)
    return ikb