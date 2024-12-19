import asyncio
import logging
from os import times

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime
from config import TOKEN, ADMIN_ID
from db import *
from buttons import *
from form import *
from price import *

create_table()
storage = MemoryStorage()  # storage=storage
dp = Dispatcher(bot=Bot, storage=storage)


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    # Foydalanuvchi ma'lumotlarini bazadan tekshirish
    data = get_user_data(message.from_user.id)  # user_data -> data
    if data:
        await message.answer(
            f"<b>Assalomu alekum! {message.from_user.full_name} Xush kelibsiz! Siz allaqachon ro'yxatdan o'tgansiz.</b>",
            reply_markup=menu, parse_mode=ParseMode.HTML)
    else:
        await message.answer(f"<b>Assalomu alekum! {message.from_user.full_name} Xush kelibsiz </b>",
                             parse_mode=ParseMode.HTML)
        await state.set_state(Form.fullname)
        await message.answer("<b>To'liq ism familiyangizni kiriting! ✍️ </b>", parse_mode=ParseMode.HTML)


@dp.message(Form.fullname)
async def full(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await state.set_state(Form.age)
    await message.answer("<b>Yoshingizni kiriting! ✍️</b>", parse_mode=ParseMode.HTML)


@dp.message(Form.age)
async def birthday(message: Message, state: FSMContext):
    await state.update_data(birthday=message.text)
    await state.set_state(Form.phone)
    await message.answer("<b>Telefon nomeringizni yuboring! 📤</b>", parse_mode=ParseMode.HTML)


@dp.message(Form.phone)
async def phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(Form.email)
    await message.answer("<b>emailingizni kiriting! ✍️</b>", parse_mode=ParseMode.HTML)


@dp.message(Form.email)
async def email(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(email=message.text)
    await state.set_state(Form.confirmation)
    data = await state.get_data()
    fullname = data.get("fullname", "Mavjud emas")
    birthday = data.get("birthday", "Mavjud emas")
    phone = data.get("phone", "Mavjud emas")
    email = data.get("email", "Mavjud emas")
    await message.answer(
        "<b>Malumot qabul qilindi! ✅</b>", parse_mode=ParseMode.HTML
    )
    await message.answer(f"<b>Quyidagi ma'lumotlar to'g'rimi? 🤔\n"
                         f"Ism: {data['fullname']} 📝\n"
                         f"Telefon: {data['phone']} 📱\n"
                         f"Yosh: {data['birthday']} 📅\n"
                         f"Email: {data['email']} 📧\n"
                         "Iltimos tasdiqlang! ✅</b>", reply_markup=confirmation_buttons, parse_mode=ParseMode.HTML)


@dp.callback_query(F.data == "yes")
async def confirm_yes(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.answer("<b>Ma'lumotlaringiz tasdiqlandi ✅. Rahmat!</b>", reply_markup=menu,
                                  parse_mode=ParseMode.HTML)

    data = await state.get_data()
    fullname = data.get("fullname", "Mavjud emas")
    birthday = data.get("birthday", "Mavjud emas")
    phone = data.get("phone", "Mavjud emas")
    email = data.get("email", "Mavjud emas")

    save_user_data(callback.from_user.id, fullname, birthday, phone, email)


@dp.callback_query(F.data == "no")
async def confirm_no(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("<b>Ma'lumotlaringiz o'chirildi 📴. Iltimos, qaytadan boshlang /start.</b>",
                                  parse_mode=ParseMode.HTML)
    await state.clear()
    await callback.answer()


@dp.callback_query(F.data == "en")
async def lang_english_callback(callback: CallbackQuery):
    await callback.message.answer("<b>Hello! Welcome to our dentistry bot ☺</b>", reply_markup=menu,
                                  parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "uz")
async def lang_uzbek_callback(callback: CallbackQuery):
    await callback.message.answer("<b>Assalomu alaykum! Bizning stomatologiya botimizga xush kelibsiz ☺</b>",
                                  reply_markup=menu, parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "ru")
async def lang_russian_callback(callback: CallbackQuery):
    await callback.message.answer("<b>Здравствуйте! Добро пожаловать в наш стоматологический бот ☺</b>",
                                  reply_markup=menu, parse_mode="HTML")
    await callback.answer()


@dp.message(F.text == "⚙️ Settings")
async def settings_callback(message: Message):
    await message.answer(
        "<b>Marhamat o'zingizga mos kelgan tilni tanlashingiz mumkin ☺</b>",
        reply_markup=lang,
        parse_mode="HTML"
    )


@dp.message(F.text == "🦷 Service")
async def settings(message: Message):
    await message.answer_photo(
        "https://openre.tech/wp-content/uploads/2024/04/360_F_303497515_ZHOwfTtuo5sYpAeoqWRZnkXZNZDKZeMz.jpg",
        "<b>Marhamat bizning xizmatlarimizdan foydalanishingiz mumkin</b>", reply_markup=services,
        parse_mode="HTML")


@dp.message(F.text == "📄 About us")
async def about(message: Message):
    await message.answer(
        "<b>ℹ️ Biz haqimizda  \n\n🌟 Ko‘p yillik tajribaga ega bo‘lgan yuqori malakali shifokorlar.  \n\n🛠️ Zamonaviy texnologiyalar va innovatsion uskunalar yordamida og‘riqsiz va samarali davolash. \n\n-- 🛠️ Bizning xizmatlarimiz \n\n🤝 Har bir bemorga individual yondashuv va qulay muhitni ta'minlash. \n\n🦷 Professional gigiyena va tishlarni oqartirish. \n\n💉 Karies va boshqa kasalliklarni davolash. \n\n🛠️ Protezlash va ortodontik xizmatlar.</b>",
        parse_mode=ParseMode.HTML)


@dp.message(F.text == "💡 Help")
async def about(message: Message):
    await message.answer(""" <b>
    📋 Qanday qilib qabulga yozilishingiz mumkin?

1️⃣ Tugmani bosing:
🔘 "Qabulga yozilish" tugmasini tanlang.


2️⃣ Ma'lumotlarni kiriting:
🖊️ To'liq ism, telefon raqamingiz va boshqa kerakli ma'lumotlarni kiriting.


3️⃣ Tasdiqlang:
✅ Kirilgan ma'lumotlarni tasdiqlang va tugmani bosing.


4️⃣ Tashrifni rejalashtiring:
📅 Tashrif vaqti va sanasini tanlang.</b>
""", parse_mode=ParseMode.HTML)


@dp.callback_query(F.data == "ter")
async def terapiya_callback(callback: CallbackQuery):
    await callback.message.answer_photo(
        photo="https://img.freepik.com/free-photo/dentistry-expert-using-dental-tools-examine-cavity-problems-treat-patient-with-toothache-dentist-doing-oral-care-consultation-with-stomatology-instrument-checkup-visit_482257-37268.jpg?t=st=1734158149~exp=1734161749~hmac=35fb06c8a38a227e29004eb3252c97873d394fb48e8a8a9b32a92da09714c071&w=1380",
        caption=f"<b> 🩺  Terapiya xizmati❕ \n\n👩‍⚕️ Sizga yuqori malakali terapevtlar xizmat ko'rsatadi❕ \n\n💰 Narxi: {terapia}❕ \n\n⏳ Navbatga yozilish uchun tugmani bosing❕ \n\n👇📲</b>",
        reply_markup=booking,
        parse_mode="HTML")


@dp.callback_query(F.data == "xir")
async def xirurgiya_callback(callback: CallbackQuery):
    await callback.message.answer_photo(
        photo="https://img.freepik.com/free-photo/dentist-hand-examining-teeth-boy-with-ultrasonic-scaler_23-2147905899.jpg?t=st=1734587509~exp=1734591109~hmac=34683c49685be4d52d34abd88702fa67a5576641a58ca245d5739e73381cdac5&w=740",
        caption=f"<b> 🔬  Xirurgiya xizmati❕ \n\n👩‍⚕️ Sizga malakali xirurglar xavfsiz xizmat ko‘rsatadi❕ \n\n💰 Narxi: {xirurgiya}❕ \n\n⏳ Navbatga yozilish uchun tugmani bosing❕ \n\n👇📲</b> ",
        reply_markup=booking,
        parse_mode="HTML")


@dp.callback_query(F.data == "imp")
async def implantatsiya_callback(callback: CallbackQuery):
    await callback.message.answer_photo(
        photo="https://img.freepik.com/free-photo/defocused-dentist-holding-dentures-with-patient_23-2148380319.jpg?t=st=1734587712~exp=1734591312~hmac=feb4dc7454384798ef747bb5b8f7596c05ca52085b90756d3d2cfb85b57727b7&w=1380",
        caption=f"<b>🦷  Implantatsiya xizmati❕\n\n👩‍⚕️ Malakali implantologlarimiz sizga yordam beradi❕\n\n💰 Narxi: {implantatsiya}❕\n\n⏳ Navbatga yozilish uchun tugmani bosing❕ \n\n👇📲</b>",
        reply_markup=booking,
        parse_mode="HTML")


@dp.callback_query(F.data == "ortoden")
async def ortodontiya_callback(callback: CallbackQuery):
    await callback.message.answer_photo(
        photo="https://img.freepik.com/free-photo/happy-young-woman-smiling_23-2148396164.jpg?t=st=1734587850~exp=1734591450~hmac=32108804d84fba97dae72b4539498762972eb8df2dedd1462412ea441b6fe711&w=1380",
        caption=f"<b>🦷  Ortodontiya xizmati❕\n\n😊 Tishlaringiz go'zalligini ta'minlaymiz❕\n\n💰 Narxi: {ortodontiya}❕\n\n⏳ Navbatga yozilish uchun tugmani bosing❕ \n\n👇📲</b>",
        reply_markup=booking,
        parse_mode="HTML")


@dp.callback_query(F.data == "orto")
async def ortopediya_callback(callback: CallbackQuery):
    await callback.message.answer_photo(
        photo="https://img.freepik.com/free-photo/happy-young-woman-smiling_23-2148396164.jpg?t=st=1734587850~exp=1734591450~hmac=32108804d84fba97dae72b4539498762972eb8df2dedd1462412ea441b6fe711&w=1380",
        caption=f"<b>🦷  Ortopediya xizmati❕\n\n👩‍⚕️ Tishlaringiz sog'lig'ini tiklaymiz❕\n\n💰 Narxi: {ortopediya}❕\n\n⏳ Navbatga yozilish uchun tugmani bosing❕ \n\n👇📲</b>",
        reply_markup=booking,
        parse_mode="HTML")


@dp.callback_query(F.data == "indo")
async def indodontiya_callback(callback: CallbackQuery):
    await callback.message.answer_photo(
        photo="https://img.freepik.com/free-photo/front-view-adult-female-dentist_23-2148396181.jpg?t=st=1734587975~exp=1734591575~hmac=c28528c4a924258117ee35d15833617bbf1048c5958f825286f3d9ed18288d30&w=1380",
        caption=f"<b>🦷  Indodontiya xizmati❕\n\n👩‍⚕️ Og'riqsiz va sifatli davolash❕\n\n💰 Narxi: {indodontiya}❕\n\n⏳ Navbatga yozilish uchun tugmani bosing❕ \n\n👇📲</b>",
        reply_markup=booking,
        parse_mode="HTML"
    )


@dp.callback_query(F.data == "orqaga")
async def back_callback(callback: CallbackQuery):
    await callback.message.answer("<b>🏠🔙 Bosh menyuga qaytdingiz</b>", parse_mode="HTML", reply_markup=menu)


@dp.callback_query(F.data == "back")
async def back_callback(callback: CallbackQuery):
    await callback.message.answer("<b>🔙 Menuga qaytdingiz</b>", parse_mode="HTML", reply_markup=menu)


@dp.callback_query(F.data == "book")
async def booking_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BookingState.service)
    await callback.message.answer("<b> Xizmat turini tanlang ✍</b>", parse_mode="HTML")


@dp.message(BookingState.service)
async def booking_service(message: Message, state: FSMContext):
    await state.update_data(service=message.text)
    await state.set_state(BookingState.times)
    await message.answer("<b> Vaqtni tanlang! ⏰ </b>", parse_mode="HTML")


@dp.message(BookingState.times)
async def booking_time(message: Message, state: FSMContext):
    await state.update_data(times=message.text)
    await state.set_state(BookingState.finish)
    data1 = await state.get_data()
    service = data1.get("service", "Mavjud emas")
    times = data1.get("times")

    await message.answer(
        "<b>Malumot qabul qilindi iltimos vaqtida keling! ✅</b>", parse_mode=ParseMode.HTML, reply_markup=menu
    )

    data = await state.get_data()
    fullname = data.get("fullname", "Mavjud emas")
    birthday = data.get("birthday", "Mavjud emas")
    phone = data.get("phone", "Mavjud emas")
    email = data.get("email", "Mavjud emas")
    data1 = await state.get_data()
    service = data1.get("service", "Mavjud emas")
    times = data1.get("times")

    save_booking_data(message.from_user.id, fullname, birthday, phone, email, service, times)


# @dp.message(Command('getuser'))
# async def get_user(message: Message):
#     user_data = get_user_data(message.from_user.id)
#     await message.answer(f"Ma'lumotlar olindi: \n\nUserid: {user_data[0]} \n\nIsm Familiya: {user_data[1]} \n\nYoshi: {user_data[2]} \n\nedh: {user_data[3]}")





@dp.message(Command('getuser'))
async def send_all_users(message: Message):
    # Adminni tekshirish
    if int(message.from_user.id) == ADMIN_ID:
        users_data = get_all_users_data()
        if users_data:
            user_info = "<b><u>Foydalanuvchilar ro'yxati:</u></b>\n\n"
            user_info += "<b>ID</b> | <b>Fullname</b> | <b>Yoshi</b> | <b>Telefon nomer</b> | <b>Service</b> | <b>Times</b>\n"
            user_info += "--------------------------------------------\n"

            for user in users_data:
                user_info += f"<b>{user[0]}</b> | <b>{user[2]}</b> | <b>{user[3]}</b> | <b>{user[4]}</b> | <b>{user[6]}</b> | <b>{user[7]}</b>\n"

            # Matnni yuborish
            try:
                await message.answer(user_info, parse_mode=ParseMode.HTML)
            except Exception as e:
                await message.answer(f"Xatolik yuz berdi: {e}")


    else:
        await message.answer("Sizda bu komandani ishlatish huquqi yo'q.")
        return




async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot, polling_timeout=5)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
