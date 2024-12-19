# Stomatologiya Bot

Bu loyiha stomatologiya sohasidagi mijozlarga qulaylik yaratish uchun ishlab chiqilgan. Bot yordamida bemorlar tezkor ravishda stomatologik xizmatlarga yozilishi, savollarga javob olishlari va xizmatlar bo‘yicha ma’lumot olishlari mumkin. Loyihaning asosiy maqsadi odamlarning vaqtini tejash va xizmat ko‘rsatishni avtomatlashtirishdir.

## Texnologiyalar

Loyihada quyidagi texnologiyalardan foydalanilgan:

- **Python**: Loyihaning asosiy dasturlash tili.
- **Aiogram**: Telegram bot yaratish uchun asinxron kutubxona.
- **PostgreSQL**: Ma’lumotlarni saqlash uchun ishonchli va tezkor ma’lumotlar bazasi.
- **Psycopg2**: Python uchun PostgreSQL bilan ishlash kutubxonasi.
- **Docker**: Loyihani konteynerizatsiya qilish uchun.
- **SQLAlchemy**: Ma’lumotlar bazasi bilan ishlashni qulaylashtirish uchun ORM kutubxonasi.
- **Redis**: Bot sessiyalarini boshqarish uchun kechiktirilgan ma’lumotlar bazasi.

## Xususiyatlar

- **Xizmatlarga yozilish**: Foydalanuvchilar o‘zlariga qulay vaqtga xizmatga yozilishlari mumkin.
- **Xizmatlar haqida ma’lumot olish**: Turli stomatologik xizmatlar ro‘yxati va ularning narxlari haqida ma’lumot.
- **Eslatmalar**: Foydalanuvchilarga ularning yozilgan vaqti haqida avtomatik eslatmalar yuboriladi.
- **Administrator uchun boshqaruv paneli**: Yangi yozuvlarni kuzatish va o‘zgartirish imkoniyati.

## Loyihani ishga tushirish

### Talablar

Loyihani ishga tushirishdan oldin quyidagilarni o‘rnating:

- **Python 3.9 yoki undan yuqori**
- **PostgreSQL**
- **Docker** (ixtiyoriy, lekin tavsiya etiladi)

### O‘rnatish

1. Repositoriyani klonlang:

    ```bash
    git clone https://github.com/foydalanuvchi/stomatology-bot.git
    cd stomatology-bot
    ```

2. Virtual muhitni faollashtiring va zarur kutubxonalarni o‘rnating:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows uchun: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. `.env` faylini yarating va kerakli konfiguratsiyalarni kiriting:

    ```env
    BOT_TOKEN=your_telegram_bot_token
    DATABASE_URL=postgresql://user:password@localhost:5432/database_name
    REDIS_URL=redis://localhost:6379
    ```

4. Ma’lumotlar bazasini sozlang:

    ```bash
    alembic upgrade head
    ```

5. Botni ishga tushiring:

    ```bash
    python bot.py
    ```

### Docker orqali ishga tushirish

Docker Compose yordamida loyihani ishga tushiring:

```bash
docker-compose up --build
