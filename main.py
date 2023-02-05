import callback as callback
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import CallbackQuery
from imdb import Cinemagoer
import markup as nav
import config as cfg
import random
import logging





logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot,storage=storage)
io = Cinemagoer()


async def check_SUB(channels, user_id):

    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
        if chat_member['status'] == 'left':
            return False
    return True

async def MovieCode(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['FilmCode'] = int(message.text)

    await state.finish()


def getKeysForValueComp(dictionary, value):
    return [key for key in dictionary if dictionary[key] == value]

def greet():

    top = io.get_popular100_movies()
    random.shuffle(top)

    title = top[0]
    movID = top[0].movieID
    url = f'https://www.imdb.com/title/tt{movID}'

    msg = f' Советую посмотреть: { title } ' \
          f'{ url }'\

    return msg


class Form(StatesGroup):
    FilmCode = State()


async def input_code(message: types.Message):
    if message.chat.type == 'private':
        if await check_SUB(cfg.SUB_CH, message.from_user.id):
                film = 0
        else:
            await bot.send_message(message.from_user.id, cfg.NOT_SUB_MES, reply_markup=nav.showChannels())
@dp.message_handler(commands=['start'])
async def Humdrum(message: types.Message):
    if message.chat.type == 'private':
        if await check_SUB(cfg.SUB_CH, message.from_user.id):
            await bot.send_message(message.from_user.id,"Спасибо за подписку, введите код от вашего фильма\U0001F37F\nИли выберите случайный фильм\U0001F3B2",reply_markup=nav.profileKeyboard)
            if message.text == "Случайный фильм\U0001F3B2":
                await bot.send_message(message.from_user.id, greet())


@dp.message_handler(content_types=["text"])
async def Event_Handler(message: types.Message):
    if message.chat.type == 'private':
        if await check_SUB(cfg.SUB_CH, message.from_user.id):
            if message.text == "Случайный фильм\U0001F3B2":
                await bot.send_message(message.from_user.id, greet())
            if message.text == "Ввести код от фильма\U0001F511":
                lll = types.ReplyKeyboardRemove()

                await bot.send_message(message.from_user.id,text="Вы можете вернуться назад, если у вас нет кода:",reply_markup=nav.BackToTheFuture())
                await bot.send_message(message.from_user.id,text="Введите код в чат! ", reply_markup=lll)

        else:
            await bot.send_message(message.from_user.id, cfg.NOT_SUB_MES , reply_markup=nav.showChannels())


@dp.callback_query_handler(text="back")
async def Backto(call: types.CallbackQuery):
    answer_data = call.data
    if answer_data == "back":
        await call.message.answer('Вот наш каталог Тест', reply_markup=nav.profileKeyboard)
@dp.callback_query_handler(text="subchanneldone")
async def Subchanneldone(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)

    if await check_SUB(cfg.SUB_CH, message.from_user.id):
        await bot.send_message(message.from_user.id, "Спасибо за подписку , введите код от вашего фильма\U0001F37F\nИли выберите случайный фильм\U0001F3B2",
                               reply_markup=nav.profileKeyboard)
    else:
        await bot.send_message(message.from_user.id, cfg.NOT_SUB_MES, reply_markup=nav.showChannels())



def register_handler_admins(dp : Dispatcher):
    dp.register_message_handler(MovieCode, state=Form.FilmCode)
    dp.register_message_handler(Event_Handler)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
