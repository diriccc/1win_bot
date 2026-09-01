import logging
import sqlite3
import requests
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

# ===== ТЕКСТЫ =====
START_TEXT = """
🌟 **БЕСПЛАТНЫЙ ВПН ДЛЯ ЛЮБЫХ УСТРОЙСТВ** 🌟

📱 **Поддержка:** Windows, macOS, Android, iOS

🔐 **Безопасно и анонимно** — ваши данные надёжно зашифрованы

🚀 **Высокая скорость** — до 100 Мбит/с

📍 **Серверы в 15 странах**

👉 Выбери нужный раздел в меню ниже:
"""

INFO_TEXT = """
🔐 **О VPN-сервисе**

✅ **Полная анонимность** — логи не хранятся
✅ **Безлимитный трафик** — без ограничений
✅ **Защита от утечек DNS** — ваши данные в безопасности
✅ **Круглосуточная поддержка** — всегда готовы помочь

🌍 **Доступные страны:**
🇺🇸 США, 🇩🇪 Германия, 🇳🇱 Нидерланды, 🇬🇧 Великобритания, 🇫🇷 Франция, 🇯🇵 Япония, 🇸🇬 Сингапур и другие
"""

HOW_TO_TEXT = """
📱 **Как подключить VPN за 3 шага:**

1️⃣ **Перейди по ссылке ниже** и нажми "Запустить VPN"

2️⃣ **Активируй пробный период** (3 дня бесплатно)

3️⃣ **Вставь индивидуальный ключ** в приложение HAPP

🔑 **Ключ активации:** приходит после нажатия "Запустить VPN"

⚡️ **Готово!** Ты в безопасности, интернет защищён!
"""

FAQ_TEXT = """
❓ **Часто задаваемые вопросы:**

🔹 **Безопасно ли использовать VPN?**  
Да! Весь трафик шифруется, ваши данные защищены.

🔹 **Снижается ли скорость?**  
Незначительно. Наши серверы оптимизированы для высокой скорости.

🔹 **Можно ли использовать на нескольких устройствах?**  
Да, один аккаунт работает на всех устройствах.

🔹 **Что такое HAPP?**  
Это приложение для подключения VPN на твоём устройстве.

🔹 **Что делать, если ключ не работает?**  
Напиши в поддержку @enotnetwork — помогут за 2 минуты.
"""

# ===== КЛАВИАТУРЫ =====
def get_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 ЗАПУСТИТЬ VPN", url="https://t.me/Enot_vpn_net_bot?start=6404068423")],
        [InlineKeyboardButton(text="📖 ИНСТРУКЦИЯ", callback_data="howto")],
        [InlineKeyboardButton(text="ℹ️ О СЕРВИСЕ", callback_data="info")],
        [InlineKeyboardButton(text="❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton(text="📍 ПРОВЕРИТЬ IP", callback_data="ip")]
    ])
    return keyboard

def back_button():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 НАЗАД", callback_data="main_menu")]
    ])
    return keyboard

# ===== КОМАНДА /start =====
@dp.message(Command("start"))
async def start_command(message: types.Message):
    user = message.from_user
    save_user(user.id, user.username, user.first_name)
    
    await message.answer_photo(
        photo="https://cdn.phototourl.com/free/2026-09-01-19e3997a-b63b-4c34-96aa-7f4b27a418ef.jpg",
        caption=START_TEXT,
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

# ===== ОБРАБОТЧИК КНОПОК =====
@dp.callback_query()
async def callback_handler(callback_query: types.CallbackQuery):
    user = callback_query.from_user
    save_user(user.id, user.username, user.first_name)
    
    # Удаляем старое сообщение с клавиатурой
    await callback_query.message.delete()
    
    if callback_query.data == "main_menu":
        # Отправляем главное меню с фото
        await callback_query.message.answer_photo(
            photo="https://cdn.phototourl.com/free/2026-09-01-19e3997a-b63b-4c34-96aa-7f4b27a418ef.jpg",
            caption=START_TEXT,
            reply_markup=get_main_menu(),
            parse_mode="Markdown"
        )
    
    elif callback_query.data == "info":
        await callback_query.message.answer(
            INFO_TEXT,
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
    
    elif callback_query.data == "howto":
        await callback_query.message.answer(
            HOW_TO_TEXT,
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
    
    elif callback_query.data == "faq":
        await callback_query.message.answer(
            FAQ_TEXT,
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
    
    elif callback_query.data == "ip":
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            ip = response.json()['ip']
            
            ip_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🚀 ЗАПУСТИТЬ VPN", url="https://t.me/Enot_vpn_net_bot?start=6404068423")],
                [InlineKeyboardButton(text="🔙 НАЗАД", callback_data="main_menu")]
            ])
            
            await callback_query.message.answer(
                f"🌐 **Твой IP-адрес:**\n\n`{ip}`\n\n"
                "🔒 **VPN не активен!** Нажми кнопку ниже, чтобы защитить себя.",
                reply_markup=ip_keyboard,
                parse_mode="Markdown"
            )
        except:
            await callback_query.message.answer(
                "❌ Не удалось определить IP. Попробуй позже.",
                reply_markup=back_button()
            )
    
    await callback_query.answer()

# ===== РАССЫЛКА =====
@dp.message(Command("broadcast"))
async def broadcast_command(message: types.Message):
    ADMIN_ID = 6404068423
    
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
