import psycopg2
from psycopg2 import sql
import logging


# Ma'lumotlar bazasiga ulanish
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="my_dent",  # Baza nomi
            user="postgres",  # Foydalanuvchi nomi
            password="1",  # Parol
            host="localhost",  # Yoki server manzilingiz
            port="5432"  # PostgreSQL porti
        )
        return conn
    except psycopg2.Error as e:
        logging.error(f"Ma'lumotlar bazasiga ulanishda xato: {e}")
        return None


# Foydalanuvchi ma'lumotlarini saqlash
def save_user_data(user_id, fullname, birthday, phone, email):
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (user_id, fullname, birthday, phone, email)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (user_id) 
                DO UPDATE SET fullname = EXCLUDED.fullname, 
                              birthday = EXCLUDED.birthday, 
                              phone = EXCLUDED.phone, 
                              email = EXCLUDED.email;
            ''', (user_id, fullname, birthday, phone, email))
            conn.commit()
            cursor.close()
            conn.close()
    except psycopg2.Error as e:
        logging.error(f"Ma'lumotlar bazasiga saqlashda xato: {e}")


# Foydalanuvchi ma'lumotlarini olish
def get_user_data(user_id):
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()
            return user_data
    except psycopg2.Error as e:
        logging.error(f"Ma'lumotlar bazasidan olishda xato: {e}")
        return None


def get_all_users_data():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM booking')  # barcha foydalanuvchilarni olish
            users_data = cursor.fetchall()  # barcha foydalanuvchilarni ro'yxat qilib olish
            cursor.close()
            conn.close()
            return users_data
    except psycopg2.Error as e:
        logging.error(f"Ma'lumotlar bazasidan olishda xato: {e}")
        return None


# Ma'lumotlar bazasini yaratish (agar yo'q bo'lsa)
def create_table():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                fullname TEXT,
                birthday TEXT,
                phone TEXT,
                email TEXT UNIQUE
            );
            ''')
            cursor.execute('''
                            CREATE TABLE IF NOT EXISTS booking (
                                id SERIAL PRIMARY KEY,
                                user_id BIGINT NOT NULL,
                                fullname TEXT,
                                birthday TEXT ,
                                phone TEXT,
                                email TEXT UNIQUE,
                                service TEXT,
                                times TEXT UNIQUE
                            );
                        ''')
            conn.commit()
            cursor.close()
            conn.close()
    except psycopg2.Error as e:
        logging.error(f"Jadvalni yaratishda xato: {e}")


def save_booking_data(user_id, fullname, birthday, phone, email, service, times):
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()

            # Agar birthday noto'g'ri bo'lsa, uni NULL qilish
            if birthday == "Mavjud emas" or not birthday:
                birthday = None

            # Foydalanuvchi ma'lumotlarini olish
            cursor.execute('''
                SELECT fullname, birthday, phone, email FROM users WHERE user_id = %s;
            ''', (user_id,))
            user_data = cursor.fetchone()

            # Agar foydalanuvchi mavjud bo'lsa, uni booking jadvaliga qo'shamiz
            if user_data:
                fullname, birthday, phone, email = user_data

                # Endi booking jadvaliga ma'lumotlarni qo'shish
                cursor.execute('''
                    INSERT INTO booking (user_id, fullname, birthday, phone, email, service, times)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                ''', (user_id, fullname, birthday, phone, email, service, times))

                # O'zgarishlarni saqlash
                conn.commit()
            else:
                print("Foydalanuvchi topilmadi!")
            cursor.close()
            conn.close()
    except psycopg2.Error as e:
        logging.error(f"Ma'lumotlar bazasiga saqlashda xato: {e}")
