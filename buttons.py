from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta

lang = types.InlineKeyboardMarkup(inline_keyboard=[
    [
        types.InlineKeyboardButton(text="English", callback_data="en"),
        types.InlineKeyboardButton(text="Русский", callback_data="ru"),
        types.InlineKeyboardButton(text="Uzbek tili", callback_data="uz")
    ],
])

menu = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="📄 About us"),
            types.KeyboardButton(text="🦷 Service")
        ],
        [
            types.KeyboardButton(text="💡 Help"),
            types.KeyboardButton(text="⚙️ Settings")
        ],
    ],
    resize_keyboard=True
)

services = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="Terapiya", callback_data="ter")],
    [types.InlineKeyboardButton(text="Xirurgiya", callback_data="xir")],
    [types.InlineKeyboardButton(text="Implantatsiya", callback_data="imp")],
    [types.InlineKeyboardButton(text="Ortodontiya", callback_data="ortoden")],
    [types.InlineKeyboardButton(text="Ortopediya", callback_data="orto")],
    [types.InlineKeyboardButton(text="Indodontiya", callback_data="indo")],
    [types.InlineKeyboardButton(text="🔙 Orqaga", callback_data="orqaga")],
        ]
)

booking = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="🔖 Buyurtma qilish", callback_data="book")],
    [types.InlineKeyboardButton(text="🔙 Orqaga", callback_data="back")]
])



confirmation_buttons = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="✅ Ha", callback_data="yes")],
    [types.InlineKeyboardButton(text="❌ Yo'q", callback_data="no")],
])

