import asyncio
import re
from aiogram import Bot, Dispatcher, F, types
from config import TOKEN, API_KEY_WEATHER
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import random
import aiohttp
from googletrans import Translator


bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class Form(StatesGroup):
    waiting_for_city = State()


class FormTranslate(StatesGroup):
    waiting_for_text = State()


@dp.message(CommandStart())
async def start(message:Message):
    await message.answer(f'Привет, {message.from_user.full_name}  Рад Вас приветствовать!!!!')


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Я умею выполнять команды \n /start \n /help \n /weather \n /audio \n /voice \n /translate')


@dp.message(F.text == "Кто такой Lionel Messi???")
async def bot_answer(message: Message):
    await message.answer('Lionel Messi -- величайший футболист всех времен')


@dp.message(F.photo)
async def add_photo(message: Message):
    await message.answer('Фотография получена. Спасибо')
    list = ['Классная фотка', 'Выглядишь отстойно']
    random_answer = random.choice(list)
    await message.answer(random_answer)
    await bot.send_chat_action(message.chat.id, 'upload_photo')
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')


@dp.message(Command('audio'))
async def send_audio(message: Message):
    audio = FSInputFile('The Kolors - Italodisco.mp3')
    await bot.send_chat_action(message.chat.id, 'upload_audio')
    await bot.send_audio(message.chat.id, audio)


@dp.message(Command('voice'))
async def send_audio(message: Message):
    voice = FSInputFile('audio_2025-04-18_23-06-51.ogg')
    await bot.send_chat_action(message.chat.id, 'record_audio')
    await message.answer_voice(voice=voice, caption='Вот голосовое сообщение!!!')


@dp.message(Command('translate'))
async def send_text(message: Message, state: FSMContext):
    await state.set_state(FormTranslate.waiting_for_text)
    await message.answer('Привет!! Напишите любое сообщение и я Вам переведу его на английский язык')


@dp.message(FormTranslate.waiting_for_text)
async def translate_text(message: types.Message):
    try:
        text = message.text
        translator = Translator()
        translation_result = translator.translate(text, dest='en')
        corrected_translation = re.sub(r'([!?.\,])(?=\S)', r'\1 ', translation_result.text)
        await message.answer(f'Перевод на английский: {corrected_translation}')
    except Exception as e:
        await message.answer(f'Ошибка перевода: {str(e)}')


@dp.message(Command('weather'))
async def waiting_city(message: Message, state: FSMContext):
    await state.set_state(Form.waiting_for_city)
    await message.answer('Введите названия города ')


@dp.message(Form.waiting_for_city)
async def get_forecast(message: types.Message):
    city = message.text
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_WEATHER}&units=metric"

    async with aiohttp.ClientSession() as session:  # создаёт сессию клиента HTTP, которая поддерживает пул соединений
        async with session.get(url) as resp:  # выполняет асинхронный GET-запрос по указанному URL
            response = await resp.json()  # конструкция async with гарантирует корректное открытие и закрытие сессии и запроса

    if response.get("cod") == 200:
        weather_description = response['weather'][0]['description']
        temperature = response['main']['temp']
        await message.answer(f'Температура в городе {city} равна {temperature}°C.\n Описание: {weather_description}')
    else:
        await message.answer(f'Не удалось получить данные о погоде')


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())