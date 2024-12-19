from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    fullname = State()
    age = State()
    phone = State()
    email = State()
    confirmation = State()

class BookingState(StatesGroup):
    service = State()
    times = State()
    finish = State()







DataUser = {
    "username": "https://t.me/all_moody",
    "password": "5728240909"
}