import asyncio
from aiogram import Bot, Dispatcher, F
from config import TOKEN
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random


bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message:Message):
    await message.answer('Привет всем!!!! Меня зовут Василий бот!!! Рад Вас приветствовать!!!!')


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Я умею выполнять команды \n /start \n /help')


@dp.message(F.text == "Кто такой Lionel Messi???")
async def bot_answer(message: Message):
    await message.answer('Lionel Messi -- величайший футболист всех времен')


@dp.message(F.photo)
async def add_photo(message: Message):
    await message.answer('Фотография получена. Спасибо')
    list = ['Классная фотка', 'Выглядишь отстойно']
    random_answer = random.choice(list)
    await message.answer(random_answer)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())