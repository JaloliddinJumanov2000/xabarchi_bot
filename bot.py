import os
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import requests

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# States for conversation
class PhoneState(StatesGroup):
    waiting_for_phone = State()


def validate_phone(phone: str) -> str:
    """Telefon raqamini tekshirish va formatlash"""
    # Faqat raqamlarni qoldirish
    phone = re.sub(r'[^\d]', '', phone)

    # +998 bilan boshlangan bo'lsa
    if phone.startswith('998'):
        phone = '+' + phone
    # 998 bilan boshlangan bo'lsa
    elif len(phone) == 12 and phone.startswith('998'):
        phone = '+' + phone
    # 9 raqam bilan boshlangan bo'lsa (masalan: 901234567)
    elif len(phone) == 9:
        phone = '+998' + phone
    else:
        return None

    # Uzunlikni tekshirish
    if len(phone) != 13:  # +998901234567
        return None

    return phone


@dp.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    await message.answer(
        "🤖 <b>Assalomu alaykum!</b>\n\n"
        "📱 Farzandingizning test natijalarini olish uchun "
        "telefon raqamingizni yuboring.\n\n"
        "📝 <i>Misol: +998901234567 yoki 901234567</i>"
    )
    await state.set_state(PhoneState.waiting_for_phone)


@dp.message(PhoneState.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    phone_text = message.text.strip()

    # Telefon raqamini tekshirish
    formatted_phone = validate_phone(phone_text)

    if not formatted_phone:
        await message.answer(
            "❌ <b>Noto'g'ri telefon raqami!</b>\n\n"
            "📱 Iltimos, to'g'ri formatda kiriting:\n"
            "• +998901234567\n"
            "• 998901234567\n"
            "• 901234567"
        )
        return

    chat_id = message.chat.id

    # Django API ga so'rov yuborish
    try:
        data = {"chat_id": str(chat_id), "phone": formatted_phone}
        response = requests.post(
            "http://127.0.0.1:8000/api/save_chat_id/",
            json=data,
            timeout=10
        )

        if response.status_code == 200:
            await message.answer(
                "✅ <b>Muvaffaqiyatli ro'yxatdan o'tdingiz!</b>\n\n"
                "🎓 Endi farzandingizning test natijalari "
                "avtomatik ravishda sizga yuboriladi.\n\n"
                "📊 Test natijalari haqida xabarlar olasiz."
            )
            await state.clear()
        else:
            error_data = response.json()
            await message.answer(
                "❌ <b>Xatolik yuz berdi!</b>\n\n"
                f"📝 Sabab: {error_data.get('error', 'Noma\'lum xatolik')}\n\n"
                "🔄 Iltimos, telefon raqamingizni qaytadan tekshiring "
                "yoki o'qituvchingiz bilan bog'laning."
            )

    except requests.RequestException as e:
        await message.answer(
            "❌ <b>Server bilan bog'lanishda xatolik!</b>\n\n"
            "🔄 Iltimos, biroz kutib qaytadan urinib ko'ring.\n\n"
            f"📝 Texnik ma'lumot: {str(e)}"
        )
        print(f"❌ API ga so'rov yuborishda xatolik: {e}")


@dp.message()
async def handle_other_messages(message: types.Message):
    await message.answer(
        "🤖 <b>Botdan foydalanish uchun /start buyrug'ini bosing</b>\n\n"
        "📱 Telefon raqamingizni ro'yxatdan o'tkazish uchun "
        "/start ni bosing."
    )


async def main():
    print("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())