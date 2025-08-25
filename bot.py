from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio, requests

BOT_TOKEN = "7620557051:AAGbUsXfg-1AixVwhONo-hRgnJPF3bQF7LU"
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    chat_id = message.chat.id
    await message.answer("Assalomu alaykum! Sizning chat_id botda saqlandi ✅")

    data = {"chat_id": chat_id, "phone": "998932511181"}
    requests.post("http://127.0.0.1:8000/api/save_chat_id/", json=data)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
