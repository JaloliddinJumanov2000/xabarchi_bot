import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TestScore

BOT_TOKEN = "7620557051:AAGbUsXfg-1AixVwhONo-hRgnJPF3bQF7LU"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


@receiver(post_save, sender=TestScore)
def send_score_to_parent(sender, instance, created, **kwargs):
    """
    Har safar TestScore qo'shilsa YOKI yangilansa ota-onaga xabar yuboradi
    """

    student = instance.student
    chat_id = student.parents_chat_id

    if not chat_id:  # ota-ona Telegram bog'lamagan bo'lsa
        return

    emoji = "🟢" if instance.score >= 90 else "🟡" if instance.score >= 70 else "🔴"

    text = (
        f"👤 O‘quvchi: {student.full_name}\n"
        f"📚 Guruh: {student.group_name.name}\n"
        f"📝 Test: {instance.test.test_title}\n"
        f"✅ Natija: {emoji} {instance.score}\n"
    )

    # izoh maydoni bo'lsa qo'shamiz
    if hasattr(instance, "comment") and instance.comment:
        text += f"💬 Izoh: {instance.comment}"

    try:
        requests.post(BASE_URL, data={"chat_id": chat_id, "text": text})
    except Exception as e:
        print(f"❌ Telegram xabar yuborilmadi: {e}")
