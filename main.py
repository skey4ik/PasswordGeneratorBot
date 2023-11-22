import settings
import keyboard
import random
import string

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

storage = MemoryStorage()
bot = Bot(settings.token)
dp = Dispatcher(bot, storage=storage)

async def on_startup(_):
    print('Спасибо что используете моего бота!')

class UserState(StatesGroup):
    letters_storage = State()
    digits_storage = State()
    punctuation_storage = State()
    length = State()
    letters_generate = State()
    digits_generate = State()
    pincuation_generate = State()

def generate_password(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password

@dp.message_handler(commands=['start'])
@dp.message_handler(Text(equals="↩Назад"), state='*')
async def start_command(message: types.message, state: FSMContext):
    await state.finish()
    await message.answer('Сгенерировать пароль 👇', reply_markup = keyboard.kb_main)

@dp.message_handler(Text(equals="🔓Легкий пароль (5)"))
async def easy(message: types.message):
    await message.answer(generate_password(5))

@dp.message_handler(Text(equals="🔒Средний пароль (10)"))
async def medium(message: types.message):
    await message.answer(generate_password(10))

@dp.message_handler(Text(equals="🔐Сложный пароль (15)"))
async def hard(message: types.message):
    await message.answer(generate_password(15))

@dp.message_handler(Text(equals="🛠Дополнительно"), state='*')
async def hard(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['letters_storage'] = "❌Буквы"
        data['digits_storage'] = "❌Цифры"
        data['punctuation_storage'] = "❌Символы"
        data['letters_generate'] = ""
        data['digits_generate'] = ""
        data['punctuation_generate'] = ""
    await UserState.length.set()
    await message.answer('🔽Настрой сам🔽', reply_markup = keyboard.kb_custom)
    await message.answer(f"Введи длину пароля:\n{data['letters_storage']} {data['digits_storage']} {data['punctuation_storage']}", reply_markup = keyboard.ikb_custom)

@dp.callback_query_handler(state='*')
async def update_button(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data = data
    if call.data == 'letters':
        if data['letters_storage'] != "✅Буквы" and data['letters_generate'] != string.ascii_letters:

            async with state.proxy() as data:
                data['letters_storage'] = "✅Буквы"
            
            async with state.proxy() as data:
                data['letters_generate'] = string.ascii_letters
        else:
            async with state.proxy() as data:
                data['letters_storage'] = "❌Буквы"
            async with state.proxy() as data:
                data['letters_generate'] = ""

        await call.message.edit_text(f"Введите длину пароля:\n{data['letters_storage']} {data['digits_storage']} {data['punctuation_storage']}", reply_markup=keyboard.ikb_custom)
    
    if call.data == 'digits':
        if data['digits_storage'] != "✅Цифры" and data['digits_generate'] != string.digits:

            async with state.proxy() as data:
                data['digits_storage'] = "✅Цифры"

            async with state.proxy() as data:
                data['digits_generate'] = string.digits
        else:
            async with state.proxy() as data:
                data['digits_storage'] = "❌Цифры"
            async with state.proxy() as data:
                data['digits_generate'] = ""

        await call.message.edit_text(f"Введите длину пароля:\n{data['letters_storage']} {data['digits_storage']} {data['punctuation_storage']}", reply_markup=keyboard.ikb_custom)
    
    if call.data == 'punctuation':
            if data['punctuation_storage'] != "✅Символы" and data['punctuation_generate'] != string.punctuation:
            
                async with state.proxy() as data:
                    data['punctuation_storage'] = "✅Символы"

                async with state.proxy() as data:
                    data['punctuation_generate'] = string.punctuation
            else:
                async with state.proxy() as data:
                    data['punctuation_storage'] = "❌Символы"
                async with state.proxy() as data:
                    data['punctuation_generate'] = ""

            await call.message.edit_text(f"Введите длину пароля:\n{data['letters_storage']} {data['digits_storage']} {data['punctuation_storage']}", reply_markup=keyboard.ikb_custom)

@dp.message_handler(state=UserState.length)
async def length(message: types.message, state: FSMContext):
    if message.text.isdigit() and 0 < int(message.text) < 4097:
        async with state.proxy() as data:
            data['length'] = int(message.text)
        
        def generate_password_custom(length):
            characters = data['letters_generate'] + data['digits_generate'] + data['punctuation_generate']
            password = ''.join(random.choice(characters) for i in range(length))
            return password
        
        await message.answer(generate_password_custom(data['length']))
    else:
        await message.answer('❌Введите число от 1 до 4096')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)