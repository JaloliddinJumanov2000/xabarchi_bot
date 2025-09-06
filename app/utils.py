import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send_message_sync(chat_id: int, text: str) -> None:
    try:
        response = requests.post(
            BASE_URL,
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML"
            },
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Telegramga yuborishda xatolik: {e}")
