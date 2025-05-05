from aiogram import Bot
from aiogram.types import ParseMode


API_TOKEN = "7795862625:AAGJDT5fCOlBCyU3-veuX19ea-6mbDqEcCU"

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)

SUPPORT_CHAT_ID = 637166903


async def send_message_async(theme: str, description: str, contacts: str):
    text = (
        f"<b>Тема:</b> {theme}\n"
        f"<b>Описание:</b> {description}\n"
        f"<b>Контакты:</b> {contacts}"
    )
    await bot.send_message(chat_id=SUPPORT_CHAT_ID, text=text)
