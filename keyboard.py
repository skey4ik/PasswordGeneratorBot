from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

kb_main = ReplyKeyboardMarkup(row_width=1)
easy = KeyboardButton("🔓Легкий пароль (5)")
medium = KeyboardButton("🔒Средний пароль (10)")
hard = KeyboardButton("🔐Сложный пароль (15)")
custom = KeyboardButton("🛠Дополнительно")
kb_main.add(easy, medium, hard, custom)

kb_custom = ReplyKeyboardMarkup(resize_keyboard=True)
back = KeyboardButton("↩Назад")
kb_custom.add(back)

ikb_custom = InlineKeyboardMarkup()
letters = InlineKeyboardButton(text='Буквы', callback_data='letters')
digits = InlineKeyboardButton(text='Цифры', callback_data='digits')
punctuation = InlineKeyboardButton(text='Символы', callback_data='punctuation')
ikb_custom.add(letters, digits, punctuation)