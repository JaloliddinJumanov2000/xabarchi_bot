import os
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio
import requests

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    print("❌ BOT_TOKEN topilmadi! .env faylini tekshiring.")
    exit(1)

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# States for conversation
class RegistrationState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_student_selection = State()

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
    await state.set_state(RegistrationState.waiting_for_phone)

@dp.message(RegistrationState.waiting_for_phone)
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
    
    # Django API dan shu telefon raqamiga tegishli o'quvchilarni olish
    try:
        response = requests.get(
            f"http://127.0.0.1:8000/api/students_by_phone/?phone={formatted_phone}",
            timeout=10
        )
        
        if response.status_code == 200:
            students = response.json()
            
            if not students:
                await message.answer(
                    "❌ <b>Bu telefon raqami bilan ro'yxatdan o'tgan o'quvchi topilmadi!</b>\n\n"
                    "📞 Iltimos, telefon raqamingizni qaytadan tekshiring "
                    "yoki o'qituvchingiz bilan bog'laning.\n\n"
                    "🔄 Qaytadan urinish uchun /start ni bosing."
                )
                await state.clear()
                return
            
            if len(students) == 1:
                # Faqat bitta o'quvchi bo'lsa, avtomatik tanlash
                student = students[0]
                await save_student_chat_id(message, state, student['id'], formatted_phone)
            else:
                # Bir nechta o'quvchi bo'lsa, tanlash uchun tugmalar
                await state.update_data(phone=formatted_phone, students=students)
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=[])
                
                for student in students:
                    button = InlineKeyboardButton(
                        text=f"👤 {student['full_name']} ({student['group_name']['name']})",
                        callback_data=f"select_student_{student['id']}"
                    )
                    keyboard.inline_keyboard.append([button])
                
                await message.answer(
                    "👥 <b>Bir nechta o'quvchi topildi!</b>\n\n"
                    "👇 Iltimos, o'z farzandingizni tanlang:",
                    reply_markup=keyboard
                )
                await state.set_state(RegistrationState.waiting_for_student_selection)
        else:
            await message.answer(
                "❌ <b>Server bilan bog'lanishda xatolik!</b>\n\n"
                "🔄 Iltimos, biroz kutib qaytadan urinib ko'ring."
            )
            
    except requests.RequestException as e:
        await message.answer(
            "❌ <b>Server bilan bog'lanishda xatolik!</b>\n\n"
            "🔄 Iltimos, biroz kutib qaytadan urinib ko'ring.\n\n"
            f"📝 Texnik ma'lumot: {str(e)}"
        )
        print(f"❌ API ga so'rov yuborishda xatolik: {e}")

@dp.callback_query(lambda c: c.data.startswith("select_student_"))
async def process_student_selection(callback: CallbackQuery, state: FSMContext):
    student_id = int(callback.data.split("_")[-1])
    data = await state.get_data()
    phone = data.get('phone')
    
    await callback.message.edit_text("⏳ <b>Ro'yxatdan o'tkazilmoqda...</b>")
    
    await save_student_chat_id(callback.message, state, student_id, phone)
    await callback.answer()

async def save_student_chat_id(message: types.Message, state: FSMContext, student_id: int, phone: str):
    """O'quvchining chat_id sini saqlash"""
    chat_id = message.chat.id
    
    try:
        data = {
            "chat_id": str(chat_id), 
            "phone": phone,
            "student_id": student_id
        }
        response = requests.post(
            "http://127.0.0.1:8000/api/save_chat_id/", 
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            await message.answer(
                "✅ <b>Muvaffaqiyatli ro'yxatdan o'tdingiz!</b>\n\n"
                f"👤 O'quvchi: {result.get('student', 'Noma\'lum')}\n"
                f"📚 Guruh: {result.get('group', 'Noma\'lum')}\n\n"
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
                "🔄 Iltimos, qaytadan urinib ko'ring yoki "
                "o'qituvchingiz bilan bog'laning."
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
    print(f"🔗 Bot username: @{(await bot.get_me()).username}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())