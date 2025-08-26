import os
import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TestScore

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ BOT_TOKEN topilmadi! .env faylini tekshiring.")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


@receiver(post_save, sender=TestScore)
def send_score_to_parent(sender, instance, created, **kwargs):
    """
    Har safar TestScore qo'shilsa YOKI yangilansa ota-onaga xabar yuboradi
    """
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN yo'q, xabar yuborilmadi")
        return

    student = instance.student
    chat_id = student.parents_chat_id

    if not chat_id:  # ota-ona Telegram bog'lamagan bo'lsa
        print(f"❌ {student.full_name} uchun chat_id topilmadi")
        return

    # Ball bo'yicha emoji tanlash
    score_float = float(instance.score)
    if score_float >= 90:
        emoji = "🟢"
        status = "A'lo"
    elif score_float >= 70:
        emoji = "🟡" 
        status = "Yaxshi"
    elif score_float >= 50:
        emoji = "🟠"
        status = "Qoniqarli"
    else:
        emoji = "🔴"
        status = "Qoniqarsiz"

    text = (
        f"📊 <b>Test natijasi</b>\n\n"
        f"👤 O‘quvchi: {student.full_name}\n"
        f"📚 Guruh: {student.group_name.name}\n"
        f"📝 Test: {instance.test.test_title}\n"
        f"✅ Natija: {emoji} {instance.score} ball ({status})\n"
    )

    # izoh maydoni bo'lsa qo'shamiz
    if instance.comment:
        text += f"💬 Izoh: {instance.comment}"

    try:
        response = requests.post(
            BASE_URL, 
            data={
                "chat_id": chat_id, 
                "text": text,
                "parse_mode": "HTML"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✅ {student.full_name} uchun xabar yuborildi")
        else:
            print(f"❌ Xabar yuborishda xatolik: {response.text}")
            
    except Exception as e:
        print(f"❌ Telegram xabar yuborilmadi: {e}")
