import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio

TOKEN = "8933568782:AAHPoNyqyoqsb8foQ8O-XsDF8gvjWhq4Uy8"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

START_TEXT = """
🎁ПОЛУЧИ КЕШБЕК 1.000Р ЗА МИНИМАЛЬНЫЙ
ДЕПОЗИТ ОТ 900Р🎁

❗️За бонусом писать в ЛС - @diric1❗️

🎰 1WIN - https://lknt.pro/11fa34 (https://9reenhouse-7apeks.com/adiuwqrxv4)

Если не открывается ссылка, то отключи VPN

🎁 ПОДАРКИ ЗА РЕГИСТРАЦИЮ:

+50 фри-спинов просто за минимальный деп (Ввести промо DENKRYTOI при регистрации).
+500% на первые пополнения

❗️ Промокод: DENKRYTOI (ОБЯЗАТЕЛЬНО УКАЗЫВАТЬ ПРИ РЕГИСТРАЦИИ. БЕЗ ПРОМО БОНУС НЕ ДАДУТ!

Дополнительно для игрока:

+ Индивидуальные бонусы
⚡️ Мгновенные выплаты без верификации
"""

def get_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 ПЕРЕЙТИ В 1WIN", url="https://lknt.pro/11fa34")]
    ])
    return keyboard

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(START_TEXT, reply_markup=get_keyboard())

async def main():
    print("✅ БОТ УСПЕШНО ЗАПУЩЕН!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
