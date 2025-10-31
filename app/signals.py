import os
import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TestScore
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


@receiver(post_save, sender=TestScore)
def send_score_to_parent(sender, instance, created, **kwargs):
    """
    Har safar TestScore yaratilganda yoki tahrirlanganda
    ota-onaga avtomatik xabar yuboradi.
    """

    student = instance.student
    chat_id = student.parents_chat_id

    if not chat_id:
        print("⚠️ Ota-onaning Telegram chat_id topilmadi.")
        return

    # Ballga qarab emoji tanlaymiz
    emoji = "🟢" if instance.score >= 90 else "🟡" if instance.score >= 70 else "🔴"

    # Xabar matni
    text = (
        f"📢 *Test natijasi yangilandi!*\n\n"
        f"👤 O‘quvchi: *{student.full_name}*\n"
        f"📚 Guruh: *{student.group_name.name}*\n"
        f"📝 Test: *{instance.test.test_title}*\n"
        f"✅ Natija: {emoji} *{instance.score}*\n"
    )

    if instance.comment:
        text += f"\n💬 Izoh: _{instance.comment}_"

    try:
        response = requests.post(
            BASE_URL,
            data={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown",
            },
            timeout=5,
        )
        if response.status_code != 200:
            print(f"⚠️ Telegram xabar yuborilmadi: {response.text}")
    except Exception as e:
        print(f"❌ Telegram xabar yuborishda xatolik: {e}")
