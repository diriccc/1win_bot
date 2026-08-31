import logging
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio

TOKEN = "8933568782:AAHPoNyqyoqsb8foQ8O-XsDF8gvjWhq4Uy8"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# БАЗА ДАННЫХ
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT)''')
    conn.commit()
    conn.close()

def save_user(user_id, username, first_name):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)',
              (user_id, username, first_name))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT user_id FROM users')
    users = c.fetchall()
    conn.close()
    return users

init_db()

# ТЕКСТ
START_TEXT = """
🎁ПОЛУЧИ КЕШБЕК 1.000Р (ВЕЙДЖЕР X1) ЗА МИНИМАЛЬНЫЙ
ДЕПОЗИТ ОТ 900Р🎁

❗️За бонусом писать в ЛС - @diric1❗️

🎰 1WIN - https://lknt.pro/11fa34

Если не открывается ссылка, то отключи VPN

🎁 ПОДАРКИ ЗА РЕГИСТРАЦИЮ:

+50 фри-спинов просто за минимальный деп (Ввести промо DENKRYTOI при регистрации).
+500% на первые пополнения

❗️ Промокод: DENKRYTOI (ОБЯЗАТЕЛЬНО УКАЗЫВАТЬ ПРИ РЕГИСТРАЦИИ. БЕЗ ПРОМО БОНУС НЕ ДАДУТ!

Дополнительно для игрока:

+ Индивидуальные бонусы
⚡️ Мгновенные выплаты без верификации

Присоединяйся к нам в канал https://t.me/denkrytoi777
Наш чат для общения https://t.me/+nkbUdyskoRRiNjAy
"""

# ССЫЛКА НА ФОТО
PHOTO_URL = "https://cdn.phototourl.com/free/2026-08-31-458982aa-ab5a-447f-905b-695a880b118c.jpg"

def get_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 ПЕРЕЙТИ В 1WIN", url="https://lknt.pro/11fa34")],
        [InlineKeyboardButton(text="📢 НАШ КАНАЛ", url="https://t.me/denkrytoi777")],
        [InlineKeyboardButton(text="💬 НАШ ЧАТ", url="https://t.me/+nkbUdyskoRRiNjAy")]
    ])
    return keyboard

@dp.message(Command("start"))
async def start_command(message: types.Message):
    user = message.from_user
    save_user(user.id, user.username, user.first_name)

    await message.answer_photo(
        photo=PHOTO_URL,
        caption=START_TEXT,
        reply_markup=get_keyboard()
    )

@dp.message(Command("broadcast"))
async def broadcast_command(message: types.Message):
    ADMIN_ID = 6404068423  # ТВОЙ ID
    
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Нет прав!")
        return
    
    text = message.text.replace("/broadcast", "").strip()
    if not text:
        await message.answer("❌ Напиши текст после /broadcast")
        return
    
    users = get_all_users()
    if not users:
        await message.answer("❌ Нет пользователей")
        return
    
    await message.answer(f"📨 Рассылка для {len(users)} пользователей...")
    
    ok = 0
    fail = 0
    for user_id in users:
        try:
            await bot.send_message(user_id[0], text)
            ok += 1
        except:
            fail += 1
    
    await message.answer(f"✅ Отправлено: {ok}\n❌ Ошибок: {fail}")

async def main():
    print("✅ БОТ ЗАПУЩЕН!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
