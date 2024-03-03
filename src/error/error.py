from fastapi import FastAPI
import requests

from .models import ErrorQueueMessage

"""
Оповещает посредством электронной почты/телеграмма/SIEM/SOAR
(на выбор с возможностью настройки, можно добавлять свои цели),
в случае получения сообщения из очереди: «Errors.
"""

app = FastAPI()


# Тут просто токен чата и бота указать. Это должно лежать в .env, но
# для простоты использования оставил здесь.
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"


@app.post("/errors")
def handle_error_message(message: ErrorQueueMessage):
    send_email_notification(message.message)
    send_telegram_notification(message.message)

    return {"message": "Error message handled successfully"}


def send_telegram_notification(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"Error message received: {message}"
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Failed to send Telegram notification")
    else:
        print("Какой же я бездарь, это просто невероятно")


def send_email_notification(message):
    logic = (f"Email sent: Error message received - {message}")
    pass
